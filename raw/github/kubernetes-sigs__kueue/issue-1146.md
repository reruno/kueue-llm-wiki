# Issue #1146: Preempted RayJob will not resume when resource reclaimed

**Summary**: Preempted RayJob will not resume when resource reclaimed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1146

**Last updated**: 2023-10-09T10:27:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-09-21T17:01:26Z
- **Updated**: 2023-10-09T10:27:57Z
- **Closed**: 2023-10-09T10:27:57Z
- **Labels**: `kind/bug`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I tried with rayJob, but I guess this applies to other jobs as well. Correct me if not.
So when a lower priority rayJob preempted by a higher one and the higher rayJob completed, the lower priority rayjob will not resume.

**What you expected to happen**:

Resume when resource is sufficient.

**How to reproduce it (as minimally and precisely as possible)**:

1. Inside a clusterQueue, configured with `preemption.withinClusterQueue=LowerPriority`
2. submit a low priority rayjob
3. submit a high priority rayjob, since resource is insufficient, the high priority rayjob will preempted the lower one.
4. when the high priority rayjob completed, the lower one will not resume.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-21T17:09:27Z

We saw this exact problem in Jobset, but it turned out that Jobset didn't have permission to update/patch jobs.
Maybe there's a problem in the rayjob implementation of suspend?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-21T17:28:57Z

Or maybe it's a problem in the integration controller, but I don't think this problem is generalized for all jobs

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-09-22T09:05:47Z

It's a bug of rayjob controller, also maybe related to the upstream ray, but let me focus on kueue at first.
/assign
