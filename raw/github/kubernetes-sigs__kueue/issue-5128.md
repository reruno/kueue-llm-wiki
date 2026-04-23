# Issue #5128: Kueue batch admin/user roles do not reflect reality that Kueue is more than batch workloads

**Summary**: Kueue batch admin/user roles do not reflect reality that Kueue is more than batch workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5128

**Last updated**: 2025-09-22T19:51:56Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-25T19:12:11Z
- **Updated**: 2025-09-22T19:51:56Z
- **Closed**: 2025-09-22T19:51:55Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

Can we rename these roles to kueue-admin or kueue-user? And avoid using batch for kueue?

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-25T19:15:59Z

For reference I am referring to https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/batch_admin_role.yaml and https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/batch_user_role.yaml.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-25T19:16:50Z

Also https://kueue.sigs.k8s.io/docs/tasks/manage/rbac/.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-25T19:19:27Z

We want to handle this as part of https://github.com/kubernetes-sigs/kueue/issues/4286 since `batch admin` concept depends on the concept for `kueue is Job queueing system`.

I think we should change `Job` term, before.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-24T19:19:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-23T19:40:59Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-22T19:51:50Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-22T19:51:56Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5128#issuecomment-3321204559):

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
