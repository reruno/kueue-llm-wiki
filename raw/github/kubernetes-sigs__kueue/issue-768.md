# Issue #768: v1beta2 wishlist

**Summary**: v1beta2 wishlist

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/768

**Last updated**: 2025-11-17T08:03:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-12T13:55:15Z
- **Updated**: 2025-11-17T08:03:59Z
- **Closed**: 2025-11-17T08:03:38Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 34

## Description

**What would you like to be cleaned**:

In a v1beta2 API, we would like to make the following breaking changes:

- Workload
  - Report resource usage by pod, instead of the entire podset, in the admission struct.
  - Remove 'kueue.x-k8s.io/original-node-selectors' annotation
- LocalQueue
  - Rename `status.flavorUsage` to `status.flavorsUsage`.

**Why is this needed**:

As we add more features, some field didn't age well.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-31T07:01:26Z

`Remove 'kueue.x-k8s.io/original-node-selectors' annotation from workload`

ref: #771

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-09-16T08:18:58Z

Has been removed in https://github.com/kubernetes-sigs/kueue/pull/834

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-30T15:26:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T21:10:41Z

/remove-lifecycle stale

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-04-05T13:15:59Z

Remove `.spec.AdmissionChecks` field in ClusterQueue and convert its content to `.spec.AdmissionCheckStrategy` 
KEP: https://github.com/kubernetes-sigs/kueue/pull/1935
Issue: https://github.com/kubernetes-sigs/kueue/issues/1432

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-15T14:18:32Z

Change `.spec.flavorFungibility`, `.spec.preemption`, `.spec.preemption.borrowWithinCohort`  type from pointer to value for `ClusterQueueSpec`.
Discussion: https://github.com/kubernetes-sigs/kueue/pull/1972#discussion_r1565513061

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T13:18:27Z

