# Issue #3994: [KubeRay] KubeRay introduces new APIs for RayJob termination

**Summary**: [KubeRay] KubeRay introduces new APIs for RayJob termination

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3994

**Last updated**: 2026-03-05T17:19:52Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kevin85421](https://github.com/kevin85421)
- **Created**: 2025-01-17T06:34:10Z
- **Updated**: 2026-03-05T17:19:52Z
- **Closed**: 2026-03-05T17:19:50Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

https://github.com/ray-project/kuberay/pull/2643 KubeRay v1.3.0 will introduce a new API to support different deletion policies for RayJob. For example, KubeRay can delete all worker Pods while keeping the head Pod alive for troubleshooting. Will this make Kueue make incorrect scheduling decisions?

cc @andrewsykim @rueian @MortalHappiness

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T12:03:26Z

IIUC the deletion policy only affects complete Jobs: 
"
	// DeletionPolicy indicates what resources of the RayJob are deleted **upon job completion.**
	// Valid values are 'DeleteCluster', 'DeleteWorkers', 'DeleteSelf' or 'DeleteNone'.
	// If unset, deletion policy is based on 'spec.shutdownAfterJobFinishes'.
	// This field requires the RayJobDeletionPolicy feature gate to be enabled.
" 
IIUC the policies only affect the RayJob / Cluster once finished, and so I think it should not impact quota management by Kueue, because Kueue does not include quota for Jobs which are finished - once a workload is marked as Finished, then  kueue deleted its resource usage in cache, see [here](https://github.com/kubernetes-sigs/kueue/blob/097262a4d0b07af58a6ddc267805953dc7131bb4/pkg/controller/core/workload_controller.go#L696-L711.  

However, I didn't go deeply into the code of the Ray changes. Do you have some specific scenario in mind @kevin85421 ?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-01-17T15:28:04Z

I tihnk we just need to update the validation logic to check for `shudownAfterJobFinishes` OR `deletionPolicy == DeleteCluster` https://github.com/kubernetes-sigs/kueue/blob/097262a4d0b07af58a6ddc267805953dc7131bb4/pkg/controller/jobs/rayjob/rayjob_webhook.go#L102-L104

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-01-17T18:45:38Z

> IIUC the deletion policy only affects complete Jobs:

It's correct.

> because Kueue does not include quota for Jobs which are finished - once a workload is marked as Finished, then kueue deleted its resource usage in cache, ...

If a RayJob finishes and terminates all Ray worker Pods, Kueue assumes that the entire RayCluster resource is released. Is it possible that for a subsequent RayJob, Kueue thinks the Kubernetes cluster has enough resources when it actually does not due to leaked head Pods?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T19:50:56Z

Yes, when the main workload is finished keueue assumes all quota resources are reclaimed, and so reclaima the quota for the leaked pods, and may give it to the subsequent workload which, as a result may got admitted but not scheduled. 

Are the leaked head pods leaked for good or just a short while?is it a bug in ray or there are legitimate use cases to leak the pods?

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-01-17T20:08:49Z

This is intended behavior. The use case is that some users want to log into the head Pod to check the Ray dashboard after the job finishes, especially if the Ray job fails.

### Comment by [@ukclivecox](https://github.com/ukclivecox) — 2025-03-10T11:36:44Z

With dynamic provisioning on GKE I see provision requests fail until I manually delete the RayJob that has completed. Is this related to this issue. I am testing with a node-pool for GPUs with max-nodes 1. I start 3 RayJobs - 1 of which the provisioning request succeeds and the other 2 fail. The other provisioning requests stay failed even after completion of the RayJob.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-03-10T12:53:21Z

>  I am testing with a node-pool for GPUs with max-nodes 1. I start 3 RayJobs - 1 of which the provisioning request succeeds and the other 2 fail.

Could you open a separate issue with more details? It sounds like potentially the other 2 provisioning requests (linked to the other 2 RayJobs) are failing due to max nodes being set to 1?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-08T13:42:13Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T14:19:46Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T14:31:29Z

/remove-lifecycle stale
/remove-lifecycle rotten

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-07-08T15:22:41Z

cc @weizhaowz

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-06T15:46:24Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T16:02:03Z

/remove-lifecycle stale 
I'm not clear about the conclusion. It would be nice if someone can investigate deeper, indicating if the issue exists or not.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-04T16:12:11Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-03T16:20:41Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-05T17:19:42Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-05T17:19:51Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3994#issuecomment-4006504440):

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
