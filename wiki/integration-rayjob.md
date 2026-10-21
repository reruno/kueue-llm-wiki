# Integration: RayJob and RayCluster

**Summary**: KubeRay's RayJob and RayCluster each have their own Kueue integration. RayCluster is a long-lived cluster you submit Ray jobs into; RayJob bundles a cluster with a job entrypoint. Kueue accounts for the head pod, the worker groups, and (for RayJob) a short-lived submitter Pod.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16870.md, pr-16882.md, pr-16897.md, pr-16908.md, pr-16915.md, pr-17060.md, pr-17097.md, pr-13244.md, pr-13996.md, pr-14036.md, pr-16853.md, pr-16854.md, pr-16884.md, pr-17366.md, pr-17367.md, pr-17205.md, pr-16259.md, pr-17466.md, pr-17464.md, pr-17513.md, raw/kueue/pkg/controller/jobs/raycluster/common.go, raw/kueue/pkg/controller/jobs/rayservice/rayservice_multikueue_adapter.go, raw/kueue/pkg/controller/jobs/ray/ray_multikueue_adapter.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/pkg/controller/jobs/rayservice/rayservice_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-21

---

## Shape

A RayCluster has `spec.headGroupSpec` and `spec.workerGroupSpecs[]`. A RayJob additionally has `spec.submitterPodTemplate`.

Kueue's RayCluster integration produces:

