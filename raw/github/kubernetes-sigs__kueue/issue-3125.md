# Issue #3125: Introduce Job-agnostic API to declare the maximal execution time for a Job

**Summary**: Introduce Job-agnostic API to declare the maximal execution time for a Job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3125

**Last updated**: 2024-11-04T09:59:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-24T10:42:11Z
- **Updated**: 2024-11-04T09:59:30Z
- **Closed**: 2024-11-04T09:59:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 11

## Description

**What would you like to be added**:

A job-agnostic API to set the maximal execution time for a Job. 

There are some open questions:
- name of the API (I would initially propose annotation ` kueue.x-k8s.io/max-exec-time-seconds`)
- semantics of the deadline (measured since last admission or cumulative execution time) - I would initially suggest to measure the cumulative execution time across admissions , and re-use it in the EXEC_TIME command for kueuectl, but it will require API changes
- what happens after exceeding the time  - I would initially propose deactivating the workload, but alternatives might be worth considering


**Why is this needed**:

Different Jobs CRDs have a field with similar semantics, but there is no standard. For example batch/Job has `spec.activeDeadlneSeconds`, while JobSet does not have such an API for now.

We would like to have such an API to use it in kueuectl command as an analog of slurm's "-t" option. Long term (but out-of-scope here) we could use this value to optimize Job scheduling.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T10:42:25Z

/cc @mwielgus @trasc @mbobrovskyi

### Comment by [@trasc](https://github.com/trasc) — 2024-09-24T12:09:17Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-24T12:24:41Z

Maybe kueue could set activeDeadlineSeconds on all the pod templates? NVM. I see that you want the limit for the entire job so I don't think pod level is the right fit here.

### Comment by [@tardieu](https://github.com/tardieu) — 2024-09-24T13:19:09Z

Very much in favor.

Specifying a deadline for a workload (possibly wall clock time instead of cumulative execution time) would also enable capacity planning and permit developing ordering strategies to, e.g., ensure large workloads have a chance to run without resorting to priorities and preemption.

An alternative to workload deactivation could be to dynamically lower the priority of the workload, hence let it run if there is excess capacity and only evict if necessary.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T14:34:57Z

> (possibly wall clock time instead of cumulative execution time)

Yeah, I was thinking that "cumulative execution time" measures wall time. I say it is  cumulative because it would add up running wall time from all admission times (say if it is admitted (3min) -> suspended (whatever) -> admitted (3min), this would account to 6min, vs activeDeadlineSeconds which accounts only 3min (last admission time).

wdyt?

> would also enable capacity planning and permit developing ordering strategies to, e.g., ensure large workloads have a chance to run without resorting to priorities and preemption.

Yeah, that is the long-term plan. IIUC its counterpart ("-t" in slurm) is used for better scheduling.

> An alternative to workload deactivation could be to dynamically lower the priority of the workload, hence let it run if there is excess capacity and only evict if necessary.

Potentially, but it sounds complex (what function should decrease the priorities). Also, some users don't like to use priorities as they have the incentive of setting them as high as possible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-24T14:57:17Z

I like this feature. Actually, users easily violate fairness using the sleep inf command. 
And the preemption is only way to prevent unfairness Jobs. Once we provide feature to enforce the deadline time, we can prevent unfairness Jobs.

My main question is, at what time can the calculation start? I guess that we need to add a dedicated field like startTime to the Workload object.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-24T14:59:41Z

Additionally, I guess that we need to consider https://github.com/kubernetes-sigs/kueue/pull/2737.
So, we may need to reset Workload startTime field (new field, and just my idea of field name) when the Workload gets WorkloadWaitForPodsReadyReplacement condition.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-24T15:05:34Z

> My main question is, at what time can the calculation start? I guess that we need to add a dedicated field like startTime to the Workload object.

Yeah, we need a new field for that, but I was rather thinking about keeping the accumulated time from the previous admissions (say `prevAdmissionsRuntime`).

Then compute exec time as:
```
execTime = prevAdmissionsRuntime + now() - Admitted.LastTransitionTime
```
I think with startTime we would not account for the time when the job is suspended. WDYT?

### Comment by [@trasc](https://github.com/trasc) — 2024-09-25T10:41:58Z

I've opened #3133 as a KEP PR for this, please have a look and let's continue the discussion there.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T07:47:47Z

I have played a bit with slurm's "-t" option, and it looks like it puts a limit on the cumulative wall clock across "suspend / resume". While we don't need to follow it exactly, it seems like a sensible inspiration.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T11:01:58Z

> I think with startTime we would not account for the time when the job is suspended. WDYT?

I was supposed to reset the startTime when the job is preempted or evicted (StopJob), similar to batch/v1 Job integration.
Anyway, we can evaluate both approaches during the proposal.
