# Issue #635: Hybrid mode in a single cluster: services + batch

**Summary**: Hybrid mode in a single cluster: services + batch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/635

**Last updated**: 2024-06-17T20:00:54Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-15T15:54:00Z
- **Updated**: 2024-06-17T20:00:54Z
- **Closed**: 2024-06-17T20:00:52Z
- **Labels**: `kind/feature`, `lifecycle/rotten`, `kind/grand-feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 10

## Description

**What would you like to be added**:

The ability to account for quota usage coming from service pods (Deployment, Daemonset, Statefulset, etc).

**Why is this needed**:

In on-prem clusters or cloud clusters with reservations, organizations want to schedule jobs on the valleys of usage by services.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T15:54:08Z

/kind grand-feature

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-03-24T15:47:01Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2023-05-05T12:21:34Z

So currently we assume that queuing is only valid for finite jobs but is there a consideration that we would want Kueue to work for services also?

ie have other apps objects have a suspend field?

I know that yunikorn/MCAD allow for queuing/scheduling of services in addition to batch workloads

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-05T12:42:03Z

Not necessarily queuing, but accounting for their usage.

The use case is hybrid clusters where you are running most services during the day, and there are valleys at night that can be used by jobs.

This is useful in fixed size clusters. But on the cloud, you could just have 2 separate clusters (one for services and one for jobs) and have autoscaling in both.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-19T18:02:02Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-19T18:45:46Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-18T19:23:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-18T19:51:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-17T20:00:48Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-17T20:00:52Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/635#issuecomment-2174320099):

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
