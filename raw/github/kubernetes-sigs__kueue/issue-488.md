# Issue #488: Flaky test for WaitForPodsReady if two workloads are considered in the same scheduling cycle

**Summary**: Flaky test for WaitForPodsReady if two workloads are considered in the same scheduling cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/488

**Last updated**: 2022-12-22T16:55:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-21T19:00:20Z
- **Updated**: 2022-12-22T16:55:28Z
- **Closed**: 2022-12-22T16:55:28Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

**What happened**:

/kind flake

Failing test:


```
Scheduler with WaitForPodsReady Suite: [It] SchedulerWithWaitForPodsReady when Scheduling workloads on clusterQueues Should block admission of one new workload if two are considered in the same scheduling cycle
```

**What you expected to happen**:

The test to succeed.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/415/pull-kueue-test-integration-main/1605630317664669696

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T19:00:29Z

/assign @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-21T19:05:27Z

Thanks for creating this! I faced this issue on #415.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-12-22T16:22:17Z

@alculquicondor please review the fix: https://github.com/kubernetes-sigs/kueue/pull/491
