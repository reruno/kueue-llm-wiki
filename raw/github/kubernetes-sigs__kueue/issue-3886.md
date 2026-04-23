# Issue #3886: Supported job frameworks with TAS

**Summary**: Supported job frameworks with TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3886

**Last updated**: 2025-03-20T12:18:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2024-12-19T06:46:37Z
- **Updated**: 2025-03-20T12:18:26Z
- **Closed**: 2025-03-20T12:18:22Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

What's the current supported job frameworks with TAS, batch job etc., it will be great to list them under https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/.

**Why is this needed**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T06:50:14Z

Good idea! We could also elaborate a bit more on how to use it for Pod Groups with rank-based ordering.
cc @mwysokin @PBundyra

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-19T06:56:04Z

Can you give a short summary about the job framework support right now? @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T07:05:33Z

Sure, the baseline TAS is supported in all Jobs which call `jobframework.PodSetTopologyRequest`: https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue+jobframework.PodSetTopologyRequest&type=code. AFAIK this are all workloads: Job, JobSet, Kubeflow, Ray, Pod Groups.

The rank-based ordering is an enhancement on top of that available for Jobs which call this function with the label indexing the pods, such as [here](https://github.com/kubernetes-sigs/kueue/blob/f98a2f99d49e0ffcd8c8c7515e1328ffd398f1c9/pkg/controller/jobs/kubeflow/kubeflowjob/kubeflowjob_controller.go#L108) for Kubeflow. To make rank-based ordering for PodGroups we introduced a dedicated label called "pod-group-pod-index". Moreover, for more flexibility we have "pod-group-pod-index-label" which indicates another third-party label which might be indexing the pods. 

I think RayJob and RayCluster currently don't support rank-based ordering, but it might be an omission.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T07:06:34Z

cc @andrewsykim are the pods created by RayJob or RayCluster indexed by a label or annotation?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-19T08:17:39Z

Thanks, we mostly want to try this with Kubeflow jobs.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-12-20T00:43:07Z

> cc @andrewsykim are the pods created by RayJob or RayCluster indexed by a label or annotation?

No, is this required for TAS?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-20T08:08:05Z


> 
> No, is this required for TAS?
> 

It is not required to use TAS in general. However if pods are indexed, TAS will place neighbouring pods next to each other if properly configured

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-20T08:57:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-20T12:18:18Z

This is described in https://kueue.sigs.k8s.io/docs/overview/#job-integrated-features

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-20T12:18:25Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3886#issuecomment-2740271263):

>This is described in https://kueue.sigs.k8s.io/docs/overview/#job-integrated-features
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
