# Issue #800: Bug: framework.Reconciler reconciles against unmanaged child batch/job

**Summary**: Bug: framework.Reconciler reconciles against unmanaged child batch/job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/800

**Last updated**: 2023-06-09T09:54:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-05-23T20:37:11Z
- **Updated**: 2023-06-09T09:54:49Z
- **Closed**: 2023-06-07T18:22:15Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The framework.Reconciler reconciles against child batch/job even if the batch/job isn't managed by kueue.
So, the kueue-controller-manager forcefully stops the unmanaged running child batch/job, and then the batch/job is dead.

https://github.com/kubernetes-sigs/kueue/blob/8a0d088e43adbc6a5bcf574aa882ef24d06c0921/pkg/controller/jobframework/reconciler.go#L110-L115

This happens when the following conditions are met:

1. Set `manageJobsWithoutQueueName=false` to kueue-controller-manager.
2. Users don't set queue names to parent jobs(e.g., MPIJob).
3. The batch/job is child one.
4. enable to watch both of parent job (MPIJob) and child job like the following:

```yaml
...
integrations:
  frameworks:
  - "batch/job"
  - "kubeflow.org/mpijob"
```

**What you expected to happen**:
The framework.Reconciler ignores the unmanaged child batch/job.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.5
- Kueue version (use `git describe --tags --dirty --always`): v0.3.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-23T20:38:43Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-26T21:29:56Z

Through more investigating, I found that the kueue-controller adds an annotation to indicate parent workload even if the parent job (e.g., MPIJob) doesn't have a queue name.

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobs/job/job_webhook.go#L63-L72

Ideally, we shouldn't add an annotation to the child batch/job if kueue doesn't manage the parent job. But, during webhooks, it is complicated to add the annotation to the child job, considering whether Kueue manages the parent job.

So, it would be better to define `standaloneJob` as a job that doesn't have an annotation to indicate a parent workload, or that has an annotation to indicate a parent workload even if the parent workload doesn't exist in the cluster.

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobframework/reconciler.go#L108

@alculquicondor What do you think?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-26T21:35:27Z

cc: @kerthcet

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-26T21:43:05Z

In the current implementation, if the child job meets the following conditions, kueue-controller-manager doesn't skip to reconcile.

1. Set manageJobsWithoutQueueName=false to kueue-controller-manager.
2. Users don't set queue names to parent jobs(e.g., MPIJob).
3. The batch/job is child one.
4. enable to watch both of parent job (MPIJob) and child job

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobframework/reconciler.go#L110-L115

So, the kueue-controller-manager suspends the unmanaged child batch/job in the following parts:

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobframework/reconciler.go#L291-L293

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-26T21:48:50Z

(If skipping the following processes, that will cause by a new bug related to `manageJobsWithoutQueueName=true`. So, we shouldn't do that.)
~~Uhm, just skipping the following processes might be better when the parent workload doesn't exist in the cluster.~~

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobframework/reconciler.go#L291-L293

> So, it would be better to define standaloneJob as a job that doesn't have an annotation to indicate a parent workload, or that has an annotation to indicate a parent workload even if the parent workload doesn't exist in the cluster.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-29T12:02:58Z

I think this line is wrong

https://github.com/kubernetes-sigs/kueue/blob/433881616b83eb495e0b6b5b82c68f5c4aadf910/pkg/controller/jobframework/reconciler.go#L112


It's correct for standalone jobs. But for child jobs, we should be checking if the parent has a queue name. If it doesn't we should skip.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-29T17:21:14Z

You're right.
I was thinking of a way not to check a parent job. But your suggested way sounds much more reasonable.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-30T16:16:43Z

> It's correct for standalone jobs. But for child jobs, we should be checking if the parent has a queue name. If it doesn't we should skip.

+1, another topic is do you think we should not reconcile the child job at all, leave the control to its parent job, then if it's a child job, we'll skip directly.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-30T16:34:29Z

> do you think we should not reconcile the child job at all, leave the control to its parent job, then if it's a child job, we'll skip directly.

I don't have use cases that would reconcile the child Job. However, since the kueue-controoler suspends the child job instead of the framework job controller (not our controller, third-party controller), reconciling the child jobs might be useful for the framework jobs without suspend semantics.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-30T17:39:34Z

If the parent CRD didn't implement the semantics correctly, we want to stop the child Job from running.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-09T09:54:49Z

> If the parent CRD didn't implement the semantics correctly, we want to stop the child Job from running.

In my opinion this is a very strange pattern, if the parent, CRD  didn't implement the semantics correctly how can have a working integration for it?

I think we should not touch any job that has a parent manageable by kueue.
