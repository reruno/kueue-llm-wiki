# Issue #6514: Provide configuration for the Node Hot Swap feature

**Summary**: Provide configuration for the Node Hot Swap feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6514

**Last updated**: 2025-12-16T14:32:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-11T07:24:30Z
- **Updated**: 2025-12-16T14:32:55Z
- **Closed**: 2025-12-16T14:32:53Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 9

## Description

**What would you like to be added**:

Currently TASReplaceNodeOnPodTermination is used to switch between two heuristics for evicting workloads on failed nodes: https://github.com/kubernetes-sigs/kueue/blob/6377f6539f023ed861b5e156d1be5f8cbe7ef527/keps/2724-topology-aware-scheduling/README.md?plain=1#L952-L956

I can see two paths forward:
1. combine the heuristics into one: 30s OR terminating Pods
2. introduce configuration in the API to switch between heuristics
3. drop one of the heuristics

I'm leaning towards (1.) as simplest. I think (2.) might be tricky for users to fully understand which heuristic they should use. I think both heuristics seem useful so I'm hesitant about (3.).

**Why is this needed**:

To unblock graduation of TASReplaceNodeOnPodTermination

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T07:24:41Z

cc @pajakd @PBundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-11T09:54:15Z

cc @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-01T12:43:10Z

Can there be cases where we have a _transient_ node failure (NotReady), which results in the pods crashing/failing? If these exist, then I'm hesitant about combining the heuristics (option 1), as we may do some false positive evictions, when some users may want the more conservative option (simply waiting a certain amount of time).

OTOH, if this failure controller is always going to be guarded by either configuration or a flag, I am more open to more aggressive evictions/false-positives.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-01T14:04:26Z

>  if this failure controller is always going to be guarded by either configuration or a flag

feature gate flags are never to guard something "always", they are transient by definition. Thus we need to figure out how the API will look in the long run.

> Can there be cases where we have a transient node failure (NotReady), which results in the pods crashing/failing?

It can happen, both approaches are just heuristics and workloads can recover despite some pods terminating. For example, IIUC torchft has capability of recovering despite some pods (replicas) failing transiently.

Certainly (2.) is an option, eg. we could have a configuration map enum like `tas.evictionTrigger` with values `Timeout`, `TerminatingPods`, or `TimoutOrTerminatingPods`. I was proposing (1.) just hoping for smaller API surface to maintain. I would assume that for most users `TimoutOrTerminatingPods` is what they actually need (not implemented currently).

EDIT: if we foresee some users may want to use just `Timeout` or just `TerminatingPods` , then I'm ok with the new configuration enum. It will not add too much complexity I think as this will translate to just simple "if" enabling some checks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-01T17:25:28Z

> > if this failure controller is always going to be guarded by either configuration or a flag
> 
> feature gate flags are never to guard something "always", they are transient by definition. Thus we need to figure out how the API will look in the long run.
> 
> > Can there be cases where we have a transient node failure (NotReady), which results in the pods crashing/failing?
> 
> It can happen, both approaches are just heuristics and workloads can recover despite some pods terminating. For example, IIUC torchft has capability of recovering despite some pods (replicas) failing transiently.
> 
> Certainly (2.) is an option, eg. we could have a configuration map enum like `tas.evictionTrigger` with values `Timeout`, `TerminatingPods`, or `TimoutOrTerminatingPods`. I was proposing (1.) just hoping for smaller API surface to maintain. I would assume that for most users `TimoutOrTerminatingPods` is what they actually need (not implemented currently).
> 
> EDIT: if we foresee some users may want to use just `Timeout` or just `TerminatingPods` , then I'm ok with the new configuration enum. It will not add too much complexity I think as this will translate to just simple "if" enabling some checks.

The horovod and torchrun surely support resiliency. But, that depends on training code implementations. Additionally, the basic MPI implementations do not support resiliency which is still leveraged in various field today.

So, I think that whether or not the distributed Training Job supports resiliency deeply depends on the Application, which means that it is not the same within a cluster. Hence, I'm wondering if we can provide any knob as an annotation and global config.

The annotation declares enabling TASFailedNodeReplacement, the global config declares the TASFailedNodeReplacement mode as Michal proposed in the above:

> Certainly (2.) is an option, eg. we could have a configuration map enum like tas.evictionTrigger with values Timeout, TerminatingPods, or TimoutOrTerminatingPods. I was proposing (1.) just hoping for smaller API surface to maintain. I would assume that for most users TimoutOrTerminatingPods is what they actually need (not implemented currently).
> 
> EDIT: if we foresee some users may want to use just Timeout or just TerminatingPods , then I'm ok with the new configuration enum. It will not add too much complexity I think as this will translate to just simple "if" enabling some checks.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:24:50Z

Let me rename to use this issue the more generic goal of defining the configuration for the Node Hot Swap

/retitle Provide configuration for the Node Hot Swap feature

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-16T14:29:05Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T14:32:48Z

/close
does not seem needed currently, let's close to avoid distractions. We can reopen it when some users need it

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-16T14:32:55Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6514#issuecomment-3660861699):

>/close
>does not seem needed currently, let's close to avoid distractions. We can reopen it when some users need it


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
