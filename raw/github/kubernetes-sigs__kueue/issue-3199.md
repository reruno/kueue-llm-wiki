# Issue #3199: [RayCluster] Using the new Suspending / Suspended conditions in RayCluster to ensure the atomicity of the suspend operation

**Summary**: [RayCluster] Using the new Suspending / Suspended conditions in RayCluster to ensure the atomicity of the suspend operation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3199

**Last updated**: 2025-12-13T08:45:13Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kevin85421](https://github.com/kevin85421)
- **Created**: 2024-10-08T18:42:48Z
- **Updated**: 2025-12-13T08:45:13Z
- **Closed**: 2025-12-13T08:45:12Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 32

## Description

@rueian introduced two conditions, `Suspending` and `Suspended`, in the RayCluster CRD in [this PR](https://github.com/ray-project/kuberay/pull/2403), and the field `.Status.State = rayv1.Suspended` will be deprecated in the long term.

With the new conditions, if `spec.suspend` is set to true, KubeRay will first set the `Suspending` condition to true and then begin deleting Pods. If the user sets `spec.suspend` back to false before all Pods are deleted, KubeRay will still wait for all Pods to be deleted, set the `Suspended` condition to true and `Suspending` to false, and then set `Suspended` to false and recreate the Pods.

Without these two conditions, the behavior of setting `spec.suspend` back to false during the suspension process is undefined.

If Kueue maintainers don't have enough bandwidth, @rueian is happy to help.

## Discussion

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-10-08T18:43:33Z

cc @andrewsykim @alculquicondor @astefanutti

### Comment by [@rueian](https://github.com/rueian) — 2024-10-08T18:46:46Z

Thank you @kevin85421 for mentioning me. I am happy to help!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-08T18:48:12Z

This is great. It can help us know if there are still running Pods after we have set the suspend field.

cc @mimowo 

We are pretty packed, so we would appreciate the help in the kueue repo to use these conditions.

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-10-08T19:56:43Z

Hi @alculquicondor, would you mind providing some guidance on the compatibility between Kueue and KubeRay? For example, which KubeRay versions will be supported by the next Kueue release?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-08T20:03:20Z

We are happy to support the latest released version. However, older versions currently supported should ideally remain supported.

We use the v1 API right now, so hopefully the first version to introduce v1 should remain supported.

IIUC, this can be done, by simply defaulting to the existing implementation if none of the new conditions exist.

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-10-08T21:25:17Z

Yeah, it is not hard to support the multiple KubeRay versions.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-09T14:01:12Z

@kevin85421 @rueian Do you know which version KubeRay started to support the new "Suspending" condition?

### Comment by [@rueian](https://github.com/rueian) — 2024-10-09T15:31:08Z

Hi @tenzen-y, I think it will be released in the next version. v1.2.3 I hope.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-09T17:15:26Z

> Hi @tenzen-y, I think it will be released in the next version. v1.2.3 I hope.

Thanks for letting me know. So, the KubeRay will release the new condition in the next patch version.
If you can contribute to Kueue, I would appreciate it.

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-10-09T18:14:05Z

I think the next release should be v1.3.0.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T12:56:03Z

> I think the next release should be v1.3.0.

@kevin85421 Thank you for letting us know. Do you have candidates for the v1.3.0 like this month or next month?

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-10-11T17:34:22Z

> Do you have candidates for the v1.3.0 like this month or next month?

Maybe next month.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T17:36:59Z

> > Do you have candidates for the v1.3.0 like this month or next month?
> 
> Maybe next month.

Thanks, in that case, we can support this Suspending condition after the next Kueue version (0.10.0).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-14T14:26:57Z

/remove-kind support
/kind feature

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-12T15:17:07Z

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

### Comment by [@rueian](https://github.com/rueian) — 2025-01-12T15:28:41Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-12T16:01:34Z

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

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-04-14T16:34:04Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T16:38:26Z

@kevin85421 Do you have any plan to stop serving deprecated `.Status.State = rayv1.Suspended` state handling mechanism?

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-04-14T16:43:17Z

@tenzen-y maybe next major release, but we don't have a clear timeline for the release v2.0.0.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T16:46:24Z

> [@tenzen-y](https://github.com/tenzen-y) maybe next major release, but we don't have a clear timeline for the release v2.0.0.

Thank you for letting me know. In that case, we might want to keep the current suspending mechanism (`.status.state` = `suspend`) in the Kueue side to keep supporting older RayJobs. After Ray has been released v2.0, we can use the new way.

cc: @mimowo @mszadkow

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-04-14T17:54:58Z

@tenzen-y, does it make sense to support both `Status.State` and `conditions` in Kueue for now? That way, when KubeRay removes the field later, the impact on users will be minimized.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-15T11:24:47Z

Isn't that conflicting with `Kueue` being the one to manipulate `spec.suspend`?
Or you talk only about the effects of setting it to false/true by the Kueue.
Because RayCluster has the feature to suspend the cluster, but it cause me some troubles when I wanted to incorporate this in our e2e tests.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-15T11:32:04Z

> Isn't that conflicting with `Kueue` being the one to manipulate `spec.suspend`? Or you talk only about the effects of setting it to false/true by the Kueue. Because RayCluster has the feature to suspend the cluster, but it cause me some troubles when I wanted to incorporate this in our e2e tests.

Good point. Indeed, we do not depend on `.status.Suspend` field in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/raycluster/raycluster_controller.go

@kevin85421 Could you clarify the expected replacement?

### Comment by [@kevin85421](https://github.com/kevin85421) — 2025-04-15T20:30:18Z

> Good point. Indeed, we do not depend on .status.Suspend field in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/raycluster/raycluster_controller.go

Oh, I do think that Kueue depends on the RayCluster CR status, but I just realized that it depends on `spec` instead.

```
func (j *RayCluster) IsSuspended() bool {
	return j.Spec.Suspend != nil && *j.Spec.Suspend
}
```

It is possible for this function to return true if the RayCluster is in the process of suspending. Will this be an issue?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-14T20:31:40Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-16T07:46:06Z

> > Good point. Indeed, we do not depend on .status.Suspend field in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/raycluster/raycluster_controller.go
> 
> Oh, I do think that Kueue depends on the RayCluster CR status, but I just realized that it depends on `spec` instead.
> 
> ```
> func (j *RayCluster) IsSuspended() bool {
> 	return j.Spec.Suspend != nil && *j.Spec.Suspend
> }
> ```
> 
> It is possible for this function to return true if the RayCluster is in the process of suspending. Will this be an issue?

IIUC, GenericJob framework interface `IsSuspsnded` function indicates if desired object is suspended.
So, the current RayCluster integration seems like better. Do you have any view that Kueue should observe the interium `Suspending` condition?

When does RayCluster have `Suspending` condition? Is it after the specified .spec.suspend=true?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-16T07:46:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-14T07:48:47Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-13T07:57:09Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-13T08:45:08Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-13T08:45:13Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3199#issuecomment-3649122459):

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
