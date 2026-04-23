# Issue #167: Using the same flavors in different resources might lead to unschedulable pods

**Summary**: Using the same flavors in different resources might lead to unschedulable pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/167

**Last updated**: 2022-08-05T17:49:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-30T20:47:41Z
- **Updated**: 2022-08-05T17:49:49Z
- **Closed**: 2022-08-05T17:49:48Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/productionization`
- **Assignees**: [@xiaoxubeii](https://github.com/xiaoxubeii), [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 20

## Description

**What happened**:

When using the same flavors in multiple resources:

```yaml
  requestableResources:
  - name: "cpu"
    flavors:
    - resourceFlavor: x86
      quota:
        guaranteed: 9
    - resourceFlavor: arm
      quota:
        guaranteed: 12
  - name: "memory"
    flavors:
    - resourceFlavor: x86
      quota:
        guaranteed: 36Gi
    - resourceFlavor: arm
      quota:
        guaranteed: 48Gi
```

a workload could get admitted for cpu and memory with different flavors.

**What you expected to happen**:

workloads to get admitted to the same flavor for different resources.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-01T02:12:30Z

This is going to be very tricky to solve. 

I think the best solution is to validate that a label key is used by one resource only.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-01T02:15:33Z

The example in the description doesn't make sense in practice and we should make sure that users can't create such setups.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-01T19:46:33Z

> I think the best solution is to validate that a label key is used by one resource only.

One issue here is if the ResourceFlavor get updated. But I think we need to make ResourceFlavor immutable any way (to ensure that admitted workloads reference the exact same flavor version assumed by the scheduler), and also prevent deleting a ResourceFlavor if there is any ClusterQueue referencing it.

Updating a ResourceFlavor should be done by creating a new object with a different name, then changing the ClusterQueues to reference the new ResourceFlavor, and then the old ResourceFlavor can be deleted. 

The idea is to make it super hard to place the system in a nonsensical state.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-02T14:52:53Z

> I think the best solution is to validate that a label key is used by one resource only.

That's not enough to prevent a flavor to be used for different resources.

A potential solution is to include the resource name in the ResourceFlavor object and validate that ClusterQueues only reference the flavor for the corresponding resource.

> The example in the description doesn't make sense in practice and we should make sure that users can't create such setups.

Why not? Your nodes might have certain cpu/memory ratio for the flavor and you might want to set the limits accordingly.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-02T20:12:53Z

> That's not enough to prevent a flavor to be used for different resources.

Preventing a flavor from being used by different resources doesn't address the issue reported here because different flavors may use the same label and so cause the same conflict. Enforcing a label key to be used by a single resource ensures that it never gets assigned different values because of conflicting assignment across resources.

> Why not? Your nodes might have certain cpu/memory ratio for the flavor and you might want to set the limits accordingly.

That is fair, but to address this case I think it is better to have an explicit API where the user can express that there is a dependency between two resources, and in which case they should have the exact same set of flavors, and so in the scheduler we check on those dependent resources together at the same time.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-02T20:18:52Z

> Enforcing a label key to be used by a single resource ensures that it never gets assigned different values because of conflicting assignment across resources.

How do you plan to implement this? When do you validate? ResourceFlavor creation or ClusterQueue creation?

> That is fair, but to address this case I think it is better to have an explicit API where the user can express that there is a dependency between two resources

I like this. Something like

```yaml
  memory:
    flavorsFrom: cpu
