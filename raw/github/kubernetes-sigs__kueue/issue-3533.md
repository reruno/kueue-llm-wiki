# Issue #3533: TAS: support rank-ordering for Pods for built-in integrations

**Summary**: TAS: support rank-ordering for Pods for built-in integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3533

**Last updated**: 2024-11-28T09:08:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-14T10:19:57Z
- **Updated**: 2024-11-28T09:08:58Z
- **Closed**: 2024-11-28T09:08:58Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@mbobrovskyi](https://github.com/mbobrovskyi), [@PBundyra](https://github.com/PBundyra)
- **Comments**: 6

## Description

**What would you like to be added**:

For Jobs which provide indexing (like batch/Job) we should place Pods with consecutive indexes (ranks) should be placed as close as possible in the topology tree.

The current implementation places pods pretty much randomly (as they show up in the API server).

Example, we have a jobs with 10pods: 0,1,2,3,4,5,6,7,8,9. We have 3 racks, each with 4 slots. 

* Current possible ordering:  [1,4,5,7][0,3,8,9][6,2] - suboptimal because communication 0-1,1-2, 2-3,3-4,5-6,6-7,7-8 cross the rack boundary and so will be slow
* Wanted:  [0,1,2,3][4,5,6,7][8,9] - optimal, only 0-9,3-4,7-8 cross the rank boundary

**Why is this needed**:

For improved performance of network communication between pods. This is especially important for AI/ML frameworks, where the pods exchange data in the ring structure (like in NCCL).

It is part of https://github.com/kubernetes-sigs/kueue/issues/3450

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T10:20:04Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T10:20:20Z

cc @PBundyra @mwysokin @mwielgus @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T09:44:13Z

An extension of this we hear would be useful for our users is to support PodGroups which are managed and indexed by an external controller. 

I think that the current (label lookup-based in TopologyUngater, [here](https://github.com/kubernetes-sigs/kueue/blob/6c98ea3a73167b244d3249d0b3f71e944d603dc1/pkg/controller/tas/topology_ungater.go#L402)) mechanism creates the incentive to support this by adding k8s-reserved labels to the custom controllers, which is not healthy.
To resolve this issue I propose API at the workload level in PodSetTopologyRequest, called `podIndexLabel` (or 2 more to also abstract JobSet, `jobIdexLabel` and `replicatedJobCount`). With this API the implemetation of the GenericJob interface will set the values depending on the framework. 
For pod groups we could have a label reserved by kueue, like `kueue.x-k8s.io/pod-group-index` (or like that).

We need a TAS KEP extension for that, and @PBundyra agreed tentatively to work on it.

cc @tenzen-y @mwysokin @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T09:57:52Z

/assign @PBundyra 
for the pod groups support and the generalized API

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T10:00:43Z

/assign @mbobrovskyi 
for the Kubeflow indexes support. For now just lookup the [pod index label](https://github.com/kubeflow/training-operator/blob/8c2e8f8fe3360dfd73cdd9d7c30c52faba8dbae9/pkg/apis/kubeflow.org/v1/common_types.go#L25) in the TopologyUngater around [here](https://github.com/kubernetes-sigs/kueue/pull/3591/files#diff-afb64db58a684de4be406c79f3fa8fbd619e1304676f9bf4709b3e4706e755cfR432). It will be later generalized by the new API + e2e test for kubeflow indexing.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T08:54:59Z

I have opened dedicated https://github.com/kubernetes-sigs/kueue/issues/3663 to address the comment in https://github.com/kubernetes-sigs/kueue/issues/3533#issuecomment-2488092129.
Then we can close this issue when we complete https://github.com/kubernetes-sigs/kueue/pull/3649
