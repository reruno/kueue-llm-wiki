# Issue #1657: Report the position of a Workload in a queue via the visibility API

**Summary**: Report the position of a Workload in a queue via the visibility API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1657

**Last updated**: 2025-04-25T03:57:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-26T17:53:34Z
- **Updated**: 2025-04-25T03:57:20Z
- **Closed**: 2025-04-25T03:57:18Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@alaypatel07](https://github.com/alaypatel07)
- **Comments**: 24

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Provide a visibility endpoint that returns the position of a workload in a LocalQueue or ClusterQueue.

This is a continuation of https://github.com/kubernetes-sigs/kueue/issues/168

**Why is this needed**:

To improve visibility to end users so they can estimate how long they will have to wait for their workloads to run

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-25T18:15:45Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T18:23:46Z

/remove-lifecycle stale

### Comment by [@highpon](https://github.com/highpon) — 2024-07-03T15:09:59Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T15:15:21Z

Note that this issue requires a design (in the keps/ folder) prior to implementation.

### Comment by [@highpon](https://github.com/highpon) — 2024-07-03T17:07:10Z

@alculquicondor 
Thanks for letting me know!
I have no experience writing KEP ... I would be glad to know if you have any resources to help me!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T18:26:33Z

The best starting point would be to read the existing KEP for the visibility API.
https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-2-pending-workloads-visibility

### Comment by [@highpon](https://github.com/highpon) — 2024-07-06T05:20:08Z

@alculquicondor 
I have a question.
Is what you want to accomplish with this issue to estimate the number of minutes until the pending workload is executed?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-08T16:23:34Z

> @alculquicondor I have a question. Is what you want to accomplish with this issue to estimate the number of minutes until the pending workload is executed?

From my understanding, the answer is no. I would like to assume the goal of this enhancement is to provide the ability to specify workload name query parameters something like `/apis/visibility.kueue.x-k8s.io/v1alpha1/namespaces/default/localqueues/user-queue/pendingworkloads?workload=myworkload`.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T19:36:50Z

yeah, we only want to know what is the current position of the workload in the queue.
We don't have the means to estimate the wait time at the moment (Kueue doesn't have long term memory).

However, this feature is a step towards that.

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-08-26T21:14:59Z

If this has not been worked on, I can help with making this feature possible. @alculquicondor @tenzen-y

### Comment by [@highpon](https://github.com/highpon) — 2024-08-27T00:23:37Z

@alaypatel07 
I have been too busy with work lately to work on this issue.
If you are able to get to it, I would be very grateful for your help in resolving this issue!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-27T01:41:50Z

@alaypatel07 If you want to work on this issue, feel free to assign yourself with `/assign`.

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-08-27T01:43:43Z

yes I can help with this issue, thanks folks.

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-27T01:50:13Z

/unassign @highpon

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-08-27T02:34:51Z

@tenzen-y @alculquicondor I have been playing around the visibility API and I can create the kep for implementing
```
/apis/visibility.kueue.x-k8s.io/v1alpha1/namespaces/default/localqueues/user-queue/pendingworkloads?workload=myworkload
```
Since workload is a namespaced resource, I wonder if this feature should only apply on localqueues?

The issue with fetching the workload from cluster queue is two fold:
1. in order to correctly resolve the workload name in cluster queue, the URI will require additional arg workloadNamespace, something like this:
```
kubectl get --raw "/apis/visibility.kueue.x-k8s.io/v1alpha1/clusterqueues/cluster-queue/pendingworkloads?workloadName=myworkload&workloadNamespace=default"
```
2. The information on where the workload is in global queue is already available from localqueue response in `positionInClusterQueue` field so not sure why the same information will be needed from globalqueue URL. 

Any thoughts on this will be helpful, TIA

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-27T15:09:29Z

I don't think you should be piggy-backing on the existing URLs.
We should have a new URL just for workloads, something like this:

`/apis/visibility.kueue.x-k8s.io/v1alpha1/namespaces/<ns>/workloads/<name>`

The next question is whether it should present any information if it's not pending, and what it should present.

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-08-27T16:13:57Z

@alculquicondor out of curiosity why would having a new URL be preferable?

IIUC, visibility API w.r.t. workload only provides information about a workload on the queue and extending the existing URL will give users a way to filter the 1 WL out of all the pending ones
 May be in the future have an additional arg of label selector as query to filter from pending workloads URL.

Are there any use case that I'm missing which will be achieved better with a separate URL?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-27T17:19:26Z

Think of it the other way: I want a way to know all the queueing information for a particular workload.

Then the endpoint gives me in which queue it's queued and what its position.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-25T17:30:11Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T03:07:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-24T03:32:14Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-26T03:37:11Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-25T03:57:13Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-25T03:57:18Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1657#issuecomment-2829317379):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
