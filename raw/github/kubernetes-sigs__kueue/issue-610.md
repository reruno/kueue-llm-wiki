# Issue #610: WaitForPodsReady: a mode where jobs don't block the queue head

**Summary**: WaitForPodsReady: a mode where jobs don't block the queue head

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/610

**Last updated**: 2023-05-16T19:01:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-03-06T20:48:55Z
- **Updated**: 2023-05-16T19:01:39Z
- **Closed**: 2023-05-16T19:01:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A mode of operation for WaitForPodsReady where jobs don't block the head of the queue, but still get suspended if they aren't ready after a while.


**Why is this needed**:
Blocking the queue until a Job is ready guarantees all-or-nothing scheduling, but it is slow at scale. Consider the case where a large number of jobs are awaiting to be scheduled and suddenly lots of resources become available (e.g., a large job finishes, releasing significant amount of resources).


**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T18:52:20Z

We probably would start optimistically admitting every workload and then setting some kind of backoff when resources are unavailable.

Should the backoff be per flavor?

Note: not expecting an answer... just dumping my current open questions :)

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-18T07:28:55Z

Hi, I think we can do two more things to help solve the problem:
1. continue admitting more workloads until there is no more resources in cohort
2. requeue the current workload if it wait too long for pods ready

How do you think? @alculquicondor @ahg-g

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-18T07:37:03Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-04-19T14:26:48Z

Hi @KunWuLuan,

> 2\. requeue the current workload if it wait too long for pods ready

is done in #599 / #689 .

I think, what we need to, is to investigate the effect of dropping the `s.cache.WaitForPodsReady(ctx) ` in 
https://github.com/kubernetes-sigs/kueue/blob/9ca57c86cf06c11a94a2d5b7badf60233a51a2f2/pkg/scheduler/scheduler.go#L179-L189 

and continue from there.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-20T01:45:57Z

Hi, @trasc  I think you are right. 💯 

Moreover, maybe we can add a switch to let user choose whether to block the admission while still waiting for pods ready.
If false, we just skip all these checking in 
https://github.com/kubernetes-sigs/kueue/blob/9ca57c86cf06c11a94a2d5b7badf60233a51a2f2/pkg/scheduler/scheduler.go#L178-L189
. Then the other jobs can continue being admitted until resources are exhausted. WDYT?

@alculquicondor If you have time, you can also participate in the discussion, which will be of great help. Thank you very much. 😆 👍

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-20T14:48:00Z

@KunWuLuan thanks for your feedback. I'm currently with limited availability as I'm attending kubecon. I'll get back to this thread next week.
If you have some time, feel free to review the open PRs listed above.

But in general, this feature should be optional.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-16T19:01:34Z

/close
Fixed in #708

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-16T19:01:39Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/610#issuecomment-1550203715):

>/close
>Fixed in #708


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
