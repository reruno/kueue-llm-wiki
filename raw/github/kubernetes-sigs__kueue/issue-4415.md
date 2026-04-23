# Issue #4415: Enable sorting of queue items based on a custom timestamp extracted from an annotation

**Summary**: Enable sorting of queue items based on a custom timestamp extracted from an annotation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4415

**Last updated**: 2025-08-26T11:04:43Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-02-26T12:55:54Z
- **Updated**: 2025-08-26T11:04:43Z
- **Closed**: 2025-08-01T23:35:37Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 11

## Description

**What would you like to be added**:

Enable sorting of queue items based on a custom timestamp extracted from an annotation.

**Why is this needed**:

Queuing plain pods created by Tekton can be highly beneficial for sharing quotas and achieving more consistent scheduling (FIFO based on the pod's creation timestamp). A short demo on this topic can be found [here](https://www.youtube.com/watch?v=lPWkvGHr6wI&t=3s).

The experience could be further improved by allowing pods in the queue to be sorted based on the creation timestamp of the Tekton PipelineRun they belong to.

This would prioritize pods associated with "older" pipelines, helping them complete first and reducing timeouts.

**Completion requirements**:

1. Kueue should be able to read a timestamp from an annotation set on the workload and use it for sorting workloads in the queue.

2. It should be possible to copy annotations from the Job to the Workload, similar to how labels can be copied.

3. Tekton should set the creation timestamp of the PipelineRun as an annotation on the pods belonging to that PipelineRun (this should be implemented in Tekton).

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-27T17:44:38Z

I am a bit confused.

https://cloud.google.com/kubernetes-engine/docs/tutorials/kueue-intro

This seems to say that we have support of FIFO for queueing.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-27T17:50:06Z

https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-27T18:26:18Z

We have received similar requests many times. However, we could not accept it since such custom timestamp could violate fairness. All workloads should be fair under the Kueue algorithms.

Such annotation allows evil users to prioritize their tasks.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-03-02T10:27:27Z

@tenzen-y thank you for your response. The feature I'm suggesting can be disabled by default and enabled by an administrator that would like it. The annotation on the Job which contains the cusotm timestamp, for example, can be protected by an admission web hook that will allow only specific controllers to set it or by using RBAC. Another example, in a multi tenant scenario, if each tenant has its own ClusterQueue, tenants can't prioritize their Workloads over other other tenants.

I think that the fact there were several similar requests is an indication for a real use case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T22:30:46Z

> The annotation on the Job which contains the cusotm timestamp, for example, can be protected by an admission web hook that will allow only specific controllers to set it or by using RBAC. 

I think the current priority and creation timestamp base queuing is a guardrail to keep consistency across all Kueue features.
If we allow them to disable it by this feature request, we will probably lose stability based on both development and User PoV.

> Another example, in a multi tenant scenario, if each tenant has its own ClusterQueue, tenants can't prioritize their Workloads over other other tenants.

Is there any reason why WorkloadPriorityClass and core PriorityClass do not satisfy this case?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-02T22:54:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-02T23:21:40Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-01T23:35:33Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-01T23:35:38Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4415#issuecomment-3146008914):

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-24T16:26:07Z

@tenzen-y would it be possible to use [AdmissionFairSharing](https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/) for this ask?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T11:04:43Z

> [@tenzen-y](https://github.com/tenzen-y) would it be possible to use [AdmissionFairSharing](https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/) for this ask?

I'm not sure since I'm not familiar with Tekton. The AFS orders the workloads in the queue based on the usage history.
