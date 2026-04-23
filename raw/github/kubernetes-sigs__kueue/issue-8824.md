# Issue #8824: [flaky test] Pod controller interacting with scheduler Should schedule pod groups as they fit in their ClusterQueue

**Summary**: [flaky test] Pod controller interacting with scheduler Should schedule pod groups as they fit in their ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8824

**Last updated**: 2026-04-17T16:35:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T15:01:41Z
- **Updated**: 2026-04-17T16:35:48Z
- **Closed**: 2026-04-17T16:35:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 8

## Description


**Which test is flaking?**:
Pod controller interacting with scheduler Should schedule pod groups as they fit in their ClusterQueue

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8818/pull-kueue-test-integration-baseline-main/2016160074942124032

**Failure message or logs**:
```
Pod Controller Suite: [It] Pod controller interacting with scheduler Should schedule pod groups as they fit in their ClusterQueue [job:pod, area:jobs] expand_less	11s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/pod/pod_controller_test.go:1866 with:
Expected
    <[]v1.PodSchedulingGate | len:2, cap:2>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
        {
            Name: "kueue.x-k8s.io/topology",
        },
    ]
to be empty failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/pod/pod_controller_test.go:1866 with:
Expected
    <[]v1.PodSchedulingGate | len:2, cap:2>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
        {
            Name: "kueue.x-k8s.io/topology",
        },
    ]
to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/pod/pod_controller_test.go:1867 @ 01/27/26 14:52:58.581
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:02:14Z

cc @sohankunkerkar @mbobrovskyi let me know if you have some ideas

### Comment by [@Piyushkhobragade](https://github.com/Piyushkhobragade) — 2026-01-30T05:52:25Z

Opened a PR that fixes the flake by making topology gate removal deterministic.
The pod controller was relying on PodSetInfo history, which can be stale under
certain reconciliation orders and leave pods gated indefinitely.

Fixes #8824

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-04-09T05:31:52Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/10322/pull-kueue-test-integration-extended-main/2041798840230612992.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-15T09:29:02Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/10458/pull-kueue-test-integration-baseline-release-0-17/2044036726346747904

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T16:29:05Z

Ohhhh, I have analyzed the logs here based on https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/10458/pull-kueue-test-integration-baseline-release-0-17/2044036726346747904 and clearly the issue is with test isolation. 

The leakage is between the two consecutive tests which both use the same ClusterQueue: dev-clusterqueue:
- Should schedule pods as they fit in their ClusterQueue, namespace "pod-sched-namespace-2td5w"
- Should schedule pod groups as they fit in their ClusterQueue, namespace "pod-sched-namespace-sn8gs"

Now, we can see the Workload "dev-pods"  in the second test fails to schedule saying "2 more needed". Note that the workload requires 5 CPU, and the CQ also has 5 CPU capacity. It turns out the 2 CPUs are still eaten by the workload from the previous test, called "pod-dev-pod-cadd1" which was using 2 CPU, up until it released it at `2026-04-14T13:07:15.777389323Z` saying "Workload deleted; removing from cache". 

**Now, this is because freeing the cache would happen in Reconcile, asynchronously.**

However, this test was running the commit 6b639b71339478add6a7500606513ca1dda13e9b, which was before our recent fix 1212e99acfa0d55e69719b5b7df2883b5eadd10a on the 0.17 branch, coming from the PR https://github.com/kubernetes-sigs/kueue/pull/10518 which returned to the synchronous cleanup of the cache: https://github.com/kubernetes-sigs/kueue/pull/10518/changes#diff-60dd240c20adbd6a189d018d1c216c2d296730f446c341d8bf449fa6657964ffR1066-R1070

So, I think this interaction between tests is not fixed with the revert. Uff.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T16:33:30Z

Following up, because the test is using BestEffortFIFO, and the first scheduling attempt failed, due to the leaked workload usage, then there was no event that would trigger re-scheduling of the new workload.

One could say this is of low priority because on a production system the inflow of new workload would trigger re-scheduling loops, but this demonstrates how non-trivial it makes debugging when we cleanup cache in Reconcile asynchronously rather than in Delete.

cc @kshalot @Singularity23x0 @gabesaba @tenzen-y @PBundyra @Ladicle

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T16:35:42Z

Finally, notably the test only was reported as flaky in 0.17 and main branches, never in 0.16 which also increases the confidence that it started with https://github.com/kubernetes-sigs/kueue/pull/8655. 

Let me close as I believe now the issue is fixed. We can re-open or create another one if I missed something and I'm wrong.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-17T16:35:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8824#issuecomment-4269714322):

>Finally, notably the test only was reported as flaky in 0.17 and main branches, never in 0.16 which also increases the confidence that it started with https://github.com/kubernetes-sigs/kueue/pull/8655. 
>
>Let me close as I believe now the issue is fixed. We can re-open or create another one if I missed something and I'm wrong.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
