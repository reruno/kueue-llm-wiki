# Issue #7250: [flaky integration test]  Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Summary**: [flaky integration test]  Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7250

**Last updated**: 2025-10-20T13:16:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T16:55:44Z
- **Updated**: 2025-10-20T13:16:40Z
- **Closed**: 2025-10-20T13:16:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 5

## Description

/kind flake

**What happened**:
failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7211/pull-kueue-test-integration-baseline-main/1977772558216335360
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```

Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit expand_less	13s
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
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:946 @ 10/13/25 16:40:10.961
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T16:58:01Z

/kind flake
cc @mwysokin @pajakd @amy

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T17:03:17Z

It seems just like a potential test flake, because FinishEvictionsOfAnyWorkloadsInCq returns the number of finished workloads, but that number is not awaited to match the expectation in the outside code. So, IIUC it is possible no workloads occasionally have the "Evicted" condition at this point visible from the test code, and so nothing is actually finished.

Maybe we should wrap this line [here](https://github.com/kubernetes-sigs/kueue/blob/af0d80ee04210a537fc25dda7a8e23445dbb2763/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go#L945) as `gomega.Expect(util.FinishEvictionsOfAnyWorkloadsInCq(ctx, k8sClient, cq2)).ToEqual(X)` whatever X should be, that will make the code loop until the expectation on the number of finished workloads is met.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T07:24:04Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-13/1979054011159941120

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-20T07:49:12Z

/assign

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-20T10:38:54Z

I think the above [comment](https://github.com/kubernetes-sigs/kueue/issues/7250#issuecomment-3398333757) has the right solution. Let me elaborate a bit why:

https://github.com/kubernetes-sigs/kueue/blob/ef20e3a7da8b611a58b568283a0377ab9628e8cc/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go#L954-L959

1. Lets say that (for some reason) the first time we try `FinishEvictionsOfAnyWorkloadsInCq` no workload is ready for eviction. 
2. Then this quietly passes and we move to `ExpectAdmittedWorkloadsTotalMetric`. 
3. `ExpectAdmittedWorkloadsTotalMetric` has another `Eventually` inside where we wait for 10s for this metric to become 1, but since we did not evict anything it will remain 0.
4. We wasted 10s waiting for the metric and we never retry `FinishEvictionsOfAnyWorkloadsInCq`

I could not reproduce the error but confirmed in the logs that there is an unfinished preemption blocking the admission of the workload from `cq1`.
