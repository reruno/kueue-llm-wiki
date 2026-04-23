# Issue #6791: Introduce a Guage metric to track the current number of "Running" workloads

**Summary**: Introduce a Guage metric to track the current number of "Running" workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6791

**Last updated**: 2026-02-17T21:25:36Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-11T09:20:37Z
- **Updated**: 2026-02-17T21:25:36Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@jimangel](https://github.com/jimangel), [@helayoty](https://github.com/helayoty)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a guage metric to track the current number of workloads with "PodsReady" - running and making progress.

**Why is this needed**:

To inform users how many workloads are actually making progress. Just "admitted" is not necessarily reflecting that.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T09:20:44Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T09:21:07Z

@MichalZylinski

### Comment by [@helayoty](https://github.com/helayoty) — 2025-09-11T15:47:09Z

/assign @helayoty

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-10T16:21:34Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-09T17:17:04Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-08T18:09:57Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-08T18:10:03Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6791#issuecomment-3867783252):

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T10:32:54Z

/reopen

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T10:32:58Z

/remove-lifecycle rotten

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-09T10:33:00Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6791#issuecomment-3870856349):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@jimangel](https://github.com/jimangel) — 2026-02-17T21:25:36Z

/assign
