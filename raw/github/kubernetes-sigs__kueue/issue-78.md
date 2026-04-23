# Issue #78: Dynamically reclaiming resources

**Summary**: Dynamically reclaiming resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/78

**Last updated**: 2023-05-12T18:33:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-26T19:46:33Z
- **Updated**: 2023-05-12T18:33:04Z
- **Closed**: 2023-05-12T18:33:04Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 31

## Description

Currently a job's resources are reclaimed by Kueue only when the whole job finishes; for jobs with multiple pods, this entails waiting until the last pod finishes. This is not efficient as the pods of a parallel job may have laggards consuming little resources compared to the overall job.

One solution is to continuously update the Workload object with the number of completed pods so that Kueue can gradually reclaim the resources of those pods.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-08-02T19:51:07Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-11T11:34:55Z

@ahg-g I think we should add a new field in the status of workload, to track the count of completed pods.
What do you think?

Is there a way to get all pods belonging to a workload?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T15:04:30Z

This is not something that kueue core controllers should do. It's specific to the kind of workload. In the case of Job, it should be done in `pkg/controller/workload/job`. And this controller doesn't need to look at Pods, just at the Job status.

> I think we should add a new field in the status of workload, to track the count of completed pods.

Yes, we need that, but I would rather see a more complete design before adding the API fields. We can probably do this for the 0.3.0 release.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T15:05:07Z

If you are willing to write a design, please feel free to take this issue.

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-11T18:19:28Z

@alculquicondor thanks for the information!

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-11T18:19:47Z

I would like to work on this task.
/assign

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-12T19:31:08Z

API field changes design here:
```
// WorkloadStatus defines the observed state of Workload
type WorkloadStatus struct {
	// conditions hold the latest available observations of the Workload
	// current state.
	// +optional
	// +listType=map
	// +listMapKey=type
	Conditions []WorkloadCondition `json:"conditions,omitempty"`

	// The number of pods which reached phase Succeeded or Failed.
	// +optional
	CompletedPods int32 `json:"completedPods"`
}
```

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-12T19:32:18Z

High-level flow:
1. The completed pods in a job is sum of Succeeded+failed pods => sum(succeeded, failed)
2. We update the workload status object if job.sum(succeded, failed) > wl.CompletedPods
3. Handle the update event of workload in its reconciler.
4. Update clusterqueue quota for resource flavor for requests of pod workload in cache.

Currently I don't see any scenario where `CompletedPods`  field will used in the reconciliation routine of workload.

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-12T19:33:03Z

Please validate the above design and approach.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-12T19:47:46Z

Why would failed pods matter? The job controller would create a replacement pod, which should be taking quota.

Not sure if a github issue is the best avenue to provide feedback on a design. Could you start a google doc? Alternatively, we could start an enhancements folder where we can add design proposals with a format similar to https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-08-13T12:20:58Z

Will start with enhancements folder and add design proposal.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-09-12T13:02:12Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-10-12T13:39:33Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-12T13:39:38Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1276190888):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-12T15:33:46Z

/reopen

@thisisprasad is currently working on the proposal

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-12T15:33:50Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1276373159):

>/reopen
>
>@thisisprasad is currently working on the proposal


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-11-11T15:56:53Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-11T15:56:57Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1311880616):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-11-14T03:19:22Z

reopen for tracking.
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-14T03:19:25Z

@kerthcet: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1313038259):

>reopen for tracking.
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-14T03:36:16Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-14T03:36:20Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1350344796):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-14T03:38:39Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-14T03:38:43Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1350345933):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-14T03:40:25Z

/remove-lifecycle rotten

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-14T20:10:16Z

/unassign @thisisprasad 
/assign @mwielgus

Thanks for the progress so far @thisisprasad

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-14T20:10:18Z

@alculquicondor: GitHub didn't allow me to assign the following users: mwielgus.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/78#issuecomment-1352094684):

>/unassign @thisisprasad 
>/assign @mwielgus
>
>Thanks for the progress so far @thisisprasad 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-11T15:22:22Z

/assign @mwielgus

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-20T12:48:56Z

@kerthcet

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-04-12T19:32:05Z

/unassign

### Comment by [@trasc](https://github.com/trasc) — 2023-04-27T12:49:26Z

/assign
