# Issue #804: Concurrent preemption within cohort can lead to over-admission.

**Summary**: Concurrent preemption within cohort can lead to over-admission.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/804

**Last updated**: 2023-05-30T19:05:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-05-24T09:42:02Z
- **Updated**: 2023-05-30T19:05:49Z
- **Closed**: 2023-05-30T19:05:49Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In a scenario in which we have three cluster  queues `cqA`, `cqB` and `cqC` with the same quotas, within the same cohort, and having two workloads admitted in `cqA`  which evenly us the entire cohort resources.

Creating two workloads in `cqB` and `cqC` using the full nominal quotas, will only preempt one workload in `cqA` and admit both.
 
**What you expected to happen**:

Both workload in `cqA` should be preempted.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): v0.4.0-devel-130-g9d3ecbc

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-05-24T09:42:23Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-24T18:11:55Z

Can you summarize what were the steps that lead to the over-admission?
