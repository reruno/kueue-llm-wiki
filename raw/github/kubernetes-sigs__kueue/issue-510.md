# Issue #510: Account for terminating pods when doing preemption

**Summary**: Account for terminating pods when doing preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/510

**Last updated**: 2023-05-04T18:52:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-01-11T14:41:04Z
- **Updated**: 2023-05-04T18:52:36Z
- **Closed**: 2023-05-04T18:52:36Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Account for the quota in use by pods that are still terminating when doing preemptions.

**Why is this needed**:

We issue preemptions by setting `Workload.spec.admission=nil` and immediately consider these resources freed. But in reality, pods take time to terminate.

We will need to keep the old admission somewhere for the calculations, and bubble up information about running pods from the Job. Maybe this will require improvements to the job controller.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-04-06T06:35:15Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2023-04-06T11:48:02Z

Hey @trasc,

@alculquicondor suggested I look into this issue as part of https://github.com/kubernetes/enhancements/pull/3940.

I think it’s good that you are looking into it because I’m a little confused on what Kueue would want for accounting for terminating pods.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T12:44:40Z

There are 2 parts to this problem:
1. In Kueue, we need to preserve the information about how the job was admitted (in which queue and using which flavors).
2. In Job status, we need the information about how many pods are still terminating.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-06T13:16:12Z

As I see this:


> 1. In Kueue, we need to preserve the information about how the job was admitted (in which queue and using which flavors).

#599 will add a new condition "Evicted" set upon preemption, an we can have this set without clearing up the  admission (both the condition and the struct) and only reset the admission when `job.IsActive()`  starts returning false, so the workload is considered "active" until we are "sure" that no resources are blocked by it. This should help to avoid over-provisioning.


> 2\. In Job status, we need the information about how many pods are still terminating.

In my opinion this is the job of  `job.IsActive()` and we can think of ways of making the implementation of it more accurate (maybe walk some kind of object ownership tree).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T13:33:33Z

> In my opinion this is the job of `job.IsActive()` and we can think of ways of making the implementation of it more accurate (maybe walk some kind of object ownership tree).

Right, we can always implement the logic in Kueue by watching pods. But ideally Kueue doesn't need to know about pods, for separation of concerns.

For the purpose of making progress, we can start with 1. and we can wait to see if we can leverage https://github.com/kubernetes/enhancements/pull/3940

### Comment by [@trasc](https://github.com/trasc) — 2023-04-06T13:34:45Z

@kannon92 in the implementation of `IsActive()` for  `batch/job`  https://github.com/kubernetes-sigs/kueue/blob/3113e4b26198d4ec8c85598c53983e42aa443677/pkg/controller/jobs/job/job_controller.go#L125-L127

we are relying on `j.Status.Active`  to determine  if a job is blocking any resources.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-04-06T13:42:14Z

Yea so the issue is that `Active` doesn't include terminating pods.  That KEP is about including terminating pods in active but I realize that there were some design decisions around termating pods being considered failed.

If PodFailurePolicy is on, then job will mark a terminating pod as failed once it is fully terminated.  If PodFailurePolicy is off, then a job immediately transitions to failed but the pod still has resources.  

I think that we will go with what @alculquicondor has suggested and probably have a status field for terminating so we can catch this intermittent state without changing the behavior.

https://github.com/kubernetes/enhancements/blob/1a9513382b0338026a2524baa4159951f66924b0/keps/sig-apps/3939-include-terminating-pods-as-active/README.md#open-questions-on-job-controller

Does this mean that if you want this feature for other workloads (MPI, etc) then they should include terminating pods in their status?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T13:50:50Z

Let's leave job conversations to k/k :)

@trasc, let start by keeping the `.status.admission` field when evicting/preempting and just updating the `Admitted` condition.
We can add the `Evicted` condition in a follow up.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T13:59:10Z

Synced with @trasc offline to understand his suggestion better.

So the idea is to add the `Evicted` condition without changing the `Admitted` condition or clearing the `.status.admission` field. Once we are "certain" that the job doesn't have running pods, we actually clear `.status.admission` and update the `Admitted` condition.

This works better and is backwards-compatible.
