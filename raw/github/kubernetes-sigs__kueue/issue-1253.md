# Issue #1253: A cluster queue may be stuck in "Terminating" if it has Reserving workloads pending on an inactive check.

**Summary**: A cluster queue may be stuck in "Terminating" if it has Reserving workloads pending on an inactive check.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1253

**Last updated**: 2023-10-25T16:51:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-10-25T06:04:17Z
- **Updated**: 2023-10-25T16:51:05Z
- **Closed**: 2023-10-25T16:51:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
A cluster queue may be stuck in "Terminating" if it has Reserving workloads pending on an inactive check.

**What you expected to happen**:
A deleted cluster queue should eventually release its  finalizer and be fully deleted.

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

### Comment by [@trasc](https://github.com/trasc) — 2023-10-25T06:05:38Z

/assign
/cc @alculquicondor 
/cc @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-25T06:15:01Z

Does "inactive" mean that cluserqueue is inactive? or admissioncontroller is inactive?

### Comment by [@trasc](https://github.com/trasc) — 2023-10-25T08:06:56Z

> Does "inactive" mean that cluserqueue is inactive? or admissioncontroller is inactive?

In this context, Admission Check, however , having an inactive Admission Check, makes the queue inactive as well.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-25T08:14:26Z

> > Does "inactive" mean that cluserqueue is inactive? or admissioncontroller is inactive?
> 
> In this context, Admission Check, however , having an inactive Admission Check, makes the queue inactive as well.

I see. Thanks. I think we should include this bug fixed in the next release. Can you open a PR?
The deadline for the next release will be coming up soon. Today or Tomorrow.
