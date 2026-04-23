# Issue #2970: [Flaky scalability test] TestScalability/ClusterQueueClasses

**Summary**: [Flaky scalability test] TestScalability/ClusterQueueClasses

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2970

**Last updated**: 2024-09-11T08:37:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T08:30:46Z
- **Updated**: 2024-09-11T08:37:12Z
- **Closed**: 2024-09-11T08:37:12Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

/kind flake

**What happened**:

The `TestScalability/ClusterQueueClasses` test failed on the main periodic branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-scheduling-perf-main/1830620553732427776

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build on CI.

**Anything else we need to know?**:

```
{Failed  === RUN   TestScalability/ClusterQueueClasses/cq
    checker_test.go:103: Usage 54.71% is less then expected 55.00%
--- FAIL: TestScalability/ClusterQueueClasses/cq (0.00s)
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T08:30:57Z

/assign @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T08:39:04Z

/kind flake

### Comment by [@trasc](https://github.com/trasc) — 2024-09-09T10:42:56Z

There is no systematic performance decrease observed for repeated runs in a more stable test environment.

#3020 adds a retry mechanism that can help in avoiding this kind of false positive failures.
