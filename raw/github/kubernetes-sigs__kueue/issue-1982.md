# Issue #1982: Include a Failed condition in Workloads

**Summary**: Include a Failed condition in Workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1982

**Last updated**: 2024-04-26T15:03:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-15T19:15:34Z
- **Updated**: 2024-04-26T15:03:33Z
- **Closed**: 2024-04-26T15:03:33Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A Failed condition when a Workload finishes because the corresponding Job failed, with a reason coming from the job integration.

Just a reason in the existing Finished condition could work, although that could lead to different job integrations choosing different strings for the common idea of "failed".

**Why is this needed**:

Improved visibility.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-15T19:15:51Z

I remember I discussed this with someone in the past. Was it you @astefanutti ?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-04-16T09:30:39Z

@alculquicondor that is likely me :) I've also touched on this with @mimowo a little while.

For the UI we're building (and generally for other services that could integrate with Kueue) the Workload API provides a convenient abstraction over the different underlying workload types.

There is already the `Finished` condition that's set when the workload has completed, though most of the time other services / UIs also need to differentiate successful completion from failed one. At the moment, each of these services / UIs has to re-implement the logic / heuristic for each integrations.

It seems that logic could be encapsulated into the framework integrations, and increase the added-value of the Workload API even more.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T12:22:30Z

Everyone ok with using a Reason to indicate failure?

Adding an additional condition could also be an option, but the current reason is just a placeholder.

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-16T13:54:04Z

Actually, this discussion happened at the KubeCon Paris 2024 with @mimowo, @astefanutti, and me :)
Also, I agree with this idea.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T14:32:16Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-04-16T14:35:37Z

The reason and message of the finished condition should already provide this, Am I missing something?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-04-16T14:40:24Z

The purpose of this is to have the reason be "fixed", like `Failed`, computed by each framework integration, similarly to how `GenericJob.Finished` is implemented.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T15:00:52Z

In the case of Job, we have reason `JobFinished` regardless of whether the job finished successfully or not:

https://github.com/kubernetes-sigs/kueue/blob/206b59fd24d0bac711a99c24f43de90e8488b347/pkg/controller/jobs/job/job_controller.go#L295

So the question is whether we want to change all implementations of `Finished` to have a common reason for the case of "Failed" or add an additional condition based on a new `Failed` method in the GenericJob interface.

A separate condition could give us a standard condition plus additional granularity for failure reasons.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T15:01:46Z

Still, it might be worth it to start just with a standard `Failed` reason in the existing `Finished` condition.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-04-16T15:17:54Z

Right, as you said previously, the current reason is just a placeholder, so this can probably be changed.

As to whether introduce a separate condition, the batch Job API has one:
```
JobFailed JobConditionType = "Failed"
```
I don't know what drove that design decision, but if that was for "good" reasons, we could be consistent with it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-16T15:24:22Z

> Right, as you said previously, the current reason is just a placeholder, so this can probably be changed.
> 
> As to whether introduce a separate condition, the batch Job API has one:
> 
> ```
> JobFailed JobConditionType = "Failed"
> ```
> 
> I don't know what drove that design decision, but if that was for "good" reasons, we could be consistent with it.

As far as I understand, the Job API was provided before the standardized metav1.Conditions including `reason`.
So, currently, I'm curious about whether we can use the `Reason` field as @alculquicondor mentioned above.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T15:31:37Z

I think we should just start simple. The current reason `JobFinished` is not helpful at all.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-04-16T15:38:13Z

That sounds good to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-18T07:36:37Z

I like this idea of starting simple and using reason in the `Finished` condition. Instead of the generic reason `JobFinished` we would have two: `Failed` and `Succeeded`.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-18T19:30:48Z

/assign
