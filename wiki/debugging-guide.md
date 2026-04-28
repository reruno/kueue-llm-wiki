# Debugging Guide

**Summary**: A practical guide to diagnosing why Kueue workloads are stuck — covering quota exhaustion, flavor mismatches, admission check hangs, TAS failures, and preemption issues — with the specific commands and conditions to check.

**Sources**: `raw/kueue/pkg/controller/core/workload_controller.go`, `raw/kueue/pkg/debugger/`, `raw/github/kubernetes-sigs__kueue/` (issues), `raw/kueue/pkg/controller/core/clusterqueue_controller.go`

**Last updated**: 2026-04-28

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
| `PodsReady` | `False` | `PodsNotReady` | Pods not all Ready yet (waitForPodsReady configured) |
| `Evicted` | `True` | `Preempted` | Preempted by a higher-priority workload |
| `Evicted` | `True` | `PodsReadyTimeout` | Pods never became ready within the timeout |
| `Evicted` | `True` | `AdmissionCheck` | An admission check failed |
| `Deactivated` | `True` | `ExceededMaximumExecutionTime` | Maximum execution time exceeded |
| `Deactivated` | `True` | `ExceededBackoffLimit` | Failed too many times |

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
- `Rejected` — check failed permanently; workload will be evicted.

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
kubectl get pods -n <namespace> -l kueue.x-k8s.io/workload=<workload-name>
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

If [[failure-recovery]] is alpha-enabled and a node went offline, pods from a previous run might be stuck in `Terminating`, consuming TAS slots. Check:
```bash
kubectl get pods --all-namespaces | grep Terminating
```

---

## Root cause 6: Workload is deactivated

**Symptom**: `Deactivated: True`. The workload has `spec.active: false`.

Possible causes:
- **Exceeded backoff limit** — the job failed too many times.
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
kubectl kueue list localqueue <name> --namespace <ns>

# Pause/resume a ClusterQueue
kubectl kueue stop clusterqueue <name>
kubectl kueue resume clusterqueue <name>

# Stop a workload (deactivate)
kubectl kueue stop workload <name> -n <namespace>
```

See [[kueuectl]] for the full command reference.

---

## Step 4: Check Kueue manager logs

The scheduler logs at `V(2)` show each cycle's nomination and admission results:

```bash
kubectl logs -n kueue-system deployment/kueue-controller-manager | grep -E "schedulingCycle|Nomination|admitted|Inadmissible"
```

Common useful log entries:
- `Nomination done` — how many workloads were nominated vs. inadmissible.
- `Attempting to schedule workload` + workload name — the scheduler is processing it.
- `Workload is inadmissible` — with the reason string.

For verbose quota details: increase log level to `V(3)` or `V(5)` in the manager deployment.

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

## Related pages

- [[kueue-overview]]
- [[workload]]
- [[admission]]
- [[cluster-queue]]
- [[local-queue]]
- [[kueuectl]]
- [[preemption]]
- [[provisioning-request]]
- [[admission-check]]
- [[topology-aware-scheduling]]
- [[metrics]]
- [[manage-jobs-selectively]]
- [[workload-max-execution-time]]
- [[failure-recovery]]
- [[scheduler-internals]]
