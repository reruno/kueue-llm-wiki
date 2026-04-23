# Issue #3754: TAS: reduce friction by defaulting the PodSet annotations

**Summary**: TAS: reduce friction by defaulting the PodSet annotations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3754

**Last updated**: 2025-03-11T09:49:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-06T14:45:43Z
- **Updated**: 2025-03-11T09:49:47Z
- **Closed**: 2025-03-11T09:49:47Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 8

## Description

**What would you like to be added**:

Allow scheduling workloads without TAS annotations  (`kueue.x-k8s.io/podset-required-topology` or `kueue.x-k8s.io/podset-preferred-topology`) on every PodSet.

The idea is to default the annotations, but we need to decide where is the configuration.

**Why is this needed**:

Currently, users of TAS need to set annotations on every PodTemplate. While this gives control, it also creates friction and room for error, because users may forget to set the annotation. Also, most users want to use the "preferred" mode, and they don't need to control the topology level.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc ([KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling) update)
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T14:45:58Z

cc @mwielgus @mwysokin @tenzen-y

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-01-15T20:55:02Z

Maybe `ResourceFlavor`? Since it's usually related to the machine type and it can benefit only some of the machine types? Maybe the default could be `kubernetes.io/hostname` since it seems to give the best compact placement?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-23T18:44:57Z

> Allow scheduling workloads without TAS annotations (kueue.x-k8s.io/podset-required-topology or kueue.x-k8s.io/podset-preferred-topology) on every PodSet.

This sounds like making TAS a default scheduling policy. 
IIUC, TAS currently tries to pack Pods into the same and high-used nodes as much as possible (mostAllocated).
However, the policy sometimes does not meet inference and other workloads.

What about adding validations? I mean, if Jobs have TAS annotations in `.metadata.annotations`, we reject the Job and return appropriate places where they should put TAS annotations.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T13:06:33Z

One lightweight idea is to make TAS default when all RFs in a given CQ have `topologyName`. Then, for every resource flavor the default is the lowest level - which would be `kubernetes.io/hostname` effectively as proposed in https://github.com/kubernetes-sigs/kueue/issues/3754#issuecomment-2593915902.

The benefit of this approach is that it allows users to migrate CQ-by-CQ to TAS, and does not require setting the annotations by the user.

> This sounds like making TAS a default scheduling policy.

Not really, we would still require a deliberate admin action to configure the ResourceFlavors to have topologyName. Otherwise, default Kueue is used.

> IIUC, TAS currently tries to pack Pods into the same and high-used nodes as much as possible (mostAllocated).
However, the policy sometimes does not meet inference and other workloads.

That is true, but I would prefer to think about this as a separate improvement to TAS. For example, we may introduce another PodSet annotation. We have "required", and "preferred", maybe we also need "spread" or "relax", etc.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T09:32:44Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-06T09:37:21Z

> One lightweight idea is to make TAS default when all RFs in a given CQ have topologyName. Then, for every resource flavor the default is the lowest level - which would be kubernetes.io/hostname effectively as proposed in https://github.com/kubernetes-sigs/kueue/issues/3754#issuecomment-2593915902.
> 
> The benefit of this approach is that it allows users to migrate CQ-by-CQ to TAS, and does not require setting the annotations by the user.

Basically, sgtm.
One question is which enforcement level (required vs preferred) should Kueue automatically insert?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T09:47:42Z

> One question is which enforcement level (required vs preferred) should Kueue automatically insert?

Preferred - this is our go to annotation recommended to users, for most workloads. "required" could make some workloads unschedulable. Still, if some workload is ultra sensitive on networking the user can set the "required" annotation and it will have precedence over the default (preferred).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-06T09:59:20Z

> > One question is which enforcement level (required vs preferred) should Kueue automatically insert?
> 
> Preferred - this is our go to annotation recommended to users, for most workloads. "required" could make some workloads unschedulable. Still, if some workload is ultra sensitive on networking the user can set the "required" annotation and it will have precedence over the default (preferred).

That sounds reasonable.
