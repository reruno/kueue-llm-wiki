# Issue #5613: MutliKueue: Local Job status is not updated upon remote Job completion.

**Summary**: MutliKueue: Local Job status is not updated upon remote Job completion.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5613

**Last updated**: 2025-06-20T20:24:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-06-11T04:20:59Z
- **Updated**: 2025-06-20T20:24:53Z
- **Closed**: 2025-06-20T20:24:53Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

In MultiKueue, the local `Job` status is not updated to reflect the termination state of the corresponding remote `Job`. This behavior contradicts the [MultiKueue batch/Job documentation](https://kueue.sigs.k8s.io/docs/concepts/multikueue/#batchjob), which states that the local Job's final status should be copied once the remote workload is marked as finished.

Final `Job`/`Workload` status appears as follows:

```
NAME             STATUS      COMPLETIONS   DURATION   AGE
job.batch/demo   Suspended   0/2                      79s

NAME                                     QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-demo-4e5de   demo    demo                     True       79s
```

**What you expected to happen**:

Once the remote workload is marked as finished, the local Job should reflect its final state, e.g.:

```
NAME             STATUS     COMPLETIONS   DURATION   AGE
job.batch/demo   Complete   2/2           27s        32s

NAME                                     QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-demo-bc108   demo    demo                     True       32s
```

**How to reproduce it (as minimally and precisely as possible)**:

Create a batch `Job` using the [MultiKueue batch/Job example](https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/job/#example) and observe the local Job's status after the remote workload completes.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.31.2`
- Kueue version (use `git describe --tags --dirty --always`): `latest release` or `main branch`
- Cloud provider or hardware configuration: `n/a`
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T04:31:56Z

This issue appears to stem from the following `if` block:
[https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job\_multikueue\_adapter.go#L64-L68](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_multikueue_adapter.go#L64-L68)

```go
if fromObject(&localJob).IsSuspended() {
	// Ensure the job is unsuspended before updating its status; otherwise, it will fail when patching the spec.
	log.V(2).Info("Skipping the sync since the local job is still suspended")
	return nil
}
```

In practice, the local Job is never resumed (i.e., unsuspended), which results in the final status of the remote Job never being synced back to the local Job. This seems to be an oversight.

**Side note:**
The comment:

```go
// Ensure the job is unsuspended before updating its status; otherwise, it will fail when patching the spec.
```

implies that the routine attempts to patch the **local Job spec**, and that leaving the Job suspended is intended to prevent a spec patching error. However, upon inspection, there does not appear to be any code within this routine that actually patches the local Job spec—only status updates are performed. If that’s the case, this check might be unnecessarily blocking status reconciliation.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T04:35:38Z

**Update:**
Removing the aforementioned `if` block resolves the issue and allows the local Job status to be updated as expected.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T04:53:49Z

@ichekrygin please try enabling MultiKueueBatchJobWithManagedBy=true. This feature gate enables the syncing. The syncing was blocked by default, because it couldn't be used on k8s versions <=1.31. This is related to the graduation to beta of the ManagedBy feature: https://github.com/kubernetes/enhancements/issues/4368

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T05:37:44Z

Hi @mimowo, thank you for looking into this issue.

Simply enabling the `MultiKueueBatchJobWithManagedBy=true` feature gate results in the workload failing admission due to the following:

```yaml
status:
  admissionChecks:
  - lastTransitionTime: "2025-06-11T05:25:09Z"
    message: 'The owner is not managed by Kueue: Expecting spec.managedBy to be "kueue.x-k8s.io/multikueue" not ""'
    name: demo
    state: Rejected
```

**Side note:**
The `multikueue.workload.go` controller appears to enter a tight retry loop at
[https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/multikueue/workload.go#L221](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/admissionchecks/multikueue/workload.go#L221) — where every second update (as it seems) fails with:

```
clearing admission: Operation cannot be fulfilled on workloads.kueue.x-k8s.io "job-demo-b36b1": the object has been modified; please apply your changes to the latest version and try again
```
This loop does not appear to back off or stop, potentially creating unnecessary load and log spam.

I attempted to set the `managedBy` field explicitly in Jobas follows:

```yaml
spec:
  ...
  managedBy: kueue.x-k8s.io/multikueue
```

However, it appears that this field is being wiped somewhere during admission. I haven’t yet pinpointed where exactly this happens.

Let me know if you have any insights or if there’s a recommended way to ensure the field is preserved and the workload passes admission.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T05:42:25Z

Honestly, I don’t think the `MultiKueueBatchJobWithManagedBy=true` feature gate is relevant in this particular case. The reason is that the check for a suspended Job—and the early return—is the **first** conditional block in the remote Job processing logic:

[https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job\_multikueue\_adapter.go#L64](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_multikueue_adapter.go#L64)

```go
// the remote job exists
if err == nil {
	if fromObject(&localJob).IsSuspended() {
		// Ensure the job is unsuspended before updating its status; otherwise, it will fail when patching the spec.
		log.V(2).Info("Skipping the sync since the local job is still suspended")
		return nil
	}

	if features.Enabled(features.MultiKueueBatchJobWithManagedBy) {
		return clientutil.PatchStatus(ctx, localClient, &localJob, func() (bool, error) {
			localJob.Status = remoteJob.Status
			return true, nil
		})
	}

	remoteFinished := false
	for _, c := range remoteJob.Status.Conditions {
		if (c.Type == batchv1.JobComplete || c.Type == batchv1.JobFailed) && c.Status == corev1.ConditionTrue {
			remoteFinished = true
			break
		}
	}
	if remoteFinished {
		return clientutil.PatchStatus(ctx, localClient, &localJob, func() (bool, error) {
			localJob.Status = remoteJob.Status
			return true, nil
		})
	}

	return nil
}
```

Since the suspended check short-circuits the logic before any feature gate or final status evaluation occurs, the presence or absence of `MultiKueueBatchJobWithManagedBy` has no effect on this path.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T05:44:49Z

^ My finding is also corroborated by the following log message:

```
{"level":"Level(-2)","ts":"2025-06-10T22:43:41.47648-07:00","caller":"job/job_multikueue_adapter.go:66","msg":"Skipping the sync since the local job is still suspended","controller":"multikueue_workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"job-demo-15e66","namespace":"demo"},"namespace":"demo","name":"job-demo-15e66","reconcileID":"24737230-2d41-4017-aed0-485837fd27f5"}
```

This clearly confirms that the sync logic exits early due to the suspended state, regardless of the feature gate.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T05:53:47Z

To my earlier comment: 

> However, it appears that this field is being wiped somewhere during admission. I haven’t yet pinpointed where exactly this happens.

It looks like I need to enable the `JobManagedBy` Kubernetes feature gate (which is disabled by default in v1.31) in order for this value to be propagated appropriately. This might be a good detail to call out explicitly in the Kueue documentation (if it isn't already)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T05:55:10Z

What is the k8s version you are using? For 1.32+ you should enable the feature gate. it was introduced specifically for this reason.

The error about multikueue not set suggest the webhook didn't kick in as it should. The webhook should set managed by.

Finally the block of code you are experimenting with deleting was introduced intentionally to prevent another bug we encountered. You can find details by tracing the PR with git blame for the block of code

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T05:56:27Z

I'm not saying there isn't a bug somewhere, but I would like to make sure first that we use the setup as intended. This will make debug easier.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T06:25:09Z

I can confirm that with both the Kubernetes `JobManagedBy` feature gate **enabled** and Kueue’s `MultiKueueBatchJobWithManagedBy` **enabled**, the Job status is updated correctly.

However, my original observation still holds true when `MultiKueueBatchJobWithManagedBy` is **disabled**, as described in the documentation:
[https://kueue.sigs.k8s.io/docs/concepts/multikueue/#multikueuebatchjobwithmanagedby-disabled](https://kueue.sigs.k8s.io/docs/concepts/multikueue/#multikueuebatchjobwithmanagedby-disabled)

Specifically, the second bullet point states:

> * Since updating the status of a local Job could conflict with the Kubernetes Job controller, the manager does not sync the Job status during the job execution. The manager copies the final status of the remote Job when the remote workload is marked as Finished.

In practice, this final status copy **does not happen**—the local Job remains suspended with no status update, even after the remote Job completes.

This suggests either:

* There’s a valid bug preventing the final status sync, or
* The documentation needs to be updated to reflect the current behavior.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T06:55:33Z

> I can confirm that with both the Kubernetes JobManagedBy feature gate enabled and Kueue’s MultiKueueBatchJobWithManagedBy enabled, the Job status is updated correctly.

Awesome. 

> However, my original observation still holds true when MultiKueueBatchJobWithManagedBy is disabled, as described in the documentation:

I see, I think we have a bug indeed. I think this PR https://github.com/kubernetes-sigs/kueue/pull/3685 actually broke the case when `MultiKueueBatchJobWithManagedBy=false`, introducing this block of code:

```golang
if fromObject(&localJob).IsSuspended() {
	// Ensure the job is unsuspended before updating its status; otherwise, it will fail when patching the spec.
	log.V(2).Info("Skipping the sync since the local job is still suspended")
	return nil
}
```
It fixed the case for `MultiKueueBatchJobWithManagedBy=true`, but when `MultiKueueBatchJobWithManagedBy=false` then it blocks the final status update for finished Job, because we never unsuspend the Job in this mode.

I think the code should look like this (putting the check under `MultiKueueBatchJobWithManagedBy=true`. Let me @ichekrygin know if you would like to submit a PR fix. 

cc @IrvingMg @mszadkow who also often contribute to MultiKueue.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-11T07:00:14Z

> I think the code should look like this (putting the check under `MultiKueueBatchJobWithManagedBy=true`. Let me [@ichekrygin](https://github.com/ichekrygin) know if you would like to submit a PR fix.

Do you mean something like:

```golang
       // the remote job exists
	if err == nil {
		if features.Enabled(features.MultiKueueBatchJobWithManagedBy) {
			if fromObject(&localJob).IsSuspended() {
				// Ensure the job is unsuspended before updating its status; otherwise, it will fail when patching the spec.
				log.V(2).Info("Skipping the sync since the local job is still suspended")
				return nil
			}
			return clientutil.PatchStatus(ctx, localClient, &localJob, func() (bool, error) {
				localJob.Status = remoteJob.Status
				return true, nil
			})
		}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T07:02:01Z

Exactly.
