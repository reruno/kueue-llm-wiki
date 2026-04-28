# Workload Maximum Execution Time

**Summary**: Kueue can enforce a maximum wall-clock execution time for any job type by automatically deactivating the workload once the cumulative admitted time exceeds `spec.maximumExecutionTimeSeconds`.

**Sources**: `raw/kueue/keps/3125-maximum-execution-time/README.md`, `raw/kueue/keps/3125-maximum-execution-time/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Beta** — Feature gate `MaxExecTime`, enabled by default since v0.9. (source: keps/3125-maximum-execution-time/kep.yaml)

## Motivation

Different job CRDs have inconsistent or missing deadline fields (`batch/Job` has `spec.activeDeadlineSeconds`; JobSet has no equivalent). Kueue provides a uniform, job-agnostic API for maximum execution time, equivalent to `-t` in SLURM. (source: keps/3125-maximum-execution-time/README.md)

## API

### Setting the limit

Use the job label to propagate the limit from a job to its workload:

```
kueue.x-k8s.io/max-exec-time-seconds: "3600"
```

The job framework reads this label at workload creation time and sets `spec.maximumExecutionTimeSeconds` (an `int32`, seconds) on the [[workload]]. (source: keps/3125-maximum-execution-time/README.md)

### Workload fields

```yaml
spec:
  maximumExecutionTimeSeconds: 3600   # total budget in seconds

status:
  accumulatedPastExecutionTimeSeconds: 1200   # time spent admitted in previous cycles
```

(source: keps/3125-maximum-execution-time/README.md)

## How enforcement works

The workload controller tracks time across preemption and re-admission cycles:

1. **On eviction/preemption**: the controller adds the time spent in `Admitted` state to `status.accumulatedPastExecutionTimeSeconds`.
2. **While admitted**: the remaining budget is `spec.maximumExecutionTimeSeconds − status.accumulatedPastExecutionTimeSeconds − (now − admittedAt)`.
3. **When budget ≤ 0**: the workload is **deactivated** (not re-queued) and an event is recorded. `accumulatedPastExecutionTimeSeconds` is reset to 0.
4. **While budget > 0**: a reconcile is queued to fire in exactly `remainingTime` seconds.

(source: keps/3125-maximum-execution-time/README.md)

## Outcome: deactivation, not re-queue

When the time limit expires the workload is **deactivated**, meaning `spec.active` is set to `false`. The job is suspended but stays in the system. This is different from preemption, which puts the workload back in the pending queue. Cluster admins or external tools must manually reactivate or delete the workload/job. (source: keps/3125-maximum-execution-time/README.md)

## Webhook validation

The webhook rejects workloads with `maximumExecutionTimeSeconds ≤ 0`. The field is immutable after creation. (source: keps/3125-maximum-execution-time/README.md)

## Interaction with preemption

If a workload is preempted before its budget expires, the elapsed time is accumulated. On re-admission, the remaining budget is smaller. A workload that is preempted many times will eventually exhaust its budget even if each individual run was short. (source: keps/3125-maximum-execution-time/README.md)

## Debugging

Check `status.accumulatedPastExecutionTimeSeconds` to see how much time has been consumed across cycles. The `WorkloadDeactivated` event indicates that the budget expired.

## Related pages

- [[workload]]
- [[admission]]
- [[preemption]]
- [[feature-gates]]
- [[gang-scheduling]]
