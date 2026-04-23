# Issue #5704: MultiKueue: Support cluster role sharing (worker and manager inside one cluster)

**Summary**: MultiKueue: Support cluster role sharing (worker and manager inside one cluster)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5704

**Last updated**: 2026-04-16T11:43:19Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-20T16:23:55Z
- **Updated**: 2026-04-16T11:43:19Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to support the cluster role sharing functionality for MultiKueue.

**Why is this needed**:

This allows us to reduce the number of managed clusters, which mitigates the operation costs for admins.

Indeed, the blocker for this feature request was mostly resolved by JobManagedBy feature and almost major Job integrations like Kubeflow and Ray support the managedBy functionality as well.

> Support for cluster role sharing (worker & manager inside one cluster) is out of scope for this KEP. We will get back to the topic once https://github.com/kubernetes/enhancements/pull/4370 is merged and becomes a wider standard.

https://github.com/kubernetes-sigs/kueue/tree/main/keps/693-multikueue#non-goals

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T16:25:49Z

cc @mimowo @mwielgus @gabesaba @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T16:42:00Z

> Indeed, the blocker for this feature request was mostly resolved by JobManagedBy feature and almost major Job integrations like Kubeflow and Ray support the managedBy functionality as well.

Yeah, it feels that on clusters with 1.32+, with managedBy, it is already supported. We can have one CQ using MK and another CQ not.

Unless I'm missing something it feels like just about adding tests and updating the KEP.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T16:46:15Z

> Yeah, it feels that on clusters with 1.32+, with managedBy, it is already supported. We can have one CQ using MK and another CQ not.
> 
> Unless I'm missing something it feels like just about adding tests and updating the KEP.

I hope that. Let us check the actual behavior!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T18:59:44Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-27T19:02:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T19:04:55Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T18:39:49Z

I think @IrvingMg @mszadkow has a lot of experience setting up MultiKueue so can easily check that

Basically, we can have one CQ using MultiKueue and on the same cluster another CQ using the local cluster.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-14T21:10:10Z

> I think [@IrvingMg](https://github.com/IrvingMg) [@mszadkow](https://github.com/mszadkow) has a lot of experience setting up MultiKueue so can easily check that
> 
> Basically, we can have one CQ using MultiKueue and on the same cluster another CQ using the local cluster.

If @IrvingMg or @mszadkow has enough bandwidth, feel free to take this issue.
It would be great if we can such integration or E2E tests to verify the behavior.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-18T08:27:16Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T08:35:53Z

I'm also fine with either integration or e2e tests, I would probably suggest to start with integration tests as easier to write and debug, and see where we are.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-18T15:00:34Z

> I'm also fine with either integration or e2e tests, I would probably suggest to start with integration tests as easier to write and debug, and see where we are.

SGTM

/unassign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-20T14:18:34Z

I was able to run the tests in GKE.

Manager cluster 
workloads:
job-sample-job-b49sg-50a94   user-queue-single   cluster-queue-single   True       True       78s
job-sample-job-h4ds2-cf483   user-queue          cluster-queue          True       True       82s

jobs:
sample-job-b49sg   Complete   3/3           67s        2m22s
sample-job-h4ds2   Complete   3/3           79s        2m25s

Also, I noticed there is no `admittedWorkloads`, even though there were... (or maybe it's cleared after the job is finished?)
NAME                   COHORT   STRATEGY         PENDING WORKLOADS   ADMITTED WORKLOADS
cluster-queue                   BestEffortFIFO   0                   0
cluster-queue-single            BestEffortFIFO   0                   0

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T14:31:53Z

> or maybe it's cleared after the job is finished?)

Yes, we only count non-finished admitted workloads:
https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1beta2/clusterqueue_types.go#L541

says **Number of admitted workloads that haven't finished yet**

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T08:54:42Z

@mszadkow please also update the documentation to say that the hybrid mode is supported. By hybrid (or role sharing) we mean the manager cluster taking the role of the manger, but also running some jobs in another CQ.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T09:40:52Z

I will follow with:
- e2e test for manager
- documentation of this feature

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-08T09:27:59Z

> I will follow with:
> 
> * e2e test for manager
> * documentation of this feature

@mimowo @tenzen-y is there anything left for this ticket?
I recall this discussion - https://github.com/kubernetes-sigs/kueue/pull/8035#issuecomment-3612681074, thus the question

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T10:41:26Z

Yes, it requires design how to support the case. One idea is that the manager cluster would create local copies of the workload in another CQ.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:27:37Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:20Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:50:51Z

/remove-lifecycle stale

### Comment by [@khrm](https://github.com/khrm) — 2026-04-16T11:43:19Z

Based on the last WG call. We can have
1. Adding the manager as a worker.
2. Copying the job with a different name. This ensures that we can copy to the manager without mutating `managedBy` field.


Problem with 2: It might not be compatible with everything. Let's say we copied and then ran for some part. Then it got evicted. The status might change if we assign the job to a different worker with different name again.
 




One other challenge that remains is how do we avoid the MultiKueue admission check after the job is copied to the manager again?


- @mimowo
