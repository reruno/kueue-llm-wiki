# Integrations

**Summary**: An "integration" is a per-job-type controller inside Kueue that observes a particular CRD (batch/v1 Job, JobSet, RayJob, PyTorchJob, etc.), wraps each labeled instance in a [[workload]], and toggles `.spec.suspend` or scheduling gates when Kueue admits the Workload. Each integration handles the quirks of its target API — how many PodSets to emit, how tolerations flow, how status mirrors back — while the core scheduler stays generic.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16773.md, pr-16779.md, pr-16370.md, pr-13375.md, issue-16517.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-16937.md, pr-17035.md, pr-16474.md, issue-16333.md, pr-15412.md, pr-16994.md, pr-17053.md, pr-17454.md, pr-16044.md, pr-17255.md, pr-16884.md, pr-16259.md, pr-17464.md, pr-17147.md, raw/kueue/pkg/features/kube_features.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, pr-17059.md, pr-16612.md, pr-17420.md, pr-16175.md, pr-17845.md, pr-17563.md, pr-16982.md, pr-17382.md, pr-18010.md, pr-18218.md, pr-18266.md, pr-18195.md, pr-18287.md, pr-17903.md, pr-18250.md, pr-18591.md, pr-18783.md, pr-17937.md, pr-18868.md, pr-18600.md, pr-17910.md, pr-18730.md, pr-18038.md, pr-18180.md

**Last updated**: 2026-11-24

---

## What an integration does

For each supported job type, the integration:

1. Watches objects of that type in the API server.
2. On create, if the object carries `kueue.x-k8s.io/queue-name: <lq>`, sets `.spec.suspend: true` (or injects scheduling gates on Pods) and creates an owned [[workload]] describing the PodSets.
3. On Workload `Admitted`, patches the object to un-suspend (or removes gates). May apply `podSetUpdates` from [[admission-check]]s (extra tolerations, node selectors).
4. Mirrors job status back to the Workload: `Finished` when the job completes, `PodsReady` when all Pods are ready.
5. On Workload `Evicted`, re-suspends the object and deletes Pods.

## Enabled integrations

Integrations are enabled via `integrations.frameworks` in the Kueue configuration. Each can be independently disabled.

See dedicated pages:

- [[integration-batchjob]] — batch/v1 Job (the baseline).
- [[integration-jobset]] — JobSet (the recommended multi-template primitive).
- [[integration-kubeflow]] — PyTorchJob, TFJob, MPIJob, PaddleJob, XGBoostJob, JAXJob.
- [[integration-trainjob]] — **[Alpha]** TrainJob (Training Operator v2; successor to the Kubeflow v1 jobs).
- [[integration-rayjob]] — RayJob and RayCluster.
- [[integration-leaderworkerset]] — LeaderWorkerSet (LWS).
- [[integration-appwrapper]] — AppWrapper (Project CodeFlare), used to wrap unsupported types.
- [[integration-argo-workflow]] — Argo Workflows (via the `pod` integration; Pod-level gating, no `integrations.frameworks` entry of its own).
- [[integration-plain-pod]] — plain Pods and PodGroups.
- [[integration-statefulset]] — **[Stable]** StatefulSet (uses pod scheduling gates instead of `spec.suspend`).
- [[integration-spark]] — **[Alpha]** SparkApplication (Kubeflow Spark Operator v2).

## `manageJobsWithoutQueueName`

A global config toggle: if true, Kueue manages every job of supported types even without the `queue-name` label, using a default LocalQueue. Historically the interaction of `manageJobsWithoutQueueName` with RayJob left admitted RayJobs in pending state ([[issue-1568]]), so operators should enable this deliberately and test integrations that lag its semantics.

## PodSets per integration

One of the hardest parts of adding an integration is getting PodSet decomposition right:

- **batch/v1 Job** — one PodSet.
- **JobSet** — one PodSet per replicated job, with `count = replicas × pods per replica`. Empty replicated jobs (`replicas: 0`) were a surprising bug ([[issue-2227]]).
- **RayJob** — head + worker groups, plus a "submitter Job Pod" that also counts against quota ([[issue-1434]] — PodSets for RayJobs should account for submitter Job Pod).
- **Kubeflow jobs** — one PodSet per replica type (master, worker, ps, chief, etc.). MPIJob specifically has launcher + workers.
- **LeaderWorkerSet** — leader + worker PodSets per group; TAS-ranked co-scheduling matters ([[issue-4531]]).

