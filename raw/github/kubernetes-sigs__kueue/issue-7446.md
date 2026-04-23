# Issue #7446: Inconsistency in finding place for leader in PodSetGrouping

**Summary**: Inconsistency in finding place for leader in PodSetGrouping

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7446

**Last updated**: 2026-04-20T05:46:29Z

---

## Metadata

- **State**: open
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-10-30T12:00:03Z
- **Updated**: 2026-04-20T05:46:29Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Kueue might fail to assign topology for a PodSet when using PodSetGrouping and there are two domains that can fit leader and:
- one has bigger worker capacity than the other
- one has smaller worker capacity than the other but is "more efficient" meaning it can fit leader with smaller decrease in worker capacity.

As a first step in TAS algorithm the infrastructure tree is traversed and capacities are collected and summarizer in higher-order domains. That means the algorithm calculates the worker capacity for each host then it summarizes the capacity of all children hosts and sets a worker capacity of a rack (and then moves on to summarizing blocks, and so on).

Leader and worker might have different resource requirements, which means assigning a leader in a particular domain might result in decrease in workers capacity within that domain. To calculate that and find a place for a leader in PodSetGrouping a new metadata `stateWithLeader` and `sliceStateWithLeader` has been introduced ([PR](https://github.com/kubernetes-sigs/kueue/pull/5845)). Those fields describe how many worker pods or worker slices can fit in a domain if a leader would be assigned there.

When algorithm is traversing infrastructure tree it has to summarize `stateWithLeader` and `sliceStateWithLeader` as well in a higher-level domain. However, it is not just a sum of `stateWithLeader` and `sliceStateWithLeader` from all its children as leader will be assigned to only one of the children. Thus, algorithm has to sum `state` and `sliceState` from all children apart from a single child that is most optimal to be assigned a leader and add `stateWithLeader` and `sliceStatewithLeader` from that child to the summary.

The most optimal child to assign a leader is a child that has the lowest "penalty" of hosting a leader which means it has the lowest `state - stateWithLeader` or `sliceState - sliceStateWithLeader`. This logic has been implemented [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1377-L1382).

At the end of the TAS algorithm, after finding domains that can fit a workload, the code traverses the infrastructure tree downwards and assigning pods to lower-level domains to eventually find assignment at leaves (hosts). In doing so it sorts children domains by the capacity and greedily assigns pods starting from the "most-free" ones ([code](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1125-L1139)).

This logic does not take into account the leader-optimization step from the beginning of the algorithm and might result in leader being assigned to not-the-most-optimal child domain, and in certain circumstances resulting in invalid state of the algorithm, as the algorithm at this stage assumes that there is enough space in this domain to assign a workload.

**An example**
Let's consider a single rack with 3 hosts:
- `h1` - 2 CPUs
- `h2` - 4 CPUs
- `h3` - 3 CPUs

Worker requirement is 2 CPUs per pod. 
Leader requirement is 1 CPU per pod.
Workload contains 1 leader and 4 workers.
Required topology is a rack

The 1st stage of the algorithm will assume the leader should be assigned to `h3` as it will 1 CPU and the number of workers will still be 1 in spite of leader being there. At the same time assigning leader to `h1` or `h2` would result in one less worker fitting there.

In the last stage of the algorithm `h1`, `h2` and `h3` would be sorted by capacity, so `h2` would be the first to greedily assign pods to. It would result in assigning the leader there (taking 1 CPU), assigning 1 worker there and leaving 1 CPU unused. Later on one worker pod would be assigned to `h3` and one to `h1`. In the end 1 last worker would be left unassigned, because there would be no space left in any of the hosts, thus resulting in invalid state of the algorithm.

**What you expected to happen**:
Algorithm should not end up in invalid state and properly assign leader and workers to the infrastructure since there's a space needed for that workload.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T12:06:32Z

cc @mwysokin to consider staffing, I think it would be nice to make the logic of 2-level scheduling sound

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:39:19Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:40:01Z

/priority important-soon
/remove-priority important-longterm
Let me actually use soon since this is a TAS-related bug

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:21Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:54Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:46:26Z

/remove-lifecycle rotten
