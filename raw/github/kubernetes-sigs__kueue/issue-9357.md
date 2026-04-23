# Issue #9357: [Flaky Performance] TestScalability/WorkloadClasses/small

**Summary**: [Flaky Performance] TestScalability/WorkloadClasses/small

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9357

**Last updated**: 2026-03-02T08:16:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-19T08:42:34Z
- **Updated**: 2026-03-02T08:16:47Z
- **Closed**: 2026-03-02T08:16:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability/WorkloadClasses/small 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9340/pull-kueue-test-scheduling-perf-main/2024397273403756544

**Failure message or logs**:
```
{Failed  === RUN   TestScalability/WorkloadClasses/small
    checker_test.go:112: Average wait for admission 247896ms is more then expected 233000ms
--- FAIL: TestScalability/WorkloadClasses/small (0.00s)
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-19T08:44:40Z

/cc @ASverdlov 

Probably it happens after https://github.com/kubernetes-sigs/kueue/pull/9238.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T08:57:18Z

> Probably it happens after https://github.com/kubernetes-sigs/kueue/pull/9238.

I think this is unlikely, because the failure is for the "baseline" test, whereas the referenced PR only changed TAS configuration.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T08:59:22Z

I would pose question differently - it seems the test was not retried despite the first failure. We should retry the performance test. We already knew in the past that sometimes the tests flake, and thus we introduced the retry mechanism, which doesn't seem to work as expected.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T08:16:41Z

/close
Fixed by https://github.com/kubernetes-sigs/kueue/pull/9581

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T08:16:47Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9357#issuecomment-3982836741):

>/close
>Fixed by https://github.com/kubernetes-sigs/kueue/pull/9581


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
