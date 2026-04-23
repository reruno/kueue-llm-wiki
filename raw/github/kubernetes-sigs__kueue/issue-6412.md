# Issue #6412: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Summary**: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6412

**Last updated**: 2025-08-04T10:31:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-08-04T09:12:17Z
- **Updated**: 2025-08-04T10:31:41Z
- **Closed**: 2025-08-04T10:31:41Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
AFS integration test flaked

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6400/pull-kueue-test-integration-baseline-main/1952288809257275392

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T09:15:37Z

cc @mimowo @IrvingMg

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T09:31:53Z

Appeared again at: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6406/pull-kueue-test-integration-baseline-main/1952295248356970496

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T09:36:21Z

Analyzed the logs and I have a hypothesis behind the root cause of the flake. This is because of a race condition between scheduler and lq's controller, where scheduler has a stale snapshot when deciding on which workload to preempt:

The flow is as following:

1. A workload from `lq-a` is admitted.
2. The test proceeds, expecting the fair sharing usage of the `lq-a` LocalQueue to be updated.
3. A new scheduling cycle begins in the scheduler.
4. The scheduler calls `s.cache.Snapshot()`
5. The race: This snapshot is created before the localqueue-reconciler's update has fully propagated back to the scheduler's cache.
6. LQ's controller updates `lq-a`'s status with usage `>12` and releases a new workload submitted to `cq2`
7. The scheduler then makes a preemption decision based on the (now stale) usage data in its snapshot

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T09:39:05Z

This is similar to what happened before in a sense that a new workload is submitted in a moment where `lq-a`'s usage is less than `lq-b`'s usage which doesnt capture the intention of the test

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T09:54:44Z

Actually, this flake might be caused because in [tests](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go#L758) we compare `milliValue` with 12 instead of 12_000.

I'll fix that and rerun a few hundreads of time to see if this is the reason indeed

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-04T10:02:01Z

Run it 100+ times already and no flakes so far. I'm creating a PR with the fix
