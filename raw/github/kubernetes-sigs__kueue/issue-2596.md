# Issue #2596: Can we preempt in more than one CQ per cohort in a cycle?

**Summary**: Can we preempt in more than one CQ per cohort in a cycle?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2596

**Last updated**: 2024-07-19T14:58:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-12T18:23:57Z
- **Updated**: 2024-07-19T14:58:44Z
- **Closed**: 2024-07-19T14:31:32Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 5

## Description

_Note: opening this more of as a discussion, rather than something that can be worked on right away._

If a CQ needs a preemption, and such preemption is taking a long time (because of the grace period), then this blocks other preemptions in the same cohort:

https://github.com/kubernetes-sigs/kueue/blob/6248b5808159b0b74586e4b63a80cfc739dcfc38/pkg/scheduler/scheduler.go#L233-L238

Can we take a more optimistic approach and allow other CQs to preempt?

A problematic scenario could be as follows:
- Workload `a` from CQ A needs to preempt `x`, `y`.
- Workload `b` from CQ B needs to preempt `y` and `z`.

Now `x`, `y` and `z` are successfully preempted, so Workload `a` can fit. But workload `b` cannot longer fit, because `a` took the space of `y`. There are 2 possibilities:
- `b` can preempt something else, in which case the situation should resolve by itself in the next iterations.
- `b` can't preempt anything else, in which case we preempted `z` unnecessarily.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-12T18:29:01Z

Maybe we can allow more preemptions, as long as each workload is preempting different workloads. But my gut feeling is that, in most scenarios, multiple CQs will be trying to preempt the same workloads.

Another avenue could be to combine the above suggestion with excluding terminating workloads from the preemption target calculations. This way, each CQ would try to preempt workloads that were not chosen by other CQs already. But we could be at risk of doing unnecessary preemptions if one of the workloads that is stuck in termination is big enough to make space for multiple workloads that needed preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-12T18:29:25Z

cc @gabesaba

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-15T12:18:13Z

> Maybe we can allow more preemptions, as long as each workload is preempting different workloads.

Let's start with this, as it can help in the cases when multiple CQs are preempting their own workloads.

/assign @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-16T12:40:40Z

> > Maybe we can allow more preemptions, as long as each workload is preempting different workloads.
> 
> Let's start with this, as it can help in the cases when multiple CQs are preempting their own workloads.
> 
> /assign @gabesaba

I think that there is a problematic case even when the sets of workloads preempted are disjoint - suppose both CQs need some remaining `FlavorResource` capacity, plus whatever capacity is reclaimed from the preemption. If the sum of `FlavorResource` capacity needed by both CQs is more than the Cohort has available, then only one can be admitted, and we did a wasteful preemption.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-19T14:58:43Z

> > > Maybe we can allow more preemptions, as long as each workload is preempting different workloads.
> > 
> > 
> > Let's start with this, as it can help in the cases when multiple CQs are preempting their own workloads.
> > /assign @gabesaba
> 
> I think that there is a problematic case even when the sets of workloads preempted are disjoint - suppose both CQs need some remaining `FlavorResource` capacity, plus whatever capacity is reclaimed from the preemption. If the sum of `FlavorResource` capacity needed by both CQs is more than the Cohort has available, then only one can be admitted, and we did a wasteful preemption.

handled this case in #2641
