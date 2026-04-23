# Issue #8729: Workload Scheduling Constraints (Workload-Level) and Preference-Aware MultiKueue Dispatching

**Summary**: Workload Scheduling Constraints (Workload-Level) and Preference-Aware MultiKueue Dispatching

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8729

**Last updated**: 2026-01-28T18:37:24Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-01-22T03:24:02Z
- **Updated**: 2026-01-28T18:37:24Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kueue today supports preference-based placement via flavor fungibility, but these preferences are **soft-only** and cannot be expressed as **hard scheduling constraints**. In addition, MultiKueue dispatching strategies (`AllAtOnce`, `Incremental`) are **race-based**, meaning the first worker cluster that admits a workload wins, regardless of whether that placement is optimal.

This issue proposes extending Kueue with **workload-level scheduling constraints** and updating MultiKueue dispatching to be **preference-aware** rather than timing-driven.


**Scheduling constraints must be specified per workload, at the workload level.**

They should **not** be global defaults and should **not** be ClusterQueue-wide policies.
The intent is to allow different workloads sharing the same ClusterQueue to express different scheduling requirements.

This mirrors Kubernetes design patterns, where constraints are typically attached to the object being scheduled (e.g., Pods), not to the scheduler or queue globally.

**Why is this needed**:

## Problem

### Single-cluster limitations

Currently, users cannot express strict workload-specific guarantees such as:

* “This workload must not preempt other workloads.”
* “This workload must not borrow quota from a cohort.”
* “If these conditions cannot be met, keep this workload pending.”

If borrowing or preemption is enabled at the ClusterQueue level, Kueue may eventually use them for *all* workloads, even when a specific workload would prefer to wait.

This makes it impossible to express **per-workload hard guarantees**, only queue-wide soft ordering.

This limits Kueue’s usefulness for:

* SLA-sensitive workloads
* Fairness- or isolation-critical workloads
* Budget- or quota-bound workloads
* Mixed workloads sharing the same ClusterQueue

### MultiKueue limitations

MultiKueue dispatching modes (`AllAtOnce`, `Incremental`) are fundamentally race-based:

* Workloads are dispatched to multiple worker clusters.
* The first cluster to admit the workload wins.
* No comparison of placement quality is performed.

This can result in:

* A cluster that admits a workload using borrowing winning over a cluster that could admit the same workload without borrowing
* A cluster that admits a workload using preemption winning over a cluster that could admit it without requiring preemption
* Non-deterministic placement driven by control-plane timing rather than placement quality
* Unnecessary workload preemption, even though the workload ultimately runs on a different cluster, because MultiKueue nominated another cluster as the winner

These semantics break the flavor fungibility mental model across clusters.

### Example

Assume a workload with **no borrowing, no preemption** constraints is dispatched to three clusters:

| Cluster | Admission Result                     |
| ------- | ------------------------------------ |
| A       | Fits without borrowing or preemption |
| B       | Fits with borrowing                  |
| C       | Fits with preemption                 |

Today, B or C may win simply because they respond faster. 

Moreover, workload preemption will be triggered on cluster C **_irrespective_** of the final workload placement, even if the workload ultimately runs on a different cluster.

Desired behavior:

* The workload should only be admitted on **A**
* If A is unavailable, the workload should remain pending

## Proposed Direction

### 1. Add workload-level constraint-aware scheduling to Kueue

Extend the Workload API to support **hard placement constraints**, evaluated per workload.

Illustrative API examples:

```yaml
spec:
  admissionConstraints:
    requireNoBorrowing: true
    requireNoPreemption: true
```

Or a more expressive form:

```yaml
spec:
  placementPolicy:
    borrowing: Forbidden | Allowed 
    preemption: Forbidden | Allowed
```

Key properties:

* Constraints are evaluated **per workload**
* Constraints override queue-wide capabilities
* If constraints are not satisfied, the workload remains pending

### 2. Surface reasoned admission rejections

Instead of only reporting admitted / not admitted, Kueue should surface structured rejection reasons: "Unsatisfied Admission Constraint due to:"
* Requires borrowing
* Requires preemption

