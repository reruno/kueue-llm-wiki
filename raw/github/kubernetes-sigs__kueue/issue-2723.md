# Issue #2723: [scalability]  TestScalability/WorkloadClasses/large fails occasionally

**Summary**: [scalability]  TestScalability/WorkloadClasses/large fails occasionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2723

**Last updated**: 2024-07-30T11:21:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-30T09:44:53Z
- **Updated**: 2024-07-30T11:21:05Z
- **Closed**: 2024-07-30T11:21:03Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

/kind flake

**What happened**:

The scalablity test fails occasionally. Example failed build: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2642/pull-kueue-test-scheduling-perf-main/1816858084459417600

If this is not a systematic regression (it does not seem so), then probably bumping the threshold is ok,

**What you expected to happen**:

No random failures.

**How to reproduce it (as minimally and precisely as possible)**:

Probably run a branch build on CI.

**Anything else we need to know?**:

failure message:
```
{Failed  === RUN   TestScalability/WorkloadClasses/large
    checker_test.go:117: Average wait for admission 11213ms is more then expected 11000ms
--- FAIL: TestScalability/WorkloadClasses/large (0.00s)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T09:45:33Z

/cc @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-07-30T11:15:28Z

This is a duplicate of #2708

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T11:21:00Z

Ah, I missed it, thanks
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-30T11:21:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2723#issuecomment-2258113223):

>Ah, I missed it, thanks
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
