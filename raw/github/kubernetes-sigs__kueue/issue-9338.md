# Issue #9338: MultiKueue "leaks" admission on the manager when a workload is evicted on a worker

**Summary**: MultiKueue "leaks" admission on the manager when a workload is evicted on a worker

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9338

**Last updated**: 2026-04-07T12:59:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2026-02-18T11:46:43Z
- **Updated**: 2026-04-07T12:59:33Z
- **Closed**: 2026-04-07T12:59:33Z
- **Labels**: `kind/bug`, `area/multikueue`
- **Assignees**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Comments**: 4

## Description

# Background

The scenario considered here is when MultiKueue admits a workload on a worker but then it gets preempted there.

Before #8477, the workload would just get stuck, as described in #8302.
After that fix, with the `MultiKueueRedoAdmissionOnEvictionInWorker` gate enabled, the behavior is better:

- the manager recognizes that a worker has evicted the workload
- the manager triggers re-execution of the admission checks, including MultiKueue AC
- the workload is dispatched to some (likely other) workers, giving it a chance to run again

That's all fine, and covered by tests.

# The issue

The issue is that the workload remains `Admitted` on the manager during that whole procedure.
This becomes particularly problematic if the workload is not going to become re-scheduled for a long time.
In such case, from the perspective of the manager cluster, `Admitted` suggests that the workload is running on some worker, while it's not the case.

I'd rather ensure that `Admitted` on a manager _implies_ `Admitted` on a worker. 
(To be strict: except the short periods when the workload lost admission on a worker but the manager hasn't yet "realized" that fact).

# How to reproduce

1. In a clone of Kueue repo, run:
   ```
   cd kueue/examples/multikueue/dev
   ./setup-kind-multikueue-tas.sh --version v0.16.0
   ```
   (setting this version is important to have #8477 on board).

2. In any directory of your choice, run [this script](https://github.com/olekzabl/kueue/blob/repro-4/hack/bug-repro/test.sh).
   (Warning: it depends on the other files in the same folder).
   The script contains comments about the specific test scenario.

The script output is [here](https://github.com/olekzabl/kueue/blob/repro-4/hack/bug-repro/output/out.log). The Kueue logs from all clusters are placed in the same folder. Notable observations:

* `job1-7` has preempted `job1-2` on `worker1`.
* `manager` noticed this and dispatched `job1-2` again to `worker2` (where it could not get quota).
* `job1-2` status is correctly reflected on `worker1` (no longer admitted, no quota reserved) and on `worker2` (no quota reserved).
* However, on `manager`, `job1-2` is still displayed as `admitted`.
* The mechanism from #8477 has been invoked; this can be seen e.g. [here](  https://github.com/olekzabl/kueue/blob/77347bc316f7494d65c4bb19ca39a71791027575/hack/bug-repro/output/manager.log#L324) in the manager logs.
  Also, the status of the MultiKueue AdmissionCheck was switched to false, as logs show [here](  https://github.com/olekzabl/kueue/blob/77347bc316f7494d65c4bb19ca39a71791027575/hack/bug-repro/output/manager.log#L326).
  Given that, it feels suspicious that the workload remained admitted.

# Idea for fixing

When the manager detects a worker-side eviction:

* Retain the `QuotaReserved` condition for the workload on the manager, to keep it actively considered by MultiKueue controller.
* However, remove the `Admitted` condition. (Bring it back when the workload gets admitted on some worker).

In my understanding, this will make the overall workload status analogous as if it's been just dispatched to the workers for the first time. (With the only difference that one of the workers has "somehow managed" to evict it). This *seems resonable at the first glance*.

However, obviously we'd **need to double-check** if this doesn't bring any trouble in practice.

Not sure if this warrants a feature gate. (If we hear no opinion on this, I'll assume "yes" for safety. Though maybe it'd make most sense to re-use the `MultiKueueRedoAdmissionOnEvictionInWorker` gate introduced in #8477).

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-18T11:48:35Z

/area multikueue

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-03T10:18:16Z

/assign

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-04T09:21:47Z

Investigated the provided example.

The issue seems to be that in the job reconciler this part seems not to execute sometimes: https://github.com/kubernetes-sigs/kueue/blob/116095b2e505386bf9837abaed36b89e899e51a6/pkg/controller/jobframework/reconciler.go#L569-L581

As per the guiding condition:
https://github.com/kubernetes-sigs/kueue/blob/116095b2e505386bf9837abaed36b89e899e51a6/pkg/controller/jobframework/reconciler.go#L567-L568

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-04T09:45:33Z

In the case described here the issue seems to be that the pods of the job persist in the Running state.

1. Job is created, dispatched and admitted on a worker. 2 pods are created and in the Running (ready) state.
2. We preempt the job - job gets suspended as expected, but pods remain in the Running (ready) state.
3. The logic that processes eviction for a job requires the job not to be active to proceed. For a job this mean "pods count" to be 0. The job in question however still has pods in the running state, which means it is still considered active and the admission is never cleared from the Manager Workload.
