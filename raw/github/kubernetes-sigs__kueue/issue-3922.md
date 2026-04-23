# Issue #3922: Add support for binding CQs to Users and Groups

**Summary**: Add support for binding CQs to Users and Groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3922

**Last updated**: 2025-07-07T17:09:49Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@KPostOffice](https://github.com/KPostOffice)
- **Created**: 2025-01-02T20:23:09Z
- **Updated**: 2025-07-07T17:09:49Z
- **Closed**: 2025-07-07T17:09:48Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A way to bind CQs to users and groups

**Why is this needed**:

In some cases the batch admin isn't required to be in the loop when new namespaces are created. When a new namespace is created a new LQ has to be created so that users in that namespace can use Kueue quota management. As it stands this requires batch admin since the ability to create LQs more or less allows users to point to any CQ on the K8 cluster. I want the ability to be more permissive with who can create LQs while still limiting it based on `spec.clusterQueue`

I've created a small PoC with how I envision this working

https://github.com/KPostOffice/kueue/tree/cq-binding

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-06T21:08:03Z

> I've created a small PoC with how I envision this working

Maybe you can open this up as a PR in your branch so you could gather feedback.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-01-07T01:23:14Z

> Maybe you can open this up as a PR in your branch so you could gather feedback.

Good idea. This would require a KEP as well I think.

[Here](https://github.com/KPostOffice/kueue/pull/1) is the link to the PR on my fork

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-02-07T14:54:28Z

A point of discussion I've had in mind is whether this ClusterQueueBinding resource will be mandatory or optional. If mandatory, then the admin would require some extra initial setup of resources, and will be a breaking change on upgrading Kueue. But, with the benefit that the admin won't be required to create LocalQueues per namespace, rather the user will be permitted to create one pointing to the bound ClusterQueue. This ensures users cannot point to unauthorized ClusterQueues.

If this resource will be optional, then we could still take advantage of this feature without causing a breaking change, but the admin would need to be attentive in ensuring all users/groups are bounded to their respective CQB, which could be prone to mistakes.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-08T15:42:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-07T16:29:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-07T17:09:44Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-07T17:09:49Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3922#issuecomment-3045960580):

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
