# Issue #485: Manage number of pods in ClusterQueues

**Summary**: Manage number of pods in ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/485

**Last updated**: 2023-05-03T13:22:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-21T15:18:21Z
- **Updated**: 2023-05-03T13:22:15Z
- **Closed**: 2023-05-03T13:22:15Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 23

## Description

**What would you like to be added**:

Mark jobs that don't have requests as inadmissible.

**Why is this needed**:

Kueue is a system that manages resource usage. It doesn't really make sense to have jobs with no requests.

Also, it can lead to user errors, such as having a resource flavor with nodeSelectors that are never applied to jobs. This is WAI: the job has no requests, so it gets no flavors and no injected node selectors. But it's confusing. Simply requiring that the jobs have requests would prevent that.

I thought about doing this via webhooks. However, this has the problem that in some clusters requests might be added via webhooks. Since it's not possible to reliably establish the order in which webhooks run, we might be breaking this use cases.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T15:19:47Z

@kerthcet @ahg-g, any concerns?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-21T17:04:43Z

One scenario I can think of is scheduling tiny jobs for best effort like we do for pods, but as you said we may have no flavors for them unless we have a default one injected. Following YAGNI, I agree to start with a strict restriction. 

Instead of marking job inadmissible, or reject the management by kueue directly and tell users the reasons. I found job's resources is immutable after creation, if so, make it inadmissible seems useless, we have to recreate them.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-12-21T17:51:29Z

> Mark jobs that don't have requests as inadmissible.

what is the behavior now for those jobs?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T18:50:21Z

> One scenario I can think of is scheduling tiny jobs for best effort like we do for pods.

A good practice there would be to give them at least some CPU and memory, like 50m cores and 1Mi, for example.

> Instead of marking job inadmissible, or reject the management by kueue directly and tell users the reasons. I found job's resources is immutable after creation, if so, make it inadmissible seems useless, we have to recreate them.

Not sure what are you suggesting. I would have liked a webhook, but as I said, it might not work well with users' own webhooks. Or maybe it's ok if it can be disabled (but enabled by default).

> what is the behavior now for those jobs?

They are admitted with no flavors assigned, as there are no resources to assign the flavors to.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-22T03:08:33Z

I mean job's resources is immutable now, so make it inadmissible doesn't make sense, we have to recreate them if we want to add resources. https://github.com/kubernetes/kubernetes/blob/d2504c94a0116d4432a8a73fc17a0ec8d003d37b/pkg/apis/batch/validation/validation.go#LL409

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-22T13:58:32Z

Right, I understand that. My question was whether you have an alternative solution.
Or is your preference to leave this as-is.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-03T15:03:32Z

If a job without request is OK from the K8S validation point of view then I guess Kueue, if nothing extra is set, should allow them. Otherwise there will be a quite surprising situation when a job with 1 millicore and 1MB request is fine and the other that doesn't put this BS settings is not.   
K8S allows to put empty pod requests but at the same time provides LimitRange that sets some reasonable CPU/Mem requests on pods that don't do that. Moreover, there might be a VPA object that can provide requests as well.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T16:21:17Z

LimitRange works on Pods only (and not pod templates), right? Maybe we should be paying attention to it in Kueue admission.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-03T17:49:10Z

That might be an interesting option to explore, together with Kueue paying attention to VPA recommendations as well.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-01T21:51:44Z

/close
in favor of #541

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-02-01T21:51:48Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/485#issuecomment-1412784738):

>/close
>in favor of #541 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-11T13:54:40Z

/reopen

@mwielgus #688 is flakying because a Workload can be admitted before the LimitRange is available in the cache.

There is no really a way to control whether a cache is "up-to-date". However, if there was a feature "do-not-admit workloads without requests", then we could use that in the test to avoid the flakyness.

Maybe we could implement this as a configuration option. WDYT?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-11T13:54:45Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/485#issuecomment-1503401132):

>/reopen
>
>@mwielgus #688 is flakying because a Workload can be admitted before the LimitRange is available in the cache.
>
>There is no really a way to control whether a cache is "up-to-date". However, if there was a feature "do-not-admit workloads without requests", then we could use that in the test to avoid the flakyness.
>
>Maybe we could implement this as a configuration option. WDYT?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-12T06:09:08Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T12:00:32Z

/unassign @mcariatm 

This is not decided yet

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T13:53:38Z

Discussed offline:

To prevent admitting an infinite number of Jobs, we can make ClusterQueues be able to define quota for number of pods.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T13:54:49Z

/retitle Control number of pods in ClusterQueues

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-12T14:22:58Z

However, this seems tricky, what's the criteria to define the number?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T16:23:58Z

In the job/workload, it's just the number of replicas.

The ClusterQueue can define a resource `pods`, similarly to how a Node has `pods` in the `allocatable` map.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-27T09:14:48Z

For this I'm thinking of adding a special resource type say `kueue.x-k8s.io/num-pods`, that, if defined in a queue's Resource Group , during the flavor assignment,  the number of pods of the workload will be used as value and treat the consumption as any other resource request from that point on.

Doing so  we only need to change the flavor assignment, no API or other major changes should be necessary.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-27T13:00:21Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-04-27T14:15:52Z

#732 has the implementation for my proposal (some cleanup and maybe integration test are needed)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-28T14:01:25Z

/retitle Manage number of pods in ClusterQueues
