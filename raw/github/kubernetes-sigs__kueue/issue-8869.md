# Issue #8869: DRAFT: Temporary Nominal Quota Reassignment via ResourceQuotaLease (Alternative to Uber ClusterQueue)

**Summary**: DRAFT: Temporary Nominal Quota Reassignment via ResourceQuotaLease (Alternative to Uber ClusterQueue)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8869

**Last updated**: 2026-02-04T20:22:18Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-01-29T01:55:29Z
- **Updated**: 2026-02-04T20:22:18Z
- **Closed**: —
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 11

## Description

### Background

The current [KEP-8826](https://github.com/kubernetes-sigs/kueue/pull/8864) proposes introducing a special type of ClusterQueue (UberQueue) that is allowed to preempt workloads across a cohort subtree, including workloads running within other ClusterQueues’ nominal (guaranteed) quota.

While the motivating use case is valid, this approach is problematic because it:

* Breaks the core invariant that nominal quota represents a protected guarantee.
* Introduces a precedent for privileged preemption semantics (“hero / uber queues”), with a risk of escalation (hero-hero, uber-uber).
* Makes “wartime” behavior implicit and less transparent to ClusterQueue owners.

### Alternative Approach

Instead of introducing a special preemption mode driven by a special type of ClusterQueue, this proposal explores a different direction:

**Introduce a temporary nominal quota reassignment mechanism**, expressed via an explicit, admin-owned object (for example, `ResourceQuotaLease`), that temporarily reassigns nominal quota from one or more donor ClusterQueues to a target ClusterQueue.

This preserves existing scheduling and preemption semantics by changing *quota ownership*, not *preemption rules*.

### High-Level Idea

* Nominal quota remains the protection boundary.
* “Wartime” is modeled as a **temporary transfer of nominal quota**, not an override of guarantees.
* Existing Kueue reclaim and preemption logic remains unchanged.

### Example

**Peacetime**

* Cohort contains:

  * CQ-A: nominal 100
  * CQ-B: nominal 100
  * CQ-C: nominal 0 (hero / training queue)
* CQ-A and CQ-B can borrow from each other subject to limits.

**Wartime (Lease Active)**

* A `ResourceQuotaLease` reassigns:

  * 100 nominal from CQ-A → CQ-C
  * 100 nominal from CQ-B → CQ-C

Resulting state:

* CQ-A: nominal 0
* CQ-B: nominal 0
* CQ-C: nominal 200

### Behavior of Already-Admitted Workloads

* No immediate evictions occur when the lease is created.
* Workloads in CQ-A and CQ-B that now exceed their reduced nominal are considered **over nominal**.
* This over-nominal usage is effectively **borrowing capacity from the cohort** and is therefore eligible for reclaim under existing Kueue semantics.
* Evictions only occur if and when CQ-C attempts to admit workloads and needs capacity.
* Existing Kueue reclaim semantics apply:

  * Only the minimum required workloads are evicted.
  * Eviction is governed by existing preemption configuration (priority, reclaimWithinCohort, etc.).
* If CQ-C has no demand, there is no disruption.

No `Hold` or `HoldAndDrain` semantics are required.

### Behavior of New Workloads

* **New workloads submitted to donor ClusterQueues (for example, CQ-A or CQ-B)** are subject to their reduced nominal quota while the lease is active.

  * If a donor CQ’s reduced nominal is fully consumed, new workloads may still be admitted only via existing borrowing semantics, subject to configured borrowing limits and cohort availability.
  * If borrowing is not possible, workloads remain pending as usual.
  * No special admission blocking or implicit draining behavior is introduced.

* **New workloads submitted to the lease holder ClusterQueue (CQ-C)** are admitted against its increased nominal quota resulting from the lease.

  * As long as sufficient nominal quota is available, workloads are admitted without borrowing.
  * If admitting a workload requires reclaiming capacity from donor ClusterQueues that are over nominal, existing Kueue preemption logic applies.
  * Only the minimum amount of reclaim needed to satisfy admission is performed.

* **No new scheduling or preemption rules are introduced** for either donors or the lease holder.

  * Admission, borrowing, and reclaim decisions continue to be governed entirely by existing Kueue primitives (nominal quota, borrowing limits, reclaimWithinCohort, priority, etc.).

This ensures that new workloads behave consistently with the adjusted quota ownership, without introducing a separate “wartime” admission mode or special-case logic.

### Why This Is Preferable

* Preserves the meaning of nominal quota as a hard guarantee.
* Avoids introducing a privileged “Uber” preemption mode.
* Makes wartime behavior explicit, auditable, and time-bound.
* Eliminates the “hero-hero / uber-uber” escalation problem.
* Keeps scheduling behavior explainable using existing Kueue primitives.
* Improves transparency: reduced nominal capacity on donor ClusterQueues is an explicit and observable result of an active lease, captured in both the `ResourceQuotaLease` object and reflected in affected ClusterQueues’ status conditions.

### Open Design Questions

* Lease lifecycle and rollback semantics (TTL, early termination, cooldown).
* Validation requirements (for example, ensuring the lease holder CQ has appropriate reclaim settings).
* Interaction with fair sharing and borrowing limits.
* Scope constraints (for example, at most one active lease per cohort subtree).

### Goal of This Issue

The goal is not to block the original KEP, but to discuss whether **temporary nominal quota reassignment** provides a safer and more transparent alternative that achieves the same operational goals without weakening Kueue’s core guarantees.

Feedback welcome.

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T03:55:27Z

Below is a **gross oversimplification** of both concepts — **UberQueue** and **ResourceQuotaLease** — but it should help convey the core idea and the semantic difference between the two.

### UberQueue (KEP-8826)

In this model, nominal ownership does **not** change. Instead, a special ClusterQueue is allowed to **preempt workloads in other ClusterQueues even when they are running within their nominal quota**.

<img width="835" height="250" alt="Image" src="https://github.com/user-attachments/assets/2bab7af3-6ee3-4484-ac7e-7fea0b28a640" />

Key properties:

* Nominal quota on CQs remains unchanged.
* Workloads are evicted **despite being within nominal**.
* Eviction is driven by privileged preemption rules, not quota ownership changes.
* “Wartime” behavior is implicit and inferred from preemption events.

---

### ResourceQuotaLease (Alternative)

In this model, nominal quota is **temporarily reassigned** from donor ClusterQueues to a target ClusterQueue via an explicit, admin-owned lease object. Existing reclaim semantics are reused.

<img width="1144" height="250" alt="Image" src="https://github.com/user-attachments/assets/b2bd2c76-e57f-4b8b-bc0b-0d4a06843064" />

Key properties:

* Nominal quota ownership changes explicitly and temporarily.
* Donor workloads become **over nominal** and therefore reclaimable.
* Evictions are demand-driven and governed by existing Kueue preemption rules.
* “Wartime” is explicit, auditable, and time-bound via the lease object.
* Lease termination restores nominal quota and adjusts workload admission accordingly.

---

The intent here is not to provide an exact behavioral model, but to highlight the **conceptual difference**:

* **UberQueue** overrides guarantees via privileged preemption.
* **ResourceQuotaLease** preserves guarantees by changing who owns nominal quota.

Both can satisfy the same operational goal, but they do so with very different tradeoffs in terms of guarantees, transparency, and precedent.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2026-01-29T08:58:47Z

Thank you for posting that, that's a very interesting idea!

If I understand correctly the cluster administrator is responsible for the whole lifecycle of the Lease CRD object - creating it in a proper size, deleting after all workloads are done, etc. 

TBH, i would rather prefer this to be automatic so that all interaction of researchers with K8S cluster do not require Kueue administrator specific knowledge. 

The idea of modifying nominal quota doesn't differ much from what I'm proposing. In the KEP #8826 there is  accessible quota and increase of borrowing limit (if present), however only in memory, without persisting it in the spec.

How can we meet somewhere in the middle?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T10:08:25Z

Interesting idea indeed.

One nice property of the dedicated CRD for `ResourceQuotaLease` is that we could have a natural place to define some extra parameters for the lease. 

I imagine "hero" workloads are handled differently in different organizations, and so some customization will be needed sooner or later. For example, we could use them to "exclude" some CQs from the "lease" or configure weights for the balancing of the "nominal quota" piece "eaten" from other ClusterQueues. 

We could also define some "start" and "end" time for the lease expiration and then maybe we could also cover business uses cases of https://github.com/kubernetes-sigs/kueue/issues/8654.

> TBH, i would rather prefer this to be automatic so that all interaction of researchers with K8S cluster do not require Kueue administrator specific knowledge.

Right, indeed in the custom CRD model researchers need to "wait" for the admin to create the lease, while in the UberClusterQueue proposal, the researchers with the privilidge just create the workloads in the UberClusterQueue.

I think we could somehow achieve it in the `ResourceQuotaLease` model. Maybe there is room to combine the two ideas: UberCQ configuration can say "Create ResourceQuotaLease when there is a workload pending in the CQ".

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T16:50:53Z

> The idea of modifying nominal quota doesn't differ much from what I'm proposing. In the KEP [#8826](https://github.com/kubernetes-sigs/kueue/issues/8826) there is accessible quota and increase of borrowing limit (if present), however only in memory, without persisting it in the spec.

Thanks for the thoughtful response, this is helpful context.

I may be seeing this a bit differently, so I wanted to clarify one point. While both approaches may lead to a similar *outcome* (capacity being made available to a critical workload), I think they differ in important ways conceptually.

In KEP-8826, the mechanism is an implicit, in-memory override: nominal ownership on ClusterQueues does not change, but a special queue is allowed to preempt workloads in other CQs even when those workloads are within nominal. From a workload or CQ owner’s perspective, this can manifest as preemption or failed admission without any visible change in their own CQ state, even when nominal capacity appears unused. The reason for disruption is therefore opaque and must be inferred.

In contrast, the lease-based approach makes the cause explicit and user-facing. Nominal quota is temporarily reassigned, and that reduced capacity is directly observable on the affected ClusterQueues and attributable to a specific lease. From a CQ owner’s point of view, preemption or failed admission is an expected and explainable consequence of temporarily reduced nominal capacity, not a hidden scheduling override. This distinction matters because the ClusterQueue is itself a user-facing API and a contract.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T16:55:34Z

> TBH, i would rather prefer this to be automatic so that all interaction of researchers with K8S cluster do not require Kueue administrator specific knowledge.

One additional thought on automation: the explicit intent is important, especially when we frame this in terms of “peacetime” vs “wartime”, but I do think there is room for automation *around* an explicit mechanism.

For example, one could imagine something like a `LeaseWatch` policy, where admitting a workload into a designated “hero/uber” ClusterQueue that lacks sufficient capacity could automatically trigger creation of a temporary lease against other ClusterQueues in the same cohort (possibly subject to opt-in / opt-out rules). The key point would be that the resulting nominal reassignment is still explicit and observable, even if the act of creating the lease is automated.

This is by no means a fully thought-through design, but I wanted to acknowledge that automation and explicit semantics don’t have to be mutually exclusive. We could preserve a clear, user-visible explanation for why capacity changed, while still avoiding manual intervention in the common case.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T17:01:24Z

> If I understand correctly the cluster administrator is responsible for the whole lifecycle of the Lease CRD object - creating it in a proper size, deleting after all workloads are done, etc.

That’s a fair reading of the initial sketch, though I want to emphasize that this isn’t fully thought through yet. The examples so far intentionally use a *complete* nominal donation to keep the discussion simple.

In practice, I don’t think a lease would have to be all-or-nothing. The lease spec could be more nuanced and allow expressing the reassignment in terms of either an absolute quantity (for example, `cq.quantity`) or a relative share (for example, `cq.%`). That would allow finer-grained control over how much nominal capacity is temporarily rebalanced, and avoid forcing a full handover when only partial capacity is needed.

The key point for me is less about the exact shape of the lease API and more about preserving explicit, user-visible quota semantics, even if the mechanism itself evolves.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T17:03:55Z

Thank you, @mwielgus and @mimowo,  for taking the time to review and discuss this alternative, I really appreciate the thoughtful engagement. A key takeaway for me is the value of focusing the discussion on **resource quota rebalancing** rather than on introducing a special dominance hierarchy between ClusterQueues with custom preemption rules. The former feels more naturally aligned with existing quota semantics and ownership, while the latter introduces a new axis of behavior that may be harder to reason about over time.

### Comment by [@saza-ku](https://github.com/saza-ku) — 2026-02-03T17:40:59Z

This feature has the potential to meet our use case requirements (#8654)

Both Uber queues and ResourceQuotaLease assume a scenario where all cluster resources are already allocated to ClusterQueues. The key challenge then becomes how to accommodate workloads (Hero Workloads) that would consume the majority of cluster resources under these conditions.

In contrast, our scenario involves ClusterQueues holding some portion of the cluster's resources, with the remainder managed by their parent cohort. Our current challenge is to automate the process of temporarily assigning these excess resources to specific ClusterQueues.

If ResourceQuotaLease could meet the following requirements, we believe it would solve our problem. How do you feel about this?
- Moving quotas from parent cohorts to ClusterQueues
- Automation through explicit specification of ResourceQuotaLease validity periods
- A design where administrators, not researchers, operate ResourceQuotaLease

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-03T18:54:21Z

> In contrast, our scenario involves ClusterQueues holding some portion of the cluster's resources, with the remainder managed by their parent cohort. Our current challenge is to automate the process of temporarily assigning these excess resources to specific ClusterQueues.

It would be very helpful to explicitly clarify **where nominal quota is held** in this scenario.

If I’m understanding your use case correctly, the setup looks something like this:

* A **Cohort** that holds some portion of nominal quota directly.
* One or more **ClusterQueues under that Cohort** (for example, CQ-A), which may also have nominal quota.
* Possibly additional sibling CQs under the same Cohort, with or without nominal quota.

The question then seems to be whether the ask is to:

* Temporarily reassign nominal quota **from the Cohort to a specific ClusterQueue (for example, Cohort → CQ-A)**, or
* Something slightly different.

Assuming the former (that is, shifting nominal quota from the Cohort down to CQ-A), I’m wondering whether this reassignment is strictly necessary. If a workload is admitted into CQ-A with sufficiently high priority, existing reclaim semantics should already allow it to preempt and reclaim capacity from within the cohort.

Would that behavior address your use case, or is there a specific requirement that reclaim-based preemption does not satisfy?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-02-03T19:10:25Z

@saza-ku 

I want to clearly delineate **two distinct use cases** that deal with nominal resource sharing and strong guarantees.

**First**, nominal resource quota sharing between a **Cohort and its ClusterQueues**, with or without contention.
Today, Kueue already provides mechanisms to handle this case, and the example above illustrates how this works. In this model, guarantees are primarily provided and enforced through **workload priority and reclaim semantics**.

**Second**, nominal resource quota sharing **between sibling ClusterQueues under the same Cohort**.
Today, a ClusterQueue may lend its nominal quota, but from the borrower’s perspective there are **no strong guarantees**—regardless of workload priority. Borrowed capacity can always be reclaimed, which makes it unsuitable for workloads that require stable guarantees.

This proposal introduces **ResourceQuotaLease** as a mechanism to address that gap by enabling **temporary nominal quota reassignment** (donation or lease), thereby providing explicit and time-bound guarantees to the lease holder.

By contrast, the original KEP proposes a different model: introducing a special type of ClusterQueue whose workloads can override and supersede other workloads in the cohort, including workloads running within other ClusterQueues’ nominal quota. This achieves a similar outcome, but via privileged workload handling rather than explicit quota ownership changes.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T20:22:18Z

> A key takeaway for me is the value of focusing the discussion on resource quota rebalancing

Indeed I think one of the strengths of the UberClusterQueue KEP currently is that the quota taken by the "UberClusterQueue" is balanced among the other ClusterQueues in the cohort, but it is not necessarily binary, just lowers the "nominal quotas" to "effective nominal quotas" uniformly. I'm confident it can be achieved here too.
