# Issue #5141: MultiKueue dispatcher API

**Summary**: MultiKueue dispatcher API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5141

**Last updated**: 2025-07-25T17:40:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-04-28T21:32:06Z
- **Updated**: 2025-07-25T17:40:28Z
- **Closed**: 2025-07-25T17:40:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 17

## Description

**What would you like to be added**:

An api through which an external controller can tell, per workload, which of the worker clusters (out of all configured for the given ClusterQueue) should be attempted for that specific workload.

**Why is this needed**:

Currently MK tires all clusters configured for a ClusterQueue at the very same time, leading to problems when the number of clusters is large (for example 40). 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T06:03:29Z

> Currently MK tires all clusters configured for a ClusterQueue at the very same time, leading to problems when the number of clusters is large (for example 40).

Does the problem indicate performance or else?

### Comment by [@mwielgus](https://github.com/mwielgus) — 2025-05-27T12:22:17Z

Both performance (distributing and keeping 40 copies of workload in cluster informers can be expensive) and practical (trying all 40 clusters at the very same time can lead to lots of unnecessary preemptions).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-27T12:30:46Z

> Both performance (distributing and keeping 40 copies of workload in cluster informers can be expensive) and practical (trying all 40 clusters at the very same time can lead to lots of unnecessary preemptions).

That makes sense. I can imagine a lot of workload copies cause the delayed informer sync.
For a practical problem, what are the differences between this proposal and https://github.com/kubernetes-sigs/kueue/issues/3757?
#3757 proposes the dispatching mechanism as well.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-27T15:58:50Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-29T06:42:58Z

Yeah, I would probably call one of them a duplicate, I'm to close mine, wdyt @mwielgus ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T06:49:26Z

Actually, when I thought about the proposed KEP https://github.com/kubernetes-sigs/kueue/pull/5410 I realize there is a difference @tenzen-y . 

Both issues mitigate the issue with too many preemptions, and performance, but:
1. in the issue https://github.com/kubernetes-sigs/kueue/issues/3757m the admin only configures strategy as sequential. Kueue could use the order of declaration of the clusters.
2. in this issue the admin needs to provide an external controller for the load-balancing.

I think both are useful, and would prefer keeping them in mind when designing the solution.

Maybe we could extend the MultiKueue AC with MultiKueueConfig, analogous to ProvisioningRequestConfig. Inside we could set 
```yaml
dispatcherMode: default / sequential
sequentialDispatcherTimeout: 5min
sequentialDispatcherName: example.com/mydispatcher
```
- If dispatcherMode: default or empty, then we get current behavior.
- If `dispatcherMode: sequential` then we use built-in sequential dispatching one-by-one. 
- If `sequentialDispatcherName` is set then external dispatcher can be used

For the needs of the dispatcher we probably will need on workload `workload.status.multiKueueNominatedCluster`.

wdyt @tenzen-y @mwielgus @mszadkow ?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-02T10:26:06Z

IIUC

Whatever WorkloadReconciler did so far gets divided in 2 steps.
1. a) Determine where to clone workload from the local.
    b) skip it if it's done by external controller.
2. Clone workload from local to the remote based on the `workload.status.multiKueueNominatedCluster`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T10:28:23Z

> Whatever WorkloadReconciler did so far gets divided in 2 steps.

yes, assuming you mean Multikueue Workload Controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-27T17:37:49Z

> Actually, when I thought about the proposed KEP [#5410](https://github.com/kubernetes-sigs/kueue/pull/5410) I realize there is a difference [@tenzen-y](https://github.com/tenzen-y) .
> 
> Both issues mitigate the issue with too many preemptions, and performance, but:
> 
> 1. in the issue https://github.com/kubernetes-sigs/kueue/issues/3757m the admin only configures strategy as sequential. Kueue could use the order of declaration of the clusters.
> 2. in this issue the admin needs to provide an external controller for the load-balancing.
> 
> I think both are useful, and would prefer keeping them in mind when designing the solution.
> 
> Maybe we could extend the MultiKueue AC with MultiKueueConfig, analogous to ProvisioningRequestConfig. Inside we could set
> 
> dispatcherMode: default / sequential
> sequentialDispatcherTimeout: 5min
> sequentialDispatcherName: example.com/mydispatcher
> * If dispatcherMode: default or empty, then we get current behavior.
> * If `dispatcherMode: sequential` then we use built-in sequential dispatching one-by-one.
> * If `sequentialDispatcherName` is set then external dispatcher can be used
> 
> For the needs of the dispatcher we probably will need on workload `workload.status.multiKueueNominatedCluster`.
> 
> wdyt [@tenzen-y](https://github.com/tenzen-y) [@mwielgus](https://github.com/mwielgus) [@mszadkow](https://github.com/mszadkow) ?

Thank you for describing that. IIUC, this issue aims to provide interface for providing dispatching algorightm, right?
And #3757 will provide the sequential strategy on top of this dispatcher API, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-27T17:40:46Z

Correct. We will introduce the new sequenial strategy with hardcoded params for now, for simplicity, on top of the generic dispatching alogithm. The current strategy will also be selectable as a special case dispatcher.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-27T17:42:37Z

> Correct. We will introduce the new sequenial strategy with hardcoded params for now, for simplicity, on top of the generic dispatching alogithm. The current strategy will also be selectable as a special case dispatcher.

That makes sense. In that case, let us keep both issues.

### Comment by [@pramodbindal](https://github.com/pramodbindal) — 2025-07-09T06:46:11Z

+1
There certain use-cases when we want a workload to be picked by specific cluster only.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T06:52:52Z

@pramodbindal thank you for the input. IIUC with the with this new Workload's nominatedClusterNames you can restrict the set of clusters to only a subset. Does it cover your use-case?

### Comment by [@pramodbindal](https://github.com/pramodbindal) — 2025-07-09T07:08:25Z

@mimowo . Will check this one
I have different challenge right now.

I am not able to admit my workload into multiKueue :-(

Mine is custom workload tekton/PIpelineRun which I want to manage via MultiKueue but did not find any support for External Frameworks in MultiKueue

Am i misssing something

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T07:12:09Z

> Mine is custom workload tekton/PIpelineRun which I want to manage via MultiKueue but did not find any support for External Frameworks in MultiKueue

External frameworks aren't currently supported in MultiKueue :(, we have an issue open about it https://github.com/kubernetes-sigs/kueue/issues/2349.

As a workaround you may try using [AppWrapper](https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/appwrapper/), or [PodGroups](https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/plain_pods/) which are both supported solutions. 

cc @dgrove-oss

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-17T13:06:00Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-17T13:06:06Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5141#issuecomment-3084005625):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
