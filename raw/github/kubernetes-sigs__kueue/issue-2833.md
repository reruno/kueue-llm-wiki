# Issue #2833: Easy way to figure out other workloads that are pending / admitted

**Summary**: Easy way to figure out other workloads that are pending / admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2833

**Last updated**: 2024-11-12T08:53:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samos123](https://github.com/samos123)
- **Created**: 2024-08-13T16:37:54Z
- **Updated**: 2024-11-12T08:53:29Z
- **Closed**: 2024-11-12T08:53:13Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**: Easy way to figure out other workloads that are pending / admitted

**Why is this needed**: As a workload owner my job went into pending state because there are other workloads admitted and in pending state. I want to know the following things:
* what are the names of the other workloads in pending and admitted state
* who submitted the workload
* how much resources are taken by each of the workloads

The reason is that I want to get an understanding of when my job may run and notify the other workload owners if needed.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-08-14T06:13:41Z

The easiest way to get a workload's position in the queue is to use [kueuectl list workload](https://kueue.sigs.k8s.io/docs/reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload/) which hase a `POSITION IN QUEUE` column.

For more details you can also check [Monitor pending Workloads](https://kueue.sigs.k8s.io/docs/tasks/manage/monitor_pending_workloads/) section.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-12T06:45:00Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-12T08:53:08Z

/close
Closing since the main use-case of:

> The reason is that I want to get an understanding of when my job may run

Is already addressed as explained in https://github.com/kubernetes-sigs/kueue/issues/2833#issuecomment-2287936324. 

> and notify the other workload owners if needed.

This part isn't done yet, but its importance isn't that clear yet. 

Also, it isn't clear what the other owners should do with that knowledge - if they run lower priority Jobs which should be stopped, then the right mechanism to do it is to use [workload priorities](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/). Then, Kueue will automatically preempt the lower priority workloads.

We can still open a dedicated issue or re-open this if this remains needed for some.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-12T08:53:13Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2833#issuecomment-2469937544):

>/close
>Closing since the main use-case of:
>
>> The reason is that I want to get an understanding of when my job may run
>
>Is already addressed as explained in https://github.com/kubernetes-sigs/kueue/issues/2833#issuecomment-2287936324. 
>
>> and notify the other workload owners if needed.
>
>This part isn't done yet, but its importance isn't that clear yet. We can still open a dedicated issue or re-open this if this remains needed for some.
>
>Also, it isn't clear what the other owners should do with that knowledge - if they run lower priority Jobs which should be stopped, then the right mechanism to do it is to use [workload priorities](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/). Then, Kueue will automatically preempt the lower priority workloads.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