Maybe we can consider to move the workload's `spec.active` to status. 
Currently, the `workload_controller` needs write access to spec, which isn't recommended (see [API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)). Also, it makes tricky to set the reason for workload's deactivation reliably, see [thread](https://github.com/kubernetes-sigs/kueue/pull/2219#discussion_r1606605695).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T17:27:36Z

I'm not too sure about that one. `active` expresses a desired state, as such, it should be in the spec. It can come from the user or it can come from the system.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-22T17:37:09Z

> I'm not too sure about that one. `active` expresses a desired state, as such, it should be in the spec. It can come from the user or it can come from the system.

That is a good point. 
In my point, I'm wondering if we should define the dedicated API for the kueue-controller-manager to deactivate the Workload in the status field.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T17:52:01Z

Tricky... because we also want the users to be able to reset the active field back to true. And they definitely shouldn't have access to status.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-05-23T07:48:11Z

Deprecate the `QueueVisibility` API.
Issue: #2256

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T19:13:31Z

> Tricky... because we also want the users to be able to reset the active field back to true. And they definitely shouldn't have access to status.

Yeah, I agree with you. My motivation is mitigating compexity of mechanism to deactivate workload by exceeding the backoffLimit in the workload controller.

Once we move or add active field in the Workload, that allows us to deactivate a workload by a single API call.

Current behavior needs to 3 reconciling: `spec.active=false` (workload controller) -> add `Evicted` condition to a workload (workload controller) -> stop Job (jobframework reconciler).
New `.status.active` needs to 2 reconciling: add `Evicted` condition to a workload (workload controller) -> stop Job (jobframework reconciler).

But, I'm sure your concerns. So, let us seek any alternative approach to mitigate complexity of mechanism of deactivation.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-06-18T12:26:23Z

Deprecate or remove the `retryDelayMinutes` from the AdmissionCheck API
Issue: #2437

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-16T13:15:36Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-16T13:32:52Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T08:16:10Z

We may also revisit promoting domains for some labels (for example to support kueue.kubernetes.io/queue-name along with kueue.x-k8s.io/queue-name), see https://github.com/kubernetes-sigs/kueue/issues/2858

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:29:54Z

> We may also revisit promoting domains for some labels (for example to support kueue.kubernetes.io/queue-name along with kueue.x-k8s.io/queue-name), see #2858

AFAIK, @kerthcet tried to add queueName field to the core PodSpec API. We may be able to retry it before adding the `kueue.kuebernetes.io/queue-name`. Although I'm not sure if the label is acceptable by core kube API.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T10:04:25Z

Also adding status to ResourceFlavor could be useful, especially for TAS, currently we only have Spec: https://github.com/kubernetes-sigs/kueue/blob/cdbb7a124430ae78c297f65e680765cc45ac8c38/apis/kueue/v1beta1/resourceflavor_types.go#L35

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-24T15:14:04Z

That doesn't need a new API version

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-22T15:27:12Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-22T15:31:59Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T14:38:09Z

Fix a field name typo in the Workload resource found at https://github.com/kubernetes-sigs/kueue/pull/4297.

incorrect:  `.status.accumulatedPastExexcutionTimeSeconds`.
correct: `.status.accumulatedPastExecutionTimeSeconds `

https://github.com/kubernetes-sigs/kueue/blob/4f01318b3a486e7b2cf4a0874c50efee1b97fdab/apis/kueue/v1beta1/workload_types.go#L350-L354

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-07T14:58:45Z

Unify name of Cohort and CQ's parent reference. Perhaps both being `parentCohort`

See https://github.com/kubernetes-sigs/kueue/pull/4473

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T14:31:12Z

Revisit the design of the API for exposing the ResourceFlavor information to the end-users (currently in LocalQueue status) as designed in the [KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/3122-expose-flavors-in-localqueue-status), see [comment](https://github.com/kubernetes-sigs/kueue/pull/4543#discussion_r1991626064). cc @mwielgus

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T15:01:17Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T15:09:24Z

/remove-lifecycle stale

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-30T11:36:53Z

In FlavorFungibility [API](https://github.com/kubernetes-sigs/kueue/blob/807f24a6cbbc8c9e1498865adb7d6e3383dec6e7/apis/kueue/v1beta1/clusterqueue_types.go#L390), `WhenCanPreempt` should have options `TryNextFlavor` and `Break`/`Stop` (instead of `Preempt`). Currently `Preempt` option is confusing: https://github.com/kubernetes-sigs/kueue/blob/807f24a6cbbc8c9e1498865adb7d6e3383dec6e7/apis/kueue/v1beta1/clusterqueue_types.go#L405 
because this field does not control the preference but only determines when we break from the loop over the flavors.

Similarly for WhenCanBorrow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-02T08:52:00Z

> In FlavorFungibility [API](https://github.com/kubernetes-sigs/kueue/blob/807f24a6cbbc8c9e1498865adb7d6e3383dec6e7/apis/kueue/v1beta1/clusterqueue_types.go#L390), `WhenCanPreempt` should have options `TryNextFlavor` and `Break`/`Stop` (instead of `Preempt`). Currently `Preempt` option is confusing:
> 
> [kueue/apis/kueue/v1beta1/clusterqueue_types.go](https://github.com/kubernetes-sigs/kueue/blob/807f24a6cbbc8c9e1498865adb7d6e3383dec6e7/apis/kueue/v1beta1/clusterqueue_types.go#L405)
> 
> Line 405 in [807f24a](/kubernetes-sigs/kueue/commit/807f24a6cbbc8c9e1498865adb7d6e3383dec6e7)
> 
>  // - `Preempt`: allocate in current flavor if it's possible to preempt some workloads. 
> 
> because this field does not control the preference but only determines when we break from the loop over the flavors.
> Similarly for WhenCanBorrow.

@pajakd @mimowo What about introducing the new enum (`Break` / `Stop`) in v1beta1.
And deprecating the `Preempt` and `Borrow` enum, but still both new enum and deprecated ones are supported during v1beta1. After v1beta2, we remove deprecated ones.

Although we need to consider the new enum name instead of `Break` / `Stop` since the proposed name is inspired by flavorAssigner behavior. But, we want to use the name which is understandable for admins who do not have flavorAssigner mechanism knowledge.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-04T15:21:28Z

I would like to consider this too: https://github.com/kubernetes-sigs/kueue/issues/5877

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-14T17:39:29Z

@mimowo @tenzen-y 

Could we create a list of items we want for v1beta2?

I'm trying to line up when this breaking change will happen and what APIs we should warn about that may potentially go away?

Will there be a conversion webhook added for v1beta1 to v1beta2?

We are getting adoption of these APIs in Kueue so we are hoping to avoid breaking changes as much as possible now.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T17:59:46Z

/assign 
I'm going to review the list and transform it into an actionable plan

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T09:18:59Z

I would like to offload the semantics of the Workload's requeueAt field by https://github.com/kubernetes-sigs/kueue/issues/6766

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T08:03:32Z

/close
As the changes are already addressed in https://github.com/kubernetes-sigs/kueue/issues/7113 (proposed changes which are not applied are discussed in the referenced doc).

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T08:03:39Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/768#issuecomment-3540437855):

>/close
>As the changes are already addressed in https://github.com/kubernetes-sigs/kueue/issues/7113 (changes not applied are discussed in the referenced doc).


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
