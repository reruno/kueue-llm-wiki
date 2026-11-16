# Issue #9852: KEP-8303: Add an explicit opt-in API for MultiKueue single-cluster preemptions

**Summary**: KEP-8303: Add an explicit opt-in API for MultiKueue single-cluster preemptions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9852

**Last updated**: 2026-11-05T12:25:47Z

---

## Metadata

- **State**: open
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2026-03-13T11:14:53Z
- **Updated**: 2026-11-05T12:25:47Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `area/multikueue`
- **Assignees**: [@alien1403](https://github.com/alien1403)
- **Comments**: 8

## Description

**What would you like to be added**:
Extend the MultiKueue `Configuration` API with fields serving as opt-in for the `MultiKueueOrchestratedPreemption` feature gate.

For example `PreemptionsMode: Concurrent|AtMostOne`.

**Why is this needed**:
https://github.com/kubernetes-sigs/kueue/pull/9721 implements the `MultiKueueOrchestratedPreemption` feature gate which serves as the opt-in mechanism for the single-cluster preemption guarantee in MultiKueue. When this feature graduates to beta without an explicit opt-in mechanism from the user, the default behavior of MultiKueue deployments would change.

We should add an API that allows the users to control the behavior of the preemptions in MultiKueue.

See https://github.com/kubernetes-sigs/kueue/pull/9721#issuecomment-4054172653 for context.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-13T11:15:02Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-11T11:54:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-07-11T12:18:29Z

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

### Comment by [@kshalot](https://github.com/kshalot) — 2026-07-11T12:22:08Z

/remove-lifecycle rotten

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-08-07T12:15:51Z

/assign alien1403

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-08-07T12:15:54Z

@olekzabl: GitHub didn't allow me to assign the following users: alien1403.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9852#issuecomment-5216938372):

>/assign alien1403


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alien1403](https://github.com/alien1403) — 2026-08-07T12:16:52Z

/assign alien1403

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-11-05T12:25:44Z

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
