# Issue #6324: [Flaky] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Summary**: [Flaky] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6324

**Last updated**: 2025-08-12T13:41:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2025-07-31T11:49:36Z
- **Updated**: 2025-08-12T13:41:16Z
- **Closed**: 2025-08-12T13:41:16Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:355 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:355 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:575 @ 07/31/25 10:47:58.158
}
```

**What you expected to happen**:
No failures

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6297/pull-kueue-test-integration-baseline-main/1950867693955452928

**Anything else we need to know?**:

/kind flake

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T14:39:59Z

We observed this again 
- https://github.com/kubernetes-sigs/kueue/pull/6536
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6536/pull-kueue-test-integration-baseline-main/1954911786192867328
