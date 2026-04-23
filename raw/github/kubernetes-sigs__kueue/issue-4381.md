# Issue #4381: PodIntegration: labels and annotations are not propagated to Workload PodSet

**Summary**: PodIntegration: labels and annotations are not propagated to Workload PodSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4381

**Last updated**: 2025-02-25T09:00:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-24T16:30:15Z
- **Updated**: 2025-02-25T09:00:53Z
- **Closed**: 2025-02-25T08:59:24Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
For the PodIntegration, `.metadata.labels` and `.metadata.annotations` are not propagated to Workload PodSet, although other kinds of Jobs propagate those to Workload.

**What you expected to happen**:
Those labels and annotations are appropriately propagated to the Workload. Indeed, For Pod Integration, we don't see TAS annotations in Workload.

**How to reproduce it (as minimally and precisely as possible)**:
As we can check in the following, the Pod PodSet constructor does not clone labels and annotations to `.template.metadata` in PodSet, which means does not copy those to `.spec.template.metadata` in Workload.

https://github.com/kubernetes-sigs/kueue/blob/72ea01afe844de88825d8bf111976aaf48e04f6a/pkg/controller/jobs/pod/pod_controller.go#L648-L657


For reference, Job case: https://github.com/kubernetes-sigs/kueue/blob/72ea01afe844de88825d8bf111976aaf48e04f6a/pkg/controller/jobs/job/job_controller.go#L255

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T16:31:03Z

cc: @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-24T17:50:07Z

+1, it looks like a bug. One thing I would like to check when fixing is if it does not impact already running Workloads during the upgrade of Kueue (I guess it is not a problem, but we have a complicated equivalence logic, so I would like to run an experiment).

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-24T18:26:57Z

There is a LabelKeysToCopy on the integration config.

```golang
	// labelKeysToCopy is a list of label keys that should be copied from the job into the
	// workload object. It is not required for the job to have all the labels from this
	// list. If a job does not have some label with the given key from this list, the
	// constructed workload object will be created without this label. In the case
	// of creating a workload from a composable job (pod group), if multiple objects
	// have labels with some key from the list, the values of these labels must
	// match or otherwise the workload creation would fail. The labels are copied only
	// during the workload creation and are not updated even if the labels of the
	// underlying job are changed.
	LabelKeysToCopy []string `json:"labelKeysToCopy,omitempty"`
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T18:42:09Z

> +1, it looks like a bug. One thing I would like to check when fixing is if it does not impact already running Workloads during the upgrade of Kueue (I guess it is not a problem, but we have a complicated equivalence logic, so I would like to run an experiment).

That makes sense. We should add tests when we fix this bug.
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-24T18:42:50Z

> There is a LabelKeysToCopy on the integration config.
> 
> 	// labelKeysToCopy is a list of label keys that should be copied from the job into the
> 	// workload object. It is not required for the job to have all the labels from this
> 	// list. If a job does not have some label with the given key from this list, the
> 	// constructed workload object will be created without this label. In the case
> 	// of creating a workload from a composable job (pod group), if multiple objects
> 	// have labels with some key from the list, the values of these labels must
> 	// match or otherwise the workload creation would fail. The labels are copied only
> 	// during the workload creation and are not updated even if the labels of the
> 	// underlying job are changed.
> 	LabelKeysToCopy []string `json:"labelKeysToCopy,omitempty"`

That is not related to this bug. The `labelKeysToCopy` will be evaluated during JobFramework.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T08:42:28Z

Throughout I investigated this more, this seems appropriate behavior since we propagate ProvisioningRequest annotation to Workload: https://github.com/kubernetes-sigs/kueue/blob/2d5a1bbf4af964c1913fdd6cf24309aa1fc79f1d/pkg/controller/jobframework/interface.go#L216

Note this was added in https://github.com/kubernetes-sigs/kueue/pull/1869.

Here, my initial expectation is propagating all TAS annotations to the Workload resource. However, non-propagation seems to be correct.
So, I would close this issue without any action. @mimowo WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-25T08:59:19Z

In the context of TAS we already have e2e tests for the Pod integration, showing that it works. 

Still, there might be some issues down the line due to not propagating Pod metadata to workload.

I'm ok to close for now, until we hit some particular problem.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-25T08:59:25Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4381#issuecomment-2681195601):

>In the context of TAS we already have e2e tests for the Pod integration, showing that it works. 
>
>Still, there might be some issues down the line due to not propagating Pod metadata to workload.
>
>I'm ok to close for now, until we hit some particular problem.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T09:00:51Z

> In the context of TAS we already have e2e tests for the Pod integration, showing that it works.
> 
> Still, there might be some issues down the line due to not propagating Pod metadata to workload.
> 
> I'm ok to close for now, until we hit some particular problem.

That makes sense.
