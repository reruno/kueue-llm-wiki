# Issue #3841: MultiKueue should remove workloads on workers if the MK admission check gets rejected

**Summary**: MultiKueue should remove workloads on workers if the MK admission check gets rejected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3841

**Last updated**: 2026-03-19T09:53:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-13T15:03:41Z
- **Updated**: 2026-03-19T09:53:06Z
- **Closed**: 2026-03-19T09:53:05Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 18

## Description

**What happened**:

Currently, workloads on the worker clusters are left if the MK admission check is rejected. 


**What you expected to happen**:

Workloads on the worker clusters to be deleted synchronously.

**How to reproduce it (as minimally and precisely as possible)**:

Create MK workload, and mark the AC as Rejected. The worker worklaods are only deleted by GC.

**Anything else we need to know?**:

see https://github.com/kubernetes-sigs/kueue/pull/3835 for more details

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-07T09:29:42Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-20T06:26:57Z

/reopen 
As per https://github.com/kubernetes-sigs/kueue/issues/4003#issuecomment-2601468903
@mszadkow please rollback adding the PR adding the test.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-20T06:27:03Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3841#issuecomment-2601470405):

>/reopen 
>As per https://github.com/kubernetes-sigs/kueue/issues/4003#issuecomment-2601468903
>@mszadkow please rollback adding the PR adding the test.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-20T07:26:49Z

https://github.com/kubernetes-sigs/kueue/pull/4005

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-25T11:57:56Z

During the work on the tests to document current behaviour one scenario became problematic and might reveal the issue - https://github.com/kubernetes-sigs/kueue/pull/4058/files.

In the test case we admit the workload by setting the `Quota Reservation` on the worker cluster and right away we set `Rejected` to MultiKueue AdmissionCheck.
This creates the situation when one of 2 things happens:
1. MultiKueue Workload Reconciler (pkg/controller/admissionchecks/multikueue/workload.go) gets the event about quota reservation first and updates the workload status.
```
		// update the message
			acs.Message = fmt.Sprintf("The workload got reservation on %q", reservingRemote)
			// update the transition time since is used to detect the lost worker state.
			acs.LastTransitionTime = metav1.NewTime(w.clock.Now())

			wlPatch := workload.BaseSSAWorkload(group.local)
			workload.SetAdmissionCheckState(&wlPatch.Status.AdmissionChecks, *acs, w.clock)
			err := w.client.Status().Patch(ctx, wlPatch, client.Apply, client.FieldOwner(kueue.MultiKueueControllerName), client.ForceOwnership)
```
Thus invalidating the workload being processed by Core Workload Reconciler (pkg/controller/core/workload_controller.go), which were in the middle of processing Rejected status of workload's AdmissionCheck.

2. Core Workload Reconciler gets the event about workload AC rejected first and updates the workload status.
```
log.V(3).Info("Workload is evicted due to admission checks")
	if workload.HasRejectedChecks(wl) {
		var rejectedCheckNames []string
		for _, check := range workload.RejectedChecks(wl) {
			rejectedCheckNames = append(rejectedCheckNames, check.Name)
		}
		workload.SetDeactivationTarget(wl, kueue.WorkloadEvictedByAdmissionCheck, fmt.Sprintf("Admission check(s): %v, were rejected", rejectedCheckNames))
		if err := workload.ApplyAdmissionStatus(ctx, r.client, wl, true, r.clock); err != nil {
			return false, client.IgnoreNotFound(err)
		}
		log.V(3).Info("Workload is evicted due to rejected admission checks", "workload", klog.KObj(wl), "rejectedChecks", rejectedCheckNames)
		rejectedCheck := workload.RejectedChecks(wl)[0]
		r.recorder.Eventf(wl, corev1.EventTypeWarning, "AdmissionCheckRejected", "Deactivating workload because AdmissionCheck for %v was Rejected: %s", rejectedCheck.Name, rejectedCheck.Message)
		return true, nil
	}
```

Thus invalidating the workload being processed by MultiKueue Workload Reconciler.

However this race condition happens on the very thin margin of about 200ms.
Adding this delay to the test in line https://github.com/kubernetes-sigs/kueue/blob/6ab0eda0ab6d0da3a4fbe2803f5dce54f55e97d9/test/integration/multikueue/multikueue_test.go#L1846
prevents the race.
This suggests that the issue is marginal, because it requires to update the status of workload AC to rejected immediately after it was changed to admitted( got reservation ) by the worker.
Introduction of the before mentioned delay made the issue not occur even in the stress tests.

Also normally workloads are removed asynchronously by Garbage Collector (that was disabled in the mentioned test).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T06:52:56Z

@mszadkow thank you for looking into the issue and the summary.

First, I opened this issue only based on static code analysis, when fixing a memory leak, rather than an actual experiment.

I'm happy to park this issue for now, as this has marginal benefits (due to existence of GC). Also the scenario requires non-standard transition from Ready to Rejected. AFAIK we don't have any automated routine which would do it currently, so it requires a manual action. 

I suggest opening a PR to remove the TODO as the place may actually be confusing.

I believe an improvement remains possible but I think the issue is more of a distraction at this point with low priority., so I'm on a fence about closing it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T12:38:13Z

Actually, I think the can leave the issue open as low priority, because disabling GC is a supported configuration: https://github.com/kubernetes-sigs/kueue/blob/main/apis/config/v1beta1/configuration_types.go#L226. I doubt anyone would do it for a production system, but it remains technically a possibility (and thus an issue).

I would welcome contributions if there are some good ideas how to improve it, but would need to weight the gain/complexity ratio for the solution.

EDIT: I think supporting disablement of GC might have not been the best idea, we may deprecate the mode, but let's wait a little bit longer.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-27T13:03:44Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-08T09:34:26Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-06T10:20:39Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:26:48Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T08:30:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-05T09:29:29Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:39:06Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:28:08Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T09:45:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:52:58Z

/close
probably low gain/effort based on the discussion the effort is high, while no one yet complained

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T09:53:06Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3841#issuecomment-4088982589):

>/close
>probably low gain/effort based on the discussion the effort is high, while no one yet complained


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
