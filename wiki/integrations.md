# Integrations

**Summary**: An "integration" is a per-job-type controller inside Kueue that observes a particular CRD (batch/v1 Job, JobSet, RayJob, PyTorchJob, etc.), wraps each labeled instance in a [[workload]], and toggles `.spec.suspend` or scheduling gates when Kueue admits the Workload. Each integration handles the quirks of its target API — how many PodSets to emit, how tolerations flow, how status mirrors back — while the core scheduler stays generic.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16773.md, pr-16779.md, pr-16370.md, pr-13375.md, issue-16517.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-16937.md, pr-17035.md

**Last updated**: 2026-10-21

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
- [[integration-kubeflow]] — PyTorchJob, TFJob, MPIJob, MXJob, PaddleJob, XGBoostJob, JAXJob.
- [[integration-trainjob]] — **[Alpha]** TrainJob (Training Operator v2; successor to the Kubeflow v1 jobs).
- [[integration-rayjob]] — RayJob and RayCluster.
- [[integration-leaderworkerset]] — LeaderWorkerSet (LWS).
- [[integration-appwrapper]] — AppWrapper (Project CodeFlare), used to wrap unsupported types.
- [[integration-argo-workflow]] — Argo Workflows (template-level gating).
- [[integration-plain-pod]] — plain Pods and PodGroups.
- [[integration-statefulset]] — **[Beta]** StatefulSet (uses pod scheduling gates instead of `spec.suspend`).
- [[integration-spark]] — **[Alpha]** SparkApplication (Kubeflow Spark Operator v2).

## `manageJobsWithoutQueueName`

A global config toggle: if true, Kueue manages every job of supported types even without the `queue-name` label, using a default LocalQueue. Historically the interaction of `manageJobsWithoutQueueName` with RayJob left admitted RayJobs in pending state ([[issue-1568]]), so operators should enable this deliberately and test integrations that lag its semantics.

## PodSets per integration

One of the hardest parts of adding an integration is getting PodSet decomposition right:

- **batch/v1 Job** — one PodSet.
- **JobSet** — one PodSet per replicated job × replica. Empty replicated jobs (`replicas: 0`) were a surprising bug ([[issue-2227]]).
- **RayJob** — head + worker groups, plus a "submitter Job Pod" that also counts against quota ([[issue-1434]] — PodSets for RayJobs should account for submitter Job Pod).
- **Kubeflow jobs** — one PodSet per replica type (master, worker, ps, chief, etc.). MPIJob specifically has launcher + workers.
- **LeaderWorkerSet** — leader + worker PodSets per group; TAS-ranked co-scheduling matters ([[issue-4531]]).

## ResourceFlavor label/toleration propagation

Every integration must flow the [[resource-flavor]]'s `nodeLabels` and `tolerations` into the pod template it controls. Bugs here show up as "pods of PyTorchJob don't go to the right node" ([[issue-1407]]) or MPIJob workers having inconsistent selectors vs. workers ([[issue-3400]]).

## MultiKueue compatibility

Not all integrations work with [[multikueue]] out-of-the-box. Each needs a MultiKueue adapter that can mirror the job to a worker cluster and mirror status back. AppWrapper's adapter is tracked under [[issue-3989]]; PodGroup support under [[issue-4719]].

## Recent cross-integration behaviour (v0.20 line)

