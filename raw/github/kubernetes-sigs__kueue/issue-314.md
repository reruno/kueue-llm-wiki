# Issue #314: Allow the upscale but block the downscale in clusterQueue

**Summary**: Allow the upscale but block the downscale in clusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/314

**Last updated**: 2022-08-11T20:55:00Z

---

## Metadata

- **State**: open
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-08-08T04:15:43Z
- **Updated**: 2022-08-11T20:55:00Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/backlog`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We should : 

1. Allow the upscale in clusterQueue, like 
- [ ] Add new resources/flavors
- [ ] Scale up the size of flavors

2. Block the downscale in clusterQueue, like 
- [ ] Remove resources, including flavors unless the flavor is not in use.
- [ ] Scale down the size of flavors unless the flavor is not in use.

We can check that in `cq.UsedResources`.

**Why is this needed**:

More scaleable.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-08T14:49:43Z

I don't think we should block downscale, or at least it should be more flexible.

Once we have preemption support, when downscaling, we could start suspending some workloads if the quota is being violated.

Maybe we could look at the current state of the cache and only allow dowscale if the quota wouldn't be violated with the active workloads, as you say. However, we would be limiting the ability of a cluster administrator to quickly scale down resources if there is some sort of emergency.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-09T00:29:23Z

Well, it's just a startup and based on the current implements. Maybe we can delay this until we implement the preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T20:54:58Z

/lifecycle frozen
/priority backlog
