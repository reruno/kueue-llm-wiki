# Issue #9043: MultiKueue v1/Job scale-up sync issue exposed by `MultiKueueBatchJobWithManagedBy` graduation

**Summary**: MultiKueue v1/Job scale-up sync issue exposed by `MultiKueueBatchJobWithManagedBy` graduation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9043

**Last updated**: 2026-02-09T10:59:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-02-06T22:41:03Z
- **Updated**: 2026-02-09T10:59:24Z
- **Closed**: 2026-02-09T10:59:24Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
ElasticJob v1/Job scale-up is broken - scale-up changes in MK job are not propagated to the worker cluster.

An issue in MultiKueue v1/Job synchronization for ElasticJobs was surfaced as part of promoting `features.MultiKueueBatchJobWithManagedBy` to beta in PR #7341.

The underlying behavior existed prior to that change, but the graduation of the feature gate changed execution paths in a way that made the issue observable in integration tests.


**What happened**: 
Remote Job is not scaled up.

**What you expected to happen**:
Remote job is scaled up.

**How to reproduce it (as minimally and precisely as possible)**:
- Create an ElasticJob in MK cluster.
- Scale Job form 1 pod to 2 pods.
- Observe the result in worker cluster.

**Anything else we need to know?**:

**Background**
The original implementation of MultiKueue v1/Job sync with ElasticJobs enabled is not fully compatible with `features.MultiKueueBatchJobWithManagedBy`. When this feature gate is enabled, scale-up updates to ElasticJobs on the manager are not propagated to the corresponding Job on the worker.

Before PR #7341, this behavior was effectively masked. The feature promotion changed admission and suspension semantics, which caused existing tests to exercise the affected path.

**What happened in PR #7341**
As part of the promotion of `features.MultiKueueBatchJobWithManagedBy` to default `true`, the integration test at:

[https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/multikueue/jobs_test.go#L1594](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/multikueue/jobs_test.go#L1594)

started failing. Some of the failures were expected and directly related to the change in feature behavior.

However, another failure, flagged [in this line](https://github.com/kubernetes-sigs/kueue/blob/c203cb5e688cfdd90a81ec660fc26bf170040391/test/integration/multikueue/jobs_test.go#L1788)

was due to a pre-existing issue: scale-up of an ElasticJob on the manager no longer resulted in the worker Job reflecting the updated parallelism.

Instead of fixing the underlying sync behavior, the test was adjusted to assert the observed (but incorrect) behavior:

```go
g.Expect(remoteJob.Spec.Parallelism).To(gomega.BeEquivalentTo(ptr.To(int32(1))))
```

This change made the test pass but unintentionally masked the real issue.

**Impact**

* ElasticJob scale-up requests are not reliably synchronized from manager to worker when `MultiKueueBatchJobWithManagedBy` is enabled.
* The current integration test asserts behavior that is inconsistent with the intended ElasticJob semantics.

**Expected behavior**
When an ElasticJob is scaled on the manager, the corresponding worker Job should reflect the updated `spec.parallelism`, regardless of `MultiKueueBatchJobWithManagedBy`.

**Proposed next steps**

* Fix MultiKueue v1/Job sync logic so ElasticJob scale-up is propagated correctly.
* Restore the integration test assertion to reflect the intended behavior.
* Add coverage to ensure compatibility between ElasticJobs and `MultiKueueBatchJobWithManagedBy` going forward.

**Related PR**

* #7341


**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
