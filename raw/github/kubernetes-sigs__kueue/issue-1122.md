# Issue #1122: Flaky: Should update of the pending workloads when a new workload is scheduled

**Summary**: Flaky: Should update of the pending workloads when a new workload is scheduled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1122

**Last updated**: 2023-09-19T16:37:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-09-14T15:54:56Z
- **Updated**: 2023-09-19T16:37:10Z
- **Closed**: 2023-09-19T16:37:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```shell
Core Controllers Suite: [It] ClusterQueue controller when Reconciling clusterQueue pending workload status Should update of the pending workloads when a new workload is scheduled 
{Timed out after 30.000s.
  &v1beta1.ClusterQueuePendingWorkloadsStatus{
  	Head: []v1beta1.ClusterQueuePendingWorkload{
+ 		{Name: "three", Namespace: "core-clusterqueue-thrgz"},
+ 		{Name: "four", Namespace: "core-clusterqueue-thrgz"},
  	},
  	... // 1 ignored field
  }
 failed [FAILED] Timed out after 30.000s.
  &v1beta1.ClusterQueuePendingWorkloadsStatus{
  	Head: []v1beta1.ClusterQueuePendingWorkload{
+ 		{Name: "three", Namespace: "core-clusterqueue-thrgz"},
+ 		{Name: "four", Namespace: "core-clusterqueue-thrgz"},
  	},
  	... // 1 ignored field
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/clusterqueue_controller_test.go:810 @ 09/14/23 05:03:31.307
}
```

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1118/pull-kueue-test-integration-main/1702185468826750976

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-15T10:26:28Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-18T13:13:07Z

This seems to be a legitimate bug, not just a flake test. When the snapshot is updated after the last reconciliation, then the  status of pending workloads remains stale, as there is nothing to trigger an update of the status. I think the fix should be to trigger reconciliation when the snapshot is changed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T06:18:27Z

> This seems to be a legitimate bug, not just a flake test. When the snapshot is updated after the last reconciliation, then the status of pending workloads remains stale, as there is nothing to trigger an update of the status.

@mimowo Thank you for investigating. It makes sense. 
However, why didn't we encounter this bug in the implementation PR? Others (updating workloads, etc...) trigger the reconciliation?

> I think the fix should be to trigger reconciliation when the snapshot is changed.

If we trigger the reconciliation for every snapshot change, it might lose the advantage of updating the snapshot by batch processing every interval, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T08:27:43Z

> However, why didn't we encounter this bug in the implementation PR? Others (updating workloads, etc...) trigger the reconciliation?

The `UpdateIntervalSeconds used in integration tests is only 1s (default is 5s), which makes it likely that the cluster queue reconciliation triggered by changed workloads will happen after the snapshot update. 

To mitigate this I propose to increase the `UpdateIntervalSeconds` to 2s, this way the issue surfaces more often, yet the test isn't much longer.

> If we trigger the reconciliation for every snapshot change, it might lose the advantage of updating the snapshot by batch processing every interval, right?

We need to update trigger reconciliation only on actual snapshot change. Also, I trigger it using `AddAfter`, to batch the reconciliations. This will trigger the reconciliation when the configured is expected to elapse, since the last change `UpdateIntervalSeconds`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T09:45:22Z

> To mitigate this I propose to increase the UpdateIntervalSeconds to 2s, this way the issue surfaces more often, yet the test isn't much longer.

SGTM

> This will trigger the reconciliation when the configured is expected to elapse, since the last change UpdateIntervalSeconds.

However, as we launch the number of snapshotWorkers workers, the suggested idea might increase the number of reconciles by the number of snapshotWorkers.

So, if we adopt the idea, can we trigger the reconciliation only once for all workers?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T10:24:32Z

> However, as we launch the number of snapshotWorkers workers, the suggested idea might increase the number of reconciles by the number of snapshotWorkers.
> So, if we adopt the idea, can we trigger the reconciliation only once for all workers?

Yes. In the worst case scenario, say we have 5 workers, and each cluster queue is changed, the number of extra reconciliations may be + number of workers. However, this is only in the 5s interval. Also, it assumes that all cluster queues change in that period. Also note that, since we use `AddAfter`, the reconciliations in the queue are deduplicated. 

As a side note, I'm wondering if we also should use `AddAfter(cqName, constants.UpdatesBatchPeriod)` for in other places, like here: https://github.com/kubernetes-sigs/kueue/blob/ee5b6ba29a1bbed1574262e362182573c5f6fa5e/pkg/controller/core/clusterqueue_controller.go#L497 or here :https://github.com/kubernetes-sigs/kueue/blob/ee5b6ba29a1bbed1574262e362182573c5f6fa5e/pkg/controller/core/clusterqueue_controller.go#L527 . @tenzen-y @alculquicondor wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T11:13:09Z

> Also note that, since we use AddAfter, the reconciliations in the queue are deduplicated.

Oh, I see. I didn't know that the requests would be deduplicated in the queue. That's great to hear.
Anyway, let me check the PR to fix this bug.


> As a side note, I'm wondering if we also should use AddAfter(cqName, constants.UpdatesBatchPeriod) for in other places, like here:

It sounds good to me. However, I'm not sure why we didn't use `AddAfter` there at the first implementation 🤔 
@alculquicondor Do you remember the reason why we used `Add` instead of `AddAfter`?
