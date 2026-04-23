# Issue #603: Swap Admitted condition value when setting .status.admission

**Summary**: Swap Admitted condition value when setting .status.admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/603

**Last updated**: 2023-04-04T17:05:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-03T17:03:17Z
- **Updated**: 2023-04-04T17:05:44Z
- **Closed**: 2023-04-04T17:05:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 4

## Description

**What would you like to be added**:

Set the Admitted condition value in the same API call that sets `.status.admission`.

Currently the admitted condition is set by the workload controller.

- Admission:
    - https://github.com/kubernetes-sigs/kueue/blob/d5075a345fe0e233c07db4765ea9823c33b4d8e9/pkg/scheduler/scheduler.go#L279
- Eviction:
    - https://github.com/kubernetes-sigs/kueue/blob/d5075a345fe0e233c07db4765ea9823c33b4d8e9/pkg/scheduler/preemption/preemption.go#L131
    - https://github.com/kubernetes-sigs/kueue/blob/d5075a345fe0e233c07db4765ea9823c33b4d8e9/pkg/controller/core/workload_controller.go#L185
- Resetting conditions:
    -  https://github.com/kubernetes-sigs/kueue/blob/d5075a345fe0e233c07db4765ea9823c33b4d8e9/pkg/controller/core/workload_controller.go#L159-L160
    - https://github.com/kubernetes-sigs/kueue/blob/d5075a345fe0e233c07db4765ea9823c33b4d8e9/pkg/controller/core/workload_controller.go#L167

**Why is this needed**:

To reduce complexity in the Workload controller and reduce API usage.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-03T18:07:43Z

Applies to the MPIJob controller as well

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-07T16:29:17Z

/assign @mwielgus

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-03-14T10:19:20Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-14T13:34:43Z

/unassign @mwielgus
