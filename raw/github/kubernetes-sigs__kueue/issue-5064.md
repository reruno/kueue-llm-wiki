# Issue #5064: Add admission and scheduling times to exposed metrics to improve observability

**Summary**: Add admission and scheduling times to exposed metrics to improve observability

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5064

**Last updated**: 2025-05-09T10:41:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2025-04-22T10:07:14Z
- **Updated**: 2025-05-09T10:41:15Z
- **Closed**: 2025-05-09T10:41:15Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I'd like to request adding 2 new metrics in a form of a histogram: 
- admission time defined as the time spent on admission (after creation before scheduling) per workload,
- scheduling time defines as the time spent on scheduling (after admission before ready/running) per workload.

**Why is this needed**:

Adding these 2 metrics will improve general observability and give a good overview of the state of the system especially at scale with many workloads. Doing it in a form of a histogram will enable integrations with analytics and visualization tools such as grafana.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-22T13:07:17Z

> admission time defined as the time spent on admission (after creation before scheduling) per workload,

I believe this we already have https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/metrics/metrics.go#L173-L180. 
I think what is missing is "creation or last requeued time to ready", but maybe you can double check @mwysokin

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-23T13:58:41Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-23T16:11:48Z

IIUC according to @mimowo we already have the `admission time defined as the time spent on admission (after creation before scheduling) per workload`
Thus we should only consider `scheduling time defines as the time spent on scheduling (after admission before ready/running) per workload`, which means that all the pods for given workload are ready.
I assume somewhere around this line: https://github.com/kubernetes-sigs/kueue/blob/eaefeaa5e46dcc0963f84c0ac9f3adbda557e680/pkg/controller/jobframework/reconciler.go#L481
, but making sure it's turning into `PodsReady` correct?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T12:17:16Z

IIUC the intention is to have two new histogram metrics:
- created or requeued -> ready (maybe `ready_wait_time_seconds`)
- admitted -> ready                      (maybe `admitted_until_ready_wait_time_seconds`)

but a confirmation from @mwysokin would be great

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-04-24T12:29:18Z

SGTM 🖖

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-25T09:33:27Z

@mimowo @mwysokin so far we track `PodsReady` status only when `waitForPodsReady` is true.
Do we want to track this even without the feature?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-25T09:56:19Z

Great question, I would say probably we want it regardless is `waitForPodsReady` is enabled. We could record the metrics `create -> PodsReady` regardless if the eviction by `waitForPodsReady` is enabled.

That being said, I see it as a follow up, if this makes the task easier / simpler. I would start with only supporting the case when `waitForPodsReady` is enabled. And we can say that when `waitForPodsReady` the semantic is currently undefined, so that we can easily change it.

wdyt @mwysokin ?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-04-29T09:26:18Z

SGTM 🖖
