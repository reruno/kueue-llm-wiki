# Issue #493: Use SSA (Server-Side Apply) for setting the workload conditions

**Summary**: Use SSA (Server-Side Apply) for setting the workload conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/493

**Last updated**: 2023-03-09T19:44:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2022-12-22T17:09:48Z
- **Updated**: 2023-03-09T19:44:32Z
- **Closed**: 2023-03-09T19:44:32Z
- **Labels**: _none_
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

With the use of SSA we will be able to avoid conflicts when different controllers set or add the conditions. For example, when a workload is admitted, the `WorkloadAdmitted` condition is set in a separate request to setting the workloads `.spec.admission` field. On the other hand, the `PodsReady` condition is added by the job controller, which may result in a conflict and a need to retry the request. This issue is exposed by the need to retry in the integration test (without the retry the test occasionally fails): https://github.com/kubernetes-sigs/kueue/blob/e688dccea0c3683a35bd51e9d67dba40a3997d83/test/integration/scheduler/podsready/scheduler_test.go#L100.
We can avoid the conflicts by using SSA with a pair of dedicated field managers - one for `PodsReady` (job controller) and `WorkloadAdmitted` (scheduler and workload controller).

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-22T17:14:28Z

Just curious what is SSA?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-22T17:15:02Z

> Just curious what is SSA?

Probably, SSA is Server-Side-Apply.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-12-22T17:18:52Z

> > Just curious what is SSA?
> 
> Probably, SSA is Server-Side-Apply.

Yes, we already use it in Kueue for admission (https://github.com/kubernetes-sigs/kueue/blob/e688dccea0c3683a35bd51e9d67dba40a3997d83/pkg/scheduler/scheduler.go#L286), but not for conditions.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T14:27:40Z

Do we always have to send all the conditions that we want to handle? Or can we send them in separate patches?

Although in the case of Workload, one condition is set by the Workload reconciler and the other by the Job reconciler, so they can use different managers.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-03-02T06:41:31Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-03-02T10:00:11Z

/assign
