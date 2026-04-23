# Issue #5004: Update Workload priority based on update of the `kueue.x-k8s.io/priority-class` label

**Summary**: Update Workload priority based on update of the `kueue.x-k8s.io/priority-class` label

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5004

**Last updated**: 2025-05-13T08:31:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-04-16T12:09:48Z
- **Updated**: 2025-05-13T08:31:19Z
- **Closed**: 2025-05-13T08:31:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Adjust Workload's priority when the owner (e.g. batch Job) updates `kueue.x-k8s.io/priority-class` label


**Why is this needed**:
Currently we allow users to mutate Workload's priority directly, but ideally we would like to hide Workload's object from the users and allow them to interact only with job objects.

If a user wants to increase priority of a Workload so it's get admitted quicker, they should have ability to change the value of the `kueue.x-k8s.io/priority-class` label in the job object, which then will be taken into account, and reflected in update Workload's `.spec.priority'

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Logic changes
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-16T12:09:55Z

cc @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T14:57:08Z

Isn't `kueue.x-k8s.io/priority-class` label in Job already mutable?

> This label is always mutable because it might be useful for the preemption.

https://github.com/kubernetes-sigs/kueue/tree/main/keps/973-workload-priority#how-to-use-workloadpriorityclass-on-job

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-17T08:15:01Z

> Isn't `kueue.x-k8s.io/priority-class` label in Job already mutable?
> 
> > This label is always mutable because it might be useful for the preemption.
> 
> https://github.com/kubernetes-sigs/kueue/tree/main/keps/973-workload-priority#how-to-use-workloadpriorityclass-on-job

It is, but changes in the label aren't reflected in Workload's `.spec.priority`

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-04-24T10:21:58Z

/assign
