# Issue #8257: TAS: better algorithm for comacting TopologyAssignment to support workloads 150k nodes

**Summary**: TAS: better algorithm for comacting TopologyAssignment to support workloads 150k nodes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8257

**Last updated**: 2026-03-19T09:53:14Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-16T10:02:04Z
- **Updated**: 2026-03-19T09:53:14Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

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
