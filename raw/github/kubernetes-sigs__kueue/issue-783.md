# Issue #783: [RayJob] Add support for partial admission.

**Summary**: [RayJob] Add support for partial admission.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/783

**Last updated**: 2024-06-23T17:31:03Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-05-19T08:36:26Z
- **Updated**: 2024-06-23T17:31:03Z
- **Closed**: 2024-06-23T17:31:00Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add support for partial admission for RayJobs. Check #420 and https://github.com/kubernetes-sigs/kueue/pull/667/files#r1198519116 for detail.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-19T13:52:41Z

FYI, we don't need a new KEP, but you can add the details to the existing one.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-19T02:57:11Z

Hi all, what's left here, our team is interested with the integration with rayJob ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-19T07:30:33Z

IIRC, we don't support partial admission on RayJob, now.
So, we need to implement `minPodsCount` and then modify functions for RayJob  based on `minPodCount` like this:

https://github.com/kubernetes-sigs/kueue/blob/f215a43a7be9b3c2788e00ec03c130b8fbc053b5/pkg/controller/jobs/job/job_controller.go#L279-L286

https://github.com/kubernetes-sigs/kueue/blob/f215a43a7be9b3c2788e00ec03c130b8fbc053b5/pkg/controller/jobs/job/job_controller.go#L199-L208

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-19T08:48:54Z

Thanks @tenzen-y for the feedbacks. cc @BinL233

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-19T14:48:54Z

@kerthcet can you share how heterogeneous your Ray jobs are?

I wonder if we can simplify support for partial admission by restricting it to one podset. Otherwise it's an NP problem.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-20T06:55:38Z

We're still exploring this, but we found the rayCluster's autoscaling is complex, and maybe that's out of the scope of kueue but related to cluster-autoscaler. It's recommended by the ray community as 1 pod(raynode) : 1 node. 

Some phenomenons like when we don't have enough resources for autoscaling, the rayjob will hang forever, although part of its tasks finished, the resources will not be reclaimed. Then I think kueue can do little here ..

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T23:10:00Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T16:11:31Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-25T16:18:44Z

cc @astefanutti @vicentefb @andrewsykim in case you have interest on this.

Partial admission is different from elastic in that, during admission, Kueue decides to give a smaller size to the RayJob and the job runs like this until it completes.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-24T16:58:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-24T17:09:16Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/783#issuecomment-2185214820):

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
