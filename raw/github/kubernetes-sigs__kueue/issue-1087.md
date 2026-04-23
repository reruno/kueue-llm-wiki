# Issue #1087: A sample for out-of-tree integrations and a directory for experimental integrations

**Summary**: A sample for out-of-tree integrations and a directory for experimental integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1087

**Last updated**: 2024-03-27T14:40:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-29T18:52:06Z
- **Updated**: 2024-03-27T14:40:21Z
- **Closed**: 2024-03-27T14:40:19Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A directory structure that allow us to host code for integrations with Kueue that are not part of the main binary.

**Why is this needed**:

This would allow:

- a sample for how to write out-of-tree integrations
- experimental integrations: integrations without long term support or that might otherwise have some caveats

A useful sample could be pod support using taints and tolerations. This is not a good candidate for long term support, as we already have a better mechanism using scheduling gates. But otherwise, the sample could be useful for users who can't upgrade to 1.27 yet.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-29T18:52:26Z

cc @tenzen-y @kerthcet 
Any concerns or ideas for interesting samples?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-29T19:21:13Z

Basically, this idea sounds good to me. However, I would suggest using a separate go module and establishing policies for maintenance. This means:

1. Using separate go module: I would like to avoid the experimental integrations as an obstacle to upgrading the main binary dependencies. In my experience, experimental codes are prone to abandonment, which can block improvement for the major features.
2. Establishing policies for maintenance: I would like to define the duration (maybe a year or 3 minor releases?) that we maintain the experimental integrations to avoid holding many non-maintained integrations. If the experimental integrations are used by many users, we can consolidate the experimental one with the main binary.

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-29T19:38:42Z

That's great feedback. I included it in the README in #1088

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-08-30T03:58:31Z

Make sense to me to reduce the maintenance cost, also the stability. A general question is how to determine a job is in-tree or out-of-tree then, based on the popularity? 

And I think we may have to provide some test libraries for integration/e2e tests with kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-30T12:32:32Z

> A general question is how to determine a job is in-tree or out-of-tree then, based on the popularity?

That could be one criteria. The other could be how long the contributor that is proposing it has been in the project. There should be some idea that they will help maintain the integration long term, for it to be in-tree.

> And I think we may have to provide some test libraries for integration/e2e tests with kueue.

I think they might be able to reuse the existing packages. But overall, we could allow code in the experimental directory to merge with much less testing. Maybe we can have a README for each folder similar to https://github.com/kubernetes-sigs/scheduler-plugins/blob/master/pkg/capacityscheduling/README.md

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-27T07:43:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-26T08:36:27Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-27T09:24:18Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-27T09:24:22Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1087#issuecomment-2022293926):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T14:39:46Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-27T14:39:49Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1087#issuecomment-2022943760):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T14:40:14Z

We can consider this as completed by #1092.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-27T14:40:19Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1087#issuecomment-2022944845):

>We can consider this as completed by #1092.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
