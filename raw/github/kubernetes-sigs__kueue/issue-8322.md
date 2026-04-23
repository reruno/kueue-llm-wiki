# Issue #8322: Workload priority class value changes are not reconciled

**Summary**: Workload priority class value changes are not reconciled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8322

**Last updated**: 2026-01-09T04:45:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-12-18T11:17:52Z
- **Updated**: 2026-01-09T04:45:39Z
- **Closed**: 2026-01-09T04:45:39Z
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: [@ASverdlov](https://github.com/ASverdlov)
- **Comments**: 3

## Description

Kueue version: 0.15.0

Since #7289, changing the `WorkloadPriorityClass` assigned to a `Workload` may be reconciled (i.e. lead to immediate change of workload's priority, up to some preemptions).

However, changing the `value` of a (fixed) `WorkloadPriorityClass` assigned to a `Workload` is still not reconciled, and has no effect on the workload.

Real repro: run [this script](https://github.com/olekzabl/kueue/blob/repro-8322/hack/bug-repro/wpc-value-change.sh) (see [its output](https://github.com/olekzabl/kueue/blob/repro-8322/hack/bug-repro/wpc-value-change.out.txt)). In short:
- Set up 2 priority classes: `prio-1` (value 1000) and `prio-2` (value 2000)
- Create `job-1` with `prio-1` (gets queued) and `job-2` with `prio-2` (gets admitted)
- Downgrade `prio-2` to have `.value = 500`
- Upgrade `prio-1` to have `.value = 3000`
- Neither of the 2 updates does any change to the workloads. (So, it doesn't matter if the workload is admitted or suspended).
  The picture is still the original one:
  ```
  NAME                    RESERVED_IN   PRIORITY
  job-repro-job-1-b77a9   <none>        1000
  job-repro-job-2-5004d   repro-cq      2000
  ```

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-12-18T11:26:45Z

CC @mwielgus - do you have opinion on what priority this deserves?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:30:26Z

/priority important-longterm
tentatively

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-01-03T17:45:36Z

Hi folks! I'd like to work on this issue if you don't mind.

/assign
