# Issue #7470: [flaky test] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Summary**: [flaky test] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7470

**Last updated**: 2025-11-12T17:09:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-31T06:48:11Z
- **Updated**: 2025-11-12T17:09:42Z
- **Closed**: 2025-11-12T17:09:42Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

/kind flake

**What happened**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7447/pull-kueue-test-integration-baseline-main/1984049822797139968
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit expand_less	14s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:695 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:695 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:982 @ 10/31/25 00:25:41.377
}
```

## Discussion

### Comment by [@pajakd](https://github.com/pajakd) — 2025-11-03T19:49:15Z

So, https://github.com/kubernetes-sigs/kueue/pull/7325 did not solve the flakiness of this integration test. 

What I see in the logs of the failed run is that more than 2 preemptions "want to happen" because the sticky workload initiates two preemptions before its deleted and then 2 more are needed for the last workload to get in.

But we expect exactly 2 preemptions in the test and we don't complete the other 2 preemptions and that is why the last workload cannot get admitted.

Now I think that the original intention of the code I changed in https://github.com/kubernetes-sigs/kueue/pull/7325 

```
gomega.Eventually(func(g gomega.Gomega) {
	util.FinishEvictionsOfAnyWorkloadsInCq(ctx, k8sClient, cq2)
	util.ExpectAdmittedWorkloadsTotalMetric(cq1, "", 1)
	util.ExpectClusterQueueWeightedShareMetric(cq1, 0)
	util.ExpectClusterQueueWeightedShareMetric(cq2, 0)
}, util.Timeout, util.Interval).Should(gomega.Succeed())
```
was to allow for any number of preemptions  and check the metrics every second. But the ExpectMetric functions have the Eventually block in them which would burn the whole 10 timeout which was the reason of the original flakiness.

To solve this we could for example directly check the metrics in the Eventually block instead of using the ExpectClusterQueueWeightedShareMetric and ExpectAdmittedWorkloadsTotalMetric helper functions.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T07:32:00Z

@pajakd do you want to fix it?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T07:52:10Z

Thank you for the summary @pajakd. It seems to me that the code just didn't wait for the second preemption, and I can see an explanation which is simple to fix. Basically use the set in FinishEvictionOfWorkloadsInCQ for `finished` (FinishEvictionsOfAnyWorkloadsInCq should also return set). Currently we only have a counter, and as a result we may double-count the same workload. We may double-count because the event handler in the test code may not yet get the updated Workload, even though the patch already succeeded.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T09:21:01Z

/assign
Let me try

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T13:22:22Z

/unassign
in case someone wants to pick it up.
I tried this approach: https://github.com/kubernetes-sigs/kueue/pull/7521, but it still flakes. So, while we may merge the improvement to the helper it will not fix the issue

EDIT: oh maybe the issue is that the first of the preempted workloads has time to get re-admitted before the other gets preempted...

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T15:43:28Z

For now I just submit https://github.com/kubernetes-sigs/kueue/pull/7528 which seems reasonable anyway to make sure we are not double-counting.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-10T08:33:15Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-12T07:50:53Z

> EDIT: oh maybe the issue is that the first of the preempted workloads has time to get re-admitted before the other gets preempted...

That’s exactly what happens. The priority of the workloads in `cq2` and the expected workload is the same. We could increase the priority of the expected workload, but I’m not sure that would reflect the correct behavior for this test case.
