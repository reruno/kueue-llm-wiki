# Issue #6230: Partially update a pod of a workload

**Summary**: Partially update a pod of a workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6230

**Last updated**: 2025-12-28T18:42:53Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@chunyang-wen](https://github.com/chunyang-wen)
- **Created**: 2025-07-29T08:00:25Z
- **Updated**: 2025-12-28T18:42:53Z
- **Closed**: 2025-12-28T18:42:52Z
- **Labels**: `kind/support`, `triage/needs-information`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

we have a workload which has 4 pods inside. Is it supported in kueue that when part of the pod failed, kueue just create a new pod to replace it?

A workload works as a whole. We can't just change only one of the pods.


We have a  case where we recreate only 3 of the pods and 1 pod from last time is still running. The 3 pods are stuck in creation.

When checking the workload, it seems i needs 4 pods and 4 pods are ready. But the 3 pods is just stuck there.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-29T12:41:16Z

What integration are you using?

If you are using pod-integration Kueue will not recreate new pods.

The recommendation would be to use a higher level worklaod like Deployment, StatefulSet, Job, or JobSet for this.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-31T17:39:09Z

/triage needs-information

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-29T18:21:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-28T18:23:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-28T18:42:47Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-28T18:42:53Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6230#issuecomment-3694953451):

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
