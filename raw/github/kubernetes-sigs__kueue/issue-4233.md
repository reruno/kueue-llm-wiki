# Issue #4233: Support PodLevelResources

**Summary**: Support PodLevelResources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4233

**Last updated**: 2026-06-15T15:53:21Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-11T20:58:40Z
- **Updated**: 2026-06-15T15:53:21Z
- **Closed**: —
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@anuragdalvi](https://github.com/anuragdalvi)
- **Comments**: 25

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
It would be great if we can support [the PodLevelResources feature](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2837-pod-level-resource-spec/kep.yaml). Indeed, this feature is still alpha stage, but the APIs has already been added to k/k corev1 API.

Indeed, we have already started to use the [`PodRequests`](https://github.com/kubernetes/kubernetes/blob/69ab91a5c59617872c9f48737c64409a9dec2957/staging/src/k8s.io/component-helpers/resource/helpers.go#L120) helper to calculate total Pod resources in https://github.com/kubernetes-sigs/kueue/pull/4177, which means we can calculate the requested Pod resources with PodLevelResources by passing something to the `PodResourceOptions`.

Once we have done the below tasks, we can confirm the PodLevelResources compatibility with Kueue.

- [ ] Add Unit / Integration testings by using Pod with `.spec.resources` (≠ `.spec.containers.resources`)
- [ ] Refine the total Pod resources calculation mechanism to support `.spec.resources` in the following:
    - https://github.com/kubernetes-sigs/kueue/blob/2738e8b05c03fe5dcf38beba1f4769fe2e1888c9/pkg/cache/tas_flavor.go
    - https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/limitrange/limitrange.go
    - https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go

> [!NOTE]
> We need to enable Kubernetes featureGate, `PodLevelResources` in kube-scheduler, kube-apiseerver, and kubelet to verify the behavior.

**Why is this needed**:
It would be better to support k/k new enhancements.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-13T18:22:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-12T21:15:19Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-13T03:17:08Z

/remove-lifecycle rotten

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T06:09:59Z

The PodLevelResource will be promoted to Beta (enabled by default) in the next k8s 1.34: https://github.com/kubernetes/enhancements/blob/ef7e11d088086afd84d26c9249a4ca480df2d05a/keps/sig-node/2837-pod-level-resource-spec/kep.yaml#L38

### Comment by [@YamasouA](https://github.com/YamasouA) — 2025-08-11T10:37:15Z

/assign

### Comment by [@YamasouA](https://github.com/YamasouA) — 2025-08-11T10:38:26Z

@tenzen-y 
I want to try this, Are there any problem?

### Comment by [@YamasouA](https://github.com/YamasouA) — 2025-08-17T14:41:21Z

@tenzen-y 
What should I write Design Doc?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T19:09:13Z

@YamasouA Thank you for bringing up this issue. Yes, starting from KEP would be better.
Especially, it would be better to clarify which Kubernetes features (e.g., DRA) and Kueue features are not compatible with PodLevelRersources. Additionally, I would mention that the resource evaluation (count) function algorithm in Kueue.

You might be able to refer the kube-scheduler evaluation algorithm.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-17T19:35:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T19:45:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-16T20:18:17Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-16T20:18:23Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4233#issuecomment-3761655287):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T20:22:44Z

/reopen
/remove-lifecycle rotten

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-16T20:22:49Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4233#issuecomment-3761674906):

>/reopen
>/remove-lifecycle rotten


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-16T20:52:50Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-17T06:04:21Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-11T17:10:45Z

/unassign @YamasouA

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-11T17:14:10Z

cc @mimowo @tenzen-y 

PodLevelResources is going GA and there are features building on this.

https://github.com/kubernetes/enhancements/pull/6169/changes#r3375866833

### Comment by [@mimowo](https://github.com/mimowo) — 2026-06-11T17:30:28Z

Yeah, it would be great to support it well, I thought we already do, but this requires checking at least. 

I think if we don't support it well, then I would probably handle as a bugfix at this point rather than a feature, but TBD.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-14T19:48:42Z

/help wanted

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-14T21:02:29Z

## Pod-Level Resources Support in Kueue v0.18.1 — Code Audit Summary

> **Disclosure:** This analysis was assisted by AI tooling per the [Kubernetes AI Tool Usage Policy](https://www.kubernetes.dev/docs/guide/pull-requests/#ai-guidance).

### Background

Kubernetes 1.32+ introduced pod-level resources (`pod.spec.resources`) via [KEP-2837](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2837-pod-level-resources), allowing CPU and memory to be specified at the pod level rather than (or in addition to) per-container. This comment summarizes how Kueue v0.18.1 handles pod-level resources based on a code audit and live cluster testing.

---

### What works ✅

**Quota accounting is correct.** Kueue's core resource calculation in `totalRequestsFromPodSets()` ([`pkg/workload/workload.go:631`](https://github.com/kubernetes-sigs/kueue/blob/v0.18.1/pkg/workload/workload.go#L631)) delegates to the upstream `k8s.io/component-helpers` `PodRequests()` function with default options (`SkipPodLevelResources: false`). This means:

- If `pod.spec.resources` is set, those values **are included** in the total resource request.
- Quota reservation, admission decisions, and `status.admission.podSetAssignments[].resourceUsage` all reflect the pod-level resources correctly.

This was verified on a live Kind cluster (Kubernetes v1.35, Kueue v0.18.1) — workloads with container-level resource requests are correctly admitted or blocked based on ClusterQueue quota.

---

### Gaps found ⚠️

While quota *accounting* works, several of Kueue's own code paths **do not account for `pod.spec.resources`**:

#### 1. LimitRange default application skips pod-level resources

`handlePodLimitRange()` in [`pkg/workload/resources.go`](https://github.com/kubernetes-sigs/kueue/blob/v0.18.1/pkg/workload/resources.go) only iterates over `initContainers` and `containers` when applying LimitRange defaults. If a user relies on `pod.spec.resources` instead of per-container resources, LimitRange defaults will not be applied.

#### 2. Limits-to-requests backfill skips pod-level resources

`UseLimitsAsMissingRequestsInPod()` in [`pkg/workload/resources.go`](https://github.com/kubernetes-sigs/kueue/blob/v0.18.1/pkg/workload/resources.go) backfills missing `requests` from `limits` — but only for `initContainers` and `containers`. Pod-level `limits` without corresponding `requests` won't be backfilled.

#### 3. Resource validation skips pod-level resources

`ValidateResources()` in [`pkg/workload/resources.go`](https://github.com/kubernetes-sigs/kueue/blob/v0.18.1/pkg/workload/resources.go) validates that `requests ≤ limits` for each container, but does not perform this check on `pod.spec.resources`.

#### 4. Immutability enforcement misses pod-level resources

`SpecShape()` in [`pkg/util/pod/pod.go`](https://github.com/kubernetes-sigs/kueue/blob/v0.18.1/pkg/util/pod/pod.go#L138) defines which pod spec fields are treated as immutable on admitted workloads. It does **not** include `pod.spec.resources`, meaning pod-level resources could theoretically be mutated after admission without Kueue detecting the change.

As a secondary note, `ContainersShape()` only tracks `resources.requests` (not `resources.limits`) per container, so container-level limits are also not enforced as immutable.

---

### Summary matrix

| Area | Quota Accounting | Validation | Immutability | LimitRange |
|------|:---:|:---:|:---:|:---:|
| Container `resources.requests` | ✅ | ✅ | ✅ | ✅ |
| Container `resources.limits` | ✅ (backfilled to requests) | ✅ | ❌ | ✅ |
| Init container / sidecar resources | ✅ | ✅ | ✅ | ✅ |
| **`pod.spec.resources` (KEP-2837)** | **✅** | **❌** | **❌** | **❌** |
| `pod.spec.overhead` | ✅ | N/A | ✅ | N/A |
| DRA `resourceClaims` | ✅ (Beta) | ✅ | ✅ | N/A |

---

### Suggested follow-up

The following functions need to be updated to handle `pod.spec.resources`:

1. **`UseLimitsAsMissingRequestsInPod()`** — backfill pod-level requests from pod-level limits
2. **`handlePodLimitRange()`** — apply LimitRange defaults to pod-level resources (if applicable per LimitRange spec)
3. **`ValidateResources()`** — validate `requests ≤ limits` at the pod level
4. **`SpecShape()`** — add `"resources": podSpec.Resources` to the immutability shape
5. **`ContainersShape()`** — consider also tracking `resources.limits` for container-level immutability

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-14T21:04:03Z

/help
/good-first-issue

In addition to the code above, we should add documentation verifying that we support this feature.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-06-14T21:04:05Z

@kannon92: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4233):

>/help
>/good-first-issue
>
>In addition to the code above, we should add documentation verifying that we support this feature.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@anuragdalvi](https://github.com/anuragdalvi) — 2026-06-15T15:33:00Z

@kannon92 @tenzen-y 
I would like to implement this. Can you assign this issue to me ?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-06-15T15:53:18Z

/assign @anuragdalvi
