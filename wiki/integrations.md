# Integrations

**Summary**: An "integration" is a per-job-type controller inside Kueue that observes a particular CRD (batch/v1 Job, JobSet, RayJob, PyTorchJob, etc.), wraps each labeled instance in a [[workload]], and toggles `.spec.suspend` or scheduling gates when Kueue admits the Workload. Each integration handles the quirks of its target API — how many PodSets to emit, how tolerations flow, how status mirrors back — while the core scheduler stays generic.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

## Related pages

- [[kueue-overview]] — the high-level role integrations play.
- [[workload]] — what integrations author.
- [[admission]] — when integrations un-suspend.
- [[webhooks]] — integrations ship their own defaulting and validation webhooks.
- [[job-framework-interface]] — the `GenericJob` contract every integration must implement.
