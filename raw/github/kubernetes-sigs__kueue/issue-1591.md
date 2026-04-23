# Issue #1591: Flaky E2E test termination

**Summary**: Flaky E2E test termination

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1591

**Last updated**: 2024-01-17T18:48:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-16T20:08:12Z
- **Updated**: 2024-01-17T18:48:31Z
- **Closed**: 2024-01-17T18:48:31Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What happened**:

Sometimes, E2E tests fail during cleanup with messages similar to this.

```
Operation cannot be fulfilled on pods "group-1": StorageError: invalid object, Code: 4, Key: /registry/pods/pod-e2e-vh69t/group-1, ResourceVersion: 0, AdditionalErrorMsg: Precondition failed: UID in precondition: 4623b7ec-757d-42cf-a77d-27afc3d885e6, UID in object meta
```

I'm not sure what causes this, and it doesn't seem like an indication of a problem in the test or production code. It is possible that the clean up logic is just racing with some kueue controllers to delete objects.

However, we can probably reduce this flakiness by using better error reporting and introducing retries during clean up.

**What you expected to happen**:

Cleanup to always succeed 

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1589/pull-kueue-test-e2e-main-1-27/1747330683421855744

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-16T20:15:47Z

FYI @roycaihw for ideas, or in case this could still be kubernetes/kubernetes#82130

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-16T21:09:51Z

From https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1592/pull-kueue-test-e2e-main-1-28/1747351345389637632, it looks like it's happening where removing finalizers via Update.
