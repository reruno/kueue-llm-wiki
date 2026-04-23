# Issue #308: Validate resources that share the same flavors in a ClusterQueue

**Summary**: Validate resources that share the same flavors in a ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/308

**Last updated**: 2022-08-15T14:54:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-07-29T20:20:32Z
- **Updated**: 2022-08-15T14:54:14Z
- **Closed**: 2022-08-15T14:54:14Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 7

## Description

This is a spinoff from https://github.com/kubernetes-sigs/kueue/issues/167#issuecomment-1180786466, and a pre-requisite for #296

We need to validate that, in a ClusterQueue *two resources either have completely different flavors or they must share all flavors, in the same order*

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-29T20:21:20Z

/kind feature

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-01T11:22:15Z

> in a ClusterQueue two resources either have completely different flavors

Why? This is too strict. I think this is similar to cluster autoscaler, when scaling up, we may have some kinds of nodes as the first choice, but we may still have fallback choices in case of insufficient of the preference ones. They maybe general nodes(compared to high-performance nodes), pay-as-you-go ones or preemptible instances. This kind of nodes can be shared by different node pools. 

In terms of flavors, it's same, we may have some kinds of nodes for general usage which referenced by a special flavor and meets the requirements of different resources.

Some immature ideas, is it possible to add `quota` to resourceFlavor instead of clusterQueue, the resourceFlavor refers to special type of resources, quota can also be part of the resource properties. Currently, resourceFlavor only plays a role as `nodeAffinity`, which can also achieved by other ways like pod's selector. It seems we haven't leverage it totally.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-03T20:08:55Z

I think the idea wasn't clear. With the proposal, this should be possible (removing the quotas just to show the point):

```yaml
  resources:
  - name: "cpu"
    flavors: ["spot", "ondemand"]
  - name: "memory"
    flavors: ["spot", "ondemand"]
  - name: "example.com/gpu"
    flavors: ["a100", "t4", "k80"]
```

In this case, CPU and memory are coupled together. When a workload is assigned to this ClusterQueue, it would be given the same flavor for CPU and memory. The next workload could get a different flavor, but it needs to be the same for CPU and memory as well.

Achieving this coupling would be difficult if we allowed something like this:

```yaml
  - name: "cpu"
    flavors: ["spot", "ondemand"]
  - name: "memory"
    flavors: ["spot", "default"]
```

Note that the limitation is within one ClusterQueue. If there is another ClusterQueue in which CPU and memory don't need to be coupled, they can use different flavors.

> Some immature ideas, is it possible to add quota to resourceFlavor instead of clusterQueue, the resourceFlavor refers to special type of resources, quota can also be part of the resource properties. Currently, resourceFlavor only plays a role as nodeAffinity, which can also achieved by other ways like pod's selector. It seems we haven't leverage it totally.

See the motivation for ResourceFlavor here: https://github.com/kubernetes-sigs/kueue/issues/59

Basically putting the node labels in a separate object prevents multiple ClusterQueues from definining the same flavor but with different labels.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-09T08:03:18Z

Still think we should allow this configurations.
```
  - name: "cpu"
    flavors: ["spot", "on-demand"]
  - name: "memory"
    flavors: ["spot", "default", "on-demand"]
```
This is actually a fallback strategy, common in use.

pseudo-code below:
```
loop:
for podSet in TotalRequests {
    qualifiedFlavors, ok := findFlavorsMeetThePodSetResourceRequirements()
    if !ok {
        return error
    }
    
    for flavor in qualifiedFlavors {
            if meetResourceQuotaRequirements {
                assignFlavors()
                break loop
            } else {
                continue
            }
    }

    if haveCohort {
        for flavor in qualifiedFlavors {
              ok = borrowFlavorSpecifiedResources()
              if ok {
                  assignFlavors()
                      break loop
                  }
               return error
        }
    }
}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-09T13:51:00Z

That particular example doesn't make sense to me: "spot" and "on-demand" are the opposite, and thus they cover all the possibilities. Also, why wouldn't "cpu": ["spot", "default", "on-demand"] not make sense?
In which case you could assign "cpu": "spot", "memory": "default"?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T20:02:12Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T20:55:41Z

/priority important-soon
