# Issue #9399: Flaky test  Job with elastic jobs via workload-slices support Should mark old pending workload-slice evicted by scheduler as finished

**Summary**: Flaky test  Job with elastic jobs via workload-slices support Should mark old pending workload-slice evicted by scheduler as finished

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9399

**Last updated**: 2026-02-23T22:05:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-20T15:14:16Z
- **Updated**: 2026-02-23T22:05:41Z
- **Closed**: 2026-02-23T22:05:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description



**Which test is flaking?**:
 Job with elastic jobs via workload-slices support Should mark old pending workload-slice evicted by scheduler as finished 
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2024841752245964800
**Failure message or logs**:
```

Job Controller Suite: [It] Job with elastic jobs via workload-slices support Should mark old pending workload-slice evicted by scheduler as finished expand_less	2s
{Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil failed [FAILED] Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:4150 @ 02/20/26 13:52:29.554
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-20T15:20:44Z

Oh I think this is fixed on the main branch by: https://github.com/kubernetes-sigs/kueue/pull/9331
cc @sohankunkerkar , cherrypicking

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-23T22:05:35Z

https://github.com/kubernetes-sigs/kueue/pull/9400 and https://github.com/kubernetes-sigs/kueue/pull/9401 are merged.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-23T22:05:41Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9399#issuecomment-3947586022):

>https://github.com/kubernetes-sigs/kueue/pull/9400 and https://github.com/kubernetes-sigs/kueue/pull/9401 are merged.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
