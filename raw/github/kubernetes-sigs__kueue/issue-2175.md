# Issue #2175: WaitForPodsReady: Store last requeued count and time

**Summary**: WaitForPodsReady: Store last requeued count and time

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2175

**Last updated**: 2025-06-20T16:59:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-09T22:38:01Z
- **Updated**: 2025-06-20T16:59:05Z
- **Closed**: 2025-06-20T16:50:00Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 28

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Depend on #2174 

Since #2063, the workload controller resets the `.status.requeueState.requeueAt` if the `requeueAt` exceeds the current time.
Also, we will reset the `.status.requeueState.count` as well to fix the bug reported in #2174.

So, I would like to propose the dedicated APIs that do not involve scheduling like this:

```yaml
[...]
status:
  lastRequeueState:
    requeueAt: $TIME
    count: 3
[...]
```

**Why is this needed**:
As initially designed, the `requeueState` is responsible for storing the last requeued time and counting and notifying the users as well. 
But, to avoid the race condition, we dropped/will drop the functionality from those APIs (`.status.requeueState`) in the Workload.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T22:38:49Z

cc: @alculquicondor @mimowo

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T13:52:26Z

> Since #2063, the workload controller resets the `.status.requeueState.requeueAt` if the `requeueAt` exceeds the current time.

What about just reverting that?

Would it be enough?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T13:58:08Z

I would be worried about adding more fields that could just cause confusion.

But maybe it isn't too bad.

WDYT @mimowo?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T14:05:41Z

@alculquicondor Sorry for the confusion. Actually, we need to reset the `.status.requeueState.count` field to avoid the race condition. So, could you check #2174 first? Thanks.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-10T14:19:37Z

> I would be worried about adding more fields that could just cause confusion.
> 
> But maybe it isn't too bad.
> 
> WDYT @mimowo?

I think we need to reset the `.status.requeueState.count` field indeed, because currently when an admin re-activates the workload it gets re-evicted immediately. So the admin needs to first clean `.status.requeueState.count` , then activate: `spec.active=true`. This is extra step and room for error.

Now, if we clear `.status.requeueState.count` it will work, but as discussed offline with @tenzen-y the admins may want to know how many retries it took before deactivating. For that, the minimal approach would be to just record the count the in the message for PodsReadyTimeout, say `Exceeded the PodsReady timeout %s` -> `The PodsReady timeout %s was exceeded %v times in a row`. And I would hope this message is enough. WDYT @tenzen-y ?

