# Issue #4646: RF nodeTaints do not work well couple with RF tolerations

**Summary**: RF nodeTaints do not work well couple with RF tolerations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4646

**Last updated**: 2025-05-01T06:53:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-17T11:08:45Z
- **Updated**: 2025-05-01T06:53:56Z
- **Closed**: 2025-05-01T06:53:56Z
- **Labels**: `kind/documentation`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
If we specify the same labels to `.spec.nodeTaints` and `.spec.tolerations` in the ResourceFlavor, `nodeTaints` does not work well. As a result, unexpected RF will be assigned to Workload without tolerations.

**What you expected to happen**:
If the Workload does not have `tolerations` corresponding to RF nodeTaints, the RF with nodeTaints is not assigned to the Workload.

https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-taints

**How to reproduce it (as minimally and precisely as possible)**:
We could imagine the following RF. Even if the Workload does not have "spot" tolerations, the flavor-assigner considers that the Workload can be scheduled since the assigner assumes the Worklod can be accommodated by tolerations propagating from RF `.spec.tolerations` to Workload in the following mechanism.

https://github.com/kubernetes-sigs/kueue/blob/0009c097f4720289e88f68540ab1344bba1bd7a8/pkg/scheduler/flavorassigner/flavorassigner.go#L541-L543

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "flavor"
  nodeTaints:
  - effect: NoSchedule
    key: spot
    value: "true"
  tolerations:
  - key: spot
    operator: "Exists"
    effect: "NoSchedule"
```

**Anything else we need to know?**:
I think that the possible fix is just adding validations for RFs so that they can not specify the same taints/tolerations in the same RF.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:09:39Z

> I think that the possible fix is just adding validations for RFs so that they can not specify the same taints/tolerations in the same RF.

@gabesaba @PBundyra @mimowo Do you have alternative better solutions?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:12:59Z

This change came from https://github.com/kubernetes-sigs/kueue/pull/3722 and was shipped to v0.9.2, v0.10.0, and later.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-17T12:07:46Z

I'm not sure where the issue is - I believe it WAI

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-17T12:08:34Z

After all, workloads will inherit tolerations from the RF, so effectively they should be able to schedule on the nodes with corresponding taints

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:14:41Z

> We could imagine the following RF. Even if the Workload does not have "spot" tolerations, the flavor-assigner considers that the Workload can be scheduled since the assigner assumes the Worklod can be accommodated by tolerations propagating from RF .spec.tolerations to Workload in the following mechanism.

Yeah, this is WAI imo as well. The `.spec.tolerations` are added during admission of Workload, so they allow the workload to run inspite of the node taints. Since the workload can run there is no need to artificially block it during scheduling.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T12:16:26Z

> After all, workloads will inherit tolerations from the RF, so effectively they should be able to schedule on the nodes with corresponding taints

They should not specify the same key and values both to `nodeTaints` and `tolerations` since they have conflict.
As we can see in https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-taints, RF `nodeTaints` is not just nodeTaints, that works as flavor taints as well.

I meant the following reproduces the same scheduling result. However, they expect `nodeTaints` works.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "flavor"
  nodeTaints:
  - effect: NoSchedule
    key: spot
    value: "true"
  tolerations:
  - key: spot
    operator: "Exists"
    effect: "NoSchedule"
```

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "flavor"
  tolerations:
  - key: spot
    operator: "Exists"
    effect: "NoSchedule"
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T12:18:46Z

In that case, why do we want to allow them to specify the same key and value both to tolerations and nodeTaints?
Doesn't it just cause confusion since `nodeTaints` does not do anything?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:20:38Z

> In that case, why do we want to allow them to specify the same key and value both to tolerations and nodeTaints?

I expect some users might have controllers which scrape the nodeTaints from the cluster nodes, whereas "tolerations" are added mostly by admins. So since they might be set by different actors the additional validation could prevent the inhouse scraping controllers to fail. 

EDIT: is there something not-working about this configuration, or you think it is just "confusing"?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T12:25:58Z

> I expect some users might have controllers which scrape the nodeTaints from the cluster nodes, whereas "tolerations" are added mostly by admins.

I was not sure what this indicate since `.spec.nodeTaints` is not nodeTains for node. the `.spec.nodeTaints` is flavor taints.
This `.spec.nodeTaints` has never been propagated to workload. 

https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-taints

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T12:30:10Z

>  is there something not-working about this configuration, or you think it is just "confusing"?

For a more concrete case, we have CPU flavor and GPU flavor with nodeTaints and toleratons. A single CQ has both flavors. In that case, workload without tolerations unexpectedly is assigned to GPU workload even though the workload should be scheduled to CPU node.

For sure, they should not create RF with same nodeTaints and tolerations. However, currently, there is no way to know the specifications.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:36:45Z

Looking at the documentation, it says:
```
Kueue adds the tolerations to the underlying Workload Pod templates.

For example, for a [batch/v1.Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/), Kueue adds the tolerations to the .spec.template.spec.tolerations field. This allows that the workloads Pods to be scheduled on nodes having specific taints.
```
So, since Kueue is adding the tolerations from RF it allows the workload to schedule. The documentation isn't conditional about presence of the nodeTaints in the RF. This is why I considered it a bug.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T12:41:36Z

> Looking at the documentation, it says:
> 
> ```
> Kueue adds the tolerations to the underlying Workload Pod templates.
> 
> For example, for a [batch/v1.Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/), Kueue adds the tolerations to the .spec.template.spec.tolerations field. This allows that the workloads Pods to be scheduled on nodes having specific taints.
> ```
> 
> So, since Kueue is adding the tolerations from RF it allows the workload to schedule. The documentation isn't conditional about presence of the nodeTaints in the RF. This is why I considered it a bug.

As we can see, nodeTaints is not propagated to workload. Or do you want to mean another thing?

```
As opposed to the behavior for [ResourceFlavor labels](https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/#resourceflavor-labels), Kueue does not add tolerations for the flavor taints.
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T14:09:13Z

I synced on that with @tenzen-y and it seems the current behavior is ok-ish, but we agree it might be confusing in the corner case of tolerations = nodeTaints. We consider to update the documentation to discuss this case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T14:55:22Z

> I synced on that with [@tenzen-y](https://github.com/tenzen-y) and it seems the current behavior is ok-ish, but we agree it might be confusing in the corner case of tolerations = nodeTaints. We consider to update the documentation to discuss this case.

Yes, I synced with Michal offline what I want to say here. 
Although the problem is each (RF `.spec.tolerations` and `.spec.nodeTaints`) is enough described and reasonable, there are no specifications anywhere if we enable both. 
So, I will describe this behavior in which `.spec.nodeTaints` are ignored during the Kueue scheduling cycle when both `.spec.tolerations` and `.spec.nodeTaints` are enabled.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T14:56:09Z

/remove-kind bug
/kind documentation

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-20T09:44:56Z

/assign
