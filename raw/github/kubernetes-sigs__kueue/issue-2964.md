# Issue #2964: Dynamic Job Parallelism and Resource Scaling Based on Backlog Metrics

**Summary**: Dynamic Job Parallelism and Resource Scaling Based on Backlog Metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2964

**Last updated**: 2025-09-14T22:42:44Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2024-09-03T06:13:11Z
- **Updated**: 2025-09-14T22:42:44Z
- **Closed**: 2025-09-14T22:42:43Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 14

## Description

**What would you like to be added**:

We would like to propose a new feature in Kueue that enables dynamic scaling of job parallelism and resource allocation (CPU, RAM, and pods) based on job backlog metrics and predefined formulas. 

Idea: This feature would introduce a custom resource definition (CRD) that allows users to define scaling formulas and thresholds, which dynamically adjust the maximum parallelism and resource limits, similar to KEDA or HPA. A generic approach could be the exposing of the `/scale` subresource to have a generic interface.

**Why is this needed**:

Currently, we are processing around 4.5 million jobs per day, and managing resource usage and costs is critical. There is a need for a mechanism that can dynamically limit or expand the maximum parallelism of jobs based on real-time backlog conditions. This would help ensure that jobs are processed efficiently without overcommitting resources or incurring unnecessary costs.

By introducing a formula-based approach to flavor resources, we can achieve a more granular and responsive system. For example, the system could increase the max CPU or RAM allocation as the admission backlog grows, ensuring that delays are minimized during high-load periods while conserving resources during low-demand times. This functionality is crucial for maintaining both performance and cost-effectiveness in large-scale Kubernetes environments.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T12:55:09Z

Reading the ask, I’m not entirely sure Kueue is the right place for this.

It sounds like you want metrics to influence elastic job scaling. AFAIK Kueue would help admit jobs based on dynamic scaling but I think the controller that looks at metrics and patches elastic jobs would probably be a separate CRD. I would think that this CRD would be separate from Kueue as it seems you want HPA at the job level.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T17:56:09Z

I'll leave the final decision on scope to @tenzen-y or @alculquicondor.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T19:01:54Z

> similar to KEDA or HPA

Why not just use KEDA or HPA?

I don't think Kueue is the right component to decide that.

Still there are two things that we need to do in Kueue to improve the experience:
- Support job resizing, which was started but not completed.
- Add any missing metrics about the length of the queues that can be fed into the external scaler.

And in Kubernetes:
- Support the `/scale` sub resource for jobs (if this is the API you are targeting).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T10:08:13Z

FYI the request to support dynamically scaled Jobs in Kueue: https://github.com/kubernetes-sigs/kueue/issues/77, it already has a KEP: https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-06T10:12:11Z

> FYI the request to support dynamically scaled Jobs in Kueue: #77, it already has a KEP: https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs

Yes, that's right. After we implement the feature, we may be able to use DynamicJob + Keda.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-05T10:39:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-05T17:47:47Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-05T17:51:16Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-04T17:54:19Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-17T21:28:07Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-16T21:54:42Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-15T22:39:51Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-14T22:42:38Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-14T22:42:44Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2964#issuecomment-3289985746):

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
