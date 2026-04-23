# Issue #9281: kubectl always lists an empty cohort for `v1beta2.ClusterQueue`

**Summary**: kubectl always lists an empty cohort for `v1beta2.ClusterQueue`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9281

**Last updated**: 2026-02-23T13:09:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2026-02-16T10:51:55Z
- **Updated**: 2026-02-23T13:09:36Z
- **Closed**: 2026-02-23T13:09:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@kshalot](https://github.com/kshalot), [@polinasand](https://github.com/polinasand)
- **Comments**: 2

## Description

**What happened**:
When you create a `ClusterQueue` belonging to a `Cohort`, the cohort's name is not displayed when running `kubectl get cq`.

**What you expected to happen**:
I'd expect the cohort's name to be displayed.

**How to reproduce it (as minimally and precisely as possible)**:
1. Create a `ClusterQueue` with `.spec.cohortName`.
2. Run `kubectl get cq`.

**Anything else we need to know?**:
The name of `.spec.cohort` was changed to `.spec.cohortName` in `v1beta2`, but `.spec.cohort` is still referenced in `genclient`:
https://github.com/kubernetes-sigs/kueue/blob/a4692d942d656caee4bce019abc563da76ab3bb4/apis/kueue/v1beta2/clusterqueue_types.go#L540

Since `v1beta2` started being used for storage in [`v0.16.0`](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.16.0), it's likely not an issue in versions `<0.16.0`.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): v0.16.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-16T10:52:55Z

/assign

^ I'll assign to myself so nobody picks it up, but this is being worked on by Polina, the new member of the MultiKueue team.

### Comment by [@polinasand](https://github.com/polinasand) — 2026-02-17T15:30:23Z

/assign
