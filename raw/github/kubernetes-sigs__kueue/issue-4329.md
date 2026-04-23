# Issue #4329: Kueue scheduler fragmentation optimization

**Summary**: Kueue scheduler fragmentation optimization

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4329

**Last updated**: 2025-07-24T20:18:55Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@shaowei-su](https://github.com/shaowei-su)
- **Created**: 2025-02-19T18:00:31Z
- **Updated**: 2025-07-24T20:18:55Z
- **Closed**: 2025-07-24T20:18:54Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
In the current Kueue implementation, each queue resources are simply added up (e.g total of 8 GPUs) without the awareness of the actual topology (e.g 1 * 8 vs 2 * 4). As a result, Kueue would admit workload that "admittable" but cannot be scheduled at runtime. This wrongly admitted workload would pending indefinitely until previously workloads free up the resources, while blocking any new workload that could have been running (e.g requesting single GPU) from running. As a result, the fragmentation issue would lead to low cluster allocation rate overall.

The suggested solution would be re-schedule if the fragmentation issue happens, and permit future workloads that immediately schedulable to be admitted.

**Why is this needed**:
Further improve the cluster allocation rate.

**Completion requirements**:
N/A

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T18:08:40Z

You might be intersted in TopologyAwareScheduling: https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/

Note that this feature is still alpha.

### Comment by [@shaowei-su](https://github.com/shaowei-su) — 2025-02-19T18:17:44Z

Thanks @tenzen-y ! I'm not aware of this alpha feature, checking it out now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T18:20:05Z

> Thanks [@tenzen-y](https://github.com/tenzen-y) ! I'm not aware of this alpha feature, checking it out now.

Does TAS satisfy your request?

### Comment by [@shaowei-su](https://github.com/shaowei-su) — 2025-02-19T19:36:38Z

Hey @tenzen-y , I read through the docs - it looks like TAS is addressing the static cluster topology (racks, blocks etc..), but the challenge in this issue is mostly around runtime deployment topology (i.e how many available resources per node at the scheduling time). So I'm afraid TAS alone won't solve this issue, but please correct me if I'm wrong.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T19:38:56Z

> Hey [@tenzen-y](https://github.com/tenzen-y) , I read through the docs - it looks like TAS is addressing the static cluster topology (racks, blocks etc..), but the challenge in this issue is mostly around runtime deployment topology (i.e how many available resources per node at the scheduling time). So I'm afraid TAS alone won't solve this issue, but please correct me if I'm wrong.

In that case, you can use flat topology by `"kubernetes.io/hostname"`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T19:42:40Z

> > Hey [@tenzen-y](https://github.com/tenzen-y) , I read through the docs - it looks like TAS is addressing the static cluster topology (racks, blocks etc..), but the challenge in this issue is mostly around runtime deployment topology (i.e how many available resources per node at the scheduling time). So I'm afraid TAS alone won't solve this issue, but please correct me if I'm wrong.
> 
> In that case, you can use flat topology by `"kubernetes.io/hostname"`.

If you specify "kubernetes.io/hostname" for topology, Kueue traverses all Node's allocatable resources, and packing Pods as much as possible to nodes (similar to kube-scheduler mostAllocated).

### Comment by [@shaowei-su](https://github.com/shaowei-su) — 2025-02-19T20:38:04Z

Thanks, we'll test this out and keep this issue updated.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-19T21:10:50Z

> Thanks, we'll test this out and keep this issue updated.

I would recommend using the main branch to confirm all features for TAS since only the main branch is guaranteed to support obviously "mostAllocated" scheduling. The older released versions do not support obviously "mostAllocated" scheduling.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-20T21:19:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-24T20:04:51Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-24T20:18:51Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-24T20:18:55Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4329#issuecomment-3114804063):

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
