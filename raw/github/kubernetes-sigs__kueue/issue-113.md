# Issue #113: Rethink Kueue.Queue end purpose

**Summary**: Rethink Kueue.Queue end purpose

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/113

**Last updated**: 2022-04-04T10:59:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-03-10T19:30:54Z
- **Updated**: 2022-04-04T10:59:32Z
- **Closed**: 2022-04-04T10:59:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please only use this template for submitting clean up requests -->

After https://github.com/kubernetes-sigs/kueue/issues/87 , there is not much point on having a controller for kueue.queue. 

- PendingWorkloads are now tracked under ClusterQueue
- AddmittedWorkloads are now tracked under ClusterQueue
- Kueue.Queue.Spec is basically a pointer to ClusterQueue

If someone wants to monitor/track a workload, this would have to be done against ClusterQueue, due the heap being there. We should consider removing `pkg/controller/core/queue.controller.go` and `api/v1aplha1/queue_types.go`

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T19:35:47Z

https://github.com/kubernetes-sigs/kueue/pull/80#issuecomment-1055570571

Also discussed in http://bit.ly/kueue-apis :)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T19:36:08Z

I agree with the fact that having kueue.queue at the user lvl can introduce security risks or resource hijacking risks, a user could create 1 queue per job, and skip the line. 

If Heap is at ClusterQueue, let's work on enhancing that model

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T19:39:20Z

Eventually, there will be a heap in each Queue too. And only the workloads that, added up, respect the queue limits will enter the ClusterQueue.

The use case is explained in the comment linked above.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T19:39:50Z

For now, the only use of kueue.Queue is discoverability.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T19:41:06Z

re-Titled to better reflect this conversation

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T13:17:25Z

Queue can have three purposes:
1) Discoverability; tenants will only have list access to their own namespaces only.
2) A source of defaults for workloads (e.g., default priority, default max runtime etc.)
3) A way to define usage limits at "experiment" level

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T13:46:35Z

I have been thinking about this as well, and here are my thoughts:

For 1 ClusterQueue
A user can submit multiple batches (Currently Queues) that are composed by job steps. (currently QueuedWorkloads) 

Example:
A bioInfo user wants to run some genetics analysis on 3 subjects(Dog, Cat, Duck), and each analysis that requires 3 steps, A,B,C that depend on each other. 
The user then creates 3 queuedworkloads

```go
  dog  := queue{queuedworkloadStepA,queuedworkloadStepB, queuedworkloadStepC}
  cat  := queuedworkload{queuedworkloadStepA,queuedworkloadStepB, queuedworkloadStepC}
  duck  := queuedworkload{queuedworkloadStepA,queuedworkloadStepB, queuedworkloadStepC}
```

And queue them to the cluster queue

```go
AddOrUpdateClusterQueue{dog}
AddOrUpdateClusterQueue{cat}
AddOrUpdateClusterQueue{duck}
```

Then the `Jobs` reconcile will grab each Queue head and push it to the ClusterQueue, where it will go to the `Scheduler` reconciler and jump into the APIServer. This gives a sense of queuing independence to every queue, maybe the `dog` queue is applied first, but the `cat` queue has a "smaller" data set and will finish first as example.

The nice thing of looking it like this, is that a `Step` or as is known currently `QueuedWorkload` could be many `batchv1.Job` that need to run in parallel (e.g MPI). Those steps that don't have parallel dependencies could be then set as another QueuedWorkload object inside a Queue.

Right now you can create a Job without creating a QueuedWorkload, the `job` reconciler will generate a generic one for you, what if, a user could create a single QueuedWorkload, and `QueuedWorkload` reconciler will create a generic Queue (a Queue of 1 ) for that single step QueuedWorkload.

This adds a more Batch like feeling to Kueue.

Thoughts?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-16T01:15:54Z

I am not sure I follow your proposal and what exactly is being suggested we change. Is it that a Queue could represent a workflow? do you find the list in https://github.com/kubernetes-sigs/kueue/issues/113#issuecomment-1067977594 not satisfactory in explaining the purpose of Queue?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-16T12:26:48Z

Maybe I was a bit confused, but to my point, is that I would like to add to your list, that queues are a way to define workload steps, kind of job dependency. "Do this, then this" . the list is satisfactory, I was just adding to it.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-16T12:55:28Z

We discussed initially that workflows are not in Kueue scope because there are multiple commonly used frameworks for that (like Argo and NextFlow). 

We could have a Queue configuration to act the way you described (e.g., strictly one workload should run at a time), but I fear this will grow into more complex requirements that turns it into a workflow manager. 

But, if we think of this in the context of better support for existing workflow managers (https://github.com/kubernetes-sigs/kueue/issues/74), then perhaps we can strike that balance between separation of concern and a rich feature set.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-16T13:19:30Z

Sounds good. let's re circle to this topic after 0.0.1

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-18T19:35:05Z

I think my head was into workloads when I commented here. now that I give it an extra thought

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-04T01:24:00Z

can we close this? it seems to me Queue has a well defined scope

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-04-04T10:59:21Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-04T10:59:32Z

@ArangoGutierrez: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/113#issuecomment-1087410741):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
