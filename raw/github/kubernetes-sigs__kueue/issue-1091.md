# Issue #1091: A mechanism to suspend a running Job without requeueing

**Summary**: A mechanism to suspend a running Job without requeueing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1091

**Last updated**: 2023-12-18T19:34:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-31T16:30:56Z
- **Updated**: 2023-12-18T19:34:11Z
- **Closed**: 2023-12-18T19:34:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@andrewsykim](https://github.com/andrewsykim)
- **Comments**: 43

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A field in the Workload API that would allow an administrator to permanently suspend a running job (no requeueing). The operation can be reversed by the administrator.

**Why is this needed**:

Some systems need the ability to "terminate" arbitrary jobs (because it's running for too long or other policies) without deleting the Job object, so it can be debugged.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-08-31T16:34:42Z

I think we can keep it generic, suspend/unsuspend workload. This is more useful that permanently suspend the job and terminating it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-31T16:35:18Z

updated the comment.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-09-07T11:35:03Z

**Automatically**(judged by running time etc.) or **Manually**, what do you expect here?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-07T16:24:47Z

Manually, by an administrator (or another controller)

### Comment by [@asm582](https://github.com/asm582) — 2023-09-14T00:00:52Z

I am curious about the load on the API server then job logs get very large, do we know any performance implications and if the job logs get rolled over after a certain size?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-18T14:30:12Z

IIUC, log rotation is independent of the existence of the job object.

Note that this feature would be opt-in. Administrators should use it at their own risk, probably having some form of garbage collection in place.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-09-18T14:52:49Z

/assign

I'd like to work on this :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-29T17:57:05Z

There is a open question about permissions:
Should the job owner have the ability to suspend a job, or just the administrator?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-12T01:33:33Z

One approach I've been thinking about is to add a `requeuePolicy` field to wworkload spec, with initial values of `Always` (default) or `Never`. This seems slightly cleaner than a field to directly suspend the job since we're not introducing new mechanisms to suspend workloads. Thoughts?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-12T02:30:45Z

This reminds me when designing the `Suspend`, maybe it should be string rather than boolean for expandability, then we can support like `pause` or something like that.

> Should the job owner have the ability to suspend a job, or just the administrator?

If we focus on the job itself, like debugging, I doubt that the administrator will dig oneself.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-12T03:13:12Z

> One approach I've been thinking about is to add a `requeuePolicy` field to wworkload spec, with initial values of `Always` (default) or `Never`. This seems slightly cleaner than a field to directly suspend the job since we're not introducing new mechanisms to suspend workloads. Thoughts?

Make sense to me, somehow likes the restartPolicy. But how to populate the field `Never` to workload, it's spawned, another annotation?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-12T03:55:06Z

> But how to populate the field Never to workload, it's spawned, another annotation?

I might be misunderstanding your question. I was thinking with a new field `workload.spec.requeuePolicy`, you can set the value to `Never` even while the workload is running. It wouldn't suspend the workload itself, but next time you suspend the workload it will ensure it won't be requeued. So taking Job API as an example, it would take 2 steps to suspend a running Job:
1. Set workload.spec.requeuePolicy = true
2. Set job.spec.suspend = true

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-16T15:03:39Z

I'm not sure this API is unambiguous.

Imagine that it is possible to create a Workload with requeuePolicy=Never. What does that mean? Should the Workload not be queued and admitted in this case?

Another sceneario: the workload just got admitted, and an administrator manages to set requeuePolicy=Never right before the controller sets suspend=false. What should happen to the job?

Maybe this can be fixed by changing the steps to suspend a running job:
- set the requeuePolicy in Workload to Never
- set the evicted condition in the Workload status

maybe requeuePolicy is not the best name, as it doesn't explain what happens when the Workload was never admitted. Maybe just `queueing: Enabled|Disabled`?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-16T19:11:25Z

> Imagine that it is possible to create a Workload with requeuePolicy=Never. What does that mean? Should the Workload not be queued and admitted in this case?

> Another sceneario: the workload just got admitted, and an administrator manages to set requeuePolicy=Never right before the controller sets suspend=false. What should happen to the job?

We could fix this with a 3rd policy, `AdmitOnce` or similar. But I don't have enough experience here to say this is a valid use-case.

> maybe requeuePolicy is not the best name, as it doesn't explain what happens when the Workload was never admitted. Maybe just queueing: Enabled|Disabled?

This seems fine to me, but we can probably just make it a bool instead then? Agree the corner cases around requeuePolicy can be misleading with jobs that were never previously admitted. Will start with `queueing` (or similar) and iterate from there.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-16T20:49:54Z

a boolean should be fine. I think it's clear that this will always be only 2 modes.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-17T02:35:02Z

> I might be misunderstanding your question.

What I mean is manually set the `Never` sounds dumb, but if we want it automated, since workload is spawned by job, then we should add a knob to the job. But if this is only for debugging, then there's no problem and we can enhance this if necessary in the future, it's easy.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-17T02:49:15Z

> a boolean should be fine. I think it's clear that this will always be only 2 modes.

If we want to make the requeueing automatically oneday as I mentioned above, then **queueing** is not a good choice because the workload will never enter into the scheduling queue semantically.

With `requeuePolicy`, we can achieve the same goal but still retain the extensibilities, like requeue for once or several times as we do for `restartPolicy`, yes, **this is not demanded** right now, but maybe possible in the future. 🤔

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T12:54:54Z

That would mean that `requeuePolicy: Never` implies that we need to queue at least once. So we need to keep a record of that. Not sure if it's worth the complexity.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-17T17:57:50Z

> That would mean that requeuePolicy: Never implies that we need to queue at least once. So we need to keep a record of that. Not sure if it's worth the complexity.

I agree that `requeuePolicy: Never` can be misleading because the term "requeue" implies it is still admitted once and the policy only applies on "requeue" (after the first queue).

What about `queuingPolicy: AdmitAlways|AdmitOnce|Suspend`? I agree with @kerthcet on the extensibility is better since there _could_ be more than 2 modes down the road.

> So we need to keep a record of that.

For the "AdmitOnce" case can we just check the status of the workload to check if it previously ran or is there limitations to this approach?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-17T17:59:40Z

As a side note ... _if_ we did add a `queuingPolicy` or `requeuePolicy` field, would it make sense to allow defaulting this policy at the LocalQueue or ClusterQueue level?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T18:20:39Z

> What about `queuingPolicy: AdmitAlways|AdmitOnce|Suspend`? I agree with Kante Yin on the extensibility is better since there _could_ be more than 2 modes down the road.

But only implement `AdmitAlways | Suspend` for now?

> For the "AdmitOnce" case can we just check the status of the workload to check if it previously ran or is there limitations to this approach?

We don't keep that information. There might be some hints, like the `Evicted` condition, or the fact that the `Admitted` condition has a transition timestamp much older than the creationTimestamp.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-17T18:45:59Z

> But only implement AdmitAlways | Suspend for now?

Sure we can defer the `AdmitOnce` policy since we don't even have a mechanism for tracking this state as you mentioned

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-18T02:49:31Z

By the way, in what condition job will requeue as it's condition is running, if it runs too long, we'll mark it as failed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-18T14:12:23Z

The job would only be requeued if it's ever suspended, not if it's marked as Failed (for example, if it reaches the ActiveDeadline)

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-25T14:35:00Z

FYI @vicentefb and I have been prototyping this change in https://github.com/kubernetes-sigs/kueue/pull/1252 -- still needs tests but welcome to initial feedback

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-26T20:44:20Z

@tenzen-y what do you think about the proposal?
I think this is small enough to deal in code review. A KEP could be a bit too much overhead, IMO.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-27T17:49:16Z

> @tenzen-y what do you think about the proposal? I think this is small enough to deal in code review. A KEP could be a bit too much overhead, IMO.

@alculquicondor I checked the above discussion. Basically, lgtm.
I think that we can discuss the detail in #1252.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-01T17:03:25Z

@vsoch and I were just discussing that we could potentially use this API to implement workflows.

Essentially, a workload manager would create all the steps (jobs) for a workflow, but tell kueue not queue them yet. Once the workflow manager determines that all the dependencies for the step are satisfied, it communicates this back to kueue.

How? We might have to have an annotation so that the workflow manager doesn't have to deal with the Workload CRD.

@vsoch note that there is a WIP in #1252.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-11-01T17:36:46Z

Thanks @alculquicondor !

I do really like the idea of Kueue exposing handles or hooks for a workflow tool to use. As I mentioned in our meeting earlier, I don't think Kueue should venture into trying to be a workflow tool and control a DAG, but rather to provide these handles for workflow tools to use. For most that I've developed for, we don't submit all at once (and then un-suspend) but rather we submit when they are ready. But (in that there is a queue) this could essentially be like a pre-submit of all steps, and then (if I understand correctly) set suspend to false to run the step exactly when needed (as opposed to submitting and waiting when it's needed).

One question I have is, given that you (some user in a Kueue queue) have submit a ton of jobs with suspend=true, isn't there a potential to (if you were to un-suspend them all at once, possibly when they have the highest priority) to dominate or clog the cluster? I am wondering if there are other issues that might arise too - I'll talk with my team about if we have any kind of similar functionality and what issues have come up.

And for reference - when I say "there are many workflow tools" here is a sample! https://github.com/pditommaso/awesome-pipeline. That list is created by Paolo, the creator of Nextflow (Seqera Labs out of Spain).
For context, I'll eventually be testing out Kueue with workflows for this executor plugin - likely after Kubecon and Supercomputing (end of year). https://github.com/snakemake/snakemake-executor-kueue

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-01T18:29:15Z

> One question I have is, given that you (some user in a Kueue queue) have submit a ton of jobs with suspend=true, isn't there a potential to (if you were to un-suspend them all at once, possibly when they have the highest priority) to dominate or clog the cluster?

That would indeed be a problem. Just like I wouldn't like to have kueue in the business of DAGs, I also wouldn't like it to be in the business of policy enforcement.

There are a few ways in which administrators can limit the ability for end users to create jobs, including good old ResourceQuotas https://kubernetes.io/docs/concepts/policy/resource-quotas/, or something like gate-keeper. Those might be enough. And the workflow manager should be resilient to the restriction, aka, create the jobs that it can, make progress with them, and create new jobs as steps progress.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-01T18:50:20Z

https://github.com/kubernetes/kubernetes/issues/121681 I opened this issue for consideration upstream.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-11-02T03:36:43Z

@alculquicondor ! I just thought of a really strong use case for this - it's related to workflows, but not specifically the step of submitting a DAG that will be suspended and reactivated later. Rather, it would be a great feature for autoscaling. Let me walk through an example.

1. I use my workflow tool that controls a DAG to submit jobs, and we do it via Kueue
2. I create a job (one step in the DAG) that uses the Flux Operator. It starts at a request for N nodes. It anticipates adding +M nodes, so adds M to the request (with suspend=true)
3. The job starts running, and the workflow tool monitors it (likely through requests to check the logs and CRD)
4. We hit a point where the workflow needs to scale, up or down, likely based on some signal from the application that bubbles up. See comment below :t-rex:
5. The workflow tool unsuspends some subset of the M (to scale up) or suspends some of N (to scale down) depending on the application needs. Because we asked for them at the same time, we are more likely to get the nodes soon (and not have to wait through the entire queue).
6. At the end of the CRD completion, everything is cleaned up (e.g., if I had suspended=true requests in there, they go away too).
 
Note that most workflow tools don't submit all the steps at once, they submit them as they are needed / the current task, which is why we can think generally on the level of a few steps (and not an entire DAG). And then there would be limits to how you submit / how many you are allowed to ask for to suspend (because they could become live at any moment) but with this strategy we would only require a workflow step to have an expected range to scale to, which (at least to start) I think is reasonable. I certainly wouldn't want to submit something to the cloud just being like "Go nuts! Scale all the way!"

:t-rex:  If we could just give the application permission (via rbac) to request doing the scale, that would actually work (see the [demo here](https://flux-framework.org/flux-operator/tutorials/elasticity.html) of a simple python script with the right permissions scaling the Flux MiniCluster up and down), but I think security wise it's probably not the best idea (beyond experimentation) to give apps this level of permission. So without that, this is still a hard point to figure out - based on discussion [here](https://github.com/kubernetes-sigs/jobset/pull/244#issuecomment-1765089445) it sounds like probes are too generic. So my thinking (still a WIP) is having some kind of sidecar that can service application specific metrics that map to how to scale via a metrics endpoint. That could either be consolidated by a namespaced metrics app, or done on the individual level (probably wouldn't scale as well). This would be feasible if we can [support more than one](https://github.com/kubernetes/enhancements/pull/4262) metrics server per cluster.

I've been thinking about the above (in several different contexts) quite a bit and I always stumble on the "need to account for the other users in the cluster" part, and I'm thinking Kueue could do that nicely here, and it could work really nicely with this feature to allow for asking for a potential set of extra nodes (that maybe you will use or not). Let me know your thoughts!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-02T17:15:19Z

cc @andrewsykim for the implications to #77

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:12:57Z

/reopen
We should add documentations.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-15T08:13:02Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1091#issuecomment-1857456745):

>/reopen
>We should add documentations.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T08:24:41Z

@vicentefb @andrewsykim Could you open a PR for documentation?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-12-15T14:58:24Z

@vicentefb can you follow-up on the documentation please?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T15:11:34Z

Oops, I wanted to send a mention to @vicentefb.

### Comment by [@vicentefb](https://github.com/vicentefb) — 2023-12-15T19:21:16Z

@tenzen-y sure, sounds good, for future reference, by documentation do you mean to add something like this https://github.com/kubernetes-sigs/kueue/pull/1444/files but for suspendable jobs ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-15T19:24:13Z

> @tenzen-y sure, sounds good, for future reference, by documentation do you mean to add something like this https://github.com/kubernetes-sigs/kueue/pull/1444/files but for suspendable jobs ?

@vicentefb Thanks for moving this forward. The https://github.com/kubernetes-sigs/kueue/pull/1226 would be helpful.

### Comment by [@vicentefb](https://github.com/vicentefb) — 2023-12-15T21:45:05Z

Okok i opened this #1474 i also saw that the API doc update was already done in #1395

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-18T19:34:05Z

Thanks
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-18T19:34:10Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1091#issuecomment-1861426230):

>Thanks
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
