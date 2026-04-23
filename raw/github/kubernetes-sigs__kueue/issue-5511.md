# Issue #5511: Deleted workload entry outlives cq in scheduler cache

**Summary**: Deleted workload entry outlives cq in scheduler cache

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5511

**Last updated**: 2025-06-10T12:32:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-06-05T06:28:12Z
- **Updated**: 2025-06-10T12:32:26Z
- **Closed**: 2025-06-10T12:32:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 7

## Description

As we see in this [log](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5461/pull-kueue-test-integration-baseline-main/1930264942032719872/build-log.txt) and many examples in the #5395.

Workload `wl1` entry from test `Nodes are created before test with the hostname being the lowest level  should evict workload when multiple assigned nodes fail` outlives the test in the scheduler's cache.
That's because it was re-queued for second pass.
Thus it is still visible in test `Preemption is enabled within ClusterQueue  should preempt the low and mid priority workloads to fit the high-priority workload` in result it is considered as possible preemption for `wl2` causing preemption failure
```
  2025-06-04T14:11:53.966698632Z	ERROR	scheduler	scheduler/scheduler.go:271	Failed to preempt workloads	{"schedulingCycle": 167, "workload": {"name":"wl2","namespace":"tas-rjx27"}, "clusterQueue": {"name":"cluster-queue"}, "error": "workloads.kueue.x-k8s.io \"wl1\" not found"}
```
and blocking `wl2` from being admitted.

**What you expected to happen**:
Delete workloads don't get scheduled for second pass, if they do scheduler do not nominates them for preemption.

**How to reproduce it (as minimally and precisely as possible)**:
Here is the reproduction [PR](https://github.com/kubernetes-sigs/kueue/pull/5513)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T06:38:11Z

/assign 
tentatively, I hope to have time this week, at least to investigate and propose how to fix

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T06:40:04Z

@mszadkow could you leave a reference to the repro test that you created? Maybe even leave it as a gist, or reference to your branch.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-05T08:21:33Z

> [@mszadkow](https://github.com/mszadkow) could you leave a reference to the repro test that you created? Maybe even leave it as a gist, or reference to your branch.

Added to the issue description

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T08:53:01Z

thx

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:11:11Z

Ok, I have analyzed the issue and I think I understand it. I will describe soonish, and I'm creating follow up issues which I discovered on the way, and which made the investigation harder than it should be, for now: https://github.com/kubernetes-sigs/kueue/issues/5559 and https://github.com/kubernetes-sigs/kueue/issues/5558

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T09:22:16Z

Other issues which interfere with this bug and make it more difficult:
- we trigger second pass for Evicted or Finished workloads https://github.com/kubernetes-sigs/kueue/issues/5561 (not source of the issue, but making it harder to reason about). The flake still sometimes surfaces
- we use two step eviction https://github.com/kubernetes-sigs/kueue/issues/5560 (not source of the issue, but makes it harder to reason about). The flake would not surface if we did that.
- when  Kueue scheduler fails to preempt (due to the target workload removed) gives up and not retries (I will open soon, still playing to better understand the circumstances around the code [here](https://github.com/kubernetes-sigs/kueue/blob/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/pkg/scheduler/scheduler.go#L266-L274)) cc @gabesaba 
- When forgetWorkload happens in the 1s delay [here](https://github.com/kubernetes-sigs/kueue/blob/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/pkg/queue/manager.go#L793C21-L793C31), then the second pass is rescheduled still (main issue)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T15:14:27Z

> * when  Kueue scheduler fails to preempt (due to the target workload removed) gives up and not retries (I will open soon, still playing to better understand the circumstances around the code [here](https://github.com/kubernetes-sigs/kueue/blob/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/pkg/scheduler/scheduler.go#L266-L274)) cc [@gabesaba](https://github.com/gabesaba)

Here is the issue: https://github.com/kubernetes-sigs/kueue/issues/5590 along with the repro PR https://github.com/kubernetes-sigs/kueue/pull/5589
