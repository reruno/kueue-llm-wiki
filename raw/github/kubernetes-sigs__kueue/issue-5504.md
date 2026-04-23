# Issue #5504: Rename WorkloadReference to Reference

**Summary**: Rename WorkloadReference to Reference

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5504

**Last updated**: 2025-06-20T04:22:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-04T17:16:39Z
- **Updated**: 2025-06-20T04:22:53Z
- **Closed**: 2025-06-20T04:22:53Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to rename `WorkloadReference` to `Reference` in https://github.com/kubernetes-sigs/kueue/blob/c47505f90ea356ed6fbf1c2238a28eaf5551d9f3/pkg/workload/workload.go#L72-L73

**Why is this needed**:

As I mentioned in https://github.com/kubernetes-sigs/kueue/pull/5366/files#r2120797124, we should avoid repeat the package name in contents like variables.
The client code calls it as `workload.WorkloadReference`. This form must be avoided and the workload pacakge allows client codes to call it as `workload.Reference`.

See more detailed recommendations in Go blog: https://go.dev/blog/package-names#naming-package-contents

> Avoid repetition. Since client code uses the package name as a prefix when referring to the package contents, the names for those contents need not repeat the package name. The HTTP server provided by the http package is called Server, not HTTPServer. Client code refers to this type as http.Server, so there is no ambiguity.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T17:18:42Z

@mimowo @vladikkuzn I opened this issue since the PR was merged before I checked your comments.
Can you post the point of view for this one if you still believe `WorkloadReference` is better?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-04T17:31:47Z

> Can you post the point of view for this one if you still believe `WorkloadReference` is better?

I posted the motivation for WorkloadReference in [response](https://github.com/kubernetes-sigs/kueue/pull/5366/files#r2123016475), but basically:
1. consistency with other "Reference" names
2. better name when we move the const to API package

Having said that I'm ok with the rename as you propose, since temporarily it looks awkward.

Alternatively we could consider moving this to API package as for ClusterQueueReference.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T17:41:09Z

> > Can you post the point of view for this one if you still believe `WorkloadReference` is better?
> 
> I posted the motivation for WorkloadReference in [response](https://github.com/kubernetes-sigs/kueue/pull/5366/files#r2123016475), but basically:
> 
> 1. consistency with other "Reference" names
> 2. better name when we move the const to API package
> 
> Having said that I'm ok with the rename as you propose, since temporarily it looks awkward.
> 
> Alternatively we could consider moving this to API package as for ClusterQueueReference.

The difference between workload and others is others are used in CRD, but workload one isn't used in CRD.
So, I still believe that having `Reference` typed in the workload package.

@mimowo Do you have any motivations that you want to have WorkloadReference typed in API package?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-04T17:59:14Z

> The difference between workload and others is others are used in CRD, but workload one isn't used in CRD.

Yeah, but using in CRD is not the only reason to declare a const in API pkg. 

For example, in core k8s you have in API declarations of consts corresponding to 
- [well_known_taints](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/well_known_taints.go#L22), example TaintNodeNotReady
- [well_known_labels](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/well_known_labels.go), example `LabelTopologyZone   = "topology.kubernetes.io/zone"`
- [well known resource types](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/types.go#L6606-L6613), example CPU

> @mimowo Do you have any motivations that you want to have WorkloadReference typed in API package?

Nothing serious, I'm totally ok to rename as workload.Reference if you prefer.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-04T18:42:50Z

In any case, Im happy to merge the rename PR. @vladikkuzn would you like to follow up?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-06-04T19:10:58Z

Yes, sure, np

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-06-04T19:11:03Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T11:11:19Z

> > The difference between workload and others is others are used in CRD, but workload one isn't used in CRD.
> 
> Yeah, but using in CRD is not the only reason to declare a const in API pkg.
> 
> For example, in core k8s you have in API declarations of consts corresponding to
> 
> * [well_known_taints](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/well_known_taints.go#L22), example TaintNodeNotReady
> * [well_known_labels](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/well_known_labels.go), example `LabelTopologyZone   = "topology.kubernetes.io/zone"`
> * [well known resource types](https://github.com/kubernetes/kubernetes/blob/8d3fb9ee0a51b6a6ea135d991391c35806422c19/staging/src/k8s.io/api/core/v1/types.go#L6606-L6613), example CPU
> 
> > [@mimowo](https://github.com/mimowo) Do you have any motivations that you want to have WorkloadReference typed in API package?
> 
> Nothing serious, I'm totally ok to rename as workload.Reference if you prefer.

For the above constants, yes that makes sense. However, the `WorkloadReference` is typed not constants, and if we host it as API package, we need to deliver Initialization function, `NewWorkloadReference` in API package as well. So, I recommended to move it to `workload` package.

In anycase, if you are ok with renaming to `workload.Reference`, I'm fine with that.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T11:16:20Z

Sure, let's go with workload Reference
