# Issue #267: Add `AssumedWorkloads` to cache.ClusterQueue

**Summary**: Add `AssumedWorkloads` to cache.ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/267

**Last updated**: 2022-06-27T03:30:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-19T16:07:49Z
- **Updated**: 2022-06-27T03:30:21Z
- **Closed**: 2022-06-15T13:15:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently `cache.assumedWorkloads` contains the whole admitted workloads, however, we can't easily tell whether a clusterQueue holds admitted workloads or not from this struct. This is useful in reconciling for clusterQueue holding admitted workloads should not be deleted directly. https://github.com/kubernetes-sigs/kueue/issues/134#issuecomment-1108177974

So I'd like to add a new field `AssumeWorkloads` to `ClusterQueue`:
```
type ClusterQueue struct {
	Name                 string
	Cohort               *Cohort
	RequestableResources map[corev1.ResourceName][]FlavorLimits
	UsedResources        Resources
	Workloads            map[string]*workload.Info
	AssumedWorkloads     sets.String
	NamespaceSelector    labels.Selector
	// The set of key labels from all flavors of a resource.
	// Those keys define the affinity terms of a workload
	// that can be matched against the flavors.
	LabelKeys map[corev1.ResourceName]sets.String
	Status    ClusterQueueStatus
}
```

When we assume a workload, we'll insert the workload name to `AssumedWorkloads`, when we delete/forget workload, we'll remove it.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-19T16:07:57Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-21T15:57:37Z

Why did we need to know if a workload was assumed?
Wasn't it enough to know that the CQ was not empty to hold the deletion?

cc @ahg-g who reviewed the PR

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-21T16:31:24Z

We hold the deletion until the admitted workloads finished, for unadmitted workloads, they may  never have change to run e.g. insufficient resources, if so, clusterQueue will stuck in terminating. But the problem left here is these workloads are isolated, but we can collect them again if we create a same name clusterQueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-21T16:51:48Z

Not sure my question is answered.

IIUC, you are saying that when an assumed workload gets forgotten, it doesn't change the status of the workload, then we wouldn't reconcile the clusterQueue again to remove the finalizer.

How does the PR for this issue solved that?

I think we can use a generic event for when a workload is forgotten to reconcile the clusterqueue

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-21T18:42:23Z

I am not following the reasoning as well, but the highlevel semantics we are looking for is described in https://github.com/kubernetes-sigs/kueue/pull/284/files#r902946904

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-22T03:46:51Z

> What we need to do is the following: delay the removal of the finalizer until all running workloads are finished, not wait for assumed workloads to be bound. During this time, no new workloads should be admitted, but we should continue to update CQ status (the counters etc.); and so we need to continue to have the CQ in the cache, but in Pending state (may be we need to change the name to suspended).

Let me explain this more clearly:
1. Firstly, just want to make sure `all running workloads` including admitted workloads and inadmissible workloads, right? So you means all workloads corresponding to the clusterQueue should finish running before we successfully delete a clusterQueue.
2. To @alculquicondor question: `Why did we need to know if a workload was assumed?`, I used to decide whether a clusterQueue can be deleted by the number of admitted workloads, if they all finished, then the clusterQueue will be deleted. I have two reasons: 
    1) workloads inadmissible may never have change to run, e.g. insufficient resources, if so, clusterQueue will never be deleted successfully until we delete the workload
    2) Considering clusterQueues should be managed by administrators, they may delete the clusterQueue for special reasons, like reallocating the cluster resources, I don't think they would like to wait for all workloads finished running, especially some workloads will never run to completion. 🤔 
3. When a clusterQueue is stuck in terminating, we should forbid other workloads get admitted any longer. I totally agree with this, I have implemented this in a follow up PR, do you think we should combine them together into one PR?
4. Different with the idea of changing the clusterQueue's status back to Pending, I added a new status named `suspended`, WDYT?
5. A new question, when clusterQueue is in terminating, we will not forbid creating new corresponding workloads like we do today, right?  If so, when batch users continuously creating workloads, the clusterQueue will never be deleted.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-24T13:25:16Z

lets have this discussion on the issue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-27T03:30:20Z

Revert the commit https://github.com/kubernetes-sigs/kueue/pull/286 after talking with ahg-g
