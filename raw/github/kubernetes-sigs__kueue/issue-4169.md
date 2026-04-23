# Issue #4169: Support partial scale-down in RayJob

**Summary**: Support partial scale-down in RayJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4169

**Last updated**: 2025-07-10T18:43:53Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@eric-higgins-ai](https://github.com/eric-higgins-ai)
- **Created**: 2025-02-07T03:35:08Z
- **Updated**: 2025-07-10T18:43:53Z
- **Closed**: 2025-07-10T18:43:52Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

**What would you like to be added**:
Currently the `RayJob` admission webhook returns an error when the job sets `enableInTreeAutoscaling: true`. It makes sense that autoscaling up isn't supported, but I would expect autoscaling down could be supported via the "dynamic reclaim" feature.

I'd potentially be down to implement this - I just wanted to open an issue to see how people feel about this feature before spending time on it.

**Why is this needed**:
We want to run hyperparameter sweeps with Ray Tune, and they have a feature that allows early exiting from trials based on metric values. With this, it's possible that at some point the job doesn't need all the resources it was initially given (because most trials have finished), and we'd like to be able to reclaim those resources.

**Completion requirements**:
`RayJob`s support dynamic reclaiming if the Ray autoscaler indicates the job should scale down

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-07T06:49:40Z

>  It makes sense that autoscaling up isn't supported, but I would expect autoscaling down could be supported via the "dynamic reclaim" feature.

Potentially, we also have a design (not implemented) for generic (any CRD) dynamic Jobs in https://github.com/kubernetes-sigs/kueue/issues/77. Maybe it is time to prioritize that work.

cc @mwielgus @mwysokin @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-10T16:46:34Z

> > It makes sense that autoscaling up isn't supported, but I would expect autoscaling down could be supported via the "dynamic reclaim" feature.
> 
> Potentially, we also have a design (not implemented) for generic (any CRD) dynamic Jobs in [#77](https://github.com/kubernetes-sigs/kueue/issues/77). Maybe it is time to prioritize that work.
> 
> cc [@mwielgus](https://github.com/mwielgus) [@mwysokin](https://github.com/mwysokin) [@tenzen-y](https://github.com/tenzen-y)

Yeah, I think so too. Could we prioritize this after the next minor release (0.12)? Because we have a lot of alpha features and trying to fix bugs in this release cycle. This seems to be a slightly big feature.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-11T17:06:22Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T17:55:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-10T18:43:47Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-10T18:43:53Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4169#issuecomment-3058553776):

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
