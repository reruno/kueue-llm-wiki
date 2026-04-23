# Issue #8807: LWS inconsistent behavior when mutating `.spec.leaderWorkerTemplate.size`

**Summary**: LWS inconsistent behavior when mutating `.spec.leaderWorkerTemplate.size`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8807

**Last updated**: 2026-01-27T17:07:17Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-01-27T05:56:01Z
- **Updated**: 2026-01-27T17:07:17Z
- **Closed**: —
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 2

## Description

### Summary

Kueue currently enforces **LeaderWorkerSet immutability at the PodTemplateSpec level**, specifically for:

* `.spec.leaderWorkerTemplate.leaderTemplate`
* `.spec.leaderWorkerTemplate.workerTemplate`

All other properties under `.spec.leaderWorkerTemplate` remain mutable. One notable mutable field is:

* `.spec.leaderWorkerTemplate.size`

This results in **inconsistent and potentially surprising behavior** when the `size` field is changed after the Workload is created, regardless of whether it has been admitted.

### Background

The `size: N` attribute defines the total number of Pods in an LWS pod group, where:

* `N > 0`
* `N = 1` → one leader Pod
* `N = 2` → one leader + one worker
* `N = 3` → one leader + two workers
* and so on

### Observed behavior

Changing the LWS `size` after creation behaves differently depending on the direction of the change.

#### Increasing `size`

* If `size` is increased beyond the original value used to construct the Workload:

  * The corresponding Workload transitions into a **Finished** terminal state.
  * This outcome seems reasonable and consistent with immutability expectations.

* **Notable exception:**
  Typically, Kueue allows Workload updates as long as the Workload has not been admitted and does not have allocated quota. This does not hold for LeaderWorkerSet. Increasing `size` on a non-admitted LWS (with no quota assigned) still results in the Workload being marked as **Finished**.

#### Decreasing `size`

* If `size` is decreased:

  * The LWS controller adjusts the number of Pods accordingly.
  * The associated **Workload object is not updated**.
  * **ClusterQueue resource usage is not updated**.

* The `size` can be reduced and increased back up to the original value repeatedly without any effect on:

  * Workload representation
  * ClusterQueue quota accounting

* Only increasing `size` beyond the original value triggers the Workload to be marked as **Finished**.

---

### Concrete example

Using the Kueue documentation example defined with `size: 3`:

[https://kueue.sigs.k8s.io/docs/tasks/run/leaderworkerset/#example](https://kueue.sigs.k8s.io/docs/tasks/run/leaderworkerset/#example)

After the LWS is created:

* `size` can be changed from `3 → 2 → 1 → 3` any number of times.
* No corresponding updates are observed in:

  * The Workload spec or status
  * ClusterQueue resource utilization
* Increasing `size` above `3` results in the Workload being marked as **Finished**.

---

### Question

Is this behavior expected?

If so:

* What is the intended contract around mutability of `leaderWorkerTemplate.size`?
* How should users reason about quota accounting and Workload representation when `size` is decreased?
* Why do size mutations on non-admitted LWS diverge from the general Workload mutation rules?

If this behavior is expected, it should be explicitly documented.

If not:

* Should `size` be treated as immutable after Workload creation?
* Or should size decreases trigger Workload and ClusterQueue updates similar to other elastic or mutable workloads?

Clarifying this would help set correct expectations and avoid subtle quota accounting issues.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-27T16:53:01Z

> Kueue currently enforces LeaderWorkerSet immutability at the PodTemplateSpec level, specifically for:

Maybe I am mistaken but kueue doesn't enforce this. The LWS controller does.

https://github.com/kubernetes-sigs/lws/blob/main/pkg/webhooks/leaderworkerset_webhook.go#L102

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-27T17:07:17Z

I don’t think LWS checks or enforces immutability on `.spec.leaderWorkerTemplate.size`. It does validate that `size > 0`, but that appears to be the extent of the validation. I was able to reproduce this behavior, which is how I initially discovered the issue, both with the Kueue integration enabled and when running LeaderWorkerSet as a standalone controller.

More generally, Kueue’s immutability enforcement is largely scoped to PodTemplateSpec fields, which makes sense given that resource requirements are typically defined there. However, there are some integration-specific edge cases. LeaderWorkerSet is particularly interesting in this regard because it exposes both `spec.replicas` and `spec.leaderWorkerTemplate.size`. While these fields serve different purposes, changes to either can effectively increase or decrease the total number of Pods.

Kueue appears to handle mutations to `spec.replicas` in a well-defined way, whereas mutations to `spec.leaderWorkerTemplate.size` follow a different path, it’s not clear whether this divergence is intentional or incidental.
