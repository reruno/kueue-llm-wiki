# Issue #4336: Metric Request: Can we add a metric for report the integrations that Kueue is configured with?

**Summary**: Metric Request: Can we add a metric for report the integrations that Kueue is configured with?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4336

**Last updated**: 2025-07-24T23:21:54Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-20T19:26:57Z
- **Updated**: 2025-07-24T23:21:54Z
- **Closed**: 2025-07-24T23:21:53Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A metric that will reports the integrations that Kueue is using

**Why is this needed**:

As we roll Kueue out to clusters, we would like to be able to see what kind of workloads people are using with Kueue.

It would be great to have a telemetry service that allows our product team to know what kind of workloads people are using with Kueue. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-21T10:53:00Z

I'm not sure if metrics is the correct technical solution for the use-case. 

Also, are you interested which integrations are configured, or which are actually used, because I see some disconnect between the title and the description: " report the integrations that Kueue is configured with" vs "to be able to see what kind of workloads people are using with Kueue.". 

Also, are you more interested in the metrics "point in time - guage" , or cummulative?

Could you propose some particular metrics to give them for discussion?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-21T14:05:04Z

I was thinking just a list of the integrations Kueue is configured with. But it may actually be worth having a counter of each framework to see what workloads are actually being used.

Maybe a metric per supported framework with a count of the workload?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-21T16:50:31Z

Opened up https://github.com/kubernetes-sigs/kueue/pull/4350 for discussion.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-22T17:34:53Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-24T23:05:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-24T23:21:49Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-24T23:21:54Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4336#issuecomment-3115308509):

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
