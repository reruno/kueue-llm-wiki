# Issue #1833: Local queues prometheus metrics

**Summary**: Local queues prometheus metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1833

**Last updated**: 2025-11-09T08:06:10Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-03-13T13:25:38Z
- **Updated**: 2025-11-09T08:06:10Z
- **Closed**: 2025-11-09T08:06:09Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice), [@varshaprasad96](https://github.com/varshaprasad96)
- **Comments**: 37

## Description

**What would you like to be added**:

Expose Prometheus metrics for local queues, equivalent to the existing cluster queue metrics, but filtered and labeled by local queues.

Similarly to the visibility API, that serves information about pending workloads in local queues, it would be possible to get metrics like like pending workloads, admitted active workloads, resource usage, etc, for local queues.

If cardinality is a concern, those metrics could be exposed behind a feature flag.

**Why is this needed**:

Metrics about local queues can be useful for the batch users persona, so they can have visibility and historical trends about their workloads.

While some metrics are already available for cluster queues, exposing them to the batch users persona presents the following challenges / limitations:
* Cluster queues metrics are global and cannot be filtered by namespaces / tenants
* Querying "cluster-scoped" metrics in secured Prometheus instances is generally only authorised for cluster admin users that have access to all namespaces / tenants

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-13T13:30:29Z

@alculquicondor @tenzen-y Do you think that'd be a useful / possible enhancement?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-13T13:58:54Z

> If cardinality is a concern, those metrics could be exposed behind a feature flag.

Yes, that's the primary concern. I wouldn't make it a feature flag, but a long-term configuration field.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-13T14:19:23Z

> @alculquicondor @tenzen-y Do you think that'd be a useful / possible enhancement?

I understand that this feature is so useful, but I have the same concern with @alculquicondor.
IIRC, previously, we had similar discussions when we designed Visibility/Visibility On-demand. 
So, if we introduce this feature, configurable this feature by [Config API](https://github.com/kubernetes-sigs/kueue/blob/74d17e38e76c2d8b47dbea74364aecc5529f3a78/config/components/manager/controller_manager_config.yaml) would be better.

Anyway, I guess that having a small KEP would be better since we may extend the existing Config API.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-13T15:11:56Z

That makes sense. There could be one or two options added to the Config API,  similar to the existing `.metrics.enableClusterQueueResources`, like `.metrics.enableLocalQueues` and `.metrics.enableLocalQueueResources`.

I can work on a small KEP if you guys give the green light.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-13T15:44:03Z

It seems simple enough.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-13T15:49:26Z

SGTM

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-13T15:55:25Z

Thanks for your quick feedback! I'll work on it asap.

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-11T16:51:36Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-24T17:02:53Z

@astefanutti are you still looking into this?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-06-25T06:51:32Z

@alculquicondor I haven't, but hopefully we'll get back to it soon.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-06-25T06:51:42Z

/remove-lifecycle stale

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-06-25T06:51:55Z

/unassign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-02T17:40:00Z

@varshaprasad96, please write `/assign` in a comment to claim this issue. It's important to communicate that you are working on an issue so that other contributors don't try to work on the same thing.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-07-10T07:13:42Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-08T07:57:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:52:50Z

/remove-lifecycle stale

@varshaprasad96 Do you still work on this enhancement?

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-08T16:54:54Z

@tenzen-y  Yes. I'm planning to get the implementation PR up by next few days.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:56:04Z

> @tenzen-y Yes. I'm planning to get the implementation PR up by next few days.

Awsome, thanks for your effort!

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-18T16:52:34Z

/assign

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-18T17:22:27Z

I've been working on the this KEP for the last couple days and overall it seemed pretty straightforward, until I got to adding the LocalQueueByStatus metric since afaict the status metric for CQs is a bubbling up of the internal [cq.status](https://github.com/kubernetes-sigs/kueue/blob/9987c0d730c1d226993428cc4709ca2b2e5142f4/pkg/cache/clusterqueue.go#L67). The only representation of LQ states exists inside the [CQ struct](https://github.com/kubernetes-sigs/kueue/blob/9987c0d730c1d226993428cc4709ca2b2e5142f4/pkg/cache/clusterqueue.go#L74), and I felt like adding all LQs to the cache struct felt wrong. My current thought is to add a new Type in metrics `LocalQueueStatus` which has the following values (`active`, `pending`, and `orphaned`) where the LQ will inherit the status from its CQ parent. If the parent is terminating the LQ status will move to pending and if the CQ is deleted then the status would move to orphaned. When reconciling the LQ to update status I can just directly grab the status from the CQ in cache.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-18T17:23:12Z

cc @mimowo @PBundyra @tenzen-y

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-11-19T14:29:52Z

@KPostOffice Could you elaborate on where exactly in `localqueue_controller` are you trying to update the metrics. IIUC - the local queue reconciler [watches](https://github.com/kubernetes-sigs/kueue/blob/b0665c7d41b998d490e1f5f8a15dba278836868e/pkg/controller/core/localqueue_controller.go#L298) the CQ, and any status updates would be reflected in [here](https://github.com/kubernetes-sigs/kueue/blob/b0665c7d41b998d490e1f5f8a15dba278836868e/pkg/controller/core/localqueue_controller.go#L110-L122).

>  I felt like adding all LQs to the cache struct felt wrong

Also, the local_queue has reference to the respective [cluster queue](https://github.com/kubernetes-sigs/kueue/blob/b0665c7d41b998d490e1f5f8a15dba278836868e/pkg/queue/local_queue.go#L34). Can't we just directly query CQ's [cache status](https://github.com/kubernetes-sigs/kueue/blob/b0665c7d41b998d490e1f5f8a15dba278836868e/pkg/controller/core/localqueue_controller.go#L61) instead while reporting metrics?

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-19T15:52:58Z

@varshaprasad96 I wasn't planning on adding the metrics to the `localqueue_controller` I was adding them to either `manager.go` or `cache` so that the metrics were reflective of Kueue's operational state, this is what is done for CQ status metrics, see [here](https://github.com/kubernetes-sigs/kueue/blob/b0665c7d41b998d490e1f5f8a15dba278836868e/pkg/cache/clusterqueue.go#L252). I'm having trouble figuring out how to exactly represent the LQ's status. I think it can just update when either:

1. a LQ is added
2. a LQ is updated
3. the LQ's underlying CQ status is updated

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T15:15:45Z

/reopen 
we can use the issue for follow up API changes and Beta graduation.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-05T15:15:51Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1833#issuecomment-2520597690):

>/reopen 
>we can use the issue for follow up API changes and Beta graduation. 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T15:17:09Z

Let's also update the documentation https://kueue.sigs.k8s.io/docs/reference/metrics/ to mention the LocalQueue metrics

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-13T16:13:35Z

I added a comment for the guarding this metric by Config API: https://github.com/kubernetes-sigs/kueue/pull/3673#discussion_r1884162004

I am still wondering if we should guard this metric by that.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-13T16:25:59Z

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/3673#discussion_r1884172427, we will introduce the feature knob to the Config API in the v0.11 version, and then we will guard the slown down Prometheus query performance.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-13T17:00:02Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T17:06:40Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-11T17:10:16Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T17:36:19Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-09T17:38:48Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T07:17:35Z

@tenzen-y I want to re-evaluate this entire KEP. 

Rather than introducing new metrics, I would like to have an extra label "local_queue" in the existing once. 

For users concerns with the cardinality, we could have configuration indicating that value for "local_queue" is left empty.

I propose similar apporach inspired by the recent proposal to introduce workload_priority label. https://github.com/kubernetes-sigs/kueue/issues/5989

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-10T07:28:25Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-09T08:06:05Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-09T08:06:10Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1833#issuecomment-3507643393):

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
