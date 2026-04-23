# Issue #8065: AccumulatedPastExecutionTimeSeconds keeps being counted even after workload is complete

**Summary**: AccumulatedPastExecutionTimeSeconds keeps being counted even after workload is complete

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8065

**Last updated**: 2025-12-05T19:52:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-12-03T21:43:49Z
- **Updated**: 2025-12-05T19:52:24Z
- **Closed**: 2025-12-05T19:52:24Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

AccumlatedPastExecutionTimeSeconds should not be incremented if the workload is complete.

**What you expected to happen**:

Once the workload transitions to Completed I would expect the seconds to no longer be incremented.

**How to reproduce it (as minimally and precisely as possible)**:

Run a workload and see that the field keeps incrementing
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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T21:45:10Z

I have a dirty branch so it may be a bug I introduced.

But filling it here as its fresh in my head.
