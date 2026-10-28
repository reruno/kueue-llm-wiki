# Debugging Guide

**Summary**: A practical guide to diagnosing why Kueue workloads are stuck — covering quota exhaustion, flavor mismatches, admission check hangs, TAS failures, and preemption issues — with the specific commands and conditions to check.

**Sources**: `raw/kueue/pkg/controller/core/workload_controller.go`, `raw/kueue/pkg/debugger/`, `raw/github/kubernetes-sigs__kueue/` (issues), `raw/kueue/pkg/controller/core/clusterqueue_controller.go`, pr-13271.md, pr-14348.md, pr-14411.md, pr-16670.md, pr-16833.md, pr-16890.md, pr-16581.md, pr-16743.md, pr-16379.md, pr-16984.md, pr-16609.md, pr-16667.md, pr-16531.md, pr-16981.md, pr-16510.md, pr-16739.md, pr-16392.md, pr-16793.md, issue-16789.md, raw/kueue/pkg/features/kube_features.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-16343.md, pr-16438.md, pr-16627.md, issue-16486.md, pr-16421.md, pr-16514.md, pr-17052.md, pr-13775.md, pr-16470.md, pr-16870.md; 2026-10-21 batch: raw/kueue/CHANGELOG/CHANGELOG-0.19.md (v0.19.9), CHANGELOG-0.20.md (v0.20.2), pr-17227.md, pr-17093.md, pr-16483.md, pr-16630.md, pr-17041.md, pr-17336.md, pr-17088.md, pr-17143.md, pr-17105.md, pr-17272.md, pr-17273.md, raw/kueue/pkg/scheduler/scheduler.go

**Last updated**: 2026-10-28

---

## Step 1: Check the Workload conditions

Every Kueue-managed job has a corresponding [[workload]] object. Start here:

```bash
kubectl describe workload <name> -n <namespace>
# or, for the workload created from a job:
kubectl get workload -n <namespace> -l kueue.x-k8s.io/job-uid=<job-uid>
```

The `status.conditions` tell you exactly where the workload is stuck:

| Condition | Status | Reason | Meaning |
|---|---|---|---|
| `QuotaReserved` | `False` | `Pending` | Waiting in the queue; quota not yet available |
| `QuotaReserved` | `False` | `Inadmissible` | Cannot fit in any flavor; see `message` for which resource |
| `QuotaReserved` | `False` | `AdmissionGated` | Blocked by [[admission-gated-by-annotation]] |
| `QuotaReserved` | `True` | — | Quota reserved; waiting for admission checks |
| `Admitted` | `True` | — | Fully admitted; job should be running |
| `PodsReady` | `False` | `WaitForStart` / `WaitForScheduling` / `WaitForRecovery` | Pods not all Ready yet (waitForPodsReady configured); see [[wait-for-pods-ready]] |
| `Evicted` | `True` | `Preempted` | Preempted by a higher-priority workload |
| `Evicted` | `True` | `PodsReadyTimeout` | Pods never became ready within the timeout |
| `Evicted` | `True` | `AdmissionCheck` | An admission check failed |
| `Evicted` | `True` | `DeactivatedDueToMaximumExecutionTimeExceeded` | Maximum execution time exceeded; workload deactivated |
| `Evicted` | `True` | `DeactivatedDueToRequeuingLimitExceeded` | Re-queued too many times (`waitForPodsReady.requeuingStrategy.backoffLimitCount`); workload deactivated |

The `message` field on the `QuotaReserved: False` condition usually tells you exactly which resource was insufficient and in which flavor.

---

## Root cause 1: Quota exhausted

**Symptom**: `QuotaReserved: False` with message like:
```
couldn't assign flavors to pod set main: insufficient unused quota for
nvidia.com/gpu in flavor gpu-a100, 4 more needed
```

**Diagnose**:
```bash
kubectl get clusterqueue <name> -o yaml | grep -A20 flavorsReservation
kubectl kueue list workloads --all-namespaces   # see what's currently admitted
```

Check `status.flavorsReservation` and `status.flavorsUsage` in the ClusterQueue. If `total` is at `nominalQuota` and there are no cohort borrowing targets, the queue is full.

**Check cohort borrowing**:
```bash
kubectl get clusterqueue -o yaml | grep -E "cohort|borrowingLimit|lendingLimit"
```

If `lendingLimit: 0` on all other ClusterQueues in the cohort, your ClusterQueue cannot borrow. If your workload requires borrowing and `borrowingLimit: 0` is set on your ClusterQueue, it's locked to its nominal quota.

---

## Root cause 2: Flavor mismatch (no matching node labels)

**Symptom**: `Inadmissible` with message about no matching flavor.

