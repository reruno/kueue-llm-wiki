# Issue #9715: ☂️ Solve the problem of non-admissible workloads in BestEffortFIFO despite enough capacity

**Summary**: ☂️ Solve the problem of non-admissible workloads in BestEffortFIFO despite enough capacity

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9715

**Last updated**: 2026-03-13T10:01:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T13:11:05Z
- **Updated**: 2026-03-13T10:01:35Z
- **Closed**: 2026-03-13T10:01:35Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

This is an umbrella issue as fixing the problem with using BestEffortFIFO at scale, because currently the issues are spread.

Consider you have 10k workloads in a BestEffortCQ. Often they would target different flavors. If one flavor is capped at full capacity (say GPU), then the inadmissible list it used to put the "NoFit" workloads aside to "drill" the CQ searching for admissible workloads in the consecutive scheduling cycles.

Now, when there are 10k worklaods (or more) the admissible workload might be at position 1k. This means that to schedule the workload Kueue needs to "drill". If requeue happens in the meanwhile, the drilling starts over again. In the result Kueue scheduler ends up processing the same set of unschedulable workloads over and over again, not making progress, while admissible workload (say CPU) are waiting.

Originally Kueue would requeue all workloads any time some workload is finished. This was very unpredictible, and on a large system it would be all the time (too frequent). With the recent improvement https://github.com/kubernetes-sigs/kueue/issues/8095 to rate limit the requeue of inadmissible workloads we improved the situation, but the problem exists, especially for TAS where each scheduling cycle is long.

For TAS each scheduling cycle takes a long time, say 500ms. So, essentially, Kueue can "drill" only 2-3 workloads within the second. Good luck scheduling something at position 1k :).

To fix the issue we need improvements in multiple areas:
- predictable rate limiting for the requeue events (done already by 1s)
- performance of the single scheduling cycle (especially for TAS)
- smaller gaps between scheduling cycles
- batch drilling by skipping of workloads with equivalent scheduling directives 

Sub-issues:
- https://github.com/kubernetes-sigs/kueue/issues/8095
- https://github.com/kubernetes-sigs/kueue/issues/9337
- https://github.com/kubernetes-sigs/kueue/issues/9716
- https://github.com/kubernetes-sigs/kueue/issues/9694
- https://github.com/kubernetes-sigs/kueue/issues/9730
- https://github.com/kubernetes-sigs/kueue/issues/9782 
- https://github.com/kubernetes-sigs/kueue/issues/9799

**Why is this needed**:

Currently this is the primary problem users report when using BestEffortFIFO at scale.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T13:12:31Z

cc @mwielgus @sohankunkerkar @j-skiba @mbobrovskyi

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-03-06T13:35:32Z

Thanks for raising this! 🙏  We finally got around to testing #9232 and found it to not help our case. We are currently waiting for #9698  to be merged. I appreciate this umbrella issue as a way to explore the different approaches to addressing the problem.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T13:42:42Z

cc @tenzen-y @gabesaba

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-03-10T00:03:37Z

We're also facing this issue. A scheduling cycle takes around 500ms in our TAS-enabled cluster, and some workloads were never getting evaluated.
As a workaround, we patched kueue to drop the FIFO ordering. Instead, we sort workloads in the CQ based on the last evaluated cycle number. It evaluates everything for now, but we know it's not a real long-term solution.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T10:01:33Z

Let me close since all sub-items are done. We can re-open, or open a dedicated improvement if we have more ideas. Feedback will be very welcome.
