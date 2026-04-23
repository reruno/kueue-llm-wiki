# Issue #10: Simple Framework to support different queuing policies

**Summary**: Simple Framework to support different queuing policies

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/10

**Last updated**: 2023-06-02T12:01:45Z

---

## Metadata

- **State**: open
- **Author**: [@denkensk](https://github.com/denkensk)
- **Created**: 2022-02-18T03:31:44Z
- **Updated**: 2023-06-02T12:01:45Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/backlog`, `lifecycle/frozen`, `kind/grand-feature`
- **Assignees**: [@denkensk](https://github.com/denkensk)
- **Comments**: 17

## Description

We need a simple framework to support different policies or algorithms for every phases in `Job scheduling`.

/kind feature
/cc @ahg-g @alculquicondor

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T03:32:02Z

/assign @denkensk

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T14:33:06Z

Can you begin by enumerating the locations where there could be multiple policies in play?

A few I have identified:
- A policy for sorting items in a Queue. Currently it's FIFO on creationTimestamp.
- A policy for re-queuing and backoff.
- A policy for choosing flavors. Currently it goes for the first flavor, even if it borrows from other capacity. Some might prefer to first use flavors without borrowing and then try to borrow starting from the top of the list again.

The next question is how many of those policies require a framework (like kube-scheduler) as opposed to being simple fields in the APIs.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T14:55:44Z

> A few I have identified:
> A policy for sorting items in a Queue. Currently it's FIFO on creationTimestamp.
> A policy for re-queuing and backoff.
> A policy for choosing flavors. Currently it goes for the first flavor, even if it borrows from other capacity. Some might prefer to first use flavors without borrowing and then try to borrow starting from the top of the list again.

In addition to the ones you mentioned above, I think there are a few other locations that need support for extension.
- A policy for sorting between different tenants.
- If we think of determining whether a workload has enough capacity to run as one of the filters, Users will have other strategies to expand as filter like cluster capacity?
- If we think of recycling the resource as `postfilter`， It will be much more policies to have in `which job will be recycled`

> The next question is how many of those policies require a framework (like kube-scheduler) as opposed to being simple fields in the APIs.

It will be sample if we use it as the fields in APIs. But this does not prevent us from providing an extensible framework.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T19:32:15Z

I think it's too early to talk about a framework, but we can keep the discussion open for the future.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T22:34:21Z

We can clean the important-soon firstly. But in any case, we need to be able to allow users to customize their own policies, right? This is really needed!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T14:23:12Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:33:24Z

/lifecycle frozen

### Comment by [@talcoh2x](https://github.com/talcoh2x) — 2023-01-11T07:35:26Z

Hi, I think adding such option to change or control on queue order is very important. we do a lot of thing on scheduler side since we have the option to extend it - queueSort, preFilter, filter, and more .. 
from my perspective kueue "hold" me the quota request and give me the option organize it before execution ( before we send the scheduler)  once i have it i can organize and send the request according to - 

-  "priority", "labels", PodGroup size ...
-  i can create "label  queue " e.g: label_queue: low label_queue: high  so for the same priority i can decide who will start first.

we cant do that today because we have resources quota kueue is the solution :)

also i don't think re-queuing and backoff so important we have the scheduler for that. just postFilter for start i believe will be good it will be user problem to take in care situation like
- quota size and more ...

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T13:30:10Z

I wonder if the requirements you have can be general enough that they could make part of kueue, although at first glance they look very custom.

It might be useful to you to think about how you would configure these sorting criteria. If you are open to share, we can provide feedback and if enough contributors find it useful we can just add it to kueue.

Otherwise, you can start a design that abstracts the different places where you could inject your own logic. I don't think the current contributors have bandwidth to work on this, but you are certainly welcome to do so. I know @denkensk and @kerthcet have been thinking along these lines.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-31T19:43:50Z

@KunWuLuan @trasc maybe we should revisit this in the context of adding more queuing policies

### Comment by [@talcoh2x](https://github.com/talcoh2x) — 2023-06-01T08:29:35Z

@alculquicondor  hi, just want to say we already implement new CRD that do the Queue as we need and support kubeflow and Kubevirt operators.
it done in a way that good for us as this solution is internal. it can be nice to share the requirements so we will be able to work with kueue also at the end

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-01T12:20:34Z

> @KunWuLuan @trasc maybe we should revisit this in the context of adding more queuing policies

I think a framework is good for future work on queuing policies.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T12:24:26Z

@talcoh2x would you be willing to present in a WG Batch meeting?

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-01T12:26:31Z

If we decide to add a framework, maybe we can start with designing some extension points. 
i have summarized a chart about the current Kueue's flowchart which may help, as the following:
![image](https://github.com/kubernetes-sigs/kueue/assets/30817980/f2402396-7ff7-4f6c-82c5-81f18f224f9f)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T20:12:47Z

The biggest recent change is that preemption calculation moved to flavorAssigment. This opens more possibilities for policies.

Perhaps something we can do is make FlavorAssigment an interface where each implementation is a policy. Then we strip down some of the existing code into library functions for building policies.

I don't currently see the possibility for a phased approach like in kube-scheduler Filters. But any ideas like this?

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-02T03:49:30Z

> I don't currently see the possibility for a phased approach like in kube-scheduler Filters. But any ideas like this?

@alculquicondor Maybe we can make queueSort policy as an interface? this can contain multi cluster queue sort and multi local queue sort for a single cluster queue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-02T12:01:45Z

Right, I would see that as a separate extension point. I agree that it could be useful.
