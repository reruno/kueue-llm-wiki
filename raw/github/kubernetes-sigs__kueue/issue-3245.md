# Issue #3245: Add timeout mechanism to ProvisioningRequest controller

**Summary**: Add timeout mechanism to ProvisioningRequest controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3245

**Last updated**: 2026-02-20T13:30:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-10-16T15:03:50Z
- **Updated**: 2026-02-20T13:30:20Z
- **Closed**: 2026-02-20T13:30:19Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add mechanism to ProvisioningRequest controller that would allow user to cap the time ClusterAutoscaler spends on retrying ProvisioningRequest

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-14T15:33:08Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-14T15:46:37Z

/remove-lifecycle stale

### Comment by [@fg91](https://github.com/fg91) — 2025-03-18T09:15:17Z

This would be a really helpful feature. Sometimes provisioning requests are accepted but then not provisioned for more than a day. Manually deleting and restarting the workload often leads to almost instant scheduling. It would be good if kueue had a timeout for the provisioning request after which it creates a new prov req attempt.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-18T10:53:44Z

Thanks for feedback @fg91!
If you wanted to limit time CA spends on retrying ProvisioningRequest completely, you can configure Kueue to use `noRetry` parameter https://github.com/kubernetes/autoscaler/pull/7496
This way, CA processes a ProvisioningRequest only once, and marks it as failed if it cannot succeed immediately. Then retry on Kueue happens with respect to the `.retryStrategy` config https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#provisioningrequestconfig

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-16T11:49:19Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-16T13:37:10Z

/remove-lifecycle stale

### Comment by [@fg91](https://github.com/fg91) — 2025-06-25T10:21:21Z

> Thanks for feedback [@fg91](https://github.com/fg91)! If you wanted to limit time CA spends on retrying ProvisioningRequest completely, you can configure Kueue to use `noRetry` parameter [kubernetes/autoscaler#7496](https://github.com/kubernetes/autoscaler/pull/7496) This way, CA processes a ProvisioningRequest only once, and marks it as failed if it cannot succeed immediately. Then retry on Kueue happens with respect to the `.retryStrategy` config https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#provisioningrequestconfig

Thanks for the suggestion!
I'm not looking for a way to cap the time CA spends on retrying provisioning requests *that fail* but rather configure how long to wait for provisioning after the provisioning request has been accepted before considering the request failed. (In order to then retry a new request.)

I sometimes see requests that are accepted but aren't provisioned in > 2 days. If I manually delete the workload and retry, they typically are accepted and provisioned immediately. This happens seldomly but it does happen often enough for me to wish there was a mechanism in Kueue to handle these cases.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-23T10:36:52Z

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

### Comment by [@fg91](https://github.com/fg91) — 2025-09-23T10:44:28Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T11:44:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-21T12:33:33Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-20T13:30:13Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-20T13:30:20Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3245#issuecomment-3934628408):

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
