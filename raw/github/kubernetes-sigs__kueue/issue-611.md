# Issue #611: Resync  the workload resource values upon  LimitRange changes

**Summary**: Resync  the workload resource values upon  LimitRange changes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/611

**Last updated**: 2023-03-23T16:02:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-03-07T07:39:43Z
- **Updated**: 2023-03-23T16:02:34Z
- **Closed**: 2023-03-23T16:02:34Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
This is a  followup of #541 with the purpose of  deciding on a way to recompute the resource values of a workload in case the cluster/namespaces LimitRanges change during the waiting time of a workload.

**Why is this needed**:

Currently I can see three options for this.

1. Keep track of the original poodset values and have the workload controller recompute the resource values when ever the LimitRanges change.
  *  **Pro** Only the workload related component (API + controller) are impacted.
  *  **Pro** The Workload position in the queue is not impacted.
  *  **Con** Requires API changes
  *  **Con** There is a chance that the result of applying the new LimiRanges to the original value to result in a invalid configuration and we need to decide what should happen then. 
2. Monitor the changes of LimitRanges in the workload controller, annotate the workloads that might be impacted by the change and have the job controller recreate the workload.
  *  **Pro** No API change is needed
  *  **Con** The actual impact of the LimitRange chances on the workload cannot be determined at the  workload-controller level and myght result in false positives.
  *  **Con** The queue position of the workload is lost
  *   **Con** Multiple controllers are impacted 
3. Drop the webhook approach and apply the default computation scheme within the scheduling logic.
  *  **Pro** Is clean
  *  **Pro** The scheduling will be done with the most up to date values
  *  **Con** Has a computation  impact on the scheduler performance

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

cc: @alculquicondor , @mwielgus

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-07T14:43:08Z

1. I like the idea of having a permanent record of the initial requests. We can keep the initial requests in the PodTemplate untouched and add a field that summarizes the total requests for all the containers in a PodSet. Then the workload controller can monitor changes in the LimitRanges, while the Job controllers can monitor changes in the PodTemplate with a simple equality check. The summary could also simplify live debugging, instead of SREs having to manually add up all requests to understand what's going on.
2. This is the least desirable idea of the three.
3. It's true that the computations in this case would be more up-to-date. But we need to keep track of the defaults applied at the time of admission, because changes in LimitRanges don't affect running pods. It would be possible to store this information in the Workload status, but we still need the logic that monitors changes in the Job spec to recreate the workload. Maybe not very important in Job, because containers are immutable. 

cc @kerthcet @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2023-03-09T13:41:09Z

I prefer 1. Two thougts:
- IIUC, it will also make the logic around workload - job equivalence simpler, which was a source of existing bugs: https://github.com/kubernetes-sigs/kueue/pull/597. 
- I wouldn't consider the API change an important **Con** since the workload's API is generally a technical detail hidden from users.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-09T15:28:40Z

+1
I wonder if we can store the calculated usage in `.status`. I am not sure if we can mutate the status from a webhook for the spec. If we can't, I don't think it's too bad to store it in the spec.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-10T04:29:37Z

Considering created pods will not be affected with LimitRange, prefer to handle this simply unless we get more feedbacks or requirements:
- when workloads admitted, we'll ignore the update with LimitRange
- when workloads unadmitted, we can modify the object or even recreate, workload will be requeued.

A special case is that when workloads admitted but the job pending to be unsuspended(or pods is waiting to be created), we update the limitRange, then the result might be wrong.  And I didn't buy the idea of designing the API for debugging, but it can be a side benefit.

Treat this as opt-4?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-10T13:40:25Z

Yes, in general we need to ignore changes in LimitRange after the workload is admitted. We might still get cases where the pods don't match the calculated requests, but we can ignore that for now assuming LimitRanges aren't supposed to change often.

> when workloads unadmitted, we can modify the object or even recreate, workload will be requeued.

Yes, that is the point of the proposal. The question is how do we detect the changes without having to look at the original object (Job, MPIJob). If we have to look at the original object, every job-controller implementation has to implement watching LimitRanges. If, instead, we just store the original requests in Workload, we only need to do the checks for LimitRanges in one place: the workload-controller. The rest of the controllers just have to do a simple semantic equality check.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-15T09:44:56Z

> The rest of the controllers just have to do a simple semantic equality check.

Yes, this is what came to my mind first.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T13:39:28Z

awesome, we are all in agreement.

When you have a chance, PTAL at the WIP https://github.com/kubernetes-sigs/kueue/pull/600

### Comment by [@trasc](https://github.com/trasc) — 2023-03-18T06:34:27Z

/asign
