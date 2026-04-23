# Issue #9015: Elastic Workloads: During scale-up, old WorkloadSlice is finished but new WorkloadSlice is not admitted, leaving Job active and unsuspended

**Summary**: Elastic Workloads: During scale-up, old WorkloadSlice is finished but new WorkloadSlice is not admitted, leaving Job active and unsuspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9015

**Last updated**: 2026-04-06T14:55:21Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-02-05T20:47:31Z
- **Updated**: 2026-04-06T14:55:21Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 22

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

During elastic scale-up, the controller may mark the existing WorkloadSlice as finished before the replacement slice is successfully admitted. If the admission of the new slice fails, for example due to transient API or scheduling errors, the Job can remain active and unsuspended while no slice is admitted and capacity accounting is not restored. This results in an inconsistent state where the Job appears to be running despite having no admitted WorkloadSlice, which should instead trigger suspension and quota restoration.

**What happened**:

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

This surfaced in #5897

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-06T00:35:01Z

This is the heart of the issue: https://github.com/kubernetes-sigs/kueue/blob/ee03ae4c7a39caba9c6a7822ae9cf8c88f2ab780/pkg/scheduler/scheduler.go#L340-L365

## What this code is really doing

Conceptually, slice replacement today is implemented as **two independent steps**:

1. **Replace / evict the old slice**

   * `replaceWorkloadSlice(...)`
   * Marks the old slice as `Finished`
   * Transfers `Status.ClusterName` for MultiKueue consistency

2. **Admit the new slice**

   * `s.admit(ctx, e, cq)`

These steps are sequential but **not transactional**.

The code itself already documents the problem accurately:

> If the admission step fails, we may end up in a state where:
>
> * the old workload is marked Finished, and
> * the new workload is not admitted.

For elastic slicing, there is an implicit invariant that must hold:

> At any point in time, either
>
> * the old slice is active, or
> * the new slice is admitted.
>
> If neither is true, the Job must be suspended, and in MultiKueue, remote state must be cleaned up.

Today, we are missing this suspension state, and that’s the bug 🐛

## What are our options

Replacement needs to be treated as **atomic with respect to admission**, even if implementation-wise it is staged.

At a minimum, one of the following must be true:

### Option A, admit first, then finish the old slice

* New slice admission succeeds
* Only then mark the old slice `Finished`
* Preserves the invariant, but may require temporary over-accounting safeguards

### Option B, two-phase replacement (more complex)

* Mark the old slice as `Replacing` rather than `Finished`
* Attempt admission
* Transition to `Finished` only after admission succeeds
* Roll back or re-activate the old slice on failure

### Option C, explicit failure recovery (minimal fix)

* If admission fails after finishing the old slice:

  * Force Job suspension

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-06T01:14:04Z

/ichekrygin

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-06T16:24:45Z

> ### Option A, admit first, then finish the old slice
> * New slice admission succeeds
> * Only then mark the old slice `Finished`
> * Preserves the invariant, but may require temporary over-accounting safeguards

@mimowo IIRC, we discussed this option during the original PR(s). I’d like to revisit it and get your current take. I still think this is likely the best of the three options listed, given that it preserves the core invariant and avoids the broken intermediate state.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T17:21:45Z

I have already got used to (and it took me time) to the mental model of the "quota gap" rather than "quota bump", so I don't want to change the model without deeper consideration. 

Intuitively I think "quota gap" is better, and more aligned with the preemption model. In this mental model I consider another way of fixing it - make the "new workload" sticky, and ensure it gets in front of even high priority workloads. If it does not "get in" after 5s or so, then we evict it - it should be very rare. 

This way we could achieve the semi-transactional model. 

With the "quota bump" we need to always have twice more quota, I'm worried this may not be compatible with various used stories, like UberClusterQueue.

So, I think for now I'm ok pursuing the quick fix which is time-based, similarly as you started in the PR, but longer term I would like to consider the "semi-transaction" by sticky workload. We already have the concept of "sticky workload" for preemptions, and it very much feels it could be re-used here.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-06T17:42:20Z

I totally get your point, and I have a similar hesitation.