**Diagnose**:
```bash
kubectl get resourceflavor <name> -o yaml  # check nodeLabels, tolerations
kubectl get nodes --show-labels | grep <label>   # verify nodes actually have the label
```

Common issue: a [[resource-flavor]] specifies `nodeLabels: {cloud.google.com/gke-accelerator: nvidia-tesla-a100}` but the nodes don't have that label, or the spelling differs.

---

## Root cause 3: Admission check not resolving

**Symptom**: `QuotaReserved: True` but `Admitted: False` — stuck indefinitely.

```bash
kubectl describe workload <name> -n <namespace> | grep -A5 "admissionChecks"
```

The `status.admissionCheckStates` list shows each check and its current state:
- `Pending` — check controller hasn't responded yet.
- `Ready` — check passed.
- `Retry` — check failed transiently; will retry.
- `Rejected` — check failed permanently; the Workload is deactivated (`Evicted` reason `DeactivatedDueToAdmissionCheck`).

**Common cause**: [[provisioning-request]] — cluster autoscaler hasn't provisioned nodes yet. Check:
```bash
kubectl get provisioningrequest -n kueue-system
kubectl describe provisioningrequest <name>
```

**Common cause**: custom check controller is not running or crashed:
```bash
kubectl get pods -n <check-controller-namespace>
kubectl logs <check-controller-pod>
```

---

## Root cause 4: WaitForPodsReady timeout

**Symptom**: `Evicted: True` with reason `PodsReadyTimeout`.

The workload was admitted, pods were created, but not all pods became `Ready` within the `waitForPodsReady.timeout`. Kueue evicts the workload and re-queues it.

**Diagnose**:
```bash
kubectl get pods -n <namespace> -o json | jq -r '.items[] | select(.metadata.annotations["kueue.x-k8s.io/workload"]=="<workload-name>") | .metadata.name'
kubectl describe pod <stuck-pod>
```

Look for `FailedScheduling` events (nodes full), `ImagePullBackOff`, or `CrashLoopBackOff` on the pods.

---

## Root cause 5: Topology-Aware Scheduling (TAS) no fit

**Symptom**: `Inadmissible` with message about topology.

```
couldn't assign flavors to pod set main: topology domain rack/block does not have
enough capacity for 8 pods
```

The workload requires all pods to fit within a single topology domain (rack, block, etc.) but no single domain has enough free nodes. See [[topology-aware-scheduling]].

**Diagnose**:
```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,RACK:.metadata.labels.rack,ALLOCATED:.status.allocatable.cpu
```

If a node went offline, pods from a previous run might be stuck in `Terminating`, consuming TAS slots, unless [[failure-recovery]] (Alpha, off by default) is enabled and the Pods carry its opt-in annotation. Check:
```bash
kubectl get pods --all-namespaces | grep Terminating
```

---

## Root cause 6: Workload is deactivated

**Symptom**: `Evicted: True` with a `Deactivated…` reason (`Deactivated`, or `DeactivatedDueTo<Cause>`). The workload has `spec.active: false`.

Possible causes:
- **Requeuing limit exceeded** — the Workload was evicted and re-queued (e.g. PodsReady timeout) `backoffLimitCount` times.
- **Exceeded maximum execution time** — `spec.maximumExecutionTimeSeconds` was reached (see [[workload-max-execution-time]]).
- **Manual deactivation** — an admin set `spec.active: false`.

**To reactivate**:
```bash
kubectl patch workload <name> -n <namespace> --type=merge -p '{"spec":{"active":true}}'
```

---

## Step 2: Check ClusterQueue and LocalQueue status

```bash
kubectl describe clusterqueue <name>
```

Look at:
- `status.conditions[type=Active]` — if `False`, the ClusterQueue is stopped or has a broken ResourceFlavor reference.
- `status.pendingWorkloads` — total pending in the queue.
- `status.admittedWorkloads` — how many are currently running.

```bash
kubectl describe localqueue <name> -n <namespace>
```

If `status.conditions[type=Active]=False`, the parent ClusterQueue is inactive or the LocalQueue references a non-existent ClusterQueue.

---

## Step 3: Use kueuectl

```bash
# List all workloads with their status
kubectl kueue list workloads --all-namespaces

# Show pending workloads in a specific queue (visibility API)
kubectl kueue list workload --localqueue <name> --status pending --namespace <ns>

# Pause/resume a ClusterQueue
kubectl kueue stop clusterqueue <name>
kubectl kueue resume clusterqueue <name>

# Stop a workload (deactivate)
kubectl kueue stop workload <name> -n <namespace>
```

See [[kueuectl]] for the full command reference.

---

## Step 4: Check Kueue manager logs

