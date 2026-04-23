# Issue #6891: Increase maximum flavors of a resource group

**Summary**: Increase maximum flavors of a resource group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6891

**Last updated**: 2025-09-22T14:38:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@LarsSven](https://github.com/LarsSven)
- **Created**: 2025-09-17T14:18:10Z
- **Updated**: 2025-09-22T14:38:18Z
- **Closed**: 2025-09-22T14:38:18Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We have a setup where we have relatively little queues, a single resource group per queue, and then quite a lot of flavors within that resource group. However, we noticed that there is a limitation of a maximum of 16 flavors per resource group. Is there a technical reason that users should not have more than 16 flavors per resource group?

**Why is this needed**:
We have a bit of an odd setup. We essentially use Kueue as an internal scheduler within our system. We have a clusterqueue per type of runtime (since we support multiple runtimes that behave differently, and the user explicitly chooses one), and then use the flavors to horizontally scale the runtimes. So if we deploy 20 VMs for a specific runtime and want to schedule on it, we deploy a single ClusterQueue that has a single resource group that has 20 flavors, which exceeds the limit.

**Completion requirements**:
The CRD validation for flavors is raised from a max of 16.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:41:05Z

Yes, +1, I opened the similar issue: https://github.com/kubernetes-sigs/kueue/issues/6007

Would it work for you? It hasn't been contested so if you like to submit a PR I think we can move forward.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:43:31Z

> However, we noticed that there is a limitation of a maximum of 16 flavors per resource group. Is there a technical reason that users should not have more than 16 flavors per resource group?

That was a precaution to make sure scheduling is fast. However, I think we can leave it to the user to decide on the performance impact they are willing to take.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-09-17T14:48:51Z

So essentially enforce that the limit is 256 flavors per clusterqueue, rather than 16 flavors per resourcegroup and 16 resourcegroups per clusterqueue?

That would work a lot better for us yeah. We have very few resourcegroups, so if the performance conerns are about the number of flavors in the clusterqueue, then this would work a lot better for us.

So yes I would like that approach, and we will ourselves make sure the performance is good enough.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:51:07Z

> So essentially enforce that the limit is 256 flavors per clusterqueue, rather than 16 flavors per resourcegroup?

Yes, instead of limiting 16 flavors per CQ, and 16 resources per flavor, we limit 256 resources per CQ. 

This will still put the constraint on the complexity of the algo which essentially depends on the number of resources.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-09-17T14:51:28Z

That makes a lot of sense, this would solve our issue 👍

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:52:33Z

We may still for sanity keep some limits of flavors per CQ, and resources per flavor, would 64 work for you?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:52:48Z

Also Lars, would you be willing to submit the PR?

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-09-17T14:54:12Z

Sure, I can have a look at it sometime in the coming week

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-09-17T14:56:07Z

For our specific usecase we'd prefer just the plain 256 for everything since we only have a single resourcegroup, but I don't think we'd hit the 64 runtimes per runtime type, so should be fine if you would like to keep that.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:57:34Z

FYI we are planning to release 0.14 next week: https://github.com/kubernetes-sigs/kueue/issues/6756

This wasn't in the original plan, but it sounds easy so I would be willing to accept it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:58:39Z

> For our specific usecase we'd prefer just the plain 256 for everything since we only have a single resourcegroup, but I don't think we'd hit the 64 runtimes per runtime type, so should be fine if you would like to keep that.

Let's keep at 64 as originally proposed in the sibling issue then

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T14:13:07Z

Sorry, Let me take a step back, summarize and find a set of limits which satisfy the requirements:

Let's see currently the total numbers:
1. Groups: 16
2. Flavors per Group: 16
3. Resources per Flavor: 16
4. Total number of Resources per Group: 16
5. Total number of Resources: 256 (16 [number of Groups]*16[Resources per Group])
6. Total number of Flavors: 256: (16 [number of Groups]*16[Flavors per Group])

Now:
- #6891 suggests to relax (2.) Flavors per Group 16 -> 64
- #6007 suggests to relax (4.) Total number of Resources per Group: 16 -> 64

So we can have:
1. Groups: 16
2. Flavors per Group: 64 [change in MaxItems for FlavorQuotas]
3. Resources per Flavor: 16
4. Total number of Resources per Group: 64 [change in MaxItems for CoveredResources]
5. Total number of Resources: 256 [we add the webhook code to verify]
6. Total number of Flavors: 256 [we add the webhook code to verify]

Sorry for late summary, hopefully this makes sense. 

I still want to keep the constraints on the total number of flavors, and resources (5.) and (6.) at the same level.

@LarsSven @gbenhaim

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-09-18T14:17:52Z

@mimowo  Just to confirm, the total number of resources are refering to the total number of unique resource types in a clusterQueue right? So it doesn't mean like:
1. You have 4 resource groups
2. You have 16 flavors
3. You have 4 resource quotas per flavor (e.g. CPU, GPU, memory and disk)

Now you're at 4 * 16 * 4 = 256 resource quotas. In this case it is just referring to the 4 for the 4 types of resources right (or maybe 4 * 4 since you need to redefine it per resource group).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T14:24:10Z

Actually, I didn't mean "unique", just total. Ok let me explain, the issue is that the unit of quota allocation in the pair `(Flavor, Resource)`. So it matters how many such unique pairs we have for the complexity of the algorithms, represented by this struct: https://github.com/kubernetes-sigs/kueue/blob/92b794c0a08ab3dcdf77cacb790173184347f69f/pkg/resources/resource.go#L28-L31

So, maybe instead of separate (5.) and (6.) I'm looking for the number of unique (Flavor, Resources) pairs. 

I'm wondering how to capture that without complicating too much to users. Suggestions are welcome.
