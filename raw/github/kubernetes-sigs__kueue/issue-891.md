# Issue #891: Add nodeSelectors when ClusterQueue has quota for Pods

**Summary**: Add nodeSelectors when ClusterQueue has quota for Pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/891

**Last updated**: 2023-06-26T15:28:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-22T19:26:25Z
- **Updated**: 2023-06-26T15:28:32Z
- **Closed**: 2023-06-26T15:28:31Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 8

## Description

**What would you like to be added**:

If a ClusterQueue defines quota for pods, and the ResourceFlavor has nodeLabels, the nodeSelectors should be applied to the Job.

**Why is this needed**:

It is already surprising that we don't add nodeSelectors if a Job doesn't define requests. But this is semantically correct, because flavors are ssociated to specific resources.

But if the ClusterQueue is managing quota for pods explicitly, then we should apply the nodeSelectors because the Pod itself is a resource.

**Completion requirements**:

Add an integration test for this.

And documentation.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T19:26:37Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-06-23T10:16:29Z

#895 adds some tests (e2e and integration) to check this, it works as expected.

The bigger problem in my opinion is 
> It is already surprising that we don't add nodeSelectors if a Job doesn't define requests. But this is semantically correct, because flavors are ssociated to specific resources.

case in which, for me is more logical to have  kueue admit the workload in the first available flavor and propagate the node selectors instead of letting the job "run wild" in the cluster.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-23T12:44:39Z

Yes, but flavors are associated to resource requests. We don't have any flavors to assign if the Job doesn't require any requests.

Hence why we added support for pod quota.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-23T14:34:19Z

Having two actors `A` and `B` sharing the same cluster and having `cqA` and `cqB` which are using resource flavors `rfA` and `rfB`, which will identify two different sets of nodes `nodesA` and `nodesB`. When a workload associated `A` is admitted it should go to one of the nodes in `nodesA` , regardless of the declared resource usage since the actual (runtime) usage will never be 0.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-23T14:35:07Z

But where should we deduce the flavors from?

### Comment by [@trasc](https://github.com/trasc) — 2023-06-23T14:35:49Z

Just get the first one  (for start).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-23T14:38:47Z

I'm not a fan of such an implicit behavior. Users should be setting pod quota if they really don't care about requests.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-26T08:36:30Z

The problem in this scenario is the the lack of configuration by `A` can have runtime side effects for `B`.
