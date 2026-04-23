# Issue #6465: [Cohort] Consider deprecating implicit Cohorts

**Summary**: [Cohort] Consider deprecating implicit Cohorts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6465

**Last updated**: 2026-01-02T16:33:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-08-05T10:12:00Z
- **Updated**: 2026-01-02T16:33:20Z
- **Closed**: 2026-01-02T16:33:19Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

**What would you like to be cleaned**:
Right now, Cohorts can be created by referencing them via a string value in a ClusterQueue (or Cohort), without a backing K8 Object. Logically and conceptually it would be simpler if we required there exist a backing Cohort object

conceptual complexity - listing Cohorts is not enough to find all that exist - also have to check parent/cohort field of all existing Cohorts/ClusterQueues:
https://github.com/kubernetes-sigs/kueue/pull/6379#discussion_r2250426506

e.g. complexity introduced in code:
https://github.com/kubernetes-sigs/kueue/blob/22e4502335b0116300b3dcc63d237cf8b7ac759a/pkg/hierarchy/manager.go#L117-L136

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-05T11:01:28Z

Basically, LGTM
The point is how to provide the migration.

We might need to remove the implicit Cohort in the v1beta2 since ClusterQueue cohort specification is already a long-running one, which means ClusterQueue v1beta1 still supports implicit Cohort.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-05T11:16:02Z

> Basically, LGTM The point is how to provide the migration.
> 
> We might need to remove the implicit Cohort in the v1beta2 since ClusterQueue cohort specification is already a long-running one, which means ClusterQueue v1beta1 still supports implicit Cohort.

Could we have that as part of ClusterQueue/Cohort webhook to create an empty Cohort during the migration phase?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T14:40:02Z

It is probably better to use controller rather than webhook. 

Still:
- if we add it then some users may start relying on it and then the removal of the controller would be a breaking change for them, which is not ideal either. 
- how would the webhook / controller know this CQ creation isn't followed by explicit Cohort creation (say next entry in the user's yaml). If the "default" cohort is created, then the user's entry may conflict.

TBH, I think it is not too bad to live with the design as is, but I'm open to be convinced otherwise if we somehow solve the above

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-05T14:58:37Z

In my experience, manifests are typycally managed by any automation system like GitOps or in-house controllers.
If we automatically create Cohort, there are some drawbacks. I can imagine the automated Cohort will go outdated soon, then uncontrollable situation.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-03T15:14:31Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-03T16:04:27Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-02T16:33:14Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-02T16:33:20Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6465#issuecomment-3705735408):

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
