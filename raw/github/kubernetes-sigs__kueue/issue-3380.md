# Issue #3380: Replace `time.Now()` code with `clock.Clock.Now()`

**Summary**: Replace `time.Now()` code with `clock.Clock.Now()`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3380

**Last updated**: 2025-09-18T14:55:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-10-30T13:45:21Z
- **Updated**: 2025-09-18T14:55:33Z
- **Closed**: 2025-02-04T21:13:00Z
- **Labels**: `kind/feature`
- **Assignees**: [@TusharMohapatra07](https://github.com/TusharMohapatra07)
- **Comments**: 27

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
There are packages like e.g. `pkg/scheduler` that use `time.Now()`. As a result this code is hard to test and prone to flakiness as we are not able to directly control the time during tests. It should be replaced with `clock.Clock.Now()` as it is  in WorkloadController

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-10-30T13:51:26Z

/cc @mbobrovskyi

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-04T06:12:40Z

can i work on this issue ? @PBundyra @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-04T06:16:53Z

> can i work on this issue ? @PBundyra @mbobrovskyi

Sure, please take it.

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-04T06:18:55Z

@mbobrovskyi thanks! i'm on it

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-04T06:25:33Z

/assign @TusharMohapatra07

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-04T06:35:14Z

@mbobrovskyi am i supposed to change the time.Now() instance everywhere inside the project or just those instances which are present inside pkg folder ??

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-04T06:47:57Z

Let's focus on `pkg/scheduler`. This is an example https://github.com/kubernetes-sigs/kueue/blob/74286b4e96d513de1f3455a5509cdd31b489c253/pkg/controller/core/workload_controller.go#L108.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T06:56:08Z

I would say the end goal is to use it everywhere, but starting with scheduler  might be a good idea to see if there are any obstacles, then feel free to follow up in the next PR.

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-04T07:05:45Z

@mimowo understood

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-06T15:38:09Z

/reopen

To fix it in other places.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-06T15:38:14Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3380#issuecomment-2460097762):

>/reopen
>
>To fix it in other places.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-06T15:40:03Z

@mbobrovskyi yes, i'm on it

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-08T15:11:57Z

@mbobrovskyi I don't see any significant place to replace time.Now in `pkg/workload`. Please confirm !

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-08T16:15:18Z

What about this one https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/workload/admissionchecks.go#L96?

Also here https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/workload/admissionchecks.go#L110.

Could you please check is it possible to propagate `clock.Clock`? Or maybe just `now time.Time`.

This is an example 

https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/workload/admissionchecks.go#L32

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-08T16:33:06Z

@mbobrovskyi Actually, LastTransitionTime takes metav1.Time, so time.Time won't work ig. We could probably pass in the clock.Clock interface inside the function to proceed with this..

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-08T16:35:16Z

> @mbobrovskyi Actually, LastTransitionTime takes metav1.Time, so time.Time won't work ig. We could probably pass in the clock.Clock interface inside the function to proceed with this..

Why we can't use like this `LastTransitionTime: metav1.NewTime(clock.Now())` or `LastTransitionTime: metav1.NewTime(now)`?

I think just propagation to function is enough for it. Also `time.Time` is enough.

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-08T16:55:22Z

@mbobrovskyi so, if we propogate it in the function, we have to pass it whenever we're calling the function ?
For ex:-
https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/scheduler/preemption/preemption.go#L225

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-08T16:57:00Z

Exactly and Preemptor should have clock? If not please add to Preemptor as well.

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-08T16:57:53Z

@mbobrovskyi understood

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-16T15:42:33Z

Hey @mbobrovskyi, sorry for being late but i'm a bit busy with some commitments. I'll restart working on this in a day or two.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-09T14:24:08Z

- [x] https://github.com/kubernetes-sigs/kueue/pull/3421
- [x] https://github.com/kubernetes-sigs/kueue/pull/3478
- [x] https://github.com/kubernetes-sigs/kueue/pull/3498
- [x] https://github.com/kubernetes-sigs/kueue/pull/3773
- [x] https://github.com/kubernetes-sigs/kueue/pull/3775
- [x] https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/admissionchecks.go
- [x] https://github.com/kubernetes-sigs/kueue/pull/3870

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T05:36:28Z

Out of curiosity, what is the advantage of using `clock.Now()` instead of `time.Now()`?
 I didn’t perform an exhaustive search, but it appears that in tests we use either:
 A) `testingclock.NewFakeClock(time.Now())`, or
 B) `testingclock.NewFakeClock(time.Now().Truncate(time.Second))`.

 I’m not entirely sure why truncation in B is needed. I assume it’s for simplified assertions, is that correct? If so, `cmpopts.EquateApproxTime(time.Second)` would achieve the same outcome without changing production code.
I understand that `ApproxTime` is not "exactly" the same as truncated seconds, and if we after detecting sub-seconds churn in LastTransitionTime - clock would be a more solid alternative. That said, I couldn't find in our test we test such churn. 

I also understand there are more advanced clock-usage patterns, such as stepping, sleeping, or setting a specific time, but I couldn’t find any of those in the Kueue code either. Am I missing something here?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-18T05:43:04Z

We are using clock.Now() to avoid flakiness in unit and integration tests.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-18T05:46:46Z

> B) testingclock.NewFakeClock(time.Now().Truncate(time.Second)).

LastTransitionTime is truncated to seconds. To simplify comparisons, we truncate it to seconds here as well.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-18T05:48:34Z

> If so, cmpopts.EquateApproxTime(time.Second) would achieve the same outcome without changing production code.

This isn’t entirely correct. Sometimes one second isn’t enough to run all tests, which causes flakes. To avoid flakiness, it’s better and more clear to use clock.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T05:55:02Z

Catching up on multiple replies here :) 

> We are using `clock.Now()` to avoid flakiness in unit and integration tests.

Understood. Could you point me to a concrete example, issue, or PR where this is used so I can see it in action?

> `LastTransitionTime` is truncated to seconds. To simplify comparisons, we truncate it to seconds here as well.

Please see my comment about using `cmpopts.EquateApproxTime(time.Second)` for assertions.

I am not questioning the usefulness of an injected clock. My point is that `testingclock.NewFakeClock(time.Now())` behaves the same as `time.Now()` unless we actually step or set the fake clock. If I am missing a case in Kueue where we do that, I would appreciate a pointer.

> This isn’t entirely correct. Sometimes one second isn’t enough to run all tests. 

I agree, so instead of "guessing" and/or "bumping" `ApproxTime` value (1s, 5s, 10s, ....) we opting for clock. It makes sense, although, would love to see an example (or two) where switching to `clock` helped to reduce flakiness, if you have one of the top.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T14:55:33Z

After looking more closely at `clock.FakeClock`, I now understand the source of my confusion.

`FakeClock` is exactly what the name implies, a non-running or "frozen" clock. When you initialize it using `NewFakeClock`, calls to `fakeClock.Now()` always return the same static time. This behavior is useful in many test cases where we want to ignore time progression and treat all actions as happening simultaneously.

However, this also means that we need to be mindful of scenarios where time progression matters, such as asserting that one event happens after another. In such cases, relying on `FakeClock` without manually advancing it can lead to misleading test behavior or missed bugs.

Thank you, @mbobrovskyi, for taking the time to answer my questions and clarify things!
