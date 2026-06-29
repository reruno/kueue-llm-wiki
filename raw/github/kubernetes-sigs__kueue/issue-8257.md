# Issue #8257: TAS: better algorithm for comacting TopologyAssignment to support workloads 150k nodes

**Summary**: TAS: better algorithm for comacting TopologyAssignment to support workloads 150k nodes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8257

**Last updated**: 2026-06-16T23:00:19Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-16T10:02:04Z
- **Updated**: 2026-06-16T23:00:19Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@ShaanveerS](https://github.com/ShaanveerS)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to add a better algorithm which is node-pool aware.

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/7544 as the introduced API allows for it already.

The idea is to group nodes which have the common prefix. Let's consider node names on GKE:
`gke-$clusterName-$nodepoolName-$nodePoolHash-$hash`
So in this setup currently we create one group of nodes with the common prefix `gke-$clusterName-`. We can do better by creating multiple groups (slices), each with common  `gke-$clusterName-$nodepoolName-$nodePoolHash-`

This optimization would also benefit other know cloud providers as they use similar naming patterns. 

**Why is this needed**:

To support workloads up to 150k nodes.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T10:02:25Z

cc @olekzabl @mwysokin @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:35:26Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:53:11Z

/remove-lifecycle stale

### Comment by [@ShaanveerS](https://github.com/ShaanveerS) — 2026-05-20T10:53:22Z

/assign

### Comment by [@amy](https://github.com/amy) — 2026-06-16T17:34:13Z

@mimowo Node prefix is kind of weird as a convention. Can you do something that groups labels instead?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-06-16T18:32:19Z

This issue is not about changing the convention just growing the number of supported nodes within the convention. 

So your question is valid but I think something already designed. The motivation for using node names are two fold
1. uniqueness ensured, no need for extra validations across cluster
2. They are already ootb on every cloud, requiring a new label to indicate a node would cause friction for adoption of TAS

### Comment by [@amy](https://github.com/amy) — 2026-06-16T22:07:28Z

@mimowo specifically, I need label support within the algorithm. (we dont denote topology via node name like this) So the mechanism needs to have a swappable entrypoint for labels vs. node name when it parses topology

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-06-16T22:52:43Z

@amy In my eyes, this issue is _only_ about _byte-packing_ the (JSON) representation of a TopologyAssignment.
Node names appear in TopologyAssignments, and take plenty bytes, leading to scalability bottlenecks.
So it's beneficial to extract common prefixes, to be able to pack more nodes within a single etcd entry (1.5 MiB limit).

Extracting these prefixes has _nothing to do_ with the actual topology.
We make _no assumptions_ how "sharing a name prefix" relates to being "topologically close".

So I don't see how labels would plug into this story.

Also, note that `Topology` already supports defining topology in terms of arbitrarily chosen Node labels.
Is there some extra functionality you'd need?

### Comment by [@amy](https://github.com/amy) — 2026-06-16T23:00:02Z

@olekzabl ah ok. Thanks for the clarification. I misinterpreted this as something more fundamental about the TAS algorithm changing based off node names. Removing my hold.