A quick clarification on the “quota bump means we need twice the quota” concern: it’s less about *needing* twice the quota, and more about the scheduler admitting a new workload slice in a way that causes a **brief quota accounting mismatch**. For a short period of time, both the old and the new slices are admitted, which may temporarily push ClusterQueue usage beyond its limit. In that sense, the “quota bump” is primarily an **accounting representation issue**, which I agree is not ideal.

The appeal of this option is that it has a different user surface and is easier to reason about and correct. Having two active slices at the same time is an anomaly that is easy to detect, and the remediation is straightforward: remove the old slice. From the user workload’s perspective, this path is effectively non-disruptive.

Failing to admit the new slice, on the other hand, is harder to detect, as it relies on a timeout-based heuristic, and more importantly, it directly disrupts the user workload. In that case, we end up suspending the job in response to this condition, which is a much more visible and user-impacting outcome.

Given that, I’m okay with pursuing the time-based quick fix for now, similar to what you started in the PR. Longer term, though, I’d still like to explore a semi-transactional approach using a “sticky” new workload. We already have a notion of stickiness in the preemption model, and it feels like that concept could potentially be reused here.

Here is side-by-side comparison.

| Aspect | **Quota Gap (Finish-then-Admit)** | **Quota Bump (Admit-then-Finish)** |
|---|---|---|
| Core idea | Preserve a gap between old and new slices, avoid over-accounting; rely on timing or stickiness to complete replacement | Admit the new slice first, then finish the old slice, allowing brief overlap |
| Mental model | Capacity is temporarily unavailable until replacement completes | Capacity is temporarily over-accounted during overlap |
| Accounting behavior | CQ usage never exceeds limits | CQ usage may briefly exceed limits due to two active slices |
| Detection mechanism | Timeout or stickiness logic to decide if admission failed | Simple invariant check, more than one active slice is an anomaly |
| Correctness signal | Harder to detect failure, relies on elapsed time heuristics | Easier to detect, two active slices is explicit and observable |
| User workload impact | Potentially disruptive, may require suspending the job | Non-disruptive from user perspective |
| Failure mode | New slice fails to admit, job gets suspended | Temporary accounting mismatch |
| Ease of remediation | More complex, involves timers and state transitions | Straightforward, finish the old slice |
| Alignment with preemption model | Strong, aligns with gap-based preemption thinking | Weaker, introduces temporary over-commit |
| Implementation complexity | Higher, requires careful timeout or stickiness handling | Lower, simpler control flow |
| Long-term extensibility | Can evolve into semi-transactional “sticky workload” model | Mostly a tactical fix |
| Short-term viability | Acceptable as a quick fix with time-based logic | Attractive for simplicity and user transparency |

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-02-10T09:02:34Z

> Intuitively I think "quota gap" is better, and more aligned with the preemption model. In this mental model I consider another way of fixing it - make the "new workload" sticky, and ensure it gets in front of even high priority workloads. If it does not "get in" after 5s or so, then we evict it - it should be very rare.

It's not rare for complex admission check, like ProvisioningRequest. So I'd suggest to go with option B.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T09:18:36Z

I wouldn't like to jump to this conclusion so quickly. The AdmissionChecks aren't yet supported, we are designing now how to do it. Let's don't over-simplify the design.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-10T16:31:52Z

