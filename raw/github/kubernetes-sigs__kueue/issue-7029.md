# Issue #7029: [Feature]: Provide a default timeout on a job per local queue

**Summary**: [Feature]: Provide a default timeout on a job per local queue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7029

**Last updated**: 2026-04-14T19:20:14Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-09-28T17:28:10Z
- **Updated**: 2026-04-14T19:20:14Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like the ability to add add a timeout to jobs if they submit to certain local queues.

We would set https://kueue.sigs.k8s.io/docs/concepts/workload/#maximum-execution-time based on the local queue.

I think we could add a timeout section on the LocalQueue API and that can automatically set a timeout. If the timeout is specified in the job, we can ignore this.

**Why is this needed**:

Requested in two separate issues.

- https://github.com/kubernetes-sigs/kueue/discussions/6684

- https://github.com/kubernetes-sigs/kueue/issues/6587#issuecomment-3342233971

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-27T17:42:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-26T18:38:41Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-25T18:41:58Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-25T18:42:04Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7029#issuecomment-3961250381):

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

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-09T20:58:10Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-09T20:58:17Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7029#issuecomment-4217432588):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-13T13:00:47Z

cc @mimowo @tenzen-y 

This is very similar to Slurm's concept of QoS. https://slurm.schedmd.com/qos.html#effects

This came up with some folks at the booth. 

I'm curious if you think there are other fields we would want to default based on LocalQueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-13T13:20:18Z

This sounds like a reasonable feature. I think anything that could be set at workload-level (but user), could also be defaulted by the LocalQueue (which is also often created by the user), for convenience.

Still, we need to answer some non-obvious questions: 
1. should we update the user-created Job based on the LQ, or just directly the workload object
2. could we design the feature more generically (label/ annotation defaulting based on the LQ), or just specific for this feature
3. what when the LQ is changed by the job, should we update/clear the default

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-13T13:31:14Z

> This sounds like a reasonable feature. I think anything that could be set at workload-level (but user), could also be defaulted by the LocalQueue (which is also often created by the user), for convenience.

Our rbac is set up so that a kueue-admin has the ability to create LocalQueues so I was thinking this could be some kind of admin level enforcement for time limits.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-13T13:32:15Z

> could we design the feature more generically (label/ annotation defaulting based on the LQ), or just specific for this feature

Yea that is one question I have. What other features do we think would be useful to include as LocalQueue defaulting? 

There was https://github.com/kubernetes-sigs/kueue/discussions/7129 which is similar in spirit.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-13T13:32:45Z

> what when the LQ is changed by the job, should we update/clear the default

Yes that makes sense to me. If someone changes a LQ does that trigger an readmission?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-14T16:50:04Z

> should we update the user-created Job based on the LQ, or just directly the workload object

I think modifying workload is good. My main reasoning is that for labels/annotations there is a poor enforcement of a policy. A user can remove those annotations/labels and there isn't much we can do.

At least if an admin sets a localQueue to have a timeout, it requires more effort to patch the workload object to remove the timeout.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-14T19:20:14Z

Opened up https://github.com/kubernetes-sigs/kueue/pull/10479
