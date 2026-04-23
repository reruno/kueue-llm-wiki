# Issue #7: Add info to ClusterQueue status

**Summary**: Add info to ClusterQueue status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7

**Last updated**: 2022-03-11T21:14:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:11:46Z
- **Updated**: 2022-03-11T21:14:44Z
- **Closed**: 2022-03-11T21:14:44Z
- **Labels**: `kind/feature`, `help wanted`, `priority/important-soon`, `size/M`
- **Assignees**: _none_
- **Comments**: 19

## Description

Suggestions:
- [x] admitted workloads
- [x] pending workloads
- [x] Capacity allocated
- [x] Capacity borrowed

/kind feature

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T19:15:20Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-01T22:01:25Z

Should we add pending workloads to capacity as well?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-01T22:17:19Z

Aggregating the sizes of all the queues pointing to it? We should be able to implement that efficiently, but could it be confusing?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-01T22:59:26Z

Why would it be confusing? The pending workloads at a queue level isn't really that useful i would say for an admin to look at compared to an aggregated view at the capacity level

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:11:24Z

/reopen

Sounds good. Although I will tackle this after https://github.com/kubernetes-sigs/kueue/pull/80#issuecomment-1057113242

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-02T18:11:36Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7#issuecomment-1057230392):

>/reopen
>
>Sounds good. Although I will tackle this after https://github.com/kubernetes-sigs/kueue/pull/80#issuecomment-1057113242


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T19:52:14Z

I strongly disagree with 

>The pending workloads at a queue level isn't really that useful 

For users, is the most important after deploying, if queues are going to be a user managed object, we need to provide as much valuable information to them at the namespace lvl.

As an admin all I care is big numbers and usage. I think we are looking at this with an admin/cloud provider point of view and not from the end user. 

we need to think as a cascade here 

CQ -> Q -> QW

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T19:53:19Z

`pending workloads at a queue level` are one of THE most important reasons why people want to have a queuing mechanism in kubernetes.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T19:54:41Z

/retitle Add info to ClusterQueue status

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T20:10:41Z

sg, I already proposed a way to track the number of admitted workloads at Q level

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T20:12:14Z

oh, you are referring to the count of pending workloads; I guess I agree in general the the more info we can surface the better

### Comment by [@xieydd](https://github.com/xieydd) — 2022-03-09T10:46:22Z

I agree with the  comment from @ArangoGutierrez . 
Considering the cascade of CQ, Q and QW, we need the more info we can of workload , we can aggregate some info for Q and CQ.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-09T11:19:12Z

sg, then with regards to this issue we need two things in CQ status:

- [x] Rename AssignedWorkloads to AdmittedWorkloads
- [ ] Pending workloads

/help
/unassign @alculquicondor

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-09T11:19:13Z

@ahg-g: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7):

>sg, then with regards to this issue we need two things in CQ status:
>
>- [ ] Rename AssignedWorkloads to AdmittedWorkloads
>- [ ] Pending workloads
>
>/help
>/unassign @alculquicondor 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T01:40:21Z

> sg, then with regards to this issue we need two things in CQ status:
> 
> * [ ]  Rename AssignedWorkloads to AdmittedWorkloads
> * [ ]  Pending workloads
> 
> /help /unassign @alculquicondor

Check first one #110

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T20:12:59Z

For `Pending workloads` do we still want to track that on kueue.clusterqueue.Status? 
as it is right now, a workload has to be admitted into a clusterqueue, so to the eyes of clusterqueue it is never pending, pending feels better at the kueue.queue lvl, tracking workloads that have not yet been admitted, right? 
if yes we can close this issue as done, and focus on #5 only

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T20:33:20Z

Pending workloads are the workloads that are still in the heap, so they haven't been admitted.

Yes, we should add that field to clusterQueue.status

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-11T21:14:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-11T21:14:44Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7#issuecomment-1065534588):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
