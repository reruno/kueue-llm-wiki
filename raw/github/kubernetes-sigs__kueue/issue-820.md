# Issue #820: [JobSet] Support partial admission

**Summary**: [JobSet] Support partial admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/820

**Last updated**: 2024-06-23T17:31:01Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-29T18:06:37Z
- **Updated**: 2024-06-23T17:31:01Z
- **Closed**: 2024-06-23T17:31:00Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support for partial admission in JobSet https://github.com/kubernetes-sigs/kueue/tree/main/keps/420-partial-admission

The open questions are:
- How to support resizing of multiple PodSets? Maximizing the size of one podset might imply reducing the size of another. Even if we have some priority to maximize the size of specific podsets, the problem is generally NP, so we might need to reduce the search space, or just limit the support to one PodSet.
- What to do if a Job is replicated? In this case, there are multiple options for sizing. But perhaps a replicated Job always has full size.

**Why is this needed**:

To be able to admit jobs of smaller size if this is acceptable to the application.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-29T18:06:50Z

@ahg-g @mwielgus for comment

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-05-31T19:26:52Z

I would opt for trying to keep things as simple as possible until we hear a strong push from the users. I'm worried that with couple of such features stacked together, it will be extremely hard to predict what should/would exactly happen. So maybe let's start with a single-dimension partial admission for one podset/replicatedjob and wait for user feedback?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-31T20:21:48Z

@trasc as FYI

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-06-01T02:50:10Z

I agree with @mwielgus, so I guess we validate that only one PodSet sets MinCount?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-01T12:04:47Z

Yes, that would be my preference.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-15T08:07:31Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-07-05T13:50:26Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-05T13:50:30Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/820#issuecomment-1621803851):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-07-19T08:56:46Z

@alculquicondor @mwielgus @ahg-g  #1001  describes what I believe we'll need in order to support this. 

Since the actual pod-set count for a jobset is `parallelism * replicas`  we can only decrement one of them, I think `replicas` should be the one changed.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T20:07:05Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T16:10:41Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-24T16:58:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-24T17:09:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-23T17:30:57Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-23T17:31:01Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/820#issuecomment-2185214814):

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
