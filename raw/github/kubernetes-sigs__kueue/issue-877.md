# Issue #877: Not allowed create job if integration is disabled

**Summary**: Not allowed create job if integration is disabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/877

**Last updated**: 2023-06-23T16:37:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@stuton](https://github.com/stuton)
- **Created**: 2023-06-19T15:43:35Z
- **Updated**: 2023-06-23T16:37:26Z
- **Closed**: 2023-06-23T16:37:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When we apply any job from an integration (JobSet, MPIJob, etc) with a local queue specified in the metadata.labels section and this integration is disabled in the queue controller configuration, we can see the uncontrolled behavior of creating / deleting jobs.

**What you expected to happen**:
When applying a job with ```kueue.x-k8s.io/queue-name``` label, get an error saying that integration is not enabled

**How to reproduce it (as minimally and precisely as possible)**:

1. Deploy Kueue controller manager with default configuration
2. Deploy Jobset controller manager
3. Create local queue
4. Apply one of JobSet examples with defined ```kueue.x-k8s.io/queue-name``` label

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

### Comment by [@stuton](https://github.com/stuton) — 2023-06-19T15:43:46Z

/assign
