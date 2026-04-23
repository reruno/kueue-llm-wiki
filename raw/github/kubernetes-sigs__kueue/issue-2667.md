# Issue #2667: [Flaky test] The scalability test TestScalability/WorkloadClasses/large  flakes

**Summary**: [Flaky test] The scalability test TestScalability/WorkloadClasses/large  flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2667

**Last updated**: 2024-07-22T15:39:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-22T14:23:04Z
- **Updated**: 2024-07-22T15:39:29Z
- **Closed**: 2024-07-22T15:39:29Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

The TestScalability/WorkloadClasses/large  failed on a non-related branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2659/pull-kueue-test-scheduling-perf-main/1815372699975815168

**What you expected to happen**:

No random failures.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-22T14:23:21Z

/cc @trasc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-22T15:21:28Z

/assign
