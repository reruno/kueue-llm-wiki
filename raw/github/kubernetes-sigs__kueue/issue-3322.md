# Issue #3322: Workload is stuck after one of the AdmissionCheck is in `Retry` state

**Summary**: Workload is stuck after one of the AdmissionCheck is in `Retry` state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3322

**Last updated**: 2024-10-28T14:32:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-10-25T16:51:03Z
- **Updated**: 2024-10-28T14:32:56Z
- **Closed**: 2024-10-28T14:32:56Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
After one of the AdmissionCheck was set to `Retry` state, Workload get evicted and never requeued again.

**What you expected to happen**:
Requeue immediately or after some backoff time - depending on the `.status.requeueState.requeuAt`.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
