# Issue #9611: [release-0.15] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Summary**: [release-0.15] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9611

**Last updated**: 2026-03-02T22:00:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-03-02T05:38:15Z
- **Updated**: 2026-03-02T22:00:25Z
- **Closed**: 2026-03-02T22:00:24Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

Scheduler Suite: [It] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2027016273371598848

**Failure message or logs**:
```shell
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:901 @ 02/26/26 14:02:14.99
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-02T21:54:21Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-02T22:00:19Z

https://github.com/kubernetes-sigs/kueue/pull/9639 should fixed the issue.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T22:00:25Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9611#issuecomment-3987159230):

>https://github.com/kubernetes-sigs/kueue/pull/9639 should fixed the issue.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
