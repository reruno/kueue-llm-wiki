# Issue #1101: OLM release so project is listed in operatorhub

**Summary**: OLM release so project is listed in operatorhub

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1101

**Last updated**: 2024-03-28T01:34:08Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@knelasevero](https://github.com/knelasevero)
- **Created**: 2023-09-08T15:15:12Z
- **Updated**: 2024-03-28T01:34:08Z
- **Closed**: 2024-03-28T01:34:05Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A new release process so kueue is listed in the operatorhub portal: https://operatorhub.io/

**Why is this needed**:
This is a nice to have. Openshift users or people that have OLM installed in their cluster would have this additional way to install the project and manage the life-cycle of this controller

**Description:**
The easier way to publish something on operatorhub is if your controller/operator was already developed with Operator SDK, as it makes it easier to generate the required artifacts to create the pull request at: https://github.com/operator-framework/community-operators

Having an operator on top of everything benefits some projects, if they are difficult to install and maintain, or if you want to limit what users can do, exposing less stuff through this operator. This is not the case for kueue (I think). So I think it would make sense to figure out a way to just publish kueue controller directly on operatorhub. More discussion about this on slack: https://kubernetes.slack.com/archives/C09TP78DV/p1694106488946969?thread_ts=1693221954.320929&cid=C09TP78DV

Would be great if all tooling that helps assembling/testing olm bundles were independent of operator-sdk, but what we can do is follow similar approach to what cert-manager folks did in https://github.com/cert-manager/cert-manager-olm#readme. They install OperatorSDK and use some hacks to generate the valid bundle/catalog images to be published at the community operatorhub. 

I created a POC here from a fork of that repo and the bundle generation seems to be ok: https://github.com/knelasevero/kueue-olm/commit/4b24b9cd448670f7146976cff506439a961feedc

To properly test this or create a new test release we first need to figure out how much of this will be possible to be automated through CI, and how much will be manual. Probably creating the PR to https://github.com/operator-framework/community-operators would be manual. We also need to figure out where to publish these bundle/catalog images (registry.k8s.io/kueue/  I assume) then we need to reference them in that PR.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
We can add the design doc (if needed) after having an initial discussion here in this issue.
- [ ] Docs update
- [ ] Figure out where we are going to push the bundle/catalog images

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-27T23:52:53Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-27T00:41:28Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-28T01:34:02Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-28T01:34:06Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1101#issuecomment-2024243046):

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
