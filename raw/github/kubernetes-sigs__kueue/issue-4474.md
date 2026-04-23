# Issue #4474: TAS: Add an algorithm that minimizes the fragmentation

**Summary**: TAS: Add an algorithm that minimizes the fragmentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4474

**Last updated**: 2025-03-18T14:04:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-03-04T13:37:23Z
- **Updated**: 2025-03-18T14:04:07Z
- **Closed**: 2025-03-18T14:04:07Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A new TAS algorithm that assigns pods to domains that will completely minimize resource fragmentation.

Let's assume we have three nodes `x1`, `x2`, `x3` with 2, 1, and 1 GPUs.
We have two workloads:

`workloadA` - requires 2 pods with 1 GPU each, pods don't require heavy communication between each other
`workloadB` - requires 1 pod with 2 GPUs

We want to schedule `workloadA` first and later `workloadB`

Currently we schedule `workloadA` on the `x1` node as it's can fit the whole workload. As a result, `workloadB` cannot be scheduled.

The algorithm I propose would schedule `workloadA` on `x2` and `x3`. Then `workloadB` could be scheduled on the `x1` node. As a result we scheduled both workloads

**Why is this needed**:
Minimize resource fragmentation, improve cluster utilization

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-04T13:37:35Z

cc @mwielgus @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-04T13:58:41Z

> E.g. if we wanted to schedule 2 pods with 1 GPU each on three nodes that can have 2, 1, 1 GPUs available, both of the available algorithms will choose the first node

Is this accurate? IIUC the new algorithm chooses the node with the least amount of free resources, meaning with 1 GPU, and both workloads will eat together nodes two and three.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-04T14:06:14Z

> > E.g. if we wanted to schedule 2 pods with 1 GPU each on three nodes that can have 2, 1, 1 GPUs available, both of the available algorithms will choose the first node
> 
> Is this accurate? IIUC the new algorithm chooses the node with the least amount of free resources, meaning with 1 GPU, and both workloads will eat together nodes two and three.

I've clarified the description, now it should be more clear

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T19:08:33Z

I think the key point is whether or not we handle the workload as a gang.
The current algorithm recognizes a Workload as a gang, but as you described here, some cases want to handle it as not a gang.

I think both (current and new algorithms) are valuable. I'm wondering if we should add annotation to indicate if the TAS workload is a gang similar to kube-scheduler-plugins co-scheduler. Or we might be enough the cluster-scoped setting.

@PBundyra My first question is about use case. Which scope (cluster-scope, workload-scope, cq-scope) in your case?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-10T10:23:31Z

> [@PBundyra](https://github.com/PBundyra) My first question is about use case. Which scope (cluster-scope, workload-scope, cq-scope) in your case?

My proposal is to introduce a new binary PodSet annotation `kueue.x-k8s.io/podset-unconstrained-topology`, that impacts the algorithm choice. At the same time, to simplify adoption of this annotation, I'd like to add a feature gate that would default this annotation's value to `true`. I'll add changes to the KEP describing that

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-10T11:16:48Z

Changes are described here:
https://github.com/kubernetes-sigs/kueue/pull/4542

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-18T14:04:06Z

The issue is addressed and the PRs are linked above
