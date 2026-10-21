# Integration: SparkApplication

**Summary**: Kueue integrates with the Kubeflow Spark Operator v2 to gate SparkApplication jobs through queue-based admission, managing driver and executor pods as separate PodSets.

**Sources**: `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_controller.go`, `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_podset.go`, `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_webhook.go`, pr-16364.md, issue-16363.md, pr-16976.md, pr-16967.md, pr-16968.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md

**Last updated**: 2026-10-21

---

> **Stage: Alpha** — Feature gate `SparkApplicationIntegration`, disabled by default.

## What is SparkApplication?

`SparkApplication` is a CRD from the [Kubeflow Spark Operator v2](https://github.com/kubeflow/spark-operator), API group `sparkoperator.k8s.io/v1beta2`. It describes an Apache Spark job with a separate driver pod and one or more executor pods. (source: pkg/controller/jobs/sparkapplication/sparkapplication_controller.go)

## PodSets

| PodSet name | Count | Description |
|---|---|---|
| `driver` | 1 | The Spark driver pod |
| `executor` | `spec.executor.instances` (unset counts as 0) | Executor pods |

Kueue reads resource requests (CPU, memory, GPU, etc.) from `spec.driver` and `spec.executor` fields, mapping them into the `kueue.PodSet` format. (source: pkg/controller/jobs/sparkapplication/sparkapplication_podset.go)

## Suspend / resume

Kueue suspends a SparkApplication by setting `spec.suspend = true`. Dynamic allocation is rejected by the webhook **unless the job is an elastic job**: "a kueue managed job can use dynamicAllocation only when the ElasticJobsViaWorkloadSlices feature gate is on and the job is an elastic job". With dynamic allocation enabled, `PodsReady` expects `dynamicAllocation.minExecutors` running executors instead of `instances`; this is the v0.20.0 fix #14505 (source: raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_webhook.go, raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). **Correction (2026-10-21)**: this page said dynamic allocation is always rejected. Elastic SparkApplication support beyond this is still open (issue-16806, issue-12944).

## MultiKueue support

**Not supported** — no `multiKueueAdapter` exists for SparkApplication. (source: pkg/controller/jobs/sparkapplication/)

## Required labels

```yaml
metadata:
  labels:
    kueue.x-k8s.io/queue-name: my-local-queue
```

## Node affinity injection

On admission, Kueue injects the ResourceFlavor's node selector and tolerations into both the driver and executor pod specs via `RunWithPodSetsInfo`. (source: pkg/controller/jobs/sparkapplication/sparkapplication_controller.go)

## Removing the `queue-name` label is rejected

`SparkApplication` shares the Ray webhook validation: removing `kueue.x-k8s.io/queue-name` from an unsuspended SparkApplication — or from a suspended one in a namespace with a default LocalQueue — is rejected, behind the Beta, default-on `ValidateRayAndSparkJobUpdates` gate. Before the fix the job kept running with its Pods uncounted against quota. See [[integration-rayjob#Removing the `queue-name` label is rejected]] ([[pr-13293]], [[pr-14666]], [[pr-14676]]).

## Node selector and resource accounting fixes

- **Application-level `spec.nodeSelector`.** `buildDriverPodTemplateSpec` / `buildExecutorPodTemplateSpec` copied only `spec.driver.nodeSelector` and `spec.executor.nodeSelector`. The application-level and per-role selectors are mutually exclusive, so `RunWithPodSetsInfo` flattens `spec.nodeSelector` into the per-role selectors and clears it; the Workload is the only place `RestorePodSetsInfo` can read it back from, so after the first eviction the selector was permanently lost and pods could land on any node. The application-level selector is now recorded in the PodSet templates (per-role selector wins on conflict), and therefore also takes part in ResourceFlavor matching (source: pr-15649.md; backports pr-15797.md, pr-15813.md).
- **Requests mirror Spark's own computation.** Only `coreRequest` and `memory` were read, so `cores` and `memoryOverhead` were ignored. The PodSet templates now reproduce Spark (`BasicDriverFeatureStep`, `BasicExecutorFeatureStep`, `ResourceProfile.getResourcesForClusterManager`): CPU = `request.cores`, falling back to `cores` (default 1); memory = `memory + memoryOverhead`, with the overhead defaulting per Spark (at least 384Mi); PySpark and off-heap memory are included; typed spec fields, `spec.memoryOverheadFactor` and the matching `spec.sparkConf` properties are honoured with `spark-submit` precedence. Memory strings must use the Java format Spark accepts (`512m`, `2g`). **Action required:** ClusterQueue quotas may need to rise, since each Pod now reserves its `cores` as CPU and at least 384Mi extra memory (source: pr-15833.md; backports pr-15923.md, pr-15924.md).
- Open: Spark-aware partial preemption ([[issue-16233]]).

## `SUBMISSION_FAILED` is not a finished state

`Finished()` used to treat `SUBMISSION_FAILED` as terminal. Kueue therefore marked the Workload Finished and released its quota. The Spark operator does **not** treat that state as terminal: with `restartPolicy.type: Always`, or `OnFailure` with `onSubmissionFailureRetries` left, it resubmits the application after the retry interval. The resubmitted driver and executors then ran outside quota, preemption and `waitForPodsReady`. Repro: point `spec.driver.serviceAccount` at a ServiceAccount that does not exist, wait for `SUBMISSION_FAILED`, then create the ServiceAccount (source: issue-16363.md).

[[pr-16364]] (fixes [[issue-16363]]): the Workload finishes only on `COMPLETED` (success) or `FAILED`. The operator moves the application to `FAILED` itself once it stops retrying. Shipped in **v0.20.0**. The release-0.19 backport [[pr-16976]] shipped in **v0.19.9** (source: pr-16364.md, raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

## Unset `executor.instances` stays unset when stopping

With `spec.executor.instances` unset, the executor PodSet count is 0. On stop, `RestorePodSetsInfo` wrote `instances: 0` back together with `suspend: true`. The SparkApplication CRD requires `instances >= 1`, so the API server rejected the **whole** patch. The job could not be suspended after eviction or deactivation, and the reconciler retried forever. A restored count of 0 is now written as an unset field (#15610; shipped in **v0.20.2** via [[pr-16968]] and **v0.19.9** via [[pr-16967]], per raw/kueue/CHANGELOG/CHANGELOG-0.20.md and CHANGELOG-0.19.md) (source: pr-16967.md, raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_controller.go).

## Related pages

- [[integrations]]
- [[job-framework-interface]]
- [[workload]]
- [[admission]]
- [[local-queue]]
- [[feature-gates]]
