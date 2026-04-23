# Issue #1490: Flaky multikueue test

**Summary**: Flaky multikueue test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1490

**Last updated**: 2023-12-19T08:55:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-18T19:32:55Z
- **Updated**: 2023-12-19T08:55:55Z
- **Closed**: 2023-12-19T08:55:55Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What happened**:

```
End To End MultiKueue Suite: kindest/node:v1.27.3: [It] MultiKueue when Using multiple clusters Cluster kubeconfig propagation worker1
```

It looks like the workload gets a Admitted=false condition before being checked for equivalency.

**What you expected to happen**:

Probably should skip status field updates altogether?

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1489/pull-kueue-test-e2e-main-1-27/1736828929580208128

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T19:33:02Z

/assign @trasc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T21:13:25Z

/kind flake
