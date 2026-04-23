# Issue #6901: Clean up: "Previously" evicted/preempted condition message.

**Summary**: Clean up: "Previously" evicted/preempted condition message.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6901

**Last updated**: 2025-09-18T13:30:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-17T19:17:33Z
- **Updated**: 2025-09-18T13:30:17Z
- **Closed**: 2025-09-18T13:30:17Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
This is a follow-up issue to: 6819.

https://github.com/kubernetes-sigs/kueue/pull/6819#discussion_r2356499034

This might not be the right place fix the bug. If I understand correctly, we’d expect the condition **message and reason** to be refreshed whenever a condition is (re)activated.

For example, if we re-evict a previously evicted and later re-admitted Workload, I’d expect the active condition to carry an eviction-specific message, e.g., “evicted by …”. The only way we end up with a repeatedly prefixed message is either:

* we do not reset the message on a new eviction (less likely), or
* we repeatedly call `SetQuotaReservation` and keep “updating” already inactive Evicted or Preempted conditions.

The second scenario seems more likely.

Rather than asserting on a message prefix, I would propose explicitly **deactivating** Evicted and Preempted when quota is reserved, and only annotating their **previous** message once, when they transition from True to False. Something like:

```go
func SetQuotaReservation(w *kueue.Workload, admission *kueue.Admission, clock clock.Clock) {
	w.Status.Admission = admission

	reason := "QuotaReserved"
	msg := fmt.Sprintf("Quota reserved in ClusterQueue %s", admission.ClusterQueue)

	apimeta.SetStatusCondition(&w.Status.Conditions, metav1.Condition{
		Type:               kueue.WorkloadQuotaReserved,
		Status:             metav1.ConditionTrue,
		Reason:             reason,
		Message:            api.TruncateConditionMessage(msg),
		ObservedGeneration: w.Generation,
	})

	resetActiveCondition(&w.Status.Conditions, w.Generation, kueue.WorkloadEvicted, reason)
	resetActiveCondition(&w.Status.Conditions, w.Generation, kueue.WorkloadPreempted, reason)
}

func resetActiveCondition(conds *[]metav1.Condition, gen int64, condType, reason string) {
	prev := apimeta.FindStatusCondition(*conds, condType)
	// Ignore not found condition or condition with inactive status.
	if prev == nil || prev.Status != metav1.ConditionTrue {
		return
	}
	apimeta.SetStatusCondition(conds, metav1.Condition{
		Type:               condType,
		Status:             metav1.ConditionFalse,
		Reason:             reason,
		Message:            api.TruncateConditionMessage("Previously: " + prev.Message),
		ObservedGeneration: gen,
	})
}
```

**Why is this needed**:
This approach not only prevents the repeated message prefix, it also minimizes the update patch, and correctly reflects the transition times for the Evicted and Preempted conditions.

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-17T19:27:23Z

A separate note on the `clock.Clock` argument in: 
```go
func SetQuotaReservation(w *kueue.Workload, admission *kueue.Admission, clock clock.Clock) ...
```

In the current implementation, we call `apimeta.SetStatusCondition(...)` to set `WorkloadQuotaReserved`. That helper sets `LastTransitionTime` using `time.Now()` internally, which ignores the provided `clock.Clock`. This can lead to inconsistent timestamps with other conditions that use `clock`.

Given that, I suggest we pick one approach for consistency:

1. **Remove `clock.Clock` from `SetQuotaReservation`**, and rely on `apimeta.SetStatusCondition(...)` everywhere we set or reset conditions.
2. **Stop using `apimeta.SetStatusCondition(...)` here**, and set the condition fields explicitly using `clock.Clock` so all timestamps come from the same source.

After reviewing unit and integration tests, I do not see cases where `clock` materially affects condition behavior, so I lean toward option 1.

UPD: To further support option 1, it appears `apimeta.SetStatusCondition` usage is already prevalent in the workload package.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-18T01:51:10Z

> Stop using apimeta.SetStatusCondition(...) here, and set the condition fields explicitly using clock.Clock so all timestamps come from the same source.

Please use option 2. We are trying to use clock everywhere where is it possible.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T02:04:33Z

> Please use option 2. We are trying to use clock everywhere where is it possible.

Choosing option 2 and standardizing on injected clock usage has a wider blast radius. 
It implies we should replace all dependencies on `apimeta.SetStatusCondition` with a clock-aware helper. 
A quick scan shows approximately 34 occurrences in pkg/ and 37 in test/. 

Given the scope, I propose we open a dedicated tracking issue and follow it with a focused PR that:
* introduces a clock-aware condition helper,
* replaces existing `apimeta.SetStatusCondition` calls,
* updates tests to use a fake clock.

If that approach sounds good, I’ll proceed with the issue and the PR. 
How does that sound, @mbobrovskyi?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-18T04:47:42Z

We already have an issue for this: https://github.com/kubernetes-sigs/kueue/issues/3380. Do you think we missed something?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T05:01:57Z

Yep, this could be a part of the same issue. 
Except, the #3380 issue is already closed :/ , @mbobrovskyi

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T05:04:45Z

Just out of curiosity, do we have examples where we set clock to a different value than `now`? 
I see this:
```go
// the clock is primarily used with second rounded times
// use the current time trimmed.
testStartTime := time.Now().Truncate(time.Second)
fakeClock := testingclock.NewFakeClock(testStartTime)
```
Unfortunately, comment doesn't say "why" this is needed.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T05:38:48Z

@mbobrovskyi , I left a question in https://github.com/kubernetes-sigs/kueue/issues/3380#issuecomment-3305497059  related to this discussion. PTAL, when you get a moment.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T08:16:49Z

> > Stop using apimeta.SetStatusCondition(...) here, and set the condition fields explicitly using clock.Clock so all timestamps come from the same source.
> 
> Please use option 2. We are trying to use clock everywhere where is it possible.

+1, we have some code which is time-sensitive, and time-based like PodsReady for example. 

Testing using real clock often leads to flakes, and they are tricky to understand, so we decided to always use clocks which can be faked in unit tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T08:18:37Z

> we repeatedly call SetQuotaReservation and keep “updating” already inactive Evicted or Preempted conditions.

yes, I think this is the more likely case

> This approach not only prevents the repeated message prefix, it also minimizes the update patch, and correctly reflects the transition times for the Evicted and Preempted conditions.

+1, it will be nice to reduce the number of calls to the API Server.
