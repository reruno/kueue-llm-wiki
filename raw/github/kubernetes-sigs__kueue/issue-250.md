# Issue #250: add condition field to ClusterQueueStatus

**Summary**: add condition field to ClusterQueueStatus

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/250

**Last updated**: 2022-12-22T19:59:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-06T06:15:59Z
- **Updated**: 2022-12-22T19:59:28Z
- **Closed**: 2022-12-22T19:59:28Z
- **Labels**: `kind/feature`, `priority/backlog`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add condition field to ClusterQueueStatus, like `WorkloadCondition`.

**Why is this needed**:
Not distant future, we have ClusterQueue status (pending vs active) in internal(after https://github.com/kubernetes-sigs/kueue/pull/230), we should reflect the status in ClusterQueue object, which is helpful to check the explicit condition of ClusterQueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-06T14:15:05Z

This requires an API change

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-15T05:55:39Z

API Design details here:
```
type ClusterQueueStatus struct {
	// usedResources are the resources (by flavor) currently in use by the
	// workloads assigned to this clusterQueue.
	// +optional
	UsedResources UsedResources `json:"usedResources"`

	// PendingWorkloads is the number of workloads currently waiting to be
	// admitted to this clusterQueue.
	// +optional
	PendingWorkloads int32 `json:"pendingWorkloads"`

	// AdmittedWorkloads is the number of workloads currently admitted to this
	// clusterQueue and haven't finished yet.
	// +optional
	AdmittedWorkloads int32 `json:"admittedWorkloads"`

	// conditions hold the latest available observations of the ClusterQueue
	// current state.
	// +optional
	// +listType=map
	// +listMapKey=type
	Conditions []ClusterQueueCondition `json:"conditions,omitempty"`
}

type ClusterQueueCondition struct {
	// type of condition could be:
	//
	// ClusterQueuePending: clusterQueue is accepted but not yet active.
	// In this state, it can't admit new workloads and its quota can't be borrowed
	// by other active ClusterQueues in the same same cohort.
	//
	// ClusterQueueActive: clusterQueue can admit new workloads and its quota
	// can be borrowed by other ClusterQueues in the same cohort.
	Type ClusterQueueConditionType `json:"type"`

	// status could be True, False or Unknown.
	Status corev1.ConditionStatus `json:"status"`

	// lastProbeTime is the last time the condition was checked.
	// +optional
	LastProbeTime metav1.Time `json:"lastProbeTime,omitempty"`

	// lastTransitionTime is the last time the condition transit from one status
	// to another.
	// +optional
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`

	// reason is a brief reason for the condition's last transition.
	// +optional
	Reason string `json:"reason,omitempty"`

	// message is a human readable message indicating details about last
	// transition.
	// +optional
	Message string `json:"message,omitempty"`
}

type ClusterQueueConditionType string

const (
	// ClusterQueuePending indicates clusterQueue is accepted but not yet active.
	// In this state, it can't admit new workloads and its quota can't be borrowed
	// by other active ClusterQueues in the same same cohort.
	ClusterQueuePending ClusterQueueConditionType = "Pending"

	// ClusterQueueActive indicates clusterQueue can admit new workloads and its quota
	// can be borrowed by other ClusterQueues in the same cohort.
	ClusterQueueActive ClusterQueueConditionType = "Active"
)
```

cc @ahg-g

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-21T09:07:24Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-08-19T09:36:53Z

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

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-19T15:48:56Z

/close 

this is done

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-19T15:49:08Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/250#issuecomment-1220826831):

>/close 
>
>this is done


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-19T15:51:39Z

oh, this was referring to reflecting the status in the CQ condition; we have that as a metric now, it might be more appropriate as a metric since the CQ status may flip between active and pending.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T16:34:34Z

Metrics need to leverage other components like grafana to display properly, I think status is still necessary.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-19T16:44:32Z

There is no serious production environment without metrics infra :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-19T19:14:29Z

I agree that a condition would be useful, but:

/priority backlog

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-17T14:10:24Z

@kerthcet Do you have any updates?
If you don't have enough time to work on this, I'd like to take this on.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-09-18T02:08:57Z

Thanks, you can take it for free .

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-18T14:57:42Z

> Thanks, you can take it for free .

Thanks for your response.
I'll work on this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-10-03T01:59:03Z

I take this.
/assign

Also, I use [the API design](https://github.com/kubernetes-sigs/kueue/issues/250#issuecomment-1126866851) suggested by @ kerthcet.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-11T02:12:57Z

/unassign
I think @tenzen-y will take over this.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-11-10T02:32:54Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-11-10T02:36:03Z

/remove-lifecycle rotten
