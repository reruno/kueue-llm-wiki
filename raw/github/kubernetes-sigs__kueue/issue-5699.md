# Issue #5699: Helm: Investigate a way to mitigate CRD API version upgrading pains

**Summary**: Helm: Investigate a way to mitigate CRD API version upgrading pains

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5699

**Last updated**: 2026-02-15T19:58:22Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-20T14:32:45Z
- **Updated**: 2026-02-15T19:58:22Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We would like to investigate a way to mitigate the painful Kueue version upgrading for Helm installation.
The possible way is the [Helm hook](https://helm.sh/docs/topics/charts_hooks/).

When we decide to go with Helm hook, we need to decide / investigate the following:

1. Investigate which hooks (https://helm.sh/docs/topics/charts_hooks/#the-available-hooks) can resolve the CRD version replacing problems
2. How long will we maintain the hook? e.g., during a minor version or more

**Why is this needed**:

Currently, we occasionally provide the manual CRD version upgrading steps in the following:

https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0

This could work well for kustomize / kubectl installation users. However, this does not work well for the admins who manage Kueue manifests by Helm.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T14:33:03Z

cc @mimowo @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T15:12:17Z

cc @kannon92 @dgrove-oss I know folks you don't install any Alpha version CRDs in your clusters, per [here](https://github.com/openshift/kueue-operator/blob/b93614cc971d89fe631e6a6244a416af1c72ec5b/pkg/operator/target_config_reconciler.go#L838), but maybe you would be interested in the Helm-managed deployment when the upgrade is automated, or maybe you have some other reasons why you think this would not work well.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-20T15:14:59Z

I'd love it if we could use Helm in my organization but its not yet supported in OLM.

:(

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-20T15:17:14Z

Does Kubernetes guarantee this for alpha? To me, alpha can be rough and breaking without warning. Putting a requirement on upgradability for alpha -> beta is giving conflicting statement here.

I would prefer efforts on upgradability of beta apis from release to release. And especially making sure beta -> v1 APIs are always valid.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T15:19:53Z

> I would prefer efforts on upgradability of beta apis from release to release. And especially making sure beta -> v1 APIs are always valid.

This and beta promotion (beta1 -> beta2) must always be guaranteed by conversion webhooks.
And, we are planning that.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T15:27:09Z

> Does Kubernetes guarantee this for alpha? To me, alpha can be rough and breaking without warning. Putting a requirement on upgradability for alpha -> beta is giving conflicting statement here.

We are free to drop Alpha APIs at any point, or break them.

However, in case of promotion alpha -> beta, as in case of 0.9.0, the promotion prevented upgrade even for users who don't use MK.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-18T15:53:48Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T15:59:57Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T16:43:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-16T17:38:17Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-15T18:36:44Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-15T18:36:50Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5699#issuecomment-3904968567):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-15T19:58:17Z

/reopen
/remove-lifecycle rotten

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-15T19:58:22Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5699#issuecomment-3905083649):

>/reopen
>/remove-lifecycle rotten
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