The scheduler logs each cycle's nomination and admission results. On **v0.20.x / v0.19.x releases** these messages are at `V(2)` (the default). On **main (v0.21 dev)** pr-17227 moved the eight cycle-progress messages (`Scheduling cycle starts`, `Obtained heads`, `Snapshot taken`, `Nomination done`, `Attempting to schedule workload`, `Workload re-queued`, `Workload processing done`, `Scheduling cycle complete`) to **`V(3)`**, so you need `-v=3` to see them there (source: pr-17227.md, raw/kueue/pkg/scheduler/scheduler.go):

```bash
kubectl logs -n kueue-system deployment/kueue-controller-manager | grep -E "schedulingCycle|Nomination|admitted|Inadmissible"
```

Common useful log entries:
- `Nomination done` — how many workloads were nominated vs. inadmissible.
- `Attempting to schedule workload` + workload name — the scheduler is processing it.
- `Workload is inadmissible` — with the reason string.

For verbose quota details: increase log level to `V(3)` or `V(5)` in the manager deployment.

Log facts worth knowing on v0.20+ (source: CHANGELOG-0.20.md unless noted):

- **Logger names changed in v0.20.0 (#15259).** Event-handler and reconcile logs of one controller now share a name: core controllers use `<kind>-reconciler` (e.g. `clusterqueue-reconciler`); MultiKueue, provisioning and TAS controllers use `<subcomponent>-<kind>-reconciler` (e.g. `multikueue-workload-reconciler`, `tas-node-reconciler`). Update log filters that matched the old names.
- **Which gates are on**: at startup the manager logs `Loaded feature gates` at `V(2)` with the effective map (`features.LogFeatureGates`) — check it before assuming a default (source: raw/kueue/pkg/features/kube_features.go).
- **Node hot swap / evictions**: Workload update events carry an `unhealthyNodes` field listing `status.unhealthyNodes` names (pr-13271, cherry-picked to 0.18/0.17) (source: pr-13271.md).
- **Fair-sharing preemption at `V(4)`**: one `Evaluating FairSharing strategy` entry per *candidate ClusterQueue* with a `strategyEvaluations` array (`targetWorkload`, `targetNewShare`, `strategyPassed`), instead of one entry per candidate Workload; DRS values are strings (`"+Inf"` included), because a raw `+Inf` float made zap drop the whole array (pr-14348) (source: pr-14348.md). See [[fair-sharing]].
- **Workload controller log keys** (pr-17093; in release branches after v0.20.2 / v0.19.9): `queue`/`prevQueue` became `localQueue`/`prevLocalQueue` and carry the namespace; QuotaReserved reason changes are logged as `Workload status updated` (`reason`, `message`) at `V(3)` after the write succeeds; routine per-Workload messages moved from V(2) to V(3) or higher. Update log filters that matched the old keys (source: pr-17093.md).
- Scheduling-hash recomputations are logged at `V(5)` (#15055); `V(6)` and below now emit valid JSON Lines (#13637); TAS assumption-violation logs are summarized, with leaf-domain IDs only at `V(6)` (#14242).

---

## Step 5: Check Prometheus metrics

Key metrics for triage (see [[metrics]]):

| Metric | Description |
|---|---|
| `kueue_pending_workloads{status="active"}` | Workloads actively being considered by the scheduler |
| `kueue_pending_workloads{status="inadmissible"}` | Workloads that failed nomination |
| `kueue_admitted_active_workloads` | Currently admitted workloads per ClusterQueue |
| `kueue_admission_attempts_total{result="inadmissible"}` | Admission cycles that produced no admissions |
| `kueue_evicted_workloads_total{reason="Preempted"}` | Preemption rate |

---

## Common pitfalls

| Symptom | Likely cause |
|---|---|
| Job is not managed by Kueue at all | Missing `kueue.x-k8s.io/queue-name` label AND `manageJobsWithoutQueueName=false` |
| Workload stuck with no conditions | The workload controller is not running or there's a watch error |
| Job starts immediately without queuing | Kueue is not managing this namespace (check [[manage-jobs-selectively]]) |
| Workload admitted but job stays suspended | `RunWithPodSetsInfo` error; check manager logs for `Failed to admit workload` |
| Re-queue loop (admit → evict → admit) | PodsReady timeout is too short; or failing admission check with `Retry` state |

---

## Pods permanently `SchedulingGated` while the Workload says `Admitted=True`

This combination — healthy-looking quota, valid TAS assignment, `Admitted=True`, but Pods that never start — has two known causes worth checking in order.

1. **The Pod is missing `kueue.x-k8s.io/queue-name`.** The Pod integration logs `"queue-name label is not set, ignoring the job"`, no workload annotation is written, the Pod is absent from the `WorkloadSliceNameKey` index, and the topology ungater finds no candidates. `waitForPodsReady` then evicts, the Pods are recreated from the same unlabelled template, and the loop repeats until `requeueState.count` reaches `backoffLimitCount` and the Workload is **deactivated**. Classic trigger: a [[integration-leaderworkerset]] created *before* the queue-name write moved into the LWS webhook, so its pod templates were never stamped. Fixed by backfilling on adoption ([[pr-14138]], [[pr-14602]], [[pr-14603]]).
2. **The ungater is limited by the admission count.** The elastic-job ungater ungates `status.admission.podSetAssignments[].count` Pods, not `podSet.count` ([[pr-14835]]). If those two differ (partial scale-up, or after a scale-down) the surplus Pods stay gated by design.

Check: `kubectl get pod -o jsonpath='{.spec.schedulingGates}'` and the Pod's `kueue.x-k8s.io/queue-name` label and `kueue.x-k8s.io/workload` annotation.

## A Pod stuck `Terminating` forever, or a replacement that never appears

Symptom A: the owning controller (Deployment-style) thrashes — it creates a replacement Pod which Kueue immediately deletes as "excess". Symptom B: a StatefulSet-owned replacement with the same ordinal name is never created at all.

Both come from the `kueue.x-k8s.io/managed` finalizer not being removed on a **non-deletion** eviction of a serving pod group (a `waitForPodsReady.recoveryTimeout` eviction, a `spec.active` toggle, or preemption). Fixed in [[pr-14632]]; the mechanics — including why the StatefulSet case is a genuine circular deadlock that previously needed a human to strip the finalizer — are in [[integration-plain-pod#Finalizer removal on eviction (serving pod groups)]].

## A Workload that stays inactive after you re-activate it

If the Workload's `Requeued=False` condition carries a derived reason such as `DeactivatedDueToRequeuingLimitExceeded`, versions before [[pr-14874]] never transitioned it, so flipping `spec.active` back to `true` had no effect. Check `.status.conditions[?(@.type=="Requeued")].reason`.

## Reading the reason on a pending Workload (v0.20)

With `UnadmittedWorkloadsObservability` (Beta, on by default in v0.20) `QuotaReserved=False` carries a specific reason (`PendingEvaluation`, `WaitingForQuota`, `NoMatchingFlavor`, `ExceedsMaxQuota`, `TopologyPlacementFailed`, `WaitingForPreemptedWorkloads`, `Misconfigured`, `Suspended`, `AdmissionGated`, `WaitingForPodsReady`, `Deactivated`, `OnHold`) instead of `Pending`/`Inadmissible`; `kubectl get clusterqueue|localqueue -o wide` now shows `ACTIVE` and `REASON` columns (pr-15633). Metrics: `kueue_unadmitted_workloads`. See [[unadmitted-workloads-observability]]. An `Evicted` reason of `Preempted` with a `Preempted` condition reason `ConfigurablePreemption` and `underlyingCause` = PreemptionConfig name points to [[configurable-preemptions]]. `PodsReady=False` with `WaitForScheduling`/`WaitForStart`/`WaitForRecovery` is explained in [[wait-for-pods-ready]].

## A Workload that stays pending after you raise a LimitRange

Event/message: **`resources didn't satisfy LimitRange constraints`**. Historically, raising a container `max` (or lowering `min`, or deleting the LimitRange) did not wake the Workloads that had been rejected, because the recomputed spec was byte-identical and the queue only woke parked Workloads on a diff (issue-14965.md). On current main the workload controller compares `Type`, `Max`, `Min`, `Default`, `DefaultRequest` and `MaxLimitRequestRatio` on every LimitRange create/update/delete and requeues the inadmissible Workloads of every affected ClusterQueue, including Workloads the scheduler had popped at that moment (pr-16129, backported to 0.19/0.18). On older versions, nudge the ClusterQueue (any event that requeues its inadmissible set) unless you run StrictFIFO. See [[workload-resource-adjustment#LimitRange changes now wake rejected and in-flight Workloads]].

## Slow MultiKueue dispatch under a burst

If manager→worker dispatch is minutes-slow with an idle scheduling loop, suspect **client-side throttling**: before v0.20 (or with `MultiKueueReuseClientConnectionConfigForWorkers` off) MultiKueue's remote clients use client-go's defaults (QPS 5 / Burst 10) and are not covered by `clientConnection`. 1000 Workloads across 10 workers measured ~15 min. See [[multikueue#Manager → worker clients: `clientConnection` QPS/Burst now applies (v0.20, Beta)]]. If the manager lags a worker after a network blip instead, see the reconnect note in [[multikueue#Behaviours worth knowing (from open issues)]].

## ClusterQueue usage that drifts below what is actually admitted

Before v0.20 (pr-15026), a workload whose per-flavor total saturated to `math.MaxInt64` collided with the `Unlimited` quota sentinel: additions onto an unlimited amount were silently dropped while removals still subtracted, leaving usage negative-looking until a manager restart (issue-14105.md). Quota `Amount`s are now exact integers with no sentinel, so this drift should not occur on v0.20+. On older versions, look for an admitted Workload with a huge per-flavor total. See [[cache-architecture#Quota amounts are exact past int64 (pr-15026)]].

## A ClusterQueue that stops admitting after a snapshot error

`Manager.Heads` pops one head per active ClusterQueue before the snapshot is built. Before [[pr-13885]], a `cache.Snapshot()` failure dropped those heads on the floor until some unrelated event requeued them. Look for the `SnapshotFailed` requeue reason; its presence means the recovery path is working.

## Reconcile errors that repeat forever on a quota-reserved Workload

A quota-reserved Workload whose owner drops its `WorkloadPriorityClass` label used to be rewritten with a `priorityClassRef` the API server refuses, once per reconcile, for the life of the reservation ([[pr-14565]]). Since [[pr-14922]] the skip is logged at `V(4)`, so you will only see it with `-v=4`.

## Metrics that lie (and the release that fixed them)

Before trusting a dashboard during triage, check whether you run a version with these bugs (details in [[metrics]]):

| Symptom | Cause | Fixed in |
|---|---|---|
| `kueue_pending_workloads` unchanged after `kueuectl stop clusterqueue` until some Workload changes | CQ updates did not refresh pending metrics | v0.20.1 / v0.19.8 (pr-16833) |
| `sum(kueue_pending_workloads)` about double after a CQ stop/resume, with a Workload-sourced custom label | stale `active`/`inadmissible` series not deleted | v0.20.1 (pr-16670) |
| Pending counts stale after a LocalQueue is created, stopped, resumed or deleted | LQ lifecycle events did not refresh metrics | v0.20.1 / v0.19.8 (#15576) |
| All of a stopped CQ's pending Workloads appear as `status="inadmissible"` | by design: an inactive CQ merges active into inadmissible | — |
| `kueue_cohort_weighted_share` = `+Inf` for a zero-weight borrowing Cohort | missing `+Inf → NaN` conversion | v0.20.1 / v0.19.8 (pr-16581) |
| `kueue_replaced_workload_slices_total` absent | never registered | v0.20.1 / v0.19.8 (pr-16743) |
| `kueue_cohort_subtree_admitted_active_workloads` zero or negative after re-parenting Cohorts | count not rebuilt on tree change | v0.20.0 / v0.19.7 / v0.18.11 (pr-16398) |
| LocalQueue metrics for every queue despite `localQueueSelector` | invalid selector parsed as "no filter" | v0.20.0 / v0.19.9 — now a startup failure (pr-16379; #16977 is ACTION REQUIRED in v0.19.9) |
| `kueue_cluster_queue_weighted_share` / `kueue_replaced_workload_slices_total` series for a deleted ClusterQueue, or a second weighted-share series with the old `cohort` label | not in the CQ cleanup scope | v0.20.2 / v0.19.9 (pr-16653) |
| Old custom-label series of a ClusterQueue or LocalQueue stay after a label change | Reconcile stored the new labels before the Update handler compared them | v0.20.2 / v0.19.9 (pr-17046) |
| `kueue_cohort_subtree_quota` / `_resource_reservations` vanish when one ClusterQueue of a Cohort is deleted | delete path cleared the Cohort's metrics and never re-recorded | v0.20.2 / v0.19.9 (pr-16762) |
| `kueue_local_queue_admitted_active_workloads` doubles after a CQ label change, or reaches -1 after an LQ label change | LQ series rebuilt from the CQ report | main; release-0.20 after v0.20.2 (pr-17336). Still broken when one LQ update changes a label **and** sets `stopPolicy` (issue-17356, open) |

## Bugs fixed in v0.20.2 / v0.19.9 (2026-10-15)

One row per user-visible fix in those changelogs that is not already covered above (source: CHANGELOG-0.20.md v0.20.2, CHANGELOG-0.19.md v0.19.9). "Both" means v0.20.2 and v0.19.9.

| Symptom | Cause | Fixed in |
|---|---|---|
| A Workload edited while the scheduler held it is over- or under-admitted (DRA) | requeued with quota charges from its previous spec; now handed back to the workload controller to recompute | both (#17208 / #17211). See [[dra]] |
| An elastic Workload's zero-count PodSet loses its flavor after an admission retry and later scale-up is blocked | flavor selection not kept across retries (`ElasticJobsViaWorkloadSlices`) | both (#17107 / #17146). See [[elastic-jobs]] |
| Workloads within nominal quota are preempted by fair sharing | the ClusterQueue borrowed on an uncontested flavor or inside a sub-Cohort, and was treated as borrowing overall | both (#17031 / #17095). See [[fair-sharing]] |
| An evicted JobSet keeps its quota and is never requeued | a JobSet restart recreated child Jobs that had already succeeded (reclaimable Pods) | both (#17215 / #17220). See [[integration-jobset]] |
| A suspended Pod / AppWrapper / Kubeflow job's queue-name was changed to a nonexistent LocalQueue; the job reconciler errors on every retry | the update was accepted; now rejected by the webhook | both (#16972 / #16973) |
| A terminating Pod group releases quota late | the deletion grace period was counted twice | both (#17077 / #17087). See [[integration-plain-pod]] |
| A single-Pod Workload preempted or evicted while still scheduling-gated stays `Requeued=False` forever; its Pod is never deleted | `SkipReassignmentForPodOwnedWorkloads` path did not requeue; stuck Workloads are requeued on upgrade | both (#17173 / #17204) |
| RayService webhook errors mention `spec.rayClusterSpec` | wrong field path; the field is `spec.rayClusterConfig` | both (#17097 / #17205) |
| ClusterQueues in one tree stop requeueing after a Cohort cycle is fixed | requeue not triggered for the tree | both (#17079 / #17080). See [[cohort]] |
| A Workload that must borrow cannot preempt in its own ClusterQueue although `withinClusterQueue` allows it | preemption path skipped within-CQ candidates when borrowing | both (#17010 / #17016). See [[preemption]] |
| (0.19) A SparkApplication with `restartPolicy` `OnFailure`/`Always` runs outside quota after a failed submission retry | the Workload was released in `SUBMISSION_FAILED` | v0.19.9 (#16976). See [[integration-spark]] |
| TAS preemption ignores Workloads on an overlapping flavor that would make room | candidates on overlapping TAS flavors were excluded; considered with `TASHandleOverlappingFlavors` | v0.20.2 (#16919) |
| With `FlavorFungibilityPreserveScanProgress`, `TryNextFlavor` Workloads retry a topology-blocked flavor or skip a viable borrowing flavor | scan progress handling | both (#17070 / #17072). See [[topology-aware-scheduling]] |
| Required-topology failure message does not say which level or that all Pods must fit one domain | message improved | both (#17172 / #17241) |
| Changing `maximumExecutionTimeSeconds` is rejected with "while workload quota reserved" though only `Admitted` blocks it | message now says "immutable while the workload is admitted" | both (#16946 / #16944) |
| AFS config errors for `usageSamplingInterval` / `resourceWeights` show the wrong value | value taken from another field | both (#16943 / #16942). See [[api-versions]] |
| A Workload with negative Pod overhead is accepted | `WorkloadValidateResourcesAreNonNegative` did not reach `spec.overhead` | both (#17201 / #17202) |
| A forged `role-hash` runs an oversized Pod under another role's quota | see the `PodExceedsRoleRequests` row below (Scheduling, TAS and integration symptoms); on these releases the check needs the **Alpha/off** `PodIntegrationVerifyRoleRequests` gate enabled | both (#17123 / #17124) |

## Fixed on main, pending the next patch release

| Symptom | Cause | Fix |
|---|---|---|
| After a cold leader start, TAS double-books nodes, or a new leader cannot borrow from Cohort quota for up to one lease duration | the scheduler started before every ClusterQueue was in the cache; Cohorts reached the cache only from `Reconcile` on followers | pr-16630 (main; release-0.20 pr-17455, after v0.20.2). See [[architecture#Startup: the scheduler waits for the initial cache]] |
| ClusterQueue usage under-counts an admitted Workload after an admission write timed out but committed | the rollback removed the cached Workload even after its update event re-added it; now `DeleteWorkloadIfUnchanged` | pr-17041 (main; release-0.20 pr-17474, after v0.20.2; the release-0.19 pick was closed) (source: pr-17041.md) |

## Visibility endpoint returns 500 / ServiceUnavailable

Before v0.20.0, a single pending Workload with nil `spec.priority` (typically a hand-made prebuilt Workload) made both `pendingworkloads` endpoints panic for every caller (pr-14411). Find it with `kubectl get workloads -A -o json | jq '.items[] | select(.spec.priority == null) | .metadata.name'` and set a priority or delete it; upgrading fixes it. See [[visibility-api]].

## Upgrade to v0.20+ fails or objects cannot be read

`v1beta1` is unserved from v0.20 and removed on main. Run `hack/migrate-to-v1beta2.sh` on the old version first; on recent versions it reports per-object failures instead of stopping, and objects whose current spec fails the validating webhook (for example a ClusterQueue with `lendingLimit > nominalQuota`) must be fixed by hand before they can be migrated (pr-16984). On large clusters, `--resources=cohorts,localqueues,clusterqueues` (main, pr-17159) migrates the small kinds first or reruns one kind. See [[api-versions]].


## Scheduling, TAS and integration symptoms (2026-10 batch)

| Symptom | Cause / fix |
|---|---|
| Preemptor stays pending; V(6) log `Discarding preemption targets: strategy verification failed` | `FairSharingVerifyFinalTargets` rejected a target set that would only be fair because of the preemptor's own preempted Workloads (the "own-only" limitation of pr-16343). Expected with the gate on; disabling it brings back the preemption loop. See [[fair-sharing]] |
| ClusterQueue `Active=False`, reason `CohortCycleDetected` | the Cohort parent chain forms a cycle; fix the `spec.parentName` links. The queue manager is now updated when a Cohort update creates a cycle (pr-16438). See [[cohort]] |
| Workload `QuotaReserved=False`, reason `PreemptionGated`, `BlockedOnPreemptionGates=True` | a MultiKueue preemption gate is closed; before pr-16627 the status update could be dropped on requeue, so the Workload showed `Pending`. See [[preemption]], [[multikueue-orchestrated-preemption]] |
| Admission retried endlessly with no condition; a non-CPU `resourceUsage` reads `9223372036854775807` | the admitted total overflowed `int64` and the API `Quantity` capped it; the webhook rejects it when not a multiple of the count. Known gap, open as of this snapshot (issue-16486). See [[scheduler-internals]] |
| Warning event `OutdatedScheduleCycle` ("Skipped admission write because the workload changed while it was being scheduled") | a TAS second pass (delayed topology assignment or failed-node replacement) was computed from a stale Workload; the write is rejected, the reservation kept, and the pass retried. Self-healing (v0.20.1 / v0.19.8). See [[topology-aware-scheduling]] |
| Pending message ends with `; topology spreading excluded N topology domain(s) at level: <key>` | a Required topology-spreading rule banned domains (pr-16421); raise the manager to `-v=3` to log the banned domain IDs and rules |
| `QuotaReserved` reason `AssignmentError`, log `Failed to compute the initial assignment` | `SchedulerLibraryDeepIntegration` (Alpha, main only) is on. **Updated 2026-10-21:** the scheduler-library planner is no longer inert; it now places Fit-mode TAS Workloads and returns an error (hence `AssignmentError`) only when the Workload needs preemption, which it does not support yet (pr-16483, pr-16482, pr-17183, pr-17209, pr-17400, pr-17278 / pr-17286). Reason `SchedulingSimulationFailed` means the simulation could not place the Pods. Turn the gate off if you need preemption. See [[topology-aware-scheduling]] |
| Elastic Pod on GKE stuck Unschedulable with nodeSelector `autoscaling.gke.io/provisioning-request=<id>` while the ProvisioningRequest is `Provisioned` | before v0.20.1 the Pod got `consume-provisioning-request` without `provisioning-class-name` (pr-16514). The nodeSelector is immutable, so delete the Pod after upgrading. See [[provisioning-request]] |
| JobSet whose TAS group members are not adjacent: Pods stuck `SchedulingGated` after admission, or carrying another ReplicatedJob's node selectors | admission info was applied by PodSet position; fixed by pr-17052 (matches by name). See [[topology-aware-scheduling]] |
| Job stays suspended with no Workload; it carries a priority-class label | look for the Warning event `WorkloadPriorityClassNotFound` (v0.20.0, pr-13775). Creating the class is picked up only on the next backoff retry (no WorkloadPriorityClass watch). See [[workload-priority]] |
| Pod-group member stuck `SchedulingGated` with event `PodExceedsRoleRequests` | the Pod requests more than the PodSet its `role-hash` names (`PodIntegrationVerifyRoleRequests`). See [[integration-plain-pod]] |
| Manager fails at startup with `MultiKueueRayInTreeAutoscaling` enabled | since v0.20.1 the gate depends on `SkipChildJobSuspension`; enable both (pr-16470). See [[feature-gates]] |
| Suspending a RayService creates a second, suspended RayCluster while the old one keeps running | `KubeRayServiceUsingTopLevelSuspend` is off (Alpha/off on release-0.20 from v0.20.1; Beta/on on main), so Kueue writes the template field `spec.rayClusterConfig.suspend`, which KubeRay treats as a zero-downtime upgrade. Turning the gate on needs KubeRay v1.7.0+ for the top-level `spec.suspend` (pr-16870, pr-16882). See [[integration-rayjob]] |
| SparkApplication cannot be stopped; the API rejects `executor.instances: 0` | Kueue wrote back `instances: 0` for an unset field; fixed by #15610, shipped in v0.20.2 (#16968) and v0.19.9 (#16967). See [[integration-spark]] |

## CLI, dashboard and test-suite symptoms

| Symptom | Cause / fix |
|---|---|
| `kueuectl version` prints only the client version on a Helm install with a non-default release name | the controller was looked up by Deployment name `kueue-controller-manager`; now by labels `app.kubernetes.io/name=kueue,control-plane=controller-manager` (pr-16609). Fixed in **v0.20.2 / v0.19.9** (#16953 / #16966). **Correction (2026-10-21):** this row earlier said v0.20.1 / v0.19.8; neither changelog lists it. A Helm `nameOverride` is still unsupported |
| `kueuectl list workload` fails with `resource name may not be empty` | a pending Workload has an empty `spec.queueName`; fixed by pr-16667, in v0.20.2 / v0.19.9 (pr-16986, pr-16978) |
| `kueuectl list workload --for` prints Workloads twice, or (0.19) never finishes when `-l` already contains `kueue.x-k8s.io/job-uid` | paginated job-UID search ending with an empty page started the owner fallback; fixed in v0.20.2 (#17084) / v0.19.9 (#16850). The hang was fixed in v0.20.0 and v0.19.9 (#16963). See [[kueuectl]] |
| `kueuectl create localqueue --dry-run=client` fails with `clusterqueues ... not found` offline | the ClusterQueue lookup ran even for client dry-run; fixed in v0.20.2 / v0.19.9 (#17109 / #17110) |
| `kueuectl create clusterqueue` fails with `must match the name in coveredResources` | flavors listed the same resources in different orders; fixed in v0.20.1 / v0.19.8 (pr-16531). `invalid resources specification` for names like `example.com/v100-gpu`: fixed by pr-16981 |
| `kueuectl delete workload` leaves the Job's Pods running | owners were deleted with the server default propagation (Orphan for Jobs); now Background, in v0.20.1 / v0.19.8 (pr-16510) |
| KueueViz list pages spin forever or keep stale rows on an empty cluster | the backend serialized nil slices as JSON `null`; fixed by pr-16739 (v0.20.2 / v0.19.9) and pr-16392. See [[dashboard]] |
| KueueViz Status column shows `QuotaReserved` for every Workload | the first condition type was shown; fixed in v0.20.2 / v0.19.9 (pr-17191 / pr-17192) |
| KueueViz Workload page for a pod group, StatefulSet or LWS shows no Pods | Pods were matched only by `controller-uid`; v0.20.2 / v0.19.9 add matching by pod-group name (feature, pr-16849) |
| KueueViz backend pod hangs in `Terminating` until SIGKILL | `Shutdown` had no deadline; 30 s timeout in v0.20.2 / v0.19.9 (pr-17198 / pr-17199) |
| KueueViz backend crash-loops after upgrade with `unsupported KUEUEVIZ_AUTH_MODE` | only `Disabled` and `TokenReview` are accepted now; before, a typo silently ran **without authentication**. Fix the value (pr-17143; release branches after v0.20.2 / v0.19.9) |
| KueueViz workload page fails after its LocalQueue was deleted; ResourceFlavor page shows "None" for node labels/taints; preemptor UID not linked | fixed on main (pr-17105, pr-17272, pr-17273), pending the next patch releases |
| KueueViz `/ws/namespaces` stops sending live updates to some users after upgrading to v0.20.2 | by design: live updates now need cluster-wide `watch localqueues`; the initial snapshot is still sent (pr-17180). Grant `watch` if those users should see updates |
| Integration suite fails in teardown | `verifyLogs` (`test/integration/framework/framework.go`) found an Error-level write-conflict log entry: log handled conflicts as diagnostics, not errors. Before pr-16793 (issue-16789) an Error entry whose `error` field was not a string (e.g. `zap.Bool("error", true)`) panicked `behavioral.IsLoggedEntryAConcurrentModification`; it now uses a checked type assertion. See [[testing-integration]] |

## Related pages

- [[kueue-overview]]
- [[workload]]
- [[workload-resource-adjustment]] — LimitRange defaults/constraints and the effective request view.
- [[admission]]
- [[cluster-queue]]
- [[local-queue]]
- [[kueuectl]]
- [[preemption]]
- [[provisioning-request]]
- [[admission-check]]
- [[visibility-api]]
- [[dashboard]]
- [[testing-integration]]
- [[api-versions]]
- [[topology-aware-scheduling]]
- [[metrics]]
- [[manage-jobs-selectively]]
- [[workload-max-execution-time]]
- [[failure-recovery]]
- [[scheduler-internals]]