This enables higher-level scheduling logic and MultiKueue dispatching to reason about failures.

### 3. Make MultiKueue dispatching preference-aware

Once workload-level constraints exist, MultiKueue dispatching can move away from races.

Instead of “first admission wins”, MultiKueue should:

```
For preference tier P1:
  Try all clusters
If none accept:
  Move to P2
Repeat
```

Preference tiers are derived from **workload-level constraints**, not queue defaults.

This preserves flavor fungibility semantics across clusters while respecting per-workload guarantees.

## Benefits

* Enables **per-workload** hard scheduling guarantees
* Allows heterogeneous workloads to safely share ClusterQueues
* Preserves flavor fungibility semantics across clusters
* Eliminates race-based placement
* Improves determinism and placement quality
* Avoids unnecessary borrowing and preemption
* Keeps a clean separation between single-cluster admission and multi-cluster dispatching

## Conclusion

This issue proposes introducing a missing scheduling primitive in Kueue: **workload-level hard scheduling constraints**, and extending MultiKueue to be **preference-aware** instead of race-based.

The guiding principle is:

> The scheduler should select the best feasible placement for a given workload, not the fastest one.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-22T15:58:39Z

This does feel like maybe we should think through how this would eventually overlap with Workload Aware Scheduling in Kubernetes.

cc @mimowo @tenzen-y @mwielgus

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-22T16:03:07Z

My main issue is that we don't really have a great way to put workload level scheduling policies on workloads like Jobs, JobSet, LWS. We could define annotations but I expect that eventually these ideas would be part of https://github.com/kubernetes/kubernetes/issues/132192

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-22T18:32:26Z

@kannon92 thank you,  for taking a look and for the feedback.

> we don't really have a great way to put workload level scheduling policies on workloads like Jobs, JobSet, LWS

That’s a fair concern, and I agree that there’s some inherent impedance mismatch between Kueue’s abstractions (Workload, ClusterQueue, etc.) and native Kubernetes workload APIs like Job, JobSet, and LWS.

That said, this mismatch already exists today, and Kueue has generally handled it by projecting its semantics onto native objects via metadata, most commonly labels, and sometimes annotations. Whether it’s labels or annotations is somewhat secondary, the important part is that this has been the established integration pattern so far.

From that perspective, expressing admission or scheduling constraints in a similar way would be consistent with existing Kueue practices, rather than introducing a fundamentally new model. Of course, if there’s a longer-term plan to make these concepts first-class in upstream APIs, that would be even better, but until then, this seems like a pragmatic and aligned approach.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T12:36:19Z

IMO this proposal runs very deep, and AFAIK against the principles of role separation in Kueue. 

Kueue intentionally takes responsibility for quota management (borrowing, preemption, etc) away from users to admins who configure the ClusterQueues. It is admins' responsibility to configure them well, and users' responsibility to send the workloads to the dedicated ClusterQueues. The proposal makes the role distinction blurry.

Also, some features like fair sharing could be violated in non-trivial ways, because Workload-specific configurations may prevent reclaiming quota etc. 

Such architectural changes need discussion at the wg-batch, so I would propose the topic there.

In the meanwhile cc @tenzen-y @gabesaba @mwielgus who may have some views here.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-26T19:37:09Z

Thank you, @mimowo, for taking a look and for the thoughtful feedback.

I fully acknowledge that this is a different type of feature request and that it warrants careful review and consideration. I welcome any feedback and discussion on the proposal. That said, once we get into the details, I don’t believe the changes are as deep or disruptive as the title may initially suggest, since they build on existing concepts rather than introducing entirely new ones. Of course, it is entirely possible that I am missing aspects of the bigger picture or more subtle interactions, and I would appreciate any insights that help surface those.

---

> Kueue intentionally takes responsibility for quota management (borrowing, preemption, etc.) away from users to admins who configure the ClusterQueues.

The proposed workload scheduling (admission) constraints are not intended to expose users to quota management itself. Rather, the intent is to allow users to express preferences around the **quality of scheduling outcomes**, not to control quota mechanics. Conceptually, this reuses the existing flavor-fungibility model, allowing it to operate not only in a preference-based mode but also in a constraint mode when stricter placement guarantees are required.

