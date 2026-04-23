# Issue #5061: single inadmissible workload from quota never gets pending condition with best effort fifo

**Summary**: single inadmissible workload from quota never gets pending condition with best effort fifo

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5061

**Last updated**: 2025-08-20T19:13:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexeldeib](https://github.com/alexeldeib)
- **Created**: 2025-04-22T00:52:20Z
- **Updated**: 2025-08-20T19:13:21Z
- **Closed**: 2025-08-20T19:13:21Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@alexeldeib](https://github.com/alexeldeib)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

While working on the integration test for https://github.com/kubernetes-sigs/kueue/issues/4934 // https://github.com/kubernetes-sigs/kueue/pull/4935 I noticed a curious issue

Workloads never get any conditions set, but are actively being hit by both the scheduler and the reconciler. The culprit seems to be a resource version conflict between scheduler and reconciler such that the scheduler never applies this status update during failed admission of head entries: https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/scheduler/scheduler.go#L659

resulting in e.g.
```
  2025-04-21T17:49:24.03698-04:00	ERROR	scheduler	scheduler/scheduler.go:685	Could not update Workload status	{"schedulingCycle": 5, "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"admission-check-wl2\": the object has been modified; please apply your changes to the latest version and try again"}
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).requeueAndUpdate
  	/Users/alexeldeib/code/kueue/pkg/scheduler/scheduler.go:685
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule
  	/Users/alexeldeib/code/kueue/pkg/scheduler/scheduler.go:302
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1
  	/Users/alexeldeib/code/kueue/pkg/util/wait/backoff.go:43
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
  	/Users/alexeldeib/code/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil
  	/Users/alexeldeib/code/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff
  	/Users/alexeldeib/code/kueue/pkg/util/wait/backoff.go:42
  sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff
  	/Users/alexeldeib/code/kueue/pkg/util/wait/backoff.go:34
```

in this case it seems there is no workload reconcile, but the workload is requeued as inadmissible and never re-scheduled/nominated when it hits https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/queue/cluster_queue.go#L406

OR the update passes, but the workload reconciler triggers a no-op update from pending to pending. see this code path https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/controller/core/workload_controller.go#L704-L705

either case ends up with the workload requeued as inadmissible, and then it may never get requeued. there is no reason a single workload would retrigger scheduling once it is inadmissible, unless other workloads are deleted, or the CQs are updated, etc.

there are two potential fixes which seem to both be required:
- trigger requeue of inadmissible workload immediately on resource version conflict (e.g. `apierrors.IsConflict`) during requeue status update
  - this solves the first case, since without immediate requeue and no additional update from workload controller, it's kaput
- trigger requeue of inadmissible workloads during the pending -> pending reconciler in workload controller as well as the default path (for spurious/uncached events).
  - this handles the case where the status update succeeds, triggers a workload reconcile, but that does not currently retrigger a scheduling loop

**What you expected to happen**:

condition status updates should occur on pending workloads

**How to reproduce it (as minimally and precisely as possible)**:

see https://github.com/kubernetes-sigs/kueue/pull/4935 -- remove the changes mentioned above and run the test added in that PR a few times, it will reproduce both variations.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2025-04-22T00:52:32Z

/assign

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2025-04-22T00:54:11Z

tracking this as a separate issue for viz in case anyone else hits it since it's ultimately different and #4935 has drifted quite a bit from the original 1-line fix for #4934, but it seems like a fix for #4934 may require fixing this issue as well to get the correct status update behavior

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-21T16:46:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-20T17:09:56Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2025-08-20T19:13:16Z

I don’t think we’ve managed to reproduce this since upgrading to 0.12

/close

On Wed, Aug 20, 2025 at 1:10 PM Kubernetes Triage Robot <
***@***.***> wrote:

> *k8s-triage-robot* left a comment (kubernetes-sigs/kueue#5061)
> <https://github.com/kubernetes-sigs/kueue/issues/5061#issuecomment-3207324056>
>
> The Kubernetes project currently lacks enough active contributors to
> adequately respond to all issues.
>
> This bot triages un-triaged issues according to the following rules:
>
>    - After 90d of inactivity, lifecycle/stale is applied
>    - After 30d of inactivity since lifecycle/stale was applied,
>    lifecycle/rotten is applied
>    - After 30d of inactivity since lifecycle/rotten was applied, the
>    issue is closed
>
> You can:
>
>    - Mark this issue as fresh with /remove-lifecycle rotten
>    - Close this issue with /close
>    - Offer to help out with Issue Triage
>    <https://www.kubernetes.dev/docs/guide/issue-triage/>
>
> Please send feedback to sig-contributor-experience at kubernetes/community
> <https://github.com/kubernetes/community>.
>
> /lifecycle rotten
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/kubernetes-sigs/kueue/issues/5061#issuecomment-3207324056>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABT4LWKUCIJMOVCUO6UIHBD3OSTXVAVCNFSM6AAAAAB3SL43D2VHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTEMBXGMZDIMBVGY>
> .
> You are receiving this because you were assigned.Message ID:
> ***@***.***>
>

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-20T19:13:21Z

@alexeldeib: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5061#issuecomment-3207720985):

>I don’t think we’ve managed to reproduce this since upgrading to 0.12
>
>/close
>
>On Wed, Aug 20, 2025 at 1:10 PM Kubernetes Triage Robot <
>***@***.***> wrote:
>
>> *k8s-triage-robot* left a comment (kubernetes-sigs/kueue#5061)
>> <https://github.com/kubernetes-sigs/kueue/issues/5061#issuecomment-3207324056>
>>
>> The Kubernetes project currently lacks enough active contributors to
>> adequately respond to all issues.
>>
>> This bot triages un-triaged issues according to the following rules:
>>
>>    - After 90d of inactivity, lifecycle/stale is applied
>>    - After 30d of inactivity since lifecycle/stale was applied,
>>    lifecycle/rotten is applied
>>    - After 30d of inactivity since lifecycle/rotten was applied, the
>>    issue is closed
>>
>> You can:
>>
>>    - Mark this issue as fresh with /remove-lifecycle rotten
>>    - Close this issue with /close
>>    - Offer to help out with Issue Triage
>>    <https://www.kubernetes.dev/docs/guide/issue-triage/>
>>
>> Please send feedback to sig-contributor-experience at kubernetes/community
>> <https://github.com/kubernetes/community>.
>>
>> /lifecycle rotten
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/kubernetes-sigs/kueue/issues/5061#issuecomment-3207324056>,
>> or unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/ABT4LWKUCIJMOVCUO6UIHBD3OSTXVAVCNFSM6AAAAAB3SL43D2VHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTEMBXGMZDIMBVGY>
>> .
>> You are receiving this because you were assigned.Message ID:
>> ***@***.***>
>>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