```

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-07T17:18:08Z

> How do you plan to implement this? When do you validate? ResourceFlavor creation or ClusterQueue creation?

If we make ResourceFlavor immutable and disallow deleting it until no CQ references it, then we can validate on CQ creation/update.

### Comment by [@xiaoxubeii](https://github.com/xiaoxubeii) — 2022-06-09T08:28:43Z

Currently, the appropriate flavor should match with CQ labels / node selector / affinity. Different resources can use different flavor, but these selected flavor are in line with the filtering criteria. So is it in line with expectations even if it cannot be scheduled?

> One issue here is if the ResourceFlavor get updated. But I think we need to make ResourceFlavor immutable any way (to ensure that admitted workloads reference the exact same flavor version assumed by the scheduler), and also prevent deleting a ResourceFlavor if there is any ClusterQueue referencing it.

I think we need to determine whether it is referenced or not during ResourceFlavor updates and deletions, and if so, disallow the operation.

### Comment by [@xiaoxubeii](https://github.com/xiaoxubeii) — 2022-06-10T12:56:53Z

I can help with that.
/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-16T13:16:14Z

Can you please hold? I don't think we have agreed in the high level solution for this problem.

### Comment by [@xiaoxubeii](https://github.com/xiaoxubeii) — 2022-06-17T01:32:25Z

> Can you please hold? I don't think we have agreed in the high level solution for this problem.

OK, I will hold the PR until agreement.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-11T18:21:01Z

For this one, perhaps the ultimate solution is to have an explicit API to express dependencies; 

For the time being I think we can validate that a CQ shouldn't have more than one resource using a label key, for this to work we need to:
1) Disallow ResourceFlavor updates if being used by a CQ
2) Validate on CQ create/update that the ResourceFlavors used across resources don't share a label key. This will require looking up the ResourceFlavors the CQ uses on admission, which I think should be fine, CQs are not resources that frequently gets created or updated.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-11T19:33:47Z

> Disallow ResourceFlavor updates if being used by a CQ

I'm worried this might cause usability problems. It might be hard for an administrator to identify which CQs are using a resource, so they can remove them. And then they have to wait for running workloads to finish.

But even if that wasn't a concern, I'm not convinced that validating that a label key is not used across resources is a necessary step to fix the issue reported.

> For this one, perhaps the ultimate solution is to have an explicit API to express dependencies;

Probably, but how does that look like? I'm not sure my suggestion above is enough

```yaml
memory:
  flavorsFrom: cpu
```

because we still need to specify the quota for each flavor.

I think what we need to express is that certain resources have the same flavors and they must be verified together. What if this is just enforced through validation? *Two resources can either have completely different flavors or they must share all flavors*. And we can just look at flavor names for this.

Then, when the scheduler identifies that some resources are grouped due to having the same resource flavors, it iterates flavors->resources to verify if a workload fits, instead of the current resources->flavors.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-11T20:06:05Z

I don't think there are usability concerns; with an API like kueue where we have multiple CRDs with dependencies, I would lean towards being more strict to avoid placing the system in a non-sense state.

>  Two resources can either have completely different flavors or they must share all flavors. And we can just look at flavor names for this.

I am ok with an implicit API, perhaps order should also be verified to be the same as well just so it is easier to do the flavors->resources iteration.

If you think that the scheduling loop can be reversed, then we can proceed with this solution.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-12T12:30:57Z

Although checking only the flavor names isn't enough because one could create flavors of different names but use the same label key...

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:25:43Z

> Although checking only the flavor names isn't enough because one could create flavors of different names but use the same label key...

I'm willing to accept that as a user error that we can document. This is on the hands of the administrator, who should be a power users.

> I am ok with an implicit API, perhaps order should also be verified to be the same as well just so it is easier to do the flavors->resources iteration.
>
> If you think that the scheduling loop can be reversed, then we can proceed with this solution.

I will tinker with the code for a bit.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-12T14:32:51Z

> I'm willing to accept that as a user error that we can document. This is on the hands of the administrator, who should be a power users.

We do have enough context and information to prevent it, and I don't think there is a use case where we would want to allow it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:37:37Z

We do... but it requires a lot of dealing with finalizers, which might be risky. If anything, I would leave it as a follow up.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-12T14:44:53Z

Leaving it as a followup is fine, it may not require more work with finalizers than what we do now if we make flavors immutable (then the question is whether this is too restrictive); in any case, we can proceed without it for now.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T20:44:39Z

/assign
For now