A possible analogy is pod or node affinity in Kubernetes. Users are not managing nodes or other pods directly, yet they can express scheduling requirements and preferences that influence placement. Similarly here, admins would continue to fully own quota configuration, borrowing, preemption, and fair-sharing policy via ClusterQueues, while users can express what kinds of placements are acceptable for a given workload.

In terms of flavor fungibility, this analogy applies as well. Today, Kueue’s support for flavor fungibility is analogous to Kubernetes affinity expressed as **“preferred”** during scheduling, influencing placement but not enforcing it. The proposed workload admission and scheduling constraints extend this model by allowing workloads to express **“required”** semantics during admission, enforcing stricter placement guarantees when needed.

---

> The proposal makes the role distinction blurry.

I do acknowledge that this proposal touches a deliberate design choice in Kueue, namely that quota semantics and fairness policy are owned by administrators and expressed via ClusterQueues, while users select an appropriate queue for their workloads. That separation is important and should be preserved.

At the same time, I do not see this proposal as changing ownership of quota policy. Admin intent remains authoritative and fully expressed through ClusterQueues. Workload-level constraints do not override or bypass admin-configured behavior; they only allow a workload to opt into *more restrictive* admission semantics within the bounds already defined by the ClusterQueue. In practice, this means a workload may wait longer or remain pending, but it cannot gain additional scheduling power or priority.

---

> Also, some features like fair sharing could be violated in non-trivial ways, because workload-specific configurations may prevent reclaiming quota, etc.

I may be misunderstanding the concern here, but I am not seeing how this would violate fair sharing. The impact of an admission or scheduling constraint is strictly limited to the workload that defines it. The effect is inherently *restrictive*: the workload may remain inadmissible longer, or indefinitely, rather than being admitted under a suboptimal placement.

Once a workload is admitted, it is subject to exactly the same quota accounting, borrowing, preemption, and fair-sharing rules as any other workload. These constraints cannot elevate a workload’s priority, protect it from reclaim, or shift pressure onto other workloads in a way that is not already permitted by ClusterQueue configuration. The worst-case outcome is reduced scheduling opportunity for that workload, not increased impact on others.

If there are concrete scenarios where this could interfere with reclaiming quota or fair-sharing guarantees, I would appreciate clarification so we can reason about those cases explicitly.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T09:00:45Z

I see, thank you for explaining! 

I was a bit confused about the title thinking the scope goes beyond that. For example I somehow assumed it would also give users the power to say "don't preempt me". 

However, if this is just about saying "I cannot preempt during admission", and "I cannot borrow during admission", then I think this is a perfectly valid request. 

I guess we could use some Job annotations like `kueue.x-k8s.io/no-preemption` or `kueue.x-k8s.io/no-borrowing`. Alternatively something more generic like `kueue.x-k8s.io/preemption-mode` like NoReclaim, etc.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-27T16:27:17Z

>I was a bit confused about the title thinking the scope goes beyond that. For example I somehow assumed it would also give users the power to say "don't preempt me".

No worries at all, I can totally see how the title could be read that way. That confusion is on me, the wording didn’t clearly convey that the scope is limited to admission-time constraints.


> I guess we could use some Job annotations like `kueue.x-k8s.io/no-preemption` or `kueue.x-k8s.io/no-borrowing`. Alternatively something more generic like `kueue.x-k8s.io/preemption-mode` like NoReclaim, etc.

My thinking is very much along the same lines.

In my PoC, I experimented with a single annotation encoding the admission constraints:

```yaml
annotations:
  # Admission constraint: AllowPreemption.AllowBorrowing.
  # Interpretation:
  # | Allowed Preemption | Allowed Borrowing | Result                                                 |
  # | ------------------ | ----------------- | -------------------------------------------------------|
  # | False              | False             | Must fit without preemption or borrowing               |
  # | False              | True              | Must fit with borrowing(if needed), but cannot preempt |
  # | True               | False             | Must fit with preemption(if needed), but cannot borrow |
  # | True               | True              | Borrowing and preemption allowed, same as default      |
  kueue.x-k8s.io/admission-constraint: "False.False"
```