If the message is not enough, because some automation wants to consume the information about the number of retries, then I think the proposal with `status.lastRequeueState` makes sense. We do something similar for pods with `lastTerminationState` [link](https://github.com/kubernetes/kubernetes/blob/f75d8e97f151943288923cf91b932e64f0fd0f4c/pkg/apis/core/types.go#L2683-L2690).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T15:05:57Z

I like the idea of just updating the condition message. The users just need a quick signal to understand what happened.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:16:55Z

> Now, if we clear .status.requeueState.count it will work, but as discussed offline with @tenzen-y the admins may want to know how many retries it took before deactivating. For that, the minimal approach would be to just record the count the in the message for PodsReadyTimeout, say Exceeded the PodsReady timeout %s -> The PodsReady timeout %s was exceeded %v times in a row. And I would hope this message is enough. WDYT @tenzen-y ?

My motivation is to provide a machine-readable state. So, I would prefer to have `lastRequeueState`.
But, as I mentioned [here](https://github.com/kubernetes-sigs/kueue/issues/2174#issuecomment-2103588835), when we deactivate the Workload, adding Evicted condition instead of modifying the `.spec.active` field allows us to avoid the race condition and avoid to add a new `.status.lastRequeueState` field.

@alculquicondor @mimowo Regarding [this](https://github.com/kubernetes-sigs/kueue/issues/2174#issuecomment-2103588835) idea, WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-10T15:24:45Z

> My motivation is to provide a machine-readable state.

Do you have a concrete use case where this information would be parsed by automation? If not, then it can introduce some form of keeping the information structured (like `lastRequeueState`) when requested by users.

> @alculquicondor @mimowo Regarding https://github.com/kubernetes-sigs/kueue/issues/2174#issuecomment-2103588835 idea, WDYT?

I'm not sure. Wouldn't we clear the `status.requeuingState.count` in that case?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-10T15:27:56Z

Actually, if we need this information structured I would be leaning towards using `lastRequeuingState`, by analogy to [`lastTerminationState` API](https://github.com/kubernetes/kubernetes/blob/f75d8e97f151943288923cf91b932e64f0fd0f4c/pkg/apis/core/types.go#L2683-L2690). Seems cleaner to have dedicated API for this purpose than overload `requeuingState` with two responsibilities: driving the mechanism, and serve for the structured reason of deactivation.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T15:30:07Z

+1 to not reuse, but I still want to know why would automation need to know all of this details? As opposed to just a reason in the Evicted condition.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:40:45Z

> Do you have a concrete use case where this information would be parsed by automation? If not, then it can introduce some form of keeping the information structured (like lastRequeueState) when requested by users.

In the platform engineering context, the admins (SWE/Ops/SRE) often develop and provide common platforms across the company to users (Researcher/DS/ML Engineer). 
In that case, we wouldn't provide permissions to operate Kubernetes to users since the users often don't know Kubernetes, and also we would handle security policy (similarly IAM concept).

So, we often provide in-house CLI, and Concole wrapped to allow users to operate Jobs (Create/List/Delete).
In that internal platform, we would notify users the `requeueState.count` and `requeueState.requeueAt` via in-house API and CLI, and Console.

Therefore, I would like to provide machine-readable API via Workload resources.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T15:43:33Z

In that case, let's go with the dedicated API

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T15:49:54Z

> In that case, let's go with the dedicated API

As you are pointing out [here](https://github.com/kubernetes-sigs/kueue/issues/2174#issuecomment-2104824414), it seems that we can not avoid resetting the `requeueState`...

So, if @alculquicondor and @mimowo are ok, I would like to add a dedicated API (`.status.lastRequeueState`).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-10T16:28:47Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T19:23:34Z

In addition to the `lastRequeueState`, I was wondering if it's worth also adding an Evicted condition right before deactivating the Workload?
That could hold a proper reason.
Otherwise, if we just deactivate, this would create its own Evicted condition with a reason Deactivated

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T16:54:34Z

> In addition to the `lastRequeueState`, I was wondering if it's worth also adding an Evicted condition right before deactivating the Workload? That could hold a proper reason. Otherwise, if we just deactivate, this would create its own Evicted condition with a reason Deactivated

Yeah, I also think it would be worth a dedicated reason.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-15T17:18:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-15T17:21:07Z

/remove-lifecycle stale

I'm still aiming for the next minor version.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-13T17:59:02Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-14T04:07:17Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-12T04:58:07Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T06:13:20Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-13T06:14:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-13T12:09:08Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T16:49:56Z

I think that the original motivation was already resolved by `.status.schedulingStats` https://github.com/kubernetes-sigs/kueue/blob/aae27eadbf053973054c87d7d3ce82850637b0d3/apis/kueue/v1beta1/workload_types.go#L410.

So, I'm closing this one.

/close

cc @mimowo

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-20T16:50:01Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2175#issuecomment-2992246367):

>I think that the original motivation was already resolved by `.status.schedulingStats` https://github.com/kubernetes-sigs/kueue/blob/aae27eadbf053973054c87d7d3ce82850637b0d3/apis/kueue/v1beta1/workload_types.go#L410.
>
>So, I'm closing this one.
>
>/close
>
>cc @mimowo 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T16:55:57Z

sgtm, thanks. 

We don't store the requeueAt yet, but we can add it later when we have a use case

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T16:59:05Z

> sgtm, thanks.
> 
> We don't store the requeueAt yet, but we can add it later when we have a use case

Yes, that's right. I still want to know when is the last time. However, I believe that we need to have another design as opposed to this issue.
I will open another issue in the future once I organize requirement to aligh with new SchedulingStats feature.
