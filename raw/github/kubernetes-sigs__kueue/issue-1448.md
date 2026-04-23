# Issue #1448: Increase the number of reconcilers for the Pod integration

**Summary**: Increase the number of reconcilers for the Pod integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1448

**Last updated**: 2024-03-11T22:18:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-12T20:59:47Z
- **Updated**: 2024-03-11T22:18:37Z
- **Closed**: 2024-03-11T22:18:36Z
- **Labels**: `kind/feature`
- **Assignees**: [@achernevskii](https://github.com/achernevskii)
- **Comments**: 5

## Description

**What would you like to be added**:

 Increase the number of reconcilers to 5, just like we do for Jobs.

The main restriction would be that currently we use Pod {namespace, name} as the keys for the reconciler. This means that a Pod group could be reconciled in parallel when multiple Pods in the group are updated. These reconciler could stumble upon each other.

We need to introduce a custom Pod handler so that we can utilize the name of the group as they key, to avoid parallel reconciliation of the same group.

**Why is this needed**:

By having one worker for the Pod reconciler, it can become a bottleneck when there are multiple pod groups sent at the same time.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-12T20:59:55Z

/assign @achernevskii

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-11T21:24:11Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-11T22:00:04Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-11T22:18:32Z

Fixed in #1502 and #1589

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-11T22:18:36Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1448#issuecomment-1989544168):

>Fixed in #1502 and #1589
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
