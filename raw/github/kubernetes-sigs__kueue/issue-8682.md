# Issue #8682: TAS: address the follow up comments to the second pass queue bugfix PR

**Summary**: TAS: address the follow up comments to the second pass queue bugfix PR

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8682

**Last updated**: 2026-04-20T09:19:50Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-20T07:46:38Z
- **Updated**: 2026-04-20T09:19:50Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@skools-here](https://github.com/skools-here)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to address the follow up comments to the bugfix PR: https://github.com/kubernetes-sigs/kueue/pull/8431

**Why is this needed**:

To improve the code readability by the proposed cleanups.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-20T07:47:08Z

/assign @skools-here 
per https://github.com/kubernetes-sigs/kueue/pull/8431#issuecomment-3759349195
cc @tenzen-y

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-20T07:47:11Z

@mimowo: GitHub didn't allow me to assign the following users: skools-here.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8682#issuecomment-3771489321):

>/assign @skools-here 
>per https://github.com/kubernetes-sigs/kueue/pull/8431#issuecomment-3759349195
>cc @tenzen-y 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-20T07:48:51Z

@skools-here feel free to assign yourself

### Comment by [@skools-here](https://github.com/skools-here) — 2026-01-20T08:10:02Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-20T08:48:35Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T09:19:29Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T09:19:50Z

@skools-here Are you still working on this?
