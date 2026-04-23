# Queueing strategy

**Summary**: Each [[cluster-queue]] has a `queueingStrategy` of `StrictFIFO` or `BestEffortFIFO`. The strategy controls whether a head-of-queue workload that can't be admitted blocks the rest of the queue (Strict) or gets skipped while subsequent workloads are tried (BestEffort).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## StrictFIFO

The head of the queue is always considered first. If it can't be admitted — quota missing, no preempt-able candidates, borrowing capped — the scheduler does not move on to the next workload. The intent is strict priority: a high-priority workload behind nothing else in the queue will never be overtaken.

Tradeoff: a big workload that nobody can currently satisfy can starve the CQ. Fixes have layered on top (preemption while borrowing, reclaim-in-cohort) but the fundamental "head blocks" property is preserved.

Known sharp edge: "StrictFIFO prevents borrowing when CQ has pending workloads" (source: issue-4809.md). This is working as intended — the pending head is why borrowing is suppressed — but surprising to operators until documented.

## BestEffortFIFO

If the head can't be admitted, try the next workload, and so on. Within priority classes the order is still preserved (higher priority before lower). Gets more throughput out of constrained queues at the cost of occasionally admitting a smaller workload before a blocked larger one.

This is typically the better default for mixed workloads.

## Priority within a queue

The queue heap is ordered by (priority descending, creation-time ascending). See [[workload-priority]]. Both strategies respect this — the difference is solely what happens when the current candidate can't be admitted.

## Immutability

`spec.queueingStrategy` has been restricted from changing on a CQ with admitted workloads because it would re-sort the queue mid-flight (source: issue-434.md, source: issue-1877.md). The user confusion in issue-1877 is the canonical "why can't I switch" explanation.

## Flaky-test heritage

StrictFIFO tests are often timing-sensitive — "should schedule workloads by their priority strictly" (source: issue-678.md) and related cohort+StrictFIFO flakes (source: issue-2020.md) are recurring. This reflects the tight race between preemption, quota release, and head-of-queue re-consideration.

## Related pages

- [[cluster-queue]] — where the strategy is declared.
- [[preemption]] — what the scheduler falls back to when head-of-queue can't fit.
- [[workload-priority]] — how priorities affect queue order.
- [[fair-sharing]] — an orthogonal option that changes *which CQ* goes next, not *which workload within a CQ*.
