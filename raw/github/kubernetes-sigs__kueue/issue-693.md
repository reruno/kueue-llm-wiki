# Issue #693: MVP Multi-cluster support

**Summary**: MVP Multi-cluster support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/693

**Last updated**: 2024-04-16T14:45:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2023-04-12T19:31:08Z
- **Updated**: 2024-04-16T14:45:17Z
- **Closed**: 2024-04-16T13:34:15Z
- **Labels**: `kind/feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Define and implement multi-cluster story for Kueue.

**Why is this needed**:

Many customers are asking how to configure and run Kueue with multiple batch clusters.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-04-12T19:31:17Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-07-11T19:39:47Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-17T07:57:48Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-28T22:13:53Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-28T22:13:57Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/693#issuecomment-1871539928):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-31T18:54:43Z

@trasc Which PRs do we need to merge by v0.6?

@alculquicondor @mimowo Did you discuss which MultiKueue features we should include in the v0.6?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-01T08:55:23Z

> @alculquicondor @mimowo Did you discuss which MultiKueue features we should include in the v0.6?

I believe we already have the basic MVP with the API, controller, and the JobSet support.

The nice-to-haves (close the the MPV status), in the order of importance:
1. label for Workloads and Jobs indicating they are created by multikueue (currently called origin)
2. https://github.com/kubernetes-sigs/kueue/pull/1643
3. https://github.com/kubernetes-sigs/kueue/pull/1668


(1.) is currently coupled with (2.) and (3.). Maybe we could decouple it as a preparatory PR to do not put it at risk? WDYT @trasc @alculquicondor ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-01T19:33:56Z

I would just focus on #1643 at this point.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-01T20:24:10Z

I'm ok with only #1643.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T14:29:43Z

@mimowo was there anything else pending for the MVP?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-16T14:44:46Z

AFIAK there is nothing pending, so we can close, and open dedicated issues / prs if we find some bugs.
