# Issue #3658: TAS: respect node taints when the lowest hierarchy level is node

**Summary**: TAS: respect node taints when the lowest hierarchy level is node

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3658

**Last updated**: 2024-11-28T15:43:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-26T16:43:02Z
- **Updated**: 2024-11-28T15:43:23Z
- **Closed**: 2024-11-28T15:43:21Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 6

## Description

**What would you like to be added**:

Respect node taints when scheduling by TAS when the lowest hierarchy level is `kubernetes.io/hostname`.

**Why is this needed**:

Some users may want to taint a node and exclude it from TAS. However, we still should include the tainted notes for which the workload has tolerations.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-26T16:43:13Z

cc @PBundyra @tenzen-y 
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T17:02:06Z

I discussed this with @mimowo offline.
Technically, we can check taints at all levels.
But, in that case, we need to traverse all hierarchical taints. 
So, we support only the lowest hierarchy-level taints.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-28T08:58:20Z

A relatively simple approach for supporting taints for any Topology levels,  I discussed with @PBundyra yesterday, is to introduce a "virtual" level for nodes, even if not specified directly by the user in the Topology object. Still, it adds a bit of complexity, so I want to deliver this in two parts:
1. respect taints if the lowest level is kubernetes.io/hostname
2. respect taints for any topology by introducing the "virtual" level corresponding to kubernetes.io/hostname

The priority of (2.) is lower, but it should be simple so I will try to fit both into 0.10

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-28T14:48:47Z

After consulting this with @mwielgus we decided to defer this decision / support for later. I open KEP update to capture the need to handle topologies without hostname better: https://github.com/kubernetes-sigs/kueue/pull/3681

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-28T15:43:17Z

/close
The main issue is addressed, we will re-consider the options when there is no kubernetes.io/hostname the last level post 0.10, proposed KEP update: https://github.com/kubernetes-sigs/kueue/pull/3681

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-28T15:43:22Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3658#issuecomment-2506395816):

>/close
>The main issue is addressed, we will re-consider the options when there is no kubernetes.io/hostname the last level post 0.10, proposed KEP update: https://github.com/kubernetes-sigs/kueue/pull/3681


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
