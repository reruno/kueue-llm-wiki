# Issue #5459: Extend the installation docs for development version with saving manifest locally

**Summary**: Extend the installation docs for development version with saving manifest locally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5459

**Last updated**: 2025-10-31T13:38:10Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-03T08:21:12Z
- **Updated**: 2025-10-31T13:38:10Z
- **Closed**: 2025-10-31T13:38:09Z
- **Labels**: `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 6

## Description

/kind documentation

I would like to add to the docs something like:

To save the development manifest locally for editing before installation under https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version: 

```sh
kubectl kustomize "github.com/kubernetes-sigs/kueue/config/default?ref=main" > kueue-manifest.yaml
```
This is because is  sometimes asked by early testers of Kueue, who want to test from main, but have a need to adjust the manifests locally

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T08:21:40Z

wdyt @tenzen-y  @kannon92 @dgrove-oss  @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-03T11:40:48Z

I discussed with @mimowo offline. 
We can add this note only for testing (development version) installation.
For production installation, the platform team typically modifies manifests using kustomize patch manifests.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-01T12:41:33Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-01T13:16:58Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-31T13:38:04Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-31T13:38:10Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5459#issuecomment-3473134346):

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
