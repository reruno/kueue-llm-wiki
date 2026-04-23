# Issue #9434: kueueviz: Add ability to edit workload priority from the dashboard

**Summary**: kueueviz: Add ability to edit workload priority from the dashboard

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9434

**Last updated**: 2026-02-23T18:28:09Z

---

## Metadata

- **State**: open
- **Author**: [@david-gang](https://github.com/david-gang)
- **Created**: 2026-02-23T18:28:09Z
- **Updated**: 2026-02-23T18:28:09Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What would you like to be added**:

The ability to edit workload priority from the kueueviz dashboard.

Kueueviz is currently read-only. Researchers and platform teams working with ML/HPC
workloads often need to reprioritize jobs at runtime — for example, bumping a pending
workload to get it admitted sooner, or lowering the priority of a running workload to
allow preemption by a more urgent job.

The Workload API already supports runtime priority changes, but the behavior differs
across the workload lifecycle, and there are some subtleties I'd like the maintainers'
input on.

### Background: Two lifecycle phases

**Phase 1 — Before admission (pending workloads)**

While a workload is pending (no `QuotaReserved` condition), both fields are mutable:
- `spec.priorityClassRef` — the reference to a PriorityClass or WorkloadPriorityClass
- `spec.priority` — the numeric priority value

Changing either affects the workload's position in the scheduling queue.

**Phase 2 — After admission (admitted/running workloads)**

Once quota is reserved, `spec.priorityClassRef` becomes immutable (enforced by CEL
validation on the CRD). However, `spec.priority` (the numeric value) remains always
mutable. The scheduler reads it live at each cycle, so changes affect preemption
decisions immediately.

### Open question: WorkloadPriorityClass override

The `WorkloadPriorityClassReconciler` watches for changes to `WorkloadPriorityClass`
objects and syncs the class's `.value` into `spec.priority` for all referencing workloads
(see `pkg/controller/core/workloadpriorityclass_controller.go:96-106`).

This means that if a user manually patches `spec.priority` on a workload that references
a `WorkloadPriorityClass`, the controller will eventually overwrite it back to the class's
value on the next reconcile.

This raises some design questions I'd appreciate guidance on:

1. **Should the UI only allow editing `spec.priority` for workloads with no
   `priorityClassRef`?** This is safe since nothing will override the value, but limits
   the feature's usefulness.

2. **Should the UI instead offer a `priorityClassRef` selector (dropdown) for pending
   workloads?** This would let users switch to a higher/lower priority class. It wouldn't
   work for admitted workloads since the ref is immutable after quota reservation.

3. **Should the UI allow editing the `WorkloadPriorityClass` value itself?** This is
   simple but affects *all* workloads using that class, not just one — which may or may
   not be the desired behavior.

4. **Is there a preferred pattern for per-workload priority overrides that coexist with
   a `WorkloadPriorityClass`?** For example, should the reconciler be made aware of
   manual overrides, or is this intentionally not supported?

### Proposed scope (pending feedback)

Regardless of the approach chosen for the above, the implementation would involve:
- A new `PATCH` endpoint in the kueueviz backend (first mutation endpoint)
- An inline-edit UI control on the WorkloadDetail page
- Toast notifications for success/error feedback
- The existing 5-second WebSocket polling handles refreshing the updated value

Happy to contribute the implementation once we align on the right UX.

**Why is this needed**:

- Researchers running ML/HPC workloads need a way to dynamically reprioritize jobs
  without using kubectl
- Priority changes affect both queue ordering (pending) and preemption eligibility
  (admitted), making this a high-impact workflow
- Kueueviz already displays priority info but offers no way to act on it

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

Note: No Kueue CRD changes are needed. "API change" here would only be a new kueueviz
REST endpoint. The design decisions above should be resolved before implementation.
