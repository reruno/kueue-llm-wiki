# Issue #5528: Add Initial implementation of KEP-77: Elastic Jobs via WorkloadSlices

**Summary**: Add Initial implementation of KEP-77: Elastic Jobs via WorkloadSlices

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5528

**Last updated**: 2025-07-23T07:16:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-06-05T23:01:43Z
- **Updated**: 2025-07-23T07:16:30Z
- **Closed**: 2025-07-23T07:16:30Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Initial implementation of KEP-77: Dynamically Sized Jobs via WorkloadSlices

**Why is this needed**:

This issue tracks the initial implementation of [KEP-77](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs), which introduces support for dynamically resizing jobs in Kueue through the concept of WorkloadSlices.

**Completion requirements**:

- [ ] Implement creation of WorkloadSlice objects upon scaling events (e.g., parallelism change for batchv1/Job).
- [ ] Add pod scheduling gates to defer scheduling until slice admission.
- [ ] Implement admission logic for WorkloadSlices.
- [ ] Support deactivation and garbage collection of preempted slices.
- [ ] Update quota and PodSetAssignments to reflect slice scaling.
- [ ] Annotate relationships between new slices and the slices they preempt.
- [ ] Add feature gate (WorkloadSlices) and opt-in annotation mechanism.
- [ ] Ensure compatibility with existing batch/v1.Job semantics.
- [ ] Unit and integration test coverage for scale-up and scale-down flows.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T16:57:51Z

/retitle Add Initial implementation of KEP-77: Elastic Jobs via WorkloadSlices
