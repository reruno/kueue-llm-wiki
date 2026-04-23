# Issue #4393: Log the full name of the preemptor workload for debuggability

**Summary**: Log the full name of the preemptor workload for debuggability

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4393

**Last updated**: 2025-02-25T17:00:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-25T12:32:33Z
- **Updated**: 2025-02-25T17:00:32Z
- **Closed**: 2025-02-25T17:00:32Z
- **Labels**: `kind/feature`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 1

## Description

**What would you like to be added**:

Ensure the full workload name is logged for the preemptor workload in this [log line](https://github.com/kubernetes-sigs/kueue/blob/f7437963455e846cc7f681218c9891721f7bf0e8/pkg/scheduler/preemption/preemption.go#L227).

I don't want to update the event message though - we don't want to put the full preemptor workload name into the message as it could leak relevant information across namespaces.

**Why is this needed**:

To improve debuggability.

## Discussion

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-02-25T15:35:48Z

/assign
