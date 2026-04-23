# Issue #9799: Introduce temporary feature gates for mitigating BestEffortFIFO issues at scale

**Summary**: Introduce temporary feature gates for mitigating BestEffortFIFO issues at scale

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9799

**Last updated**: 2026-03-12T18:08:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-11T08:27:29Z
- **Updated**: 2026-03-12T18:08:07Z
- **Closed**: 2026-03-12T17:47:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I propose introducing two feature gates, temporarily. We will drop them at 0.20 if no one needs them as knobs / configuration.

- SchedulerLongRequeueInterval - increases the 1s base interval to 10s
- SchedulerTimestampPreemptionBuffer - introduces 5min buffer so that workloads which with the scheduling timestamps within 5min buffer don't preempt each other on the LowerOrNewerEqualPriority basis

Maybe long term instead of increasing the base interval we could introduce exponential backoff to 16s or so. The feature gates are meant to collect feedback. They are part of the umbrella issue: https://github.com/kubernetes-sigs/kueue/issues/9715. Basically, we introduced a number of improvements, and it is hard to tell if they are enough. The feature gates would help us to experiment with alternative values if the improvements "don't help". If the feature gates are not needed to be used we will drop them.

**Why is this needed**:

- 1s requeue rate limiting parameter is arbitrary, on very large environments this may still not be enough
- the higher the requeue parameter the more likely the workloads will get admitted "out of order" risking preemptions

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T08:28:07Z

cc  @mwielgus @mwysokin @tenzen-y @gabesaba @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-11T11:48:43Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T11:57:44Z

FYI, let's start with the FG for 1s->10s, this one is more important for now. We are yet discussing the importance of the second actually. Certainly separate PRs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T17:38:38Z

I'd like to clarify what the default value is for both feature gates.
If both default values are false, I'm ok with that.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T17:47:50Z

Yes, both would be false. And we will drop them unless explicitly request to be kept and replaced by knobs. For now we only have conclusion to actually add SchedulerLongRequeueInterval

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:28:56Z

> Yes, both would be false. And we will drop them unless explicitly request to be kept and replaced by knobs. For now we only have conclusion to actually add SchedulerLongRequeueInterval

Cool, in that case, we might be able to backport the FG to released branches. But, it depends on the complex of the changes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:31:04Z

> SchedulerTimestampPreemptionBuffer - introduces 5min buffer so that workloads which with the scheduling timestamps within 5min buffer don't preempt each other on the LowerPriorityOrNewer basis


Instead of a fixed 5 min time, we might want to introduce a preemption strategy, whether or not we should preempt non-PodsReady Jobs. But, this is just an idea, I'd be happy to discuss more.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T18:39:24Z

The first FG is very simple code we already have a PR. A knob for this if needed will be relatively straighforward

For the second I would like to discuss more internally tomorrow. Im more cautious here because replacing the FG with a knob might be tricker.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-11T18:50:05Z

> The first FG is very simple code we already have a PR. A knob for this if needed will be relatively straighforward

yes, but I'd like to consider a knob after v0.17. Before introducing a knob, I'd like to consider a side effect. 
But, FG could be introduced immediately.

> For the second I would like to discuss more internally tomorrow. Im more cautious here because replacing the FG with a knob might be tricker.

We have continued to discuss the preemption loop (preempt a->b->c->a...). I'd like to consider the comprehensive approach both for classic preemption and fair sharing.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2026-03-12T11:48:43Z

SchedulerTimestampPreemptionBuffer - What about hiding it entirely behind a FeatureGate for 0.17 and 0.16 cherry-pick? We will evaluate the feature in the upcoming ~2 months and two things will happen:
* We will get a confirmation that this is needed and the thing will get a proper API.
* We will drop it as not needed.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T12:07:11Z

> We have continued to discuss the preemption loop (preempt a->b->c->a...). I'd like to consider the comprehensive approach both for classic preemption and fair sharing.

This feature gate is not meant to cover preemption loops. It is just to protect against too many preemptions in case of "out of order admission", when `LowerOrNewerEqualPriority` is used. The idea is to say "NewerWithBuffer", so that we don't preempt if the difference in creation timestamps is just 1min, for example.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-12T17:28:17Z

> The idea is to say "NewerWithBuffer", so that we don't preempt if the difference in creation timestamps is just 1min, for example.

Yeah, that sounds reasonable idea, the additional discussion point is how long should we wait for preemption? 1min? 10 min? ...? or user specified arbitrary time?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T18:08:07Z

> how long should we wait for preemption? 1min? 10 min? ...? or user specified arbitrary time?

Do you mean how long we want to wait for the preemption to conclude? This is not changing in the proposal. The proposal is just a small "toleration buffer", as implemented in https://github.com/kubernetes-sigs/kueue/pull/9835.
