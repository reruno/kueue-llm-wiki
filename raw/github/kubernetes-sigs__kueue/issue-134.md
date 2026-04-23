# Issue #134: Add "Frozen" ClusterQueue state

**Summary**: Add "Frozen" ClusterQueue state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/134

**Last updated**: 2022-07-13T19:07:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-19T17:01:39Z
- **Updated**: 2022-07-13T19:07:35Z
- **Closed**: 2022-07-13T19:07:34Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/productionization`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 9

## Description

Introduce a new "OutOfCommision/Frozen" state for ClusterQueue. A ClusterQueue can enter this state in the following cases:
- it is referencing a non-existent ResourceFlavor.
- being deleted while there are still running workloads previously admitted via the ClusterQueue. This will require adding a finalizer to prevent deleting the object until the workloads finish.

ClusterQueues in this state should be taken out of the cohort and no jobs can schedule via them until the referenced flavors are defined.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-14T07:58:41Z

/assign
I'd like to take a look.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-25T07:27:24Z

ToDoList:
- [x] [add status field to clusterQueue](https://github.com/kubernetes-sigs/kueue/pull/230)
- [ ] add finalizer to clusterQueue 
- [ ] [add finalizer to resourceFlavor, when flavors are in use, they should not be deleted directly](https://github.com/kubernetes-sigs/kueue/pull/263)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-24T13:31:35Z

> Firstly, just want to make sure all running workloads including admitted workloads and inadmissible workloads, right? So you means all workloads corresponding to the clusterQueue should finish running before we successfully delete a clusterQueue.

We only need to wait for running workloads to finish. We can do this as follows: 1) change the CQ status to suspended; this will prevent any new workloads from being admitted 2) wait until existing admitted workloads finish.

> To @alculquicondor question: Why did we need to know if a workload was assumed?, I used to decide whether a clusterQueue can be deleted by the number of admitted workloads, if they all finished, then the clusterQueue will be deleted. I have two reasons:
workloads inadmissible may never have change to run, e.g. insufficient resources, if so, clusterQueue will never be deleted successfully until we delete the workload
Considering clusterQueues should be managed by administrators, they may delete the clusterQueue for special reasons, like reallocating the cluster resources, I don't think they would like to wait for all workloads finished running, especially some workloads will never run to completion. 🤔

The admin will have to delete admitted running workloads manually, I don't think we can do that on their behalf.

> When a clusterQueue is stuck in terminating, we should forbid other workloads get admitted any longer. I totally agree with this, I have implemented this in a follow up PR, do you think we should combine them together into one PR?

I think this should be the first PR, or you can merge them together.

> Different with the idea of changing the clusterQueue's status back to Pending, I added a new status named suspended, WDYT?

I think we need one state, I would change pending to suspended and have different reasons based on the why the CQ is in that state.

> A new question, when clusterQueue is in terminating, we will not forbid creating new corresponding workloads like we do today, right? If so, when batch users continuously creating workloads, the clusterQueue will never be deleted.

It will based on the logic I described above, we don't care about workloads that are not yet admitted, once the CQ is actually deleted, they will get their status updated that the CQ doesn't exist and users can make a decision what to do with them.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-24T13:41:09Z

Note that the Assumed state is temporary. A workload is assumed when the scheduler decides that it should fit and then it's Forgotten if the API call fails. So it's completely fine to wait for these workloads to either be admitted and finished or to get removed from the clusterqueue.

In all scenarios, all that should matter is whether the cache's ClusterQueue is empty.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-25T10:55:25Z

The admin is aware of the status of all the workloads, when he wants to delete the clusterQueue, he should be responsible for the results(we will only wait for the admitted workloads to complete). 

Oppositely, if he wants to delete the clusterQueue, but stuck in terminating for several unadmitted workloads pending for special reasons, it doesn't make sense. 

Of course he can delete the unadmitted workloads manually, but if we have hundreds of unadmitted workloads, it's struggle.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-27T02:33:32Z

> The admin is aware of the status of all the workloads, when he wants to delete the clusterQueue, he should be responsible for the results(we will only wait for the admitted workloads to complete).
> Oppositely, if he wants to delete the clusterQueue, but stuck in terminating for several unadmitted workloads pending for special reasons, it doesn't make sense.

What are you proposing? that Kueue deletes running workloads? if so, I don't think we can do that, we should be conservative when handling user workloads, deleting the workloads is super aggressive and may not be what the admin/user wants. 

> Of course he can delete the unadmitted workloads manually, but if we have hundreds of unadmitted workloads, it's struggle.

A tool can be created for that; we plan to have a kubectl plugin for kueue, such a feature can be created there.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-27T03:35:56Z

> We only need to wait for running workloads to finish. We can do this as follows: 1) change the CQ status to suspended; this will prevent any new workloads from being admitted 2) wait until existing admitted workloads finish

My opinion is the same as yours actually.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-13T19:07:25Z

with https://github.com/kubernetes-sigs/kueue/pull/284 merged, I think this one is done. We still need to add the finalizers in the webhook though. Which are now tracked in separate issues.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-07-13T19:07:35Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/134#issuecomment-1183578931):

>with https://github.com/kubernetes-sigs/kueue/pull/284 merged, I think this one is done. We still need to add the finalizers in the webhook though. Which are now tracked in separate issues.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
