# Issue #9341: Job controller with TAS and ElasticJobsViaWorkloadSlices should scale up an elastic job with TAS unconstrained topology

**Summary**: Job controller with TAS and ElasticJobsViaWorkloadSlices should scale up an elastic job with TAS unconstrained topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9341

**Last updated**: 2026-02-18T23:38:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-18T12:22:00Z
- **Updated**: 2026-02-18T23:38:57Z
- **Closed**: 2026-02-18T23:38:45Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 5

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

Job Controller Suite: [It] Job controller with TAS and ElasticJobsViaWorkloadSlices should scale up an elastic job with TAS unconstrained topology 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9340/pull-kueue-test-integration-baseline-main/2024091523188002816

**Failure message or logs**:
```
{Expected a new workload slice to be created
Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil failed [FAILED] Expected a new workload slice to be created
Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:3687 @ 02/18/26 12:08:54.224
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-18T12:23:00Z

/cc @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-18T23:38:33Z

https://github.com/kubernetes-sigs/kueue/pull/9331 should address this issue as well.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-18T23:38:40Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-18T23:38:45Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9341#issuecomment-3923810232):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-18T23:38:54Z

/assign
