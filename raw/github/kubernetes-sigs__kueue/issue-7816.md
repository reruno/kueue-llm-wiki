# Issue #7816: Upgrade testing from latest release to current main

**Summary**: Upgrade testing from latest release to current main

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7816

**Last updated**: 2026-03-19T10:52:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-11-21T15:18:51Z
- **Updated**: 2026-03-19T10:52:39Z
- **Closed**: 2026-03-19T10:52:38Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

It would be great if there was a test lane that verifies that kueue can upgrade from latest release to current main.

I don't think this is a trivial undertaken so it may be worth drafting a KEP or a design doc on how we can add upgrade testing.


**Why is this needed**:

Offering upgrades is important.

Testing upgrades could catch https://github.com/kubernetes-sigs/kueue/issues/7344 early.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-21T15:19:09Z

cc @mimowo @tenzen-y @sohankunkerkar

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-21T16:58:27Z

An area that we would like to target for upgrade testing is that user workloads will not be impacted by a Kueue upgrade.

ie if a user has a workload that has been admitted and running, kueue upgrades will not impact this.

It would also be ideal to verify that kueue resources (cluster queues, local queues, etc) created in previous release are still able to be modified to a newer release.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-21T22:10:43Z

cc @amy 

Curious on your thoughts on what you expect to happen for workloads during kueue upgrades?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T18:47:49Z

/close
we already have the upgrade tests after this is merged: https://github.com/kubernetes/test-infra/pull/35955

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-24T18:47:55Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7816#issuecomment-3572231688):

>/close
>we already have the upgrade tests after this is merged: https://github.com/kubernetes/test-infra/pull/35955


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T20:02:42Z

/reopen

I'd like to keep this open to maybe consider more usecases on upgrade testing.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-24T20:02:48Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7816#issuecomment-3572505751):

>/reopen
>
>I'd like to keep this open to maybe consider more usecases on upgrade testing.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T14:44:02Z

> I'd like to keep this open to maybe consider more usecases on upgrade testing.

Can you define the use-cases? If not defined then this issue is non-actionable I think.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-27T14:51:47Z

Yes I wanted to get some usecases from community on expectations of upgrades for Kueue. I have my own but I wanted to call out to the community for this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:02:22Z

> Yes I wanted to get some usecases from community on expectations of upgrades for Kueue. I have my own but I wanted to call out to the community for this.

@kannon92 any update here? Maybe you can list your use cases so that it is clear for people looking for tasks what to do. 

Otherwise since we haven't heard for 3 weeks I think we can close to avoid distractions and just re-open when we have a use case, wdyt?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T10:52:32Z

/close
I think the issue is currently non-actionable without a list of specific scenarios to cover. The suite with a baseline scenario is already there. Feel free to re-open or open another issue when you have the testing scenarios. For now closing to avoid distractions.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T10:52:39Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7816#issuecomment-4089290085):

>/close
>I think the issue is currently non-actionable without a list of specific scenarios to cover. The suite with a baseline scenario is already there. Feel free to re-open or open another issue when you have the testing scenarios. For now closing to avoid distractions.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
