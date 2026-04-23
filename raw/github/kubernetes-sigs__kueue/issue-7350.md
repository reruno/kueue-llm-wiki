# Issue #7350: [MultiKueue] Eviction initiated on manager doesn't work

**Summary**: [MultiKueue] Eviction initiated on manager doesn't work

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7350

**Last updated**: 2025-12-19T16:56:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-10-23T07:18:44Z
- **Updated**: 2025-12-19T16:56:32Z
- **Closed**: 2025-12-19T16:56:32Z
- **Labels**: `kind/bug`, `priority/critical-urgent`, `area/multikueue`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I'm trying to create high priority job to preempt low priority job but it is not working as expect. The workload stuck on.

Status from high priority job:

```yaml
- lastTransitionTime: "2025-10-23T06:33:18Z"
   message: 'couldn''t assign flavors to pod set main: insufficient unused quota
    for memory in flavor default, 1953125Ki more needed. Pending the preemption
    of 1 workload(s)'
   observedGeneration: 1
   reason: Pending
   status: "False"
   type: QuotaReserved
```

Status from low priority job:

```yaml
conditions:
  - lastTransitionTime: "2025-10-23T06:33:17Z"
   message: Quota reserved in ClusterQueue q1
   observedGeneration: 1
   reason: QuotaReserved
   status: "True"
   type: QuotaReserved
  - lastTransitionTime: "2025-10-23T06:33:18Z"
   message: 'Preempted to accommodate a workload (UID: 9f542104-a9e2-4344-ad2e-9c136204da18,
    JobUID: a20d0a6a-64a3-46ce-9b95-8cfb3bf6e675) due to prioritization in the
    ClusterQueue'
   observedGeneration: 1
   reason: Preempted
   status: "True"
   type: Evicted
  - lastTransitionTime: "2025-10-23T06:33:18Z"
   message: The workload is admitted
   observedGeneration: 1
   reason: Admitted
   status: "True"
   type: Admitted
  - lastTransitionTime: "2025-10-23T06:33:18Z"
   message: 'Preempted to accommodate a workload (UID: 9f542104-a9e2-4344-ad2e-9c136204da18,
    JobUID: a20d0a6a-64a3-46ce-9b95-8cfb3bf6e675) due to prioritization in the
    ClusterQueue'
   reason: InClusterQueue
   status: "True"
   type: Preempted
```

Logs from the manager cluster occurring in a loop:

```
2025-10-23T07:13:10.668141483Z	DEBUG	events	recorder/recorder.go:104	couldn't assign flavors to pod set main: insufficient unused quota for memory in flavor default, 1953125Ki more needed. Pending the preemption of 1 workload(s)	{"type": "Warning", "object": {"kind":"Workload","namespace":"multikueue-vggw9","name":"job-job2-f620a","uid":"4cc488da-107c-4814-8248-b44ac9462816","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"14153"}, "reason": "Pending"}
2025-10-23T07:13:10.76844517Z	LEVEL(-3)	scheduler	queue/manager.go:661	Obtained ClusterQueue heads	{"schedulingCycle": 12168, "count": 1}
2025-10-23T07:13:10.768592836Z	LEVEL(-3)	scheduler	scheduler/fair_sharing_iterator.go:69	Returning workload from ClusterQueue without Cohort	{"schedulingCycle": 12168, "clusterQueue": {"name":"q1"}, "workload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}}
2025-10-23T07:13:10.768610128Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:252	Attempting to schedule workload	{"schedulingCycle": 12168, "workload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}, "clusterQueue": {"name":"q1"}}
2025-10-23T07:13:10.768633711Z	LEVEL(-3)	scheduler	preemption/preemption.go:190	Preemption ongoing	{"schedulingCycle": 12168, "workload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}, "clusterQueue": {"name":"q1"}, "targetWorkload": {"name":"job-job1-6f320","namespace":"multikueue-vggw9"}, "preemptingWorkload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}}
2025-10-23T07:13:10.768676628Z	LEVEL(-3)	scheduler	scheduler/logging.go:42	Workload evaluated for admission	{"schedulingCycle": 12168, "workload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}, "clusterQueue": {"name":"q1"}, "status": "", "reason": "couldn't assign flavors to pod set main: insufficient unused quota for memory in flavor default, 1953125Ki more needed. Pending the preemption of 1 workload(s)"}
2025-10-23T07:13:10.768709211Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:778	Workload re-queued	{"schedulingCycle": 12168, "workload": {"name":"job-job2-f620a","namespace":"multikueue-vggw9"}, "clusterQueue": {"name":"q1"}, "queue": {"name":"q1","namespace":"multikueue-vggw9"}, "requeueReason": "PendingPreemption", "added": true, "status": ""}
```

**What you expected to happen**:
The high priority job should be successfully admitted.

**How to reproduce it (as minimally and precisely as possible)**:
- Create low priority job
- Create high priority job

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-23T07:18:59Z

/cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-29T15:20:11Z

This is prerequisite issue for https://github.com/kubernetes-sigs/kueue/issues/7429

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T08:40:41Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T11:22:55Z

We checked this together with @mszadkow and found the problem.

After eviction, we should stop the job (which works fine):
https://github.com/kubernetes-sigs/kueue/blob/7a8b75bc06450cc4e319280eb2091f95e84f2de5/pkg/controller/jobframework/reconciler.go#L540-L542

After that, if the job is not active and has a reservation, we should unset the quota reservation:
https://github.com/kubernetes-sigs/kueue/blob/7a8b75bc06450cc4e319280eb2091f95e84f2de5/pkg/controller/jobframework/reconciler.go#L543-L559

We get stuck here because the status:
https://github.com/kubernetes-sigs/kueue/blob/7a8b75bc06450cc4e319280eb2091f95e84f2de5/pkg/controller/jobs/job/job_controller.go#L157-L159

is never updated — we only run SyncJob if it is finished:
https://github.com/kubernetes-sigs/kueue/blob/7a8b75bc06450cc4e319280eb2091f95e84f2de5/pkg/controller/admissionchecks/multikueue/workload.go#L347-L357

and if it’s creation:
https://github.com/kubernetes-sigs/kueue/blob/7a8b75bc06450cc4e319280eb2091f95e84f2de5/pkg/controller/admissionchecks/multikueue/workload.go#L402-L421

I think this issue affects not only preemption but also other types of eviction.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T11:24:47Z

/reopen

Sorry, closed by mistake.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-04T11:24:53Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7350#issuecomment-3485475824):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T11:33:01Z

I think to fix this, we need to update the workload controller and all adapters — specifically, the SyncJob function in each of them. We should copy the job spec from the local job to the remote job in each change, and copy the remote job status back to the local one. In that case, it should work, and we’ll be able to update and know the Active() status in the local (manager) cluster.

@mimowo @tenzen-y WDYT?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-09T14:25:56Z

After investigating, I found that the problem is not only with preemption (as part of eviction) but with eviction itself. So I decided to rename the issue.

/retitle [MultiKueue] The eviction is not working

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T13:16:56Z

/retitle [MultiKueue] Eviction initiated on manager doesn't work

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:22:19Z

/area multikueue
/priority critical-urgent
