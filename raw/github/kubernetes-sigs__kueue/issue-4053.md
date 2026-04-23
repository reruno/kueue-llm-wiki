# Issue #4053: Create structs for ui objects in kueue-viz instead of ad-hoc objects

**Summary**: Create structs for ui objects in kueue-viz instead of ad-hoc objects

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4053

**Last updated**: 2025-11-23T20:21:24Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2025-01-24T09:54:03Z
- **Updated**: 2025-11-23T20:21:24Z
- **Closed**: 2025-11-23T20:21:24Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In most backend functions, ad-hoc objects are created to convey data from the kube api to the websocket layer. This was done for several reasons:
- forwarding directly the kubernetes objects would have been too heavy as most of the fields are not used on the ui side
- the dashboard is, currently, a read-only view of aggregated data from the kubernetes api, so, it would not have been necessary to convey kubernetes data back for saving (for example)
- the sake of quick development


**Why is this needed**:
It could be interesting to have dedicated objects for this usage for better debuggability, especially on the client side, and to ensure data consistency.


As a first pass, we can create structs manually based on the existing ad-hoc objects. But, if we can find a way to generate them later it could be more efficient.

## Discussion

### Comment by [@akram](https://github.com/akram) — 2025-01-24T13:24:44Z

/kind dashboard

### Comment by [@akram](https://github.com/akram) — 2025-03-25T05:59:01Z

@tenzen-y we have discussed privately yesterday the requirement to have a protobuf API for `keueviz-backend`. Do you think you can elaborate here on the requirement?
Maybe we can rename this issue also if it the same permimeter. wdyt ?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T00:07:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-26T16:31:50Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-26T17:55:30Z

> [@tenzen-y](https://github.com/tenzen-y) we have discussed privately yesterday the requirement to have a protobuf API for `keueviz-backend`. Do you think you can elaborate here on the requirement? Maybe we can rename this issue also if it the same permimeter. wdyt ?

Thank you for raising this issue based on our discussion.
My recommendation is to have a dashboard server-side dedicated protocol-buffers to avoid dependencies for Kueue CRD.
In the first dashboard implementation step, depending on Kueue CRD makes sense since it could realize the rapid implementation and deliver dashboard features to users.

However, in the long term, I assume that the dashboard wants to have a dedicated API to avoid server-side response construction every time, and we want to avoid expanding CRD only for the dashboard.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-24T18:49:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-24T19:46:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-23T20:21:19Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-23T20:21:24Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4053#issuecomment-3568301531):

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
