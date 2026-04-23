# Issue #6216: Prevent re-admission of "old" workload slices that have not been properly finalized

**Summary**: Prevent re-admission of "old" workload slices that have not been properly finalized

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6216

**Last updated**: 2025-07-29T16:40:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-07-28T17:00:34Z
- **Updated**: 2025-07-29T16:40:28Z
- **Closed**: 2025-07-29T16:40:28Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 5

## Description

**Description:**

During dynamic job scaling, it is possible for both the **old** workload slice and its **scaled-up successor** to coexist in an active (non-`Finished`) state. This creates a race condition where both workloads are eligible for scheduling, and the **old** slice may be re-admitted **after it was previously evicted**, violating the intended 1:1 relationship between a Job and its active Workload.

This issue is a regression introduced by changes in [#6203](https://github.com/kubernetes-sigs/kueue/pull/6203).

---

### ⚠️ Problem Summary

While investigating recent behavior related to workload slice aggregation and eviction, we observed the following scenario:

1. A Job is scaled up → a **new** workload slice is created.
2. The scheduler evicts the **old** workload due to unrelated quota pressure.
3. The generic job reconciler ignores the **old** workload slice (regression) and proceeds with reconciling the **new** slice, without marking the old one as `Finished`.
4. Since the **old** slice is still active and not marked `Finished`, it is re-enqueued and becomes eligible for re-admission.
5. If the **old** workload fits within the quota (e.g., it's smaller), the scheduler may admit it **after** the new slice.
6. This results in **two admitted workloads for the same Job**, violating correctness expectations and undermining the workload slice replacement logic.

**Note:**
If step 5 instead results in the **old** slice being picked *before* the **new** one, the impact is a **delayed handling of the scale-up event**. While suboptimal, this is less critical than the case where both slices are admitted concurrently.

---

### 💡 Expected Behavior

The **old** workload slice should be **marked as `Finished`** (or `out-of-sync`) by the generic job reconciler to enforce a strict 1:1 relationship between a Job and its active workload slice.

This logic is already implemented here:
[MarkFinishedOldWorkloads](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workloadslicing/workloadslicing.go#L198)

---

### 🧩 Root Cause

A regression in [FindNotFinishedWorkloads](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workloadslicing/workloadslicing.go#L128) altered its behavior by **excluding** un-finished, active old workload slices from its return value.

As a result, those slices are silently skipped by the reconciler and left eligible for re-admission.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T17:17:23Z

Thank you for opening and reporting. Indeed the regression is likely. It would be great to add an integration test along with the fix. 

It may require additional investigation, but it seems to me that since marking as Finished "out-of-sync" was in Job reconciler, then it was possible that for a brief moment after eviction both workloads would be pending and ready for re-admission, nonetheless. 

So, my gut feeling is, that to prevent race conditions we may consider:
1. extending the eviction process to first ensure the "old" workload is finished
2. adapt scheduler to exclude "old" workload from scheduling when the "new" exists.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-28T18:22:05Z

To clarify, **prior to the regression**, the **old workload slice** was marked as `Finished` by both the **scheduler** and the **generic job reconciler**, with the latter handling the **preemption edge case**.

---

> **1. Extend the eviction process to first ensure the "old" workload is finished**

The scheduler already (and still) marks the replaced workload slice as `Finished` in the context of scheduling the **new** slice.

> **2. Adapt the scheduler to exclude the "old" workload from scheduling when the "new" exists**

When the scheduler encounters a workload that might be an "old" slice, one that has been "virtually" replaced by a newer slice but has not yet been marked as `Finished`, it should avoid scheduling it and instead mark it as `Finished`.
This is a reasonable enhancement, but currently, the scheduler has no way to determine that a workload slice is "virtually replaced" just by inspecting the "old" slice alone. "Virtually" in this context means that the slice has been logically replaced, but the actual transition wasn't observed (e.g., the old slice wasn’t in the cache at the time the new one was admitted).

That said, we could make this determination possible via the following approaches:

**a.** The scheduler could traverse all workloads in the cache to look for a workload with an annotation pointing to the current "old" slice, indicating it has been replaced.
**b.** At the time of new slice creation, we could annotate both workloads:

* currently we set `new → old`
* we could add `old → new` as well
  This would allow more efficient lookup and clearer context for the scheduler to act on.

**c.** Do both (a) and (b)
**d.** Do neither and revert the regression

---

### Summary

Before the regression, it was possible to have a **transient inconsistency** where both the old and new workloads briefly appeared in a scheduled state. This occurred due to the generic job reconciler lagging behind the scheduler in marking the old slice as `Finished`. However, this inconsistency would resolve on the next reconciliation cycle.

In contrast, **post-regression**, the **old** workload may **never** be marked as `Finished` by the generic job reconciler, resulting in a **permanent inconsistency**.

To support **(d)**, I recommend **reverting the regression** by restoring the original behavior of `FindNotFinishedWorkloads`, combined with improved workload slice sorting. Then, evaluate whether a **transient inconsistency** is acceptable for the workload slice mechanism. Only if it is not, should we consider additional scheduler logic.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T18:38:10Z

We certainly want to revert the regression, but I'm not convinced to reverting the PR as is, because it fixes race conditions already detected by existing tests.

I would like to explore the following approach: prevent having two "active" workloads at the same time even for a short while. One way to achieve it is to mark the "old" workload slice (indicated by the "replacement-for" annotation) when the "new" workload is being Evicted / Preempted. 

I believe we could do around [here](https://github.com/kubernetes-sigs/kueue/blob/6243fca5de31e6cbd3844b8821822bd3bc0019b1/pkg/controller/jobframework/reconciler.go#L530-L553 ). If I'm not missing anything this would be even less code, and more resilient as we would never allow for two "Pending" workloads, even for a while.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-28T19:23:38Z

> We certainly want to revert the regression, but I'm not convinced to reverting the PR as is

Correct, regression only, not the PR wholesale.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-28T23:26:28Z

/bug
