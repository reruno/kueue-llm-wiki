# Issue #663: Introduce possibility to disable protection on /metrics endpoint

**Summary**: Introduce possibility to disable protection on /metrics endpoint

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/663

**Last updated**: 2024-02-18T03:53:17Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mikouaj](https://github.com/mikouaj)
- **Created**: 2023-03-27T13:19:37Z
- **Updated**: 2024-02-18T03:53:17Z
- **Closed**: 2024-02-18T03:53:15Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make it possible to disable protection on `/metrics` endpoint via configuration.

**Why is this needed**:

This is needed for Google Cloud Managed Service for Prometheus managed data collection.
As for now, GMP scraping does not support authentication on metrics endpoints. Thus, it is not possible to use GMP managed data collection on kueue metrics.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-28T09:58:22Z

Do we, I think we didn't enable the authentication.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-28T13:48:41Z

IIRC, you can try removing this patch https://github.com/kubernetes-sigs/kueue/blob/main/config/default/manager_auth_proxy_patch.yaml

and point GMP to the 8080 port of the pods.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-06-26T15:09:01Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-27T02:51:56Z

Any feedbacks? @mikouaj

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-19T03:00:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-18T03:53:12Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-18T03:53:16Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/663#issuecomment-1950933605):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