- Feature gates that shape integration behaviour: `PodIntegrationCountSucceededPodsAsReady` (Beta, on), `DeploymentJobUIDLabel` (Beta, on), `ValidateRayAndSparkJobUpdates` (Beta, on), `FinalizeTerminatingPodGroups` (Alpha, off), `EnforceProvisioningPodTemplateContents` (see [[provisioning-request]]). See [[integration-plain-pod]] (sources: pr-15734.md, pr-15641.md, pr-15628.md, pr-13015.md).
- **Serving integrations (StatefulSet, LeaderWorkerSet, Deployment) share the Pod reconciler.** Webhooks for these three run on update as well as create, which makes them sensitive to defaulting bugs: with `WorkloadPriorityClassDefaulting`, the mutating webhook adds `kueue.x-k8s.io/priority-class: default` on update even for unmanaged objects without a queue-name, and the validating webhook rejects it on Ready objects ("WorkloadPriorityClass cannot be added to a non-suspended workload"); open at writing ([[issue-16333]], source: issue-16333.md). **Correction (2026-10-21)**: this page listed Workload control metadata being inherited from the Job or Pod ([[issue-16322]]) as open. It is fixed: Kueue's internal labels/annotations are never copied (v0.20.1 / v0.19.8), and naming them in `labelKeysToCopy` is logged at startup. See [[job-framework-interface#Internal labels and annotations are never inherited]] (source: pr-16773.md, pr-16779.md).
- **Pod-level `WorkloadAnnotation`** must be set by every integration that creates Pods (StatefulSet, LWS done) so the simulator can map Pods to Workloads (source: pr-15142.md).
- **Quota accounting per integration:** batch Job reclaimable pods ([[integration-batchjob#Reclaimable pods when `parallelism > completions`]]); Spark requests mirror Spark's computation ([[integration-spark]]); PodRequests helper ([[integration-plain-pod#Pod-level requests and quota]]).
- **RBAC:** AppWrapper was the only CRD integration without editor and viewer ClusterRoles; they were added modelled on SparkApplication's, and `rbac.md` now lists what batch-admin and batch-user cover (source: pr-16096.md). JAXJob/TrainJob delete permission: [[integration-trainjob]].
- **Ray:** head-container validation is shared across RayCluster/RayJob/RayService ([[integration-rayjob#Head-container validation]]). An absent worker `replicas` now counts as 0. RayService suspends through the top-level `spec.suspend` (KubeRay ≥ 1.7, gate `KubeRayServiceUsingTopLevelSuspend`) ([[integration-rayjob]]).
- **Child jobs:** with `SkipChildJobSuspension` (Alpha, off) the generic reconciler no longer suspends Kueue-managed child jobs. The parent controller handles that ([[job-framework-interface#Child jobs: `SkipChildJobSuspension`]]).
- **Defaulting:** the default `queue-name` is no longer injected in namespaces excluded by `managedJobsNamespaceSelector` (v0.20.0, [[local-queue-defaulting]]). A changed queue name is validated on update for every integration ([[job-framework-interface#Queue-name format is validated on update]]).
- **Serving rollouts:** StatefulSet/LWS current-revision Pods stay gated until admission, and the legacy finalizer cleanup is removed ([[integration-statefulset]]). An LWS percentage `maxSurge` is honoured ([[integration-leaderworkerset]]).
- **Pod groups:** forged role hashes are caught before ungating, PodSet order comes from shape, and the deletion-deadline activity check is fixed ([[integration-plain-pod]]). Pods owned by a known integration still cannot opt into plain-Pod management ([[issue-16517]], closed without implementation).
- **Spark:** `SUBMISSION_FAILED` no longer finishes the Workload ([[integration-spark]]).

## Graduation levels (docs overview table)

The integrations overview page in the docs now lists each in-tree integration's stability level, with deprecated integrations moved to the end of the table (source: pr-16937.md, pr-17035.md):

| Level | Integrations |
|---|---|
| Stable | AppWrapper, batch/v1 Job, Deployment, JobSet, LeaderWorkerSet, MPIJob, Pod and pod groups, RayCluster, RayJob, RayService, StatefulSet |
| Alpha | SparkApplication, TrainJob (Kubeflow Trainer v2) |
| Deprecated | JAXJob, PaddleJob, PyTorchJob, TFJob, XGBoostJob (Kubeflow Trainer v1): migrate to TrainJob or JobSet |

Reviewers asked why JobSet is Stable while TrainJob is still Alpha; the table was merged as is. The level describes the integration code in Kueue, not the stability of the upstream operator.

## Related pages

- [[kueue-overview]] — the high-level role integrations play.
- [[workload]] — what integrations author.
- [[admission]] — when integrations un-suspend.
- [[webhooks]] — integrations ship their own defaulting and validation webhooks.
- [[job-framework-interface]] — the `GenericJob` contract every integration must implement.
