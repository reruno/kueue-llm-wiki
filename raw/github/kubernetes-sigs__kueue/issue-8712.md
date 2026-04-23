# Issue #8712: MultiKueue: Support Elastic RayJob

**Summary**: MultiKueue: Support Elastic RayJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8712

**Last updated**: 2026-02-16T10:49:37Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-21T07:24:14Z
- **Updated**: 2026-02-16T10:49:37Z
- **Closed**: —
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: [@highpon](https://github.com/highpon)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to support elastic RayJob via MultiKueue. 

The main problem with the current approach of Workload a the RayCluster level is that we only create the instance of RayCluster on the worker cluster, thus:
1. there is no RayJob instance to create the RaySubmitterJob on the worker cluster


**Why is this needed**:

To run Elastic Ray Job via MultiKueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T07:24:36Z

/assign @highpon 
cc @yaroslava-serdiuk 
Who is already working on that

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T07:25:13Z

cc @andrewsykim

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T10:06:30Z

related to https://github.com/kubernetes-sigs/kueue/issues/8201 , actually this is going the opposite way

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-01-21T17:08:35Z

Working on [PR 8341](https://github.com/kubernetes-sigs/kueue/pull/8341) related to this issue.

Previously we discussed to make RayCluster always top level and remove RayJob integration. Turned out that did not work with MultiQueue. In MultiQueue, we need to manage RayJob in Management Cluster, and copy it to Worker Cluster.

There are also other changes needed, see details in [PR 8341](https://github.com/kubernetes-sigs/kueue/pull/8341).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:49:34Z

/area multikueue