Using a single field was mostly a convenience choice. That said, I now tend to prefer **discrete, explicit annotations**, similar to what you suggested, since they are easier to read, reason about, and evolve:

```yaml
annotations:
  kueue.x-k8s.io/cannot-preempt: "true"   # default: false
  kueue.x-k8s.io/cannot-borrow: "true"    # default: false
```

This feels more self-descriptive, avoids encoding semantics into a string, and leaves room to extend admission-time constraints incrementally without redefining a combined schema.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-27T16:37:44Z

@mimowo, If there are no objections from other maintainers, what would you see as the best way forward?

Do you think this could be addressed as part of this issue alone, or do you see a strong reason why it would need to be followed by a KEP?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T16:45:38Z

> @mimowo, If there are no objections from other maintainers, what would you see as the best way forward?

No objections from me, looks quite reasonable, I already include it tentatively in the plan for 0.17: https://github.com/kubernetes-sigs/kueue/issues/8829

cc @gabesaba @tenzen-y 

> Do you think this could be addressed as part of this issue alone, or do you see a strong reason why it would need to be followed by a KEP?

I would prefer to start with a KEP, because this is API surface for users.

> annotations:
>  kueue.x-k8s.io/cannot-preempt: "true"   # default: false
>  kueue.x-k8s.io/cannot-borrow: "true"    # default: false

This looks reasonable, but let's discuss the details in the KEP. I'm still wondering about "enum"-like annotations to open for the future variants, but I don't have a strong view here.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-27T16:57:47Z

> This looks reasonable, but let's discuss the details in the KEP. I'm still wondering about "enum"-like annotations to open for the future variants, but I don't have a strong view here.

Sounds good. I’ll move forward with drafting a KEP and we can use that to discuss the details, including whether an enum-like annotation makes sense for future extensibility.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T18:48:02Z

I understand the described user stories, and I agree with moving to the KEP phase.

> kueue.x-k8s.io/cannot-preempt

I would like to investigate the possibility of extending WorkloadPriorityClass with no preemption mode instead of introducing Workload level annotation. @ichekrygin Is this new WorkloadPriorityClass enhancement can help your story?

> kueue.x-k8s.io/cannot-borrow

In this scenario, we probably need to introduce such workload-level labels (or annotations). I have no idea for alternative approach. Technically, we might be able to expand WorkloadPriorityClass, but borrowing is not executed based on Priority.
So, the label approach might be better.

Anyway, I'm happy with discussing in KEP!

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-27T20:08:13Z

Thanks, @tenzen-y, for the thoughtful suggestions. I’m drafting a KEP and will include extending `WorkloadPriorityClass` (WPC) as a possible alternative.

One concern with relying solely on priority classes is a semantic mismatch. A WorkloadAdmissionConstraint (WAC) is **unidirectional**: `cannot-preempt` only restricts this workload’s ability to preempt others, independent of its priority. In contrast, `WorkloadPriorityClass` is **bidirectional**, it affects both whom the workload can preempt and who can preempt it.

As a result, using a very low priority to avoid preempting others also makes the workload more likely to be preempted itself, which is not always the intended behavior. WAC allows expressing this intent more precisely.

I’ll cover this distinction and the trade-offs between WAC and WPC in more detail in the KEP.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T06:49:31Z

> As a result, using a very low priority to avoid preempting others also makes the workload more likely to be preempted itself, which is not always the intended behavior. WAC allows expressing this intent more precisely.

Yes, that is a discussion point about (a) WPC vs (b) Job annotations. I assume the use case for (a) is that cluster admins restrict choice for preference representation (guardrail), which means researchers can represent WAC preference only within matched Priority × Preemption Preference. The use case for (b) is that the cluster admins fully delegate decision-making to researchers, which is flexible for researchers, but it might cause inefficient cluster capacity usage.

But I think both (a) and (b) can be introduced. 
If your story is only (b), I'm ok with treating (a) as a separate enhancement.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T18:37:22Z

/assign @ichekrygin
