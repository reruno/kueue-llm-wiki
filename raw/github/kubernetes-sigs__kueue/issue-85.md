# Issue #85: Rename Capacity to ClusterQueue

**Summary**: Rename Capacity to ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/85

**Last updated**: 2022-03-07T18:26:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-02T14:58:36Z
- **Updated**: 2022-03-07T18:26:55Z
- **Closed**: 2022-03-07T18:26:55Z
- **Labels**: `priority/important-soon`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 21

## Description

Capacity not only defines usage limits for a set of tenants, but it is the level at which ordering will be done for workloads submitted to queues sharing a capacity.

Renaming Capacity to ClusterQueue could provide clarify, with Queue being the namespaced equivalent serving two purposes:

1. discoverability: tenants can simply list the queues that exist in their namespace to find which ones they can submit their workloads to, so it is simply a pointer to the cluster-scoped ClusterQueue.
2. address the use case where a tenant is running an experiment and want to define usage limits for that experiment; in this use case an experiment is modeled as a queue; which means tenants should be able to create/delete queues as they see fit.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-02T15:07:39Z

1. Are we thinking of creating a default Queue after the ClusterQueue created?  It may be difficult because we don't know the namespace, maybe in default?  But this will make it easier for users to use

2. We need a more precise and detailed description so that users can distinguish between Queue and ClusterQueue when they first try to use Kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T16:24:43Z

1. I don't think we should
2. For the most part, end users should only care about Queue. But yes, we need to make it clear in the documentation for admins to understand the difference.

+1 on renaming.

FYI @ArangoGutierrez for extra input.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T16:47:58Z

In HPC/Academia this is known as "Partitions" (see: https://slurm.schedmd.com/scontrol.html#lbAN) 

+1 renaming, just not to `ClusterQueue`

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T16:51:18Z

But Partition is just limited to Slurm, I wouldn't say it is a common term.

What is the concern with ClusterQueue? we still want to align with k8s nomenclature

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T17:32:17Z

I am thinking that this will look similar to RBAC role/ClusterRole implementation, and by doing so, I like the idea.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T17:42:07Z

yeah, we also have ResourceQuota and ClusterResourceQuota (from openshift)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T17:44:29Z

but that got me thinking, should they look similar? or at least share some fields in the API, similar to role/ClusterRole and the likes

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T17:55:29Z

Right now capacity and queue have a master-worker relation
- E.g like a ServiceAccount get's assigned to a Role via a RoleBinding

But planning the name be `ClusterQueue` , is based on the ClusterScoped/Namespaced point of view, so we should address that as well. 

- E.g you can not assign a Role to a ClusterRole

So moving to `ClusterQueue` name, to honor k8s naming conventions, should also consider the above

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:06:15Z

Did you mean to say that QueuedWorkloads should only point to Queues, and not ClusterQueues? If so, I agree.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:07:54Z

> but that got me thinking, should they look similar?

I think they will look more similar when we implement Queue limits and budgets. However, maybe we wouldn't have all the flavor options, just total resources.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T18:08:23Z

not to derail the conversation but, `QueuedWorkloads` could be just `Workloads` that you assign to a Q (TODO conversation)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T18:22:11Z

We discussed this before and are planning to change it; I didn't do it yet because Workload is quite an overloaded term. QW is still easy to understand what we are referring to and replace in the code once we decide on a proper name. Any suggestions?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:27:38Z

If we rename to `ClusterQueue`, does it still make sense for a QW to be "assigned to a ClusterQueue"? Maybe the `QueuedWorkloadSpec` field could be renamed to `AssignedByClusterQueue`?

It makes a lot of sense for the field to just be a boolean to signal whether the QW is "assigned", but we need to store the name of the ClusterQ in case the Queue is deleted.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:35:10Z

Here is my proposal:
1. Rename `Capacity` to `ClusterQueue`
2. Introduce a field `assignment` in `QueuedWorkload`

```go
type QueuedWorkloadSpec struct {
  assignment *Assignment
}

type Assignment struct {
  ClusterQueue string
  PodFlavors []PodFlavor
}

type PodFlavor struct {
  Name string  // same names as spec.Pods
  ResourceFlavors map[corev1.ResourceName]string
}
```

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T18:42:08Z

sounds good to me, I like the grouping of assignment into one place.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T18:56:49Z

if a queue is to a namespace, what a job is to a QW, why do we want to store the CQ in the WQ? 
I think we should be OK, with assuming that if a Q is deleted, it's WQ will be gone as well, no? as how jobs in a NS get deleted when the NS is deleted

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:57:45Z

/assign
People can still comment while I'm on it, but I think I rather address this and #87 as part of the same effort.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:59:39Z

> I think we should be OK, with assuming that if a Q is deleted, it's WQ will be gone as well, no? as how jobs in a NS get deleted when the NS is deleted

Yes, I think they should be "gone" (more accurately, they are not considered in scheduling). But "assigned" workloads should continue running and being accounted for the CQ.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T19:04:48Z

oh running ones, sure, agree 
+1

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T21:01:05Z

actually, should we rename `assignment`/`assigned` by `admission`/`admitted`?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T21:07:45Z

I have no complains about it
