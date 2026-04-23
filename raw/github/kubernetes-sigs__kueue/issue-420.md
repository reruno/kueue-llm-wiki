# Issue #420: Allow partial admission of jobs

**Summary**: Allow partial admission of jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/420

**Last updated**: 2023-06-07T12:50:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-10-18T20:26:05Z
- **Updated**: 2023-06-07T12:50:16Z
- **Closed**: 2023-06-07T12:50:15Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 19

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A mode of operation that allows partial admission of jobs, for example if parallelism is x and there is only quota available for y < x, then jobs should still be admitted. 

In this mode, the job needs to specify some minimum number of pods that is less than parallelism. To force the job controller to start only what was allowed, we need to reset parallelism to match the partial assignment, we can do that in the same update request that unsuspends the job

**Why is this needed**:

Not all jobs require all-or-nothing.

**Completion requirements**:

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-03T15:33:33Z

I'm interested in tackling this feature.  If there is no object, I will assign it to me and I will attempt a design doc first.  

/assign @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-03T19:03:40Z

> A mode of operation that allows partial admission of jobs, for example if parallelism is x and there is only quota available for y < x, then jobs should still be admitted.

So I am reading this as we probably want some kueue configuration option to allow this globally?


I know that we probably want to implement this without "hard-coding" anything on the Job API as we want Kueue to be a general solution for workloads other than the Job API.  So I am a bit confused on where this item should live?  A user will submit a Job with a CQ annotation so I don't think it should be an API field on the Job API.   

Should a user opt-in into this via a CQ setting?  Or do we want a global setting in the Kueue Configuration that allows this behavior if an admin enables it?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T19:42:04Z

> So I am reading this as we probably want some kueue configuration option to allow this globally?

No, the each workload should dictate whether they can handle lower parallelism.

It probably needs to be an annotation for now.

I think we might be able to justify a field upstream, if we offer some behavior for it. For example, you could have the job controller stop retrying pod creations if it has reached the `minParallelism` and the last pod creation failed because of lack of ResourceQuota. But I'm just thinking out-loud.

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-09T17:56:04Z

I'm afraid I may not have the time to tackle this in the short term.  /unassign @kannon92

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-06T14:56:07Z

MPIJob has a parameter like this, although not properly supported kubeflow/mpi-operator#518

### Comment by [@ahaysx](https://github.com/ahaysx) — 2023-02-17T03:05:45Z

A few questions

1. Should a `min-parallelism` annotation be hooked into the all-or-nothing scheduling feature? For example, if a Kueue has `waitForPodsReady` enabled, should the annotation replace parallelism when determining `PodsReady`? Or are you just asking to consider this annotation when admitting for quota.
2. Do you want this feature to be gated at the Kueue level? Or should the annotation always be respected?
3. By design doc are you looking for a KEP or something more informal.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-17T04:03:51Z

> Should a min-parallelism annotation be hooked into the all-or-nothing scheduling feature? 

I think it's independent of `waitForPodsReady`, currently we only admit the job iff there's enough quota for parallelism or completions pods, with the feature enabled, `min-parallelism` pods is enough. But we may also treat job ready when `min-parallelism` is reached, so we should also change the codes with `waitForPodsReady`.

> Do you want this feature to be gated at the Kueue level? Or should the annotation always be respected?

I think we can have a flag like `waitForPodsReady`.

> By design doc are you looking for a KEP or something more informal.

Yes, see https://github.com/kubernetes-sigs/kueue/tree/main/keps

Some thoughts, I think we should implant the field to Workload maybe inside the PodSet, to make it awared by Kueue, one more thing is should we also record the original parallelism?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-17T13:28:29Z

There are two things at play here:
- How to define and support min-parallelism in an abstract way. This usually implies changes to the Workload API and the admission logic.
- How to apply the selected parallelism to the (custom) job API. In the case of a kubernetes Job, we probably need to update the `parallelism` field itself, before setting `suspend=false`.

> Do you want this feature to be gated at the Kueue level? Or should the annotation always be respected?

Since the annotation is opt-in, I don't see why we need a gate.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T07:22:12Z

Probably, we want to add this feature for the MPIJob with Elastic Training (Elastic Horovod). Also, PytorchJob has Elastic Training mode.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-22T13:52:54Z

This is simpler than elastic. Here we want to start a job with Y pods (where Y>=X), and keep the number at Y during the life of the job.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T15:55:34Z

> This is simpler than elastic. Here we want to start a job with Y pods (where Y>=X), and keep the number at Y during the life of the job.

Ah, I see. Thanks for clarifying.

### Comment by [@trasc](https://github.com/trasc) — 2023-05-10T08:51:27Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-05-10T09:24:10Z

Do we need a KEP for this?

The way I see it: 

After #756 we will have a way of knowing the number of pods for which the admission was done 

https://github.com/epam/kubernetes-kueue/blob/0d840050ad4a09f36b00db2988552955db46898b/apis/kueue/v1beta1/workload_types.go#LL67C1-L84C2

What's still needed:
+ core
  - a way to mark that a podSet accepts partial admission (likely API change)
  - if the case, try the flavor assigment with lower pod count
  - prepare the job for partial execution,  this should be done similary to the way node selectors are handled (likely with restore mechanism)
+ batch/job 
  - a way to mark that a job supports partial admission (likely annotation)
  - implement set/restore parallelism for partial admission
  - change the job vs workload equivalent function to account for partial admission

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-10T10:23:07Z

If we don't need to modify any APIs (adding new APIs), I'm ok with no KEP.
@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-10T12:37:22Z

We need to add new APIs. Otherwise how do users communicate that they are ok with partial admission. And how do we communicate back to the user what was the decision taken?

And the implementation might not be trivial. So a KEP helps put everything in perspective. As the project grows, we might be requiring more KEPs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-10T12:39:10Z

> And the implementation might not be trivial. So a KEP helps put everything in perspective. As the project grows, we might be requiring more KEPs.

That's right.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-25T18:52:15Z

/reopn

#763 was only the high level design

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-26T04:09:11Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-26T04:09:15Z

@kerthcet: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/420#issuecomment-1563784798):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