- One PodSet for the head.
- One PodSet per worker group. Its `count` is `effectiveWorkerCount`: `replicas` **clamped to `[minReplicas, maxReplicas]`**, multiplied by `numOfHosts` when `numOfHosts > 1` (see [[#Worker counts respect `minReplicas` and `maxReplicas`]]). **An absent `replicas` counts as `minReplicas`** (0 when that is unset too), matching the KubeRay CRD default (`+kubebuilder:default:=0`; KubeRay itself falls back to `minReplicas`, which defaults to 0). The helper is shared by `BuildPodSets`, `UpdatePodSets` and the MultiKueue elastic replica sync (source: raw/kueue/pkg/controller/jobs/raycluster/common.go). **Correction (2026-10-21)**: this page said `count = replicas × minReplicas`. Before [[pr-16897]] an absent `replicas` counted as **1**, so an object built before API defaulting could yield a different PodSet count from the stored object. The fallback changed in v0.20.1 ([[pr-16908]]) and v0.19.8 ([[pr-16915]]) (source: pr-16897.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md). Applying `minReplicas`/`maxReplicas` bounds to the count is now done by [[pr-16884]] (next section). **Correction (2026-10-21)**: this page listed it as open work.

The RayJob integration further accounts for the **submitter Pod** — a transient Pod that drives the job via the Ray client. "PodSets for RayJobs should account for submitter Job Pod" ([[issue-1434]]) tracked making that accounting explicit so the cluster's quota picture doesn't omit it.

**Worker-group cap.** Because each worker group becomes its own PodSet and the head reserves one PodSet, the number of worker groups is bounded by the [[workload]] `spec.podSets` length limit. [[pr-11388]] raised that limit from 8 to **10**, so a RayCluster/RayJob/RayService can now declare up to **9 worker groups** (was 7).

## Adding RayCluster support

RayCluster came later than RayJob ("Add support for RayCluster" — [[issue-1272]]). The integration posed questions about longer-lived Workloads whose underlying object doesn't naturally have a "finished" state.

## Suspend vs scheduling gates

RayCluster's native `spec.suspend` flag controls whether the Ray head and workers are created. Kueue toggles it. Dynamic scaling (adding worker replicas after admission) uses Pod scheduling gates per [[elastic-jobs]]; "Kueue sometimes does not inject scheduling gates for elastic jobs" ([[issue-10167]]) and "RayCluster with elastic jobs via workload-slices support should support scheduling pending workload after freeing capacity on scale-down" ([[issue-10170]]) are the canonical elastic+Ray issues.

## Operational quirks

- **Status timeliness.** RayJob status updates lagged ([[issue-1164]]). Admitted RayJobs sometimes stayed pending when `manageJobsWithoutQueueName: true` was enabled ([[issue-1568]]).
- **Preempted RayJob resume.** "Preempted RayJob will not resume when resource reclaimed" ([[issue-1146]]) was an earlier bug; resuming Ray state after preemption is not trivial.
- **In-tree autoscaling.** "Flaky E2E: Kuberay Should run a rayjob with InTreeAutoscaling" ([[issue-10438]], [[issue-10642]]) — interaction with Ray's internal autoscaler is complex because it changes replica counts outside Kueue's direct control.
- **redis-cleanup Pods.** "Kueue does not remove the scheduling gate from Ray's redis-cleanup jobs" ([[issue-8443]]) — a post-termination Pod got left gated.

## Ray version pin (v0.18.0)

Kueue's e2e fixtures and the RayJob submitter image were bumped from **Ray 2.41.0 → 2.53.0** in [[pr-10707]] (cherry-picks [[pr-10958]] and [[pr-10959]]). The 2.41.0 line had a SIGABRT in the opencensus dependency (`ray-project/kuberay#4760`) that destabilized the Ray submitter Pod. 2.53.0 also requires that Kueue's TAS RayJob e2e bumps the head CPU and CQ quota — see the test bump in PR #10970. Operators upgrading to v0.18 should plan for this Ray version's resource baseline.

## Redis cleanup Job accounting (GCS fault tolerance, v0.19)

When KubeRay **GCS fault tolerance** is enabled, KubeRay spawns a short-lived **Redis cleanup Job** during RayCluster teardown (to clear the cluster's data from the external Redis). Kueue built PodSets only from the head + worker groups, so the cleanup Job's requests were never reserved → quota **under**-accounting ([[pr-11260]], fixes [[issue-10946]]).

The fix **folds** the cleanup Job's requests into the **Ray head PodSet** using max-accounting, rather than adding a separate PodSet (which would have eaten one of the 8 `MaxPodSets` slots). Details:

- The cleanup Job's requests are **hardcoded in KubeRay** at **200m CPU / 256Mi memory**; `accountForRedisCleanupInHeadPodSet` merges them into the head container via `MergeResourceListKeepMax` (so the head's reservation is `max(head, cleanup)`, not a sum).
- Gated by the **`KubeRayAccountForRedisCleanup`** feature gate (Beta, default on; introduced v0.19, GA targeted v0.21) — a bailout for clusters running the KubeRay operator with `ENABLE_GCS_FT_REDIS_CLEANUP=false`. The accounting only applies when GCS fault tolerance is actually detected (`GcsFaultToleranceOptions != nil` or the annotation).
- `ExpectedPodSetsCount = len(workerGroupSpecs) + 1`; the PodSet count is **unchanged** because the cleanup is folded into the head. Applies to all three controllers — **RayCluster, RayJob, and RayService**.

## MultiKueue

RayJob and RayCluster have MultiKueue adapters; cross-cluster status mirroring is nontrivial because Ray's state space is large.

**RayService worker RBAC.** RayService has been MultiKueue-managed since v0.17.0, but the worker-cluster ClusterRole generated by `create-multikueue-kubeconfig.sh` originally omitted `rayservices` / `rayservices/status`, so a dispatched RayService failed at the API level on the worker. [[pr-11400]] adds those rules; hand-written worker ClusterRoles must include them. See [[multikueue#RBAC: RayService on worker clusters]].

## TAS

Rank-based ordering within TAS for Ray worker groups is tracked ([[issue-3716]] — TAS: Implement e2e tests for RayJob with TAS).

## Removing the `queue-name` label is rejected

Removing `kueue.x-k8s.io/queue-name` from an **unsuspended** RayJob / RayCluster / RayService / SparkApplication used to be accepted. The job then stopped being managed by Kueue while its Pods kept running, and its resources stopped counting against quota — a straightforward quota leak that any job owner could trigger.

[[pr-13293]] (cherry-picks [[pr-14666]], [[pr-14676]]) rejects the removal in the validating webhook:

- from an **unsuspended** job, always;
- from a **suspended** job in a namespace that has a default LocalQueue (where the label would otherwise be re-defaulted inconsistently).

Controlled by the `ValidateRayAndSparkJobUpdates` feature gate, **Beta and enabled by default**. Also covers [[integration-spark]].

## KubeRay v1.7.0

The bundled `github.com/ray-project/kuberay/ray-operator` dependency moved **v1.6.2 → v1.7.0** ([[pr-14669]]). `hack/make/deps.mk` derives both the e2e `KUBERAY_VERSION` and the generated `dep-crds/ray-operator` from this module version, so the operator and CRDs used by the KubeRay e2e suite move with it — no separate bump. No Kueue source changes were needed. `go mod tidy` dropped `github.com/hashicorp/golang-lru/v2` and `github.com/smallnest/chanx` from the indirect set.

v1.7.0 is the first KubeRay release shipping the top-level `RayService.Spec.Suspend` field and its `Suspending`/`Suspended` lifecycle (kuberay#4841), which the RayService upgrade-gating work depends on.

## Elastic RayCluster specifics

- **MultiKueue + in-tree autoscaling is rejected at admission** ([[pr-14061]], [[pr-13244]]). The reason was a mismatch in autoscaler-sidecar accounting between manager and worker, which finished the Workload right after admission. Opt-in through `MultiKueueRayInTreeAutoscaling`, which now also requires `SkipChildJobSuspension`. See [[multikueue#Elastic RayCluster with in-tree autoscaling]] and [[elastic-jobs#MultiKueue rejects an autoscaling elastic RayCluster]].
- **Non-elastic autoscaling error message** ([[pr-13996]]) now names the fix: enable `ElasticJobsViaWorkloadSlices` and set `kueue.x-k8s.io/elastic-job: "true"`. The text is built from the constants (source: pr-13996.md).
- **Partial scale-up (Alpha)** — with `ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp` on, the `kueue.x-k8s.io/elastic-job-scale-up-strategy: partial` annotation set, and `minReplicas` configured, `BuildPodSets` sets the worker PodSet's `MinCount` to the effective minimum worker count ([[pr-14909]]). No effect with the gate off.

## Worker counts respect `minReplicas` and `maxReplicas`

KubeRay always runs at least `minReplicas` and at most `maxReplicas` Pods per worker group, whatever `replicas` says. Kueue used the raw `replicas`. When `replicas < minReplicas`, the worker PodSet was smaller than the real number of worker Pods, and the extra Pods stayed scheduling-gated until `replicas` was raised (source: pr-16884.md).

Production trigger: on Ray 2.55.1 (autoscaler v2) with `minReplicas = maxReplicas = 2`, an allocation timeout (`RAY_AUTOSCALER_RECONCILE_ALLOCATE_STATUS_TIMEOUT_S`) makes the autoscaler terminate one Pod and set `replicas` to 1. KubeRay keeps 2 Pods because of the minimum, but Kueue shrank the PodSet to 1. A bug in that Ray version keeps the autoscaler from raising `replicas` back, so one Pod stayed gated forever, even after capacity freed up. Ray 2.46.0 (autoscaler v1) and 2.58.0 restore `replicas` and do not hit it (source: pr-16884.md).

[[pr-16884]] makes `effectiveWorkerCount` clamp the count (source: raw/kueue/pkg/controller/jobs/raycluster/common.go):

| `replicas` | Count used |
|---|---|
| nil, or below `minReplicas` (default 0) | `minReplicas` |
| above `maxReplicas` (default `MaxInt32`) | `maxReplicas` |
| otherwise | `replicas` |

The result is multiplied by `max(numOfHosts, 1)`. `BuildPodSets` (PodSet `count`, and `MinCount` for partial scale-up), `UpdatePodSets` (runtime counts read from a RayJob's or RayService's child RayCluster; a group with nil `replicas` is skipped there) and `WorkerGroupPodCounts` (MultiKueue runtime state) all use it. This makes Kueue independent of the Ray autoscaler version.

Releases: `main` (merged 2026-10-16), release-0.20 ([[pr-17366]]) and release-0.19 ([[pr-17367]]). All merged after v0.20.2 / v0.19.9, so the next patch releases are the first to include it (source: pr-17366.md, pr-17367.md).

## Head-container validation

A Ray head Pod template with an empty `containers` list is allowed by the CRD schema but breaks Kueue: with `submissionMode: K8sJobMode` and no `submitterPodTemplate`, the default submitter template is built from the head Ray container image, indexing the head containers unchecked (webhook and reconciler panic). A controller-side guard (pr-16055) was **reverted** (pr-16089) in favour of admission validation: the shared `raycluster.ValidateCreate` helper now rejects RayCluster specs whose head Pod has no containers, and RayJob and RayService return those errors before topology validation can consume the spec (source: pr-16055.md, pr-16067.md, pr-16089.md; backports pr-16084.md, pr-16085.md, and reverts pr-16106.md, pr-16107.md). Consequence: RayJobs created before the webhook validation existed are not protected by a controller fallback.

The RayCluster webhook now reuses the same shared `raycluster.ValidateCreate` used for the embedded `RayClusterSpec` in RayJob and RayService, so autoscaling validation, the maximum PodSet count and the reserved head group name are checked in one place; the actionable autoscaling error (which feature gate and annotation enable the supported configuration) is the same for all three. RayCluster-specific elastic-job validation stays in the RayCluster webhook as an additive check (source: pr-16071.md). `RestorePodSetsInfo` skips restoring (and logs at V(2) with expected/actual counts) when the job's pod set count differs from the Workload's, e.g. after a worker group is added to a running RayCluster (source: pr-13114.md; see [[job-framework-interface#`RestorePodSetsInfo` takes a context]]).

## Elastic partial scale-up and MultiKueue autoscaling

- With the partial scale-up annotation, `BuildPodSets` sets each worker PodSet's `MinCount` to its own effective count (`effectiveWorkerCount`: `Replicas` clamped to the replica bounds since pr-16884); `MinReplicas` is no longer *required*, and PodSets are matched by name across slices. Details in [[elastic-jobs#Partial scale-up: the baseline/target model]] (source: pr-16209.md, pr-16242.md, pr-16289.md).
- RayJob is the top-level Kueue-managed object for in-tree autoscaling, so enabling autoscaling must not change `spec.suspend`; the test helper `EnableInTreeAutoscaling` no longer forces `Suspend=false` (source: pr-15840.md; backports pr-15841.md, pr-15842.md).
- MultiKueue reverse sync for an autoscaling RayJob is triggered from the child RayCluster on the worker cluster, see [[elastic-jobs#MultiKueue and elastic slices]] (source: pr-16315.md).
- `RayService.PodSets` uses the `client.Client` passed in (no package-level reconciler state) (source: pr-16042.md).

## RayService suspend uses the top-level `spec.suspend` (KubeRay ≥ 1.7)

Kueue used to read and write `spec.rayClusterConfig.suspend` on a RayService. That field is the suspend setting of the RayCluster **template**. Setting it to true makes KubeRay start a zero-downtime upgrade: it creates a **new** suspended RayCluster while the old one keeps running, and the new one stays suspended forever. KubeRay v1.7.0 added a real top-level `RayService.spec.suspend` (source: pr-16870.md).

- [[pr-16870]] switches `IsSuspended`, `Suspend` and `RunWithPodSetsInfo` to `spec.suspend` behind **`KubeRayServiceUsingTopLevelSuspend`**: **Beta, on by default on `main`** (versioned 0.21, planned GA in 0.23). With the gate off, the legacy nested field is used (source: raw/kueue/pkg/controller/jobs/rayservice/rayservice_controller.go, raw/kueue/pkg/features/kube_features.go). RayJob already used its top-level field correctly; the RayService code was a copy-paste leftover from RayCluster.
- **ACTION REQUIRED**: if you use the RayService integration, upgrade KubeRay to **v1.7.0+** before upgrading Kueue to a release that has the gate on. Otherwise disable the gate.
- Backports: release-0.20 ships the gate **Alpha, off by default**, in v0.20.1 ([[pr-16882]]). The release-0.19 backport (pr-16883) was closed, because release-0.19 vendors KubeRay v1.6.2, which has no top-level field (source: pr-16870.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).
- Related: with KubeRay ≥ 1.7, suspending a RayService deletes its child RayCluster. This is why disabling Kueue's own child suspension (`SkipChildJobSuspension`) is considered safe for RayService; see [[job-framework-interface#Child jobs: `SkipChildJobSuspension`]].

## RayService validation errors use `spec.rayClusterConfig`

RayService webhook errors reported paths under `spec.rayClusterSpec` (the Go field name). The serialized field is `spec.rayClusterConfig`. For example, the autoscaling error appeared at `spec.rayClusterSpec.enableInTreeAutoscaling`. [[pr-17060]] fixes the head-group, worker-group and cluster-spec paths (`field.NewPath("spec", "rayClusterConfig", ...)`). Shipped in **v0.20.2** ([[pr-17097]]) and **v0.19.9** ([[pr-17205]]) (source: pr-17060.md, pr-17205.md, raw/kueue/pkg/controller/jobs/rayservice/rayservice_webhook.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

## MultiKueue: RayService `serveConfigV2` edits are forwarded

With `MultiKueueRemoteSpecSync` (Beta/on in v0.20.0; also in v0.19.1 / v0.18.5), editing `serveConfigV2` on the manager RayService is applied in place to the worker copy within about a second. `rayClusterConfig` and `upgradeStrategy` changes are still **not** forwarded. See [[multikueue#Manager-side gate `MultiKueueRemoteSpecSync`]] ([[pr-14036]]).

## MultiKueue: RayService worker autoscaling

A MultiKueue-managed RayService with `enableInTreeAutoscaling` used to be rejected always, even with `MultiKueueRayInTreeAutoscaling` on. [[pr-16259]] adds RayService to worker-side autoscaling, next to RayCluster and RayJob. It needs `MultiKueueRayInTreeAutoscaling` (**Alpha, off**) and an elastic RayService (`kueue.x-k8s.io/elastic-job: "true"`, `ElasticJobsViaWorkloadSlices`). The manager reads worker counts from the worker RayService's **active** child RayCluster (`status.activeServiceStatus.rayClusterName`), writes them onto the manager copy as runtime annotations, creates or updates the workload slice, and repoints the worker RayService once the replacement slice is admitted. The lookup ignores a RayCluster that the RayService does not control or that has worker groups the service does not declare. In-place `serveConfigV2` updates during autoscaling were dropped at first and are fixed by [[pr-17464]]. Details: [[multikueue#RayService worker autoscaling]].

Releases: `main` and **release-0.20 only** ([[pr-17466]], [[pr-17513]]), merged 2026-10-20, after v0.20.2. Maintainers backported the feature to complete KubeRay autoscaling support in 0.20. There is no release-0.19 backport (source: pr-16259.md, pr-17466.md, pr-17513.md).

## RayJob `ValidationFailed` puts the Workload on hold

`RayJob` implements `JobWithOnHold`: `IsOnHold()` is true when `status.jobDeploymentStatus == ValidationFailed`. The generic reconciler then releases the Workload's quota with `QuotaReserved=False`, reason `OnHold`, and does not requeue it (source: raw/kueue/pkg/controller/jobs/rayjob/rayjob_controller.go). See [[job-framework-interface#`JobWithOnHold`]].

## Multi-host worker groups: topology subgroups

For worker groups with `replicas` and `numOfHosts`, the worker PodSet's TopologyRequest now carries `SubGroupCount = replicas`, `PodIndexLabel = ray.io/replica-host-index` and `SubGroupIndexLabel = ray.io/worker-group-replica-index`. TAS (and the GKE slice controller) can then place each replica's `numOfHosts` Pods as one group. Before this, such Workloads were never admitted, because the slice size was computed wrongly. Gate `KubeRayEvictOnInconsistentTopologyRequest` (Alpha, **off**) decides whether an already-admitted Workload without these fields is treated as inconsistent and replaced. With the default off, it keeps running (#15677; v0.20.1 pr-16853, v0.19.8 pr-16854; the 0.19 backport omits the MultiKueue runtime-count topology updates) (source: pr-16854.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). See [[topology-aware-scheduling]].

KubeRay version support: maintainers intend to document support for only the last few KubeRay releases (N-2/N-3); issue-16906 is open (source: pr-16897.md).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — head + workers + submitter decomposition.
- [[elastic-jobs]] — Ray is the biggest consumer.
- [[multikueue]] — Ray + multi-cluster.
- [[topology-aware-scheduling]] — Ray + topology.
- [[job-framework-interface]]
