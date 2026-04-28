# Integration: SparkApplication

**Summary**: Kueue integrates with the Kubeflow Spark Operator v2 to gate SparkApplication jobs through queue-based admission, managing driver and executor pods as separate PodSets.

**Sources**: `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_controller.go`, `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_podset.go`, `raw/kueue/pkg/controller/jobs/sparkapplication/sparkapplication_webhook.go`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gate `SparkApplicationIntegration`, disabled by default.

## What is SparkApplication?

`SparkApplication` is a CRD from the [Kubeflow Spark Operator v2](https://github.com/kubeflow/spark-operator), API group `sparkoperator.k8s.io/v1beta2`. It describes an Apache Spark job with a separate driver pod and one or more executor pods. (source: pkg/controller/jobs/sparkapplication/sparkapplication_controller.go)

## PodSets

| PodSet name | Count | Description |
|---|---|---|
| `driver` | 1 | The Spark driver pod |
| `executor` | `spec.executor.instances` | Executor pods |

Kueue reads resource requests (CPU, memory, GPU, etc.) from `spec.driver` and `spec.executor` fields, mapping them into the `kueue.PodSet` format. (source: pkg/controller/jobs/sparkapplication/sparkapplication_podset.go)

## Suspend / resume

Kueue suspends a SparkApplication by setting `spec.suspend = true`. Dynamic allocation is explicitly rejected by the webhook — SparkApplications with dynamic allocation enabled cannot be managed by Kueue because the executor count would be unpredictable. (source: pkg/controller/jobs/sparkapplication/sparkapplication_webhook.go)

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

## Related pages

- [[integrations]]
- [[job-framework-interface]]
- [[workload]]
- [[admission]]
- [[local-queue]]
- [[feature-gates]]
