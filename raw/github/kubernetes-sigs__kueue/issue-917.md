# Issue #917: The job controller can potentially set `minCount` when  `features.PartialAdmission` is disabled

**Summary**: The job controller can potentially set `minCount` when  `features.PartialAdmission` is disabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/917

**Last updated**: 2023-06-30T13:38:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-06-29T05:21:00Z
- **Updated**: 2023-06-30T13:38:44Z
- **Closed**: 2023-06-30T13:38:44Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If the job controller creates a workload specifying `minCont` for its podSet and `features.PartialAdmission` is not enabled, 
the mutation workload webhook will reset the `minCount` and make the workload `!equivalent` to the job.

**What you expected to happen**:

The job controller should not set the minCount if the featuregate is not enabled.

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

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-06-29T05:21:09Z

/assign
