# Issue #59: Flavors with matching names should have identical labels/taints

**Summary**: Flavors with matching names should have identical labels/taints

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/59

**Last updated**: 2022-03-21T22:22:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-24T02:47:25Z
- **Updated**: 2022-03-21T22:22:47Z
- **Closed**: 2022-03-21T22:22:47Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 7

## Description

A capacity can borrow resources from flavors matching the names of ones defined in the capacity. Those flavors with matching names should also have identical labels and taints.

One solution is to define a cluster-scoped object API that represents resource flavors that capacities refer to by name when setting a quota. It would look like this:

```
type ResourceFlavorSpec struct {  
  // the object name serves as the flavor name, e.g., nvidia-tesla-k80. 

  // resource is the resource name, e.g., nvidia.com/gpus.   
  Resource v1.ResourceName  

  // labels associated with this flavor. Those labels are matched against or  
  // converted to node affinity constraints on the workload’s pods.  
  // For example, cloud.provider.com/accelerator: nvidia-tesla-k80.  
  Labels map[string]string  

  // taints associated with this constraint that workloads must explicitly   
  // “tolerate” to be able to use this flavor.  
  // e.g., cloud.provider.com/preemptible="true":NoSchedule  
  Taints      []Taint
}
```

This will avoid duplicating labels/taints on each capacity and so makes it easier to create a cohort of capacities with similar resources. 

The downside is of course now we have another resource that the batch admin needs to deal with. But I expect that the number of flavors will typically be small.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T14:41:57Z

I would add that the ResourceFlavor shouldn't be mandatory.

OTOH, that means that we should proceed with scheduling even if we can't find a matching ResourceFlavor object. This can lead to jobs scheduling on flavors they shouldn't, specially during restarts. Is this acceptable?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-01T20:47:03Z

Are we settled on having a ResourceFlavor CRD?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-01T20:57:08Z

I think we should do that, yes.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-01T21:00:28Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:57:11Z

/unassign

leaving this for now (feel free to take it)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T21:09:07Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-14T17:47:30Z

I would delay this until after 0.0.1; I think it is more important to focus on testing and verifying scale now.
