# Issue #8965: Add label filters for TAS e2e tests

**Summary**: Add label filters for TAS e2e tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8965

**Last updated**: 2026-10-17T10:53:59Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-02-03T14:55:47Z
- **Updated**: 2026-10-17T10:53:59Z
- **Closed**: 2026-10-17T10:53:58Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: [@laxmi-333](https://github.com/laxmi-333)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

It would be nice to have label filters for tas e2e tests like here - https://github.com/kubernetes-sigs/kueue/pull/8005 too. It takes a lot of time to setup the cluster for these tests.

**Why is this needed**:

Quicker cluster setup time when running specific suites of TAS e2e tests

## Discussion

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-14T11:03:47Z

Hi @j-skiba, I would like to work on this issue.

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-14T11:07:10Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-12T11:09:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-07-12T11:40:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-10-17T10:53:52Z

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

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-10-17T10:53:59Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8965#issuecomment-6233051519):

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
