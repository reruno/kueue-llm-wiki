# Issue #973: Workload priority

**Summary**: Workload priority

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/973

**Last updated**: 2023-09-24T02:20:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-11T13:27:21Z
- **Updated**: 2023-09-24T02:20:57Z
- **Closed**: 2023-09-24T02:20:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@Gekko0114](https://github.com/Gekko0114)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A priority that is independent from Pod priority.
The priority value should be part of the Workload spec and be mutable.

The jobs can express the priority via an annotation. A PriorityClass could be used to give pre-determined values.

#884 goes along these lines.

**Why is this needed**:

Tying a Job queueing priority to Pod priority could be problematic as the latter is also tied to Pod preemption.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-14T14:01:34Z

@Gekko0114 do you want to take this?

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-07-14T14:16:53Z

@alculquicondor 
Thank you!
Yes, I want to take this. Should I write KEP first?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-14T14:21:50Z

One important question is whether we need our own PriorityClass object. The KEP could reflect the advantages and disadvantages.
An alternative would be to just reuse the existing k8s PriorityClass, but leave the door open to have our own in the future. We need to explore how to do that.

The easiest starting point would be just to have a numerical value as a job annotation that is reflected as a numerical field in the Workload object.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-07-14T14:34:40Z

Thanks for your explanation!
Based on your comment, I will roughly write KEP.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-17T08:22:09Z

Have we considered adding a job priority to batchv1.Job, it sounds more reasonable. And the job priority could be inherited by the pod. 
> whether we need our own PriorityClass object

Prefer to reuse the PriorityClass, IMHO, we should not invent too many concepts since we're working with the upstream, and I think it's ok to change the priority value inside kueue based on the policies.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-17T12:30:24Z

> I think it's ok to change the priority value inside kueue based on the policies.

I initially thought this could be a good idea. But from my experience, different organizations have wildly different ideas of how priority policies should work.
Once there is a separate field for priority, organizations could write small controllers to change the value.

Another alternative would be to look at existing policies in other systems and see if they make sense for Kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-18T12:29:30Z

+1 on this feature.

Currently, some proposals are submitted for the kueue scheduling order. Once this feature is supported, I think we can simplify those features.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-19T08:35:20Z

Another question about `tying job priority to pod priority` is if we decoupled them, a high-priority job with low-priority pods may never run to completion because it maybe preempted always then make it admitted is somehow meaningless.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-19T14:38:32Z

That is generally true, but less relevant in an environment with autoscaling.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-08-02T14:37:54Z

I think it's better to create a new priority class for `workload` rather than reusing the k8s `priorityClass`. 
If we reuse `priorityClass` for `workload`, we will have to consider all feature extensions of the k8s `priorityClass`. 
The current k8s `priorityClass` has several fields, but some fields are not necessary for `workload`, like `peremptionPolicy`.
https://github.com/kubernetes/kubernetes/blob/99190634ab252604a4496882912ac328542d649d/pkg/apis/scheduling/types.go

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-08-02T15:05:04Z

Once the directions regarding `priorityClass` and `Preemption` are determined, I can write the KEP.

`Tying a Job queueing priority to Pod priority could be problematic as the latter is also tied to Pod preemption.`

I think it's OK using workload priority for Preemption calculations in Kueue. In fact, when calculating preemption in Kueue, it seems we are already using the priority of running workloads.
https://github.com/kubernetes-sigs/kueue/blob/913d53674ec0f535b28e37a3e854b29575eecce0/pkg/scheduler/preemption/preemption.go#L225

Please correct me if I misunderstood

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-03T17:09:59Z

> If we reuse priorityClass for workload, we will have to consider all feature extensions of the k8s priorityClass.

My thinking is that different organisations might want to have different "PriorityClass" CRDs for their own extensions. Then, it might be nice to have a Kueue PriorityClass, but it should be rather simple. The fields should be:

- (initial) priority
- Rereference to another object that could be a CRD defined by an organization.

Regarding the preemption discussion, I think it's ok to have a numeric priority for Kueue that is different from kube-scheduler's priority. We should document the risks of pod preemption to users. We can also point users to create PriorityClasses for their pods that are non-preempting https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#non-preempting-priority-class

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-08-05T06:57:35Z

I see. Thanks for your inputs!
I will write a KEP then.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-08-05T06:57:41Z

/assign
