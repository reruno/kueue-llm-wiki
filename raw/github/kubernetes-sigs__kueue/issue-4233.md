# Issue #4233: Support PodLevelResources

**Summary**: Support PodLevelResources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4233

**Last updated**: 2026-04-17T06:04:23Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-11T20:58:40Z
- **Updated**: 2026-04-17T06:04:23Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@YamasouA](https://github.com/YamasouA)
- **Comments**: 16

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
