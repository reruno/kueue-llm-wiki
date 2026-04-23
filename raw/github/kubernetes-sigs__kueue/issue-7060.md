# Issue #7060: Significant increase in informer cache list requests to api server from kueue 0.12.8 to 0.13.4 upgrade

**Summary**: Significant increase in informer cache list requests to api server from kueue 0.12.8 to 0.13.4 upgrade

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7060

**Last updated**: 2026-02-26T18:54:11Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-29T16:42:11Z
- **Updated**: 2026-02-26T18:54:11Z
- **Closed**: 2026-02-26T18:54:10Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Related to: https://github.com/kubernetes-sigs/kueue/issues/6971

If you turn zap logging level up to 8, this will log the full http request and response made by informer cache to apiserver. We noticed a giant spike from 5G to 23Gi when upgrading from 0.12.8 to 0.13.4, both having log level 10. 

We should potentially investigate if there's a bug/regression in controller runtime or k8s with the significant difference in list requests at controller startup. See https://github.com/kubernetes-sigs/kueue/issues/6971 for full context

**Why is this needed**:

Not an immediate issue. Issue create for tracking in case we encounter future related issues. Perhaps down the line we'll see issues with apiserver load on kueue controller restart.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-28T18:52:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-27T18:53:43Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-26T18:54:01Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-26T18:54:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7060#issuecomment-3968559685):

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
