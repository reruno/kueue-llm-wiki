# Issue #1530: Filling up the gap between kueue with scheduler

**Summary**: Filling up the gap between kueue with scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1530

**Last updated**: 2024-01-03T11:56:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-12-29T06:40:53Z
- **Updated**: 2024-01-03T11:56:04Z
- **Closed**: 2024-01-03T03:11:31Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kueue and kube-scheduler are separation of concerns, there's a gap under the hood, like kueue admits, but failed in scheduler, 
which will lead to underutilized resources as job is pending but resources are occupied. Job preemption is something out of this scope.

There's no better way standing out so far but we can mitigate this with **TTL** strategy. The general idea is when Job is **Not Ready** for a duration of time, we'll suspend the job for reclaim. But the tricky thing is how we handle this kind of Jobs, maybe a backoffQ is something we can consider.

Post for ideas.


**Why is this needed**:

As the title describes.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-29T08:20:05Z

@kerthcet What is different between `waitForPodsReady`?
IIUC, `waitForPodsReady` seems to be sufficient for your use cases.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-02T02:33:27Z

The mainly difference is it's non-blocking, but will **reclaim** the Job if pending in starting for a period of time, **waitForPodsReady** is slow. It's also opt-in.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T19:04:03Z

> The mainly difference is it's non-blocking, but will **reclaim** the Job if pending in starting for a period of time, **waitForPodsReady** is slow. It's also opt-in.

@kerthcet Given that the `blockAdmission` is false, kueue wouldn't block the following jobs and could reclaim the resources used in the job that exceeded the timeout.

https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#WaitForPodsReady

@kerthcet Any other difference?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-03T02:38:42Z

Doesn't the timeout only works when `waitForPodsReady` is enabled? Do you mean when `waitForPodsReady` is enabled and `blockAdmission` is disabled, we'll have a non-blocking queue and will reclaim not-ready jobs after timeout? Based on my understanding, that's not implemented, but I'll try.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-03T03:11:27Z

> Do you mean when waitForPodsReady is enabled and blockAdmission is disabled, we'll have a non-blocking queue and will reclaim not-ready jobs after timeout

seems the right path, I'll close this then. Thanks.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-03T03:11:32Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1530#issuecomment-1874797863):

>> Do you mean when waitForPodsReady is enabled and blockAdmission is disabled, we'll have a non-blocking queue and will reclaim not-ready jobs after timeout
>
>seems the right path, I'll close this then. Thanks.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-03T11:56:03Z

> Do you mean when waitForPodsReady is enabled and blockAdmission is disabled, we'll have a non-blocking queue and will reclaim not-ready jobs after timeout

Yes, I meant what you say. The kueue manager will block jobs only when both `waitForPodsReady=true` and `blockAdmission=true`:

https://github.com/kubernetes-sigs/kueue/blob/7bf4e920808eaac7324bee05c636721861a0280c/cmd/kueue/main.go#L365-L367

Also, the kueue manager will reclaim resources from jobs that exceeded the timeout regardless of `blockAdmission`:

https://github.com/kubernetes-sigs/kueue/blob/7bf4e920808eaac7324bee05c636721861a0280c/pkg/controller/core/core.go#L68-L79
