# Issue #8320: Adding a priority class to a workload (none -> some) is not reconciled

**Summary**: Adding a priority class to a workload (none -> some) is not reconciled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8320

**Last updated**: 2026-01-13T08:05:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-12-18T10:34:51Z
- **Updated**: 2026-01-13T08:05:39Z
- **Closed**: 2026-01-13T08:05:39Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@andrewseif](https://github.com/andrewseif)
- **Comments**: 3

## Description

Kueue version: 0.15.0

When a workload's PriorityClass name is _changed_ (from one value to another), its priority is updated accordingly. This has been added in #7289.

However, when a PriorityClass is _added_ (changed from "none" to "some"), this does not happen, because the [reconciliation logic excludes this case](https://github.com/kubernetes-sigs/kueue/blob/b29f1b3a14194b70681524d9cc0a6ca2b3dfc86e/pkg/controller/core/workload_controller.go#L994).

For _running_ workloads, this is not a problem, because _adding_ a priority class is [disallowed](https://github.com/kubernetes-sigs/kueue/blob/b29f1b3a14194b70681524d9cc0a6ca2b3dfc86e/pkg/controller/jobframework/validation.go#L168-L170) for them.

However, for _suspended_ workloads, it is allowed, and is not reconciled.

Real repro: see [this script](https://github.com/olekzabl/kueue/blob/repro-8320/hack/bug-repro/add-wpc.sh) (and its [output](https://github.com/olekzabl/kueue/blob/repro-8320/hack/bug-repro/add-wpc.out.txt)). In short:
- set up 2 priority classes: `prio-1` (value 1000) and `prio-2` (value 2000)
- create `job-1` (with `prio-1`, gets admitted) and `job-2` (no priority class, gets queued)
- update `job-2` to have `prio-2` class
- `job-2` has still `.spec.priority == 0`, and remains suspended:
  ```
  NAME                    RESERVED_IN   PRIORITY
  job-repro-job-1-353d4   repro-cq      1000
  job-repro-job-2-1a7ee   <none>        0
  ```

For contrast: when `job-2` is initially configured with `prio-1`, then updating its priority class to `prio-2` leads to preempting `job-1`, which feels right:

```
NAME                    RESERVED_IN   PRIORITY
job-repro-job-1-08307   <none>        1000
job-repro-job-2-13269   repro-cq      2000
```

---

Ideas how to fix: either of:

- relax [this condition](https://github.com/kubernetes-sigs/kueue/blob/b29f1b3a14194b70681524d9cc0a6ca2b3dfc86e/pkg/controller/core/workload_controller.go#L994) accordingly;
- tighten validation rules to prevent adding WPC to workloads (just like removing is currently disallowed; cf. #5241 and #8334).

---

Note: once #8321 is fixed, I expect the same problem will affect _removing_ workload priority class labels.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T10:39:13Z

+1, if we haven't covered this with validation then we should fix it by supporting the operation

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:30:39Z

/priority important-soon

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-01-05T10:01:38Z

I would like to work on this issue 😄 
/assign