I am biased toward Option A. At the same time, I agree that there is no critical urgency to change it right now. I suspect we may see manifestations of this problem, in some shape or form, [in this area](https://github.com/kubernetes-sigs/kueue/pull/8861/changes#r2788968355).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T16:55:40Z

I'm in the quota gap camp, because this is the model how our beloved preemption already works. Introducing another mode is another cognitive load. I'm happy to be convinced otherwise with some good examples, but this is where my intuition is.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-17T03:49:39Z

Not expert here, still learning... is this idea possible? Instead of finishing the old workload slice (condition type == `Finished`), we add another condition type `Replaced`, indicating the workload slice is replaced by another one. During resource counting, there is special handling for `Replaced` workload to only count the workload difference.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-17T04:46:46Z

> Not expert here, still learning... is this idea possible? ...

Yes, it is possible. At its core, this corresponds to the **Option B**, two-phase replacement.

Today, the ClusterQueue is completely agnostic to the existence of workload slices, while the scheduler has limited awareness of them, primarily in the context of delta capacity, flavor stickiness, and slice replacement. It would be possible to extend ClusterQueue semantics so it understands that two workload slices are related and accounts for utilization correctly during the transition. Conceptually, this would allow proper handling of replacement without introducing quota gaps or accounting anomalies, and may represent the most robust long-term solution.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-17T05:05:02Z

I think I’m not ready to give up on Option A 🙂

Conceptually, Option B can be seen as a more refined version of Option A, where the ClusterQueue is aware that both slices belong to the same logical workload and accounts for quota accordingly. Instead of temporarily representing the overlap as an artificial quota bump, ClusterQueue would treat the replacement as a transition and account only for the effective capacity of the workload.

In that sense, Option A exposes the underlying replacement behavior explicitly, while Option B formalizes it by making quota accounting replacement-aware.

I want to reiterate that the "quota bump" is artificial in nature, since there is no actual increase in the number of Pods or consumed resources. It is purely a side effect of the ClusterQueue not recognizing that the two workload slices represent the same logical workload and are part of a single replacement transition.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-17T05:21:18Z

## Quota Gap
Within a single scheduling cycle:
* Finish the old slice
* Admit the new slice

Failure mode, admission fails:
* Admission is retried in subsequent scheduling cycles, but may no longer succeed due to quota or scheduling contention
* Job reconciler converges to the new desired state and suspends the Job, since no slice remains admitted
* Workload user experience, instead of completing scale-up, the workload transitions to suspended or pending state

<img width="1023" height="476" alt="Image" src="https://github.com/user-attachments/assets/1b0f0fd5-0c78-4321-b8e6-208f6871bd54" />

This model preserves strict quota accounting at all times, but introduces a disruptive failure mode when replacement admission does not complete successfully.

## Quota Bump
Within a single scheduling cycle:
* Admit the new slice
* Finish the old slice

Failure mode, finishing the old slice is delayed or retried:
* No additional admission cycles are required, since the new slice is already admitted
* Job reconciler converges naturally, and the old slice is eventually marked Finished
* Workload user experience remains consistent with scale-up semantics, with no suspension or disruption
* Side effect:
  * For a brief period, ClusterQueue utilization may be temporarily inflated, as both slices are accounted simultaneously
  * This is an accounting artifact rather than an increase in actual resource usage, since both slices represent the same logical workload transition

<img width="1047" height="494" alt="Image" src="https://github.com/user-attachments/assets/889c65bb-b64c-4436-8d5f-9f963b957875" />

This model preserves workload continuity and avoids disruptive failure modes, at the cost of temporary accounting inconsistency.

## Quota Bump without Bump (a.k.a. Option B)

An improved version of Quota Bump, where ClusterQueue is aware of the relationship between workload slices representing the same logical workload. Instead of accounting both slices independently, ClusterQueue treats the transition as a replacement operation and accounts only for the effective capacity of the workload.

This preserves the non-disruptive admission behavior of Quota Bump while eliminating the artificial quota inflation caused by double accounting during the transition.

---

## Why I believe ‘Quota Bump’ is the better option

* Preserves a consistent, non-disruptive user experience during scale-up, the workload remains admitted throughout the transition and avoids suspension or rollback behavior
* Failure modes are localized to accounting artifacts rather than workload lifecycle disruption, making them easier to detect, reason about, and remediate
* Aligns with the natural replacement semantics of elastic workloads, where capacity is transferred rather than relinquished and reacquired
* Avoids reliance on timeout-based heuristics or stickiness mechanisms to restore correctness
* Provides a natural evolutionary path toward "Quota Bump without Bump", where ClusterQueue becomes replacement-aware and eliminates artificial over-accounting while preserving non-disruptive semantics

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-02-17T09:48:15Z

Not sure I follow. In Quota Bump you mentioned: `No additional admission cycles are required, since the new slice is already admitted`. What if the admission fails and the new admission cycle is required?

@mimowo, regarding `because this is the model how our beloved preemption already works`. I agree, however, I don't thing the preemption was designed to take ProvisioningRequest into account. However, we want to support it for elastic workloads.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-17T16:18:19Z

> Not sure I follow. In Quota Bump you mentioned: `No additional admission cycles are required, since the new slice is already admitted`. What if the admission fails and the new admission cycle is required?

It is important to keep the context in mind. We are not dealing with general scheduling, which may indeed require multiple admission cycles. Instead, we are discussing a specific edge case during slice replacement, where two ordered steps must occur and the behavior differs depending on their order.

In the "Quota Gap" model, the first step is "Finish Old Workload Slice". If the second step, "Admit New Workload Slice", fails, the system enters a state where no slice is admitted. From there, we must either rely on additional scheduling cycles to admit the new slice and restore the intended state, or trigger cleanup by suspending or unadmitting the workload. In other words, the system must either catch up or clean up.

In the "Quota Bump" model, the first step is "Admit New Workload Slice". If this step fails, nothing changes, the old slice remains admitted and the workload continues running. This is equivalent to a scale-up attempt that did not succeed and does not introduce any inconsistency. The important distinction is that the two-step replacement process only begins after the new slice has been successfully admitted. Once that happens, the second step, "Finish Old Workload Slice", is a convergence action. If finishing is delayed or retried, it does not require additional scheduling cycles, because the workload is already admitted and quota accounting can be corrected asynchronously by the Job reconciler.

I hope this helps clarify the distinction. Please let me know if this still seems inconsistent or if additional clarification would be helpful.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-17T16:22:15Z

> [@mimowo](https://github.com/mimowo), regarding `because this is the model how our beloved preemption already works`. I agree, however, I don't thing the preemption was designed to take ProvisioningRequest into account. However, we want to support it for elastic workloads.

@mimowo I agree that the quota gap model aligns well with how preemption works today. However, workload slice replacement is fundamentally different from preemption.

Preemption represents a transfer of quota between unrelated workloads. It inherently requires multiple scheduling cycles, one to evict or finish the preempted workload, and one or more subsequent cycles to admit the replacement workload once quota becomes available. This multi-cycle behavior is expected, since the scheduler must first reclaim capacity before reallocating it.

Workload slice replacement, on the other hand, is an internal transition of a single logical workload. Under normal operation, replacement completes within a single scheduling cycle, admit the new slice and then finish the old slice. There is no transfer of quota between independent workloads, only reassignment within the same workload.

Because of this, replacement should preserve workload continuity and quota ownership across the transition. The apparent "quota bump" is therefore an accounting artifact caused by ClusterQueue not recognizing the relationship between slices, rather than an actual increase in resource usage or a violation of quota semantics.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T16:32:57Z

@ichekrygin thank you for the extensive summary. Indeed, if we could make `Option B` then it is probably best conceptually, I'm just a little bit afraid of the new complexity added, but I agree having continuity of admission looks best. Re-using "preemption" mechanism "works", but tclearly it wasn't design for the case when two workloads share Pods.

I believe this would also help @sohankunkerkar for the integration in TAS to more atomically transfer the Pod sasignments between workloads.

Let me ask a more engineering question, assuming we choose this option, what does it entail? IIUC: we need change order, first admit the new, then Finish the old - which is also a novelty. Do we need the new "Replacing" state for that, or could we infer the steps based on already existing primitives?

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-02-19T09:14:30Z

@ichekrygin thanks for clarifying! 
I agree that the preemption case need to be finished before admitting the workload, because otherwise we may not have the capacity to run the workload. For the WorkloadSlice replacement this is a different case, since the new WorkloadSlice is already partially running and we just removing scheduling gate from the new pods. All operations with WorkloadSlice replacement is actually the inner kitchen. And it seems that Quota Bump option is actually better serves the WorloadSlice replacement story.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-01T15:45:51Z

@mimowo @tenzen-y 

Should we close this?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-01T17:26:31Z

let me re evaluate this next week

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-04-06T11:21:23Z

Were any changes made regarding the issue?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-04-06T14:55:21Z

@yaroslava-serdiuk not sure if the question is directed specifically to me or more broadly to the reviewers and maintainers.

From my perspective, there haven’t been any substantial changes addressing the core issue. It seems possible that maintainers may be considering a different direction that does not center around WorkloadSlices, which could explain the lack of meaningful progress.

That said, I may be wrong, so would appreciate clarification if there have been updates or a shift in approach.
