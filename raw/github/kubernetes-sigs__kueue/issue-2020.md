# Issue #2020: [Flaky] Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads

**Summary**: [Flaky] Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2020

**Last updated**: 2024-04-26T10:11:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-19T13:28:05Z
- **Updated**: 2024-04-26T10:11:30Z
- **Closed**: 2024-04-26T10:11:30Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

Flaky integration test `Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads`

```
{Timed out after 5.000s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 5.000s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/preemption_test.go:536 @ 04/18/24 21:15:44.15
}
```

**What you expected to happen**:

Not to flake

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2002/pull-kueue-test-integration-main/1781067120407220224

I think I saw it again in a different PR as well.

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-25T07:28:13Z

/assign
I have a local repro. It seems only a test issue.
