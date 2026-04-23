# Issue #6384: ElasticJob scale-down does not trigger re-scheduling of pending inadmissible workloads

**Summary**: ElasticJob scale-down does not trigger re-scheduling of pending inadmissible workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6384

**Last updated**: 2025-08-04T08:37:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-08-03T23:18:31Z
- **Updated**: 2025-08-04T08:37:47Z
- **Closed**: 2025-08-04T08:37:47Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

Currently, scaling down a `batch/v1.Job` with ElasticJob enabled does **not** trigger re-evaluation or re-submission of workloads that are pending due to prior admission failures (e.g., due to insufficient resources).

**What you expected to happen**:

When an ElasticJob scales down and releases resources, this should result in a corresponding update to the reclaimable pod count. In turn, the system should requeue and re-evaluate pending workloads in the same ClusterQueue for admission.

**How to reproduce it (as minimally and precisely as possible)**:

1. Enable the `ElasticJobsViaWorkloadSlices` feature gate.
2. Configure a LocalQueue and ClusterQueue according to Kueue documentation, e.g.:

```yaml
resourceGroups:
- coveredResources: ["cpu", "memory"]
  flavors:
    - name: "default-flavor"
      resources:
        - name: "cpu"
          nominalQuota: 2
        - name: "memory"
          nominalQuota: 36Gi
```

3. Create a `batch/v1.Job` with the following configuration:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: demo-slice
  namespace: demo
  annotations:
    kueue.x-k8s.io/elastic-job: "true"
  labels:
    kueue.x-k8s.io/queue-name: demo
spec:
  parallelism: 3
  completions: 10
  template:
    spec:
      containers:
        - name: dummy-job
          image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
          args: ["600s"]
          resources:
            requests:
              cpu: "500m"
              memory: "100Mi"
      restartPolicy: Never
```

4. Observe CPU flavor utilization in the ClusterQueue and LocalQueue at `1500m`.
5. Submit a second Job with the same configuration.
6. Observe that the second Job remains in the **Pending** state due to insufficient available CPU quota (`500m` available, `1500m` required).
7. Scale down the first Job by patching `parallelism: 1`.
8. Observe that flavor utilization drops to `500m`.
9. However, the second Job remains in **Pending**, even though sufficient capacity is now available to admit it.

**Anything else we need to know?**:

This issue stems from the fact that ElasticJob does not update the `reclaimablePods` during scale-down, preventing the system from recognizing the reclaimed capacity and re-evaluating pending workloads.

**Environment**:

* Kubernetes version (use `kubectl version`):
* Kueue version (use `git describe --tags --dirty --always`):
* Cloud provider or hardware configuration:
* OS (e.g., `cat /etc/os-release`):
* Kernel (e.g., `uname -a`):
* Install tools:
* Others:

/bug

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-03T23:43:53Z

**Root Cause**:

During a scale-down operation, the generic job controller updates only the `Workload` spec to reflect the new pod set counts. However, it does **not** update the `reclaimablePods` field in the corresponding `Workload` status. As a result, the scheduler is unaware that capacity has been released and does **not** requeue pending workloads that could now be admitted.

To address this, we could consider two possible approaches:

---

### **1. Workload-Scope Solution**

* Detect scale-down changes in the workload controller and trigger requeueing of pending workloads in the scheduler.
* This would follow a similar mechanism to the logic already used here:
  [https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload\_controller.go#L756](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L756)

**Pros**:

* Change is isolated to the workload controller.
* No changes required to reclaimablePods routines.
* Preserves the current interpretation of reclaimable pods as representing *completed* pods only.

**Cons**:

* The workload controller would need new logic to detect scale-down events.
* While the controller already handles triggering requeues, detecting scale-down would be a new responsibility.

---

### **2. Reclaimed Pods Update During Scale-Down**

* In addition to updating the workload spec to reflect a lower pod count (as is currently done), also update the workload **status** to include reclaimable pod counts corresponding to the scaled-down pods.

**Pros**:

* No changes needed in the workload controller, since it already monitors updates to the reclaimablePods field and requeues pending workloads accordingly.

**Cons**:

* Broader scope of changes:

  * `workloadslicing` must be extended to patch reclaimable pod status during scale-down.
  * Webhook logic must be updated to support the new validation semantics for reclaimable pods.

**Validation Concern**:

* Today, the webhook validates that reclaimable pod counts do **not** exceed the corresponding values in the workload’s `spec.podSets[].count`. However, in this approach, the spec is itself updated during scale-down, rendering that validation rule ineffective or incorrect.
* This could produce reclaimable values that would currently be rejected (e.g., if the reclaimable count temporarily exceeds the updated spec count).

**Proposed Adjustment**:

* Instead of validating reclaimable pods against the *spec* count, consider validating against the **admitted** count, as recorded in `status.admission.podSetAssignments`.
* This field reflects the original pod set admission and remains unchanged during scale-down.
* Additionally, this approach introduces a useful implicit check: only *admitted* workloads can have reclaimable pods, which aligns with our intended semantics.
