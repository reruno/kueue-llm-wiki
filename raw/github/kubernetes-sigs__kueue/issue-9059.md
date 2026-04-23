# Issue #9059: KubeRay integration: Support RayService as a top-level Job

**Summary**: KubeRay integration: Support RayService as a top-level Job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9059

**Last updated**: 2026-02-24T17:24:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-09T13:18:00Z
- **Updated**: 2026-02-24T17:24:43Z
- **Closed**: 2026-02-24T07:01:38Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to introduce support for RayService as a top-level Job, rather than via RayCluster.

**Why is this needed**:

To support dispatching RayService via MultiKueue, see related effort in KubeRay: https://github.com/ray-project/kuberay/issues/4486


Currently RayService can only be managed by Kueue at the RayCluster level, see https://kueue.sigs.k8s.io/docs/tasks/run/rayservices/ but this solution does not transfer fully to MultiKueue, because then the Gateway is not created on the worker cluster.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T13:19:24Z

cc @hiboyang @andrewsykim

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T13:20:37Z

/assign @hiboyang
Tentatively as Bo is already driving the effort.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-09T13:20:41Z

@mimowo: GitHub didn't allow me to assign the following users: hiboyang.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9059#issuecomment-3871669506):

>/assign @hiboyang
>Tentatively as Bo is already driving the effort.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2026-02-09T14:15:48Z

should we also consider autoscaler's case?

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2026-02-09T14:16:56Z

I mean right now kueue works well with rayservice CR, but actually kueue didn't have rayserivce controller, we rely on raycluster controller, it is a little bit hacky IMO.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T15:03:19Z

@Future-Outlier I need more context to better understand the questions, can you please elaborate? 

For now, the main usecase for making RayService top-level is MultiKueue. Here it is necessary to make sure Gateway is created on the worker cluster.

If we have more use-cases opened by this change, then great!

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-09T17:22:11Z

Yes, will be great to have RayService as top-level job to support MultiKueue. I will work on this, or chat with our internal team, to figure out people to work on this.

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2026-02-10T01:45:11Z

Hi @mimowo,
In this folder we don’t have a RayService controller. It still works, but the structure looks a bit odd. Are we planning to add a RayService controller here?
https://github.com/kubernetes-sigs/kueue/tree/9a1de0101409e94adf3bc6ccc4e02831f587f987/pkg/controller/jobs

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T06:03:16Z

iiuc you say weird because the service controller will be in the job folder?

Yes, this is because Kueue historically we supported batch workloads, thus we introduced Job framework. Since then we havent figured out a better name than Job for whatever Kueue is managing.

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2026-02-10T06:57:37Z

> iiuc you say weird because the service controller will be in the job folder?
> 
> Yes, this is because Kueue historically we supported batch workloads, thus we introduced Job framework. Since then we havent figured out a better name than Job for whatever Kueue is managing.

got it, thank you

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-16T22:19:40Z

I got basic working with RayService as top level job: https://github.com/kubernetes-sigs/kueue/pull/9102

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T11:40:16Z

/reopen
This yet requires making sure the rayservice is enabled in the integrations, or at least added there as disabled (commented out). 

Also, I would expect documentation before we can close.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-23T11:40:22Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9059#issuecomment-3944264759):

>/reopen
>This yet requires making sure the rayservice is enabled in the integrations, or at least added there as disabled (commented out). 
>
>Also, I would expect documentation before we can close.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-24T17:24:42Z

> /reopen This yet requires making sure the rayservice is enabled in the integrations, or at least added there as disabled (commented out).
> 
> Also, I would expect documentation before we can close.

This PR https://github.com/kubernetes-sigs/kueue/pull/9430 enabled rayservice in the integration:
```
    integrations:
      frameworks:
      - "batch/job"
      - "kubeflow.org/mpijob"
      - "ray.io/rayjob"
      - "ray.io/rayservice"
      - "ray.io/raycluster"
      - "jobset.x-k8s.io/jobset"
      - "trainer.kubeflow.org/trainjob"
```

Will create a follow-up PR to update RayService doc