## ResourceFlavor label/toleration propagation

Every integration must flow the [[resource-flavor]]'s `nodeLabels` and `tolerations` into the pod template it controls. Bugs here show up as "pods of PyTorchJob don't go to the right node" ([[issue-1407]]) or MPIJob workers having inconsistent selectors vs. workers ([[issue-3400]]).

## MultiKueue compatibility

Not all integrations work with [[multikueue]] out-of-the-box. Each needs a MultiKueue adapter that can mirror the job to a worker cluster and mirror status back. AppWrapper's adapter is tracked under [[issue-3989]]; PodGroup support under [[issue-4719]].

## Recent cross-integration behaviour (v0.20 line)

- Feature gates that shape integration behaviour: `PodIntegrationCountSucceededPodsAsReady` (Beta, on), `DeploymentJobUIDLabel` (Beta, on), `ValidateRayAndSparkJobUpdates` (Beta, on), `FinalizeTerminatingPodGroups` (Beta, on since v0.20; Alpha/off on release-0.19), `EnforceProvisioningPodTemplateContents` (see [[provisioning-request]]). See [[integration-plain-pod]] (sources: pr-15734.md, pr-15641.md, pr-15628.md, pr-13015.md).
- **Serving integrations (StatefulSet, LeaderWorkerSet, Deployment) share the Pod reconciler.** Webhooks for these three run on update as well as create, which makes them sensitive to defaulting bugs: with `WorkloadPriorityClassDefaulting`, the mutating webhook adds `kueue.x-k8s.io/priority-class: default` on update even for unmanaged objects without a queue-name, and the validating webhook rejected it on Ready objects ("WorkloadPriorityClass cannot be added to a non-suspended workload") ([[issue-16333]]). Fixed by [[pr-16474]]: the defaulting now skips a running object that did not have the label. On `main`, release-0.20 and release-0.19, after v0.20.2 / v0.19.9. See [[workload-priority#Default WorkloadPriorityClass is skipped on updates to running serving workloads]] (source: pr-16474.md). **Correction (2026-10-21)**: this bullet listed issue-16333 as open. **Correction (2026-10-21)**: this page listed Workload control metadata being inherited from the Job or Pod ([[issue-16322]]) as open. It is fixed: Kueue's internal labels/annotations are never copied (v0.20.1 / v0.19.8), and naming them in `labelKeysToCopy` is logged at startup. See [[job-framework-interface#Internal labels and annotations are never inherited]] (source: pr-16773.md, pr-16779.md).
- **Pod-level `WorkloadAnnotation`.** `kueue.x-k8s.io/workload` is written into each PodSet's template info by the shared jobframework path when the job starts. Since [[pr-15412]] (`main` only) it is written regardless of feature gates, so every integration's Pods carry it. See [[job-framework-interface#`kueue.x-k8s.io/workload` is always set on the PodTemplate]] (source: pr-15412.md). **Correction (2026-10-21)**: this bullet said StatefulSet and LWS each set it themselves. They rely on the shared path (pr-15142 merged as tests only).
- **Quota accounting per integration:** batch Job reclaimable pods ([[integration-batchjob#Reclaimable pods when `parallelism > completions`]]); Spark requests mirror Spark's computation ([[integration-spark]]); PodRequests helper ([[integration-plain-pod#Pod-level requests and quota]]).
- **RBAC:** AppWrapper was the only CRD integration without editor and viewer ClusterRoles; they were added modelled on SparkApplication's, and `rbac.md` now lists what batch-admin and batch-user cover (source: pr-16096.md). JAXJob/TrainJob delete permission: [[integration-trainjob]].
- **Ray:** head-container validation is shared across RayCluster/RayJob/RayService ([[integration-rayjob#Head-container validation]]). An absent worker `replicas` now counts as `minReplicas` (0 if unset). RayService suspends through the top-level `spec.suspend` (KubeRay ≥ 1.7, gate `KubeRayServiceUsingTopLevelSuspend`) ([[integration-rayjob]]).
- **Child jobs:** with `SkipChildJobSuspension` (Alpha, off) the generic reconciler no longer suspends Kueue-managed child jobs. The parent controller handles that ([[job-framework-interface#Child jobs: `SkipChildJobSuspension`]]).
- **Defaulting:** the default `queue-name` is no longer injected in namespaces excluded by `managedJobsNamespaceSelector` (v0.20.0, [[local-queue-defaulting]]). A changed queue name is validated on update for every integration ([[job-framework-interface#Queue-name format is validated on update]]).
- **Serving rollouts:** StatefulSet/LWS current-revision Pods stay gated until admission, and the legacy finalizer cleanup is removed ([[integration-statefulset]]). An LWS percentage `maxSurge` is honoured ([[integration-leaderworkerset]]).
- **Pod groups:** forged role hashes are caught before ungating, PodSet order comes from shape, and the deletion-deadline activity check is fixed ([[integration-plain-pod]]). Pods owned by a known integration still cannot opt into plain-Pod management ([[issue-16517]], closed without implementation).
- **Spark:** `SUBMISSION_FAILED` no longer finishes the Workload ([[integration-spark]]).

## Fixes merged 2026-10-14 to 2026-10-21

Most of these went to `main`, release-0.20 and release-0.19 after v0.20.2 / v0.19.9 were cut. All unmarked items shipped in **v0.20.3** and **v0.19.10**, except the RayService items, which are on release-0.20 only and shipped in v0.20.3. The two items marked as shipped were already in v0.20.2 / v0.19.9 (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md). **Correction (2026-10-28)**: this note said they would first ship in the next patch releases.

- **Prebuilt Workloads:** a job no longer adopts an unrelated prebuilt Workload that is already finished ([[job-framework-interface#A finished prebuilt Workload is not adopted]], pr-16994).
- **Single Pods:** with `SkipReassignmentForPodOwnedWorkloads`, a Workload evicted while its Pod is still gated is requeued instead of parked forever. Shipped in v0.20.2 / v0.19.9 ([[integration-plain-pod#Single-Pod Workloads evicted while still gated are requeued]], pr-17053).
- **Pod groups:** a new group Workload is not built from Pods that are still terminating on a node ([[integration-plain-pod#Mixed groups: terminating Pods do not shape a new Workload]], pr-17454).
- **StatefulSet:** scale-to-zero keeps quota until owned Pods are inactive ([[integration-statefulset#Scale-to-zero keeps quota while owned Pods are active]], pr-16044).
- **LeaderWorkerSet:** a queue-name change is rejected while any group Workload holds quota ([[integration-leaderworkerset]], pr-17255).
- **Ray:** worker PodSet counts respect `minReplicas` / `maxReplicas` ([[integration-rayjob#Worker counts respect `minReplicas` and `maxReplicas`]], pr-16884). MultiKueue RayService worker autoscaling is supported (`main` and release-0.20 only), and `serveConfigV2` edits reach the worker while it autoscales ([[multikueue#RayService worker autoscaling]], pr-16259, pr-17464).
- **JobSet:** an evicted Workload is no longer stuck holding quota after a JobSet restart ([[integration-jobset#Eviction after a JobSet restart]], pr-17147). Shipped in v0.20.2 / v0.19.9.

## Fixes merged 2026-10-21 to 2026-10-27

- **batch/Job (MultiKueue):** a re-dispatched Job no longer loops on `PodsReady` evictions on Kubernetes 1.35+, because the manager's `status.failed` is never lowered. Shipped in v0.20.3 / v0.19.10 ([[integration-batchjob#MultiKueue]], pr-17059).
- **TrainJob:** the dry-run Workload used for PodSet defaulting has a generated name, so a same-named Workload no longer blocks admission. Shipped in v0.20.3 / v0.19.10 ([[integration-trainjob#PodSet defaulting uses a dry-run Workload with a generated name]], pr-17563).
- **All integrations:** a job whose Namespace is not yet in the informer cache is requeued instead of left without a Workload (`main`, release-0.20, release-0.19; [[job-framework-interface#A Namespace missing from the cache requeues the job]], pr-16982).
- **LeaderWorkerSet (MultiKueue):** the shared remote LWS is kept until its last group leaves the worker, and a scale-down shrinks it (`main`, release-0.20, release-0.19; [[integration-leaderworkerset#MultiKueue]], pr-16612).
- **Single Pods (MultiKueue):** the gated manager Pod's copied status is reset after the Workload is requeued (`main`, release-0.20; [[integration-plain-pod#MultiKueue]], pr-17420).
- **MultiKueue (all adapters):** a worker watch reconnect resyncs the affected manager Workloads at once (`main`, release-0.20; [[multikueue#Reconnect triggers an immediate Workload resync]], pr-16175 / pr-17845).
- **SparkApplication:** PodSet index constants only, with no behaviour change (pr-17382).

Unless marked as shipped, these are not in the v0.20.3 / v0.19.10 notes (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

## Graduation levels (docs overview table)

The integrations overview page in the docs now lists each in-tree integration's stability level, with deprecated integrations moved to the end of the table (source: pr-16937.md, pr-17035.md):

| Level | Integrations |
|---|---|
| Stable | AppWrapper, batch/v1 Job, Deployment, JobSet, LeaderWorkerSet, MPIJob, Pod and pod groups, RayCluster, RayJob, RayService, StatefulSet |
| Alpha | SparkApplication, TrainJob (Kubeflow Trainer v2) |
| Deprecated | JAXJob, PaddleJob, PyTorchJob, TFJob, XGBoostJob (Kubeflow Trainer v1): migrate to TrainJob or JobSet |

Reviewers asked why JobSet is Stable while TrainJob is still Alpha; the table was merged as is. The level describes the integration code in Kueue, not the stability of the upstream operator.

## Recent integration changes (v0.21 main)

- **Job**: Workload `AlreadyExists` race is no longer an error ([[integration-batchjob]], pr-18010); `max-exec-time-seconds` is int32-bounded (pr-18218).
- **Pod / groups**: stale single-pod requests for pods that joined a group are dropped (pr-18266); unretriable groups finish `Failed` unless all Pods succeeded, behind `DeclareWorkloadFailureOnUnretriablePodGroups` (pr-18195). See [[integration-plain-pod]].
- **Deployment**: adding `kueue.x-k8s.io/priority-class` to a running Deployment is allowed; removal is still rejected (pr-18287). See [[webhooks]].
- **LeaderWorkerSet**: container/init-container changes allowed when effective requests are unchanged (pr-17903); `groupIdentity: Hash` rejected, gate `LeaderWorkerSetRejectGroupIdentityHash` (pr-18250, pr-18591); `AlreadyExists` on create ignored (pr-18783). See [[integration-leaderworkerset]].
- **StatefulSet**: gate `DisableStatefulSetWorkloadNameFallback` (pr-17937); TAS request refreshed before quota reservation (pr-18868). See [[integration-statefulset]].
- **SparkApplication**: elastic support on main with partial scale-up, sparkConf resolution and executor-Pod based PodsReady ([[integration-spark]]).
- **RayCluster/RayJob/RayService**: elastic + required/preferred topology rejected at creation ([[integration-rayjob]]).
- **AppWrapper**: implicit TAS no longer causes repeated suspension (pr-18600, [[integration-appwrapper]]).
- **Argo**: docs now list which templates create Pods (pr-17910, [[integration-argo-workflow]]).
- **TrainJob**: shared runtime patch helper package (pr-18730, [[integration-trainjob]]).
- **`ValidateRayAndSparkJobUpdates`** is GA; **`AssignQueueLabelsForPods`** is GA in v0.21 (pr-18038, pr-18180).
(source: the PRs cited in each bullet)

## Related pages

- [[kueue-overview]] — the high-level role integrations play.
- [[workload]] — what integrations author.
- [[admission]] — when integrations un-suspend.
- [[webhooks]] — integrations ship their own defaulting and validation webhooks.
- [[job-framework-interface]] — the `GenericJob` contract every integration must implement.
