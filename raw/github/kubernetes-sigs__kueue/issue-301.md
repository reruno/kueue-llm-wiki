# Issue #301: Avoid queueing workloads that don't match CQ namespaceSelector

**Summary**: Avoid queueing workloads that don't match CQ namespaceSelector

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/301

**Last updated**: 2022-08-12T18:48:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-07-18T17:32:54Z
- **Updated**: 2022-08-12T18:48:35Z
- **Closed**: 2022-08-12T18:48:35Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Currently all workloads pointing to a CQ are queued irrespective whether or not they match the CQ's namespaceSelector. The selector is checked at scheduling time, which is quite late and causes two issues:
1. wastes scheduling cycles
2. more importantly, in strict fifo, such workloads will block other legitimate workloads from getting scheduled


**What you expected to happen**:

those workloads shouldn't be queued at all, they should stay in an inadmissible list until either CQ selector is changed or their namespace labels are updated to match the CQ.

The workload controller should take care of updating the workload controller with the reason for inadmissibility just like the case where the CQ is not existent.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-09T10:24:59Z

/assign

As part of release 0.2.0

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-09T12:29:58Z

Thanks @kerthcet , I actually have a PR in the works for this. Do you mind taking the last validation bit related to CQ instead?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-09T14:37:20Z

Plz go ahead.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T20:56:01Z

/priority important-soon

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-12T08:53:43Z

/unassign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-12T14:30:36Z

/assign @ahg-g
