# Issue #6187: FlavorFungibility: Change the enum values to be less misleading

**Summary**: FlavorFungibility: Change the enum values to be less misleading

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6187

**Last updated**: 2025-10-14T09:37:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-25T13:13:53Z
- **Updated**: 2025-10-14T09:37:38Z
- **Closed**: 2025-10-14T09:37:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@ganczak-commits](https://github.com/ganczak-commits)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to introduce new API enum value `Stop` for the fields, `whenCanPreempt` and `whenCanBorrow`. 

I like the proposal here: https://github.com/kubernetes-sigs/kueue/issues/768#issuecomment-3018818387. Since these are just enum values we don't need to wait until v1beta2.

So, we can have `Stop` instead of `Preempt` and `Borrow`:
```
whenCanPteempt: Stop / TryNextFlavor
whenCanBorrow: Stop / TryNextFlavor
```
I would like to also deprecate the old enum values in v1beta1, so that we can consider removal in v1beta2, and adjust the documentation to use new enum values.

Instead of "Stop" we can consider alternatives, maybe `StopAndChooseBestFlavor` ?

**Why is this needed**:

The current enum values are misleading. For example 

```
whenCanPreempt: Preempt
whenCanBorrow: TryNextFlavor
```
suggests we would be preempting whenever possible, however, **this is not true**. We may get two flavors:
`(Borrow, Fit), (NoBorrow, Preempt)`. Now, we will choose flavor 1, because borrowing is implicitly preferred over pteemption by default. 

What `whenCanPreempt: Preempt` really does it is just : stop looking for more flavors once Preempting flavor is found.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T13:16:23Z

cc @tenzen-y @pajakd @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-25T13:16:28Z

What about supporting both `Preempt` and `Stop` during v1beta1 and marking `Preempt` as deprecated?
When we graduate the API to v1beta2, we can remove `Preempt`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T13:28:51Z

> What about supporting both Preempt and Stop during v1beta1 and marking Preempt as deprecated?

Yes, this is consistent with my proposal actually here: "I would like to also deprecate the old enum values in v1beta1, so that we can consider removal in v1beta2, and adjust the documentation to use new enum values.".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-25T14:53:20Z

> > What about supporting both Preempt and Stop during v1beta1 and marking Preempt as deprecated?
> 
> Yes, this is consistent with my proposal actually here: "I would like to also deprecate the old enum values in v1beta1, so that we can consider removal in v1beta2, and adjust the documentation to use new enum values.".

Awesome, lgtm. Regarding the new mode name, let me reconsider it after 0.13 release.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-09T13:34:29Z

In my feeling, for a config like

```
whenCanPreempt: Stop
whenCanBorrow: TryNextFlavor
```

it may be still quite unclear (to a user) how the clash between `Stop` and `TryNextFlavor` is resolved.
I mean, given a flavor with `(Borrow, Preempt)` - do we stop, or do we try next flavor?

My understanding of the code is that `TryNextFlavor` always wins over `Stop` (currently still named `Borrow` / `Preempt`).
However, these names - at least in my feeling - suggest _otherwise_.
("Stop" feels more imperative, more definite, or so. It feels like the winner. It feels like "stop no matter what").

I'm thinking if we could somehow _weaken_ the `Stop` (or _strengthen_ the `TryNextFlavor`) to make this clearer. For example:

* `StopIfFeasible` / `TryNextFlavor`
* `FineToStop` / `TryNextFlavor`
* `Stop` / `ForceTryNext`

What would you say? @pajakd @mimowo @tenzen-y

### Comment by [@ganczak-commits](https://github.com/ganczak-commits) — 2025-09-14T08:11:48Z

To me, `Stop` was confusing. I now understand it means "Stop the loop of looking for an adequate flavor" - but it took me a while to figure this out, my first thought was "is it stop as in 'stop the job instead of preempting (killing) it'?".

I'd vote for the combination `UseIfFeasible`/`TryNextFlavor`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T06:57:25Z

> it may be still quite unclear (to a user) how the clash between Stop and TryNextFlavor is resolved.

Good point!

> I'm thinking if we could somehow weaken the Stop (or strengthen the TryNextFlavor) to make this clearer. 

I agree with this direction.

> StopIfFeasible / TryNextFlavor
> FineToStop / TryNextFlavor

Sound ok-ish, but maybe `Fine` is too informal, also "Feasible" suggests there are more checks to be done.

What about `ReadyToStop` / `TryNextFlavor` .

Then `whenCanBorrow: ReadyToStop` + `whenCanPreempt: TryNextFlavor` reads naturally, wdyt?

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-15T19:12:56Z

> Then `whenCanBorrow: ReadyToStop` + `whenCanPreempt: TryNextFlavor` reads naturally, wdyt?

I like it - though I'd like it even more if we follow the comment from @ganczak-commits and replace `Stop` with `Use`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T19:49:49Z

As much as I like short names, wouldnt Use suffer from the same as Stop?

I mean that it sounds defnitive, and thus is confusing because:
1. it suggests the flavor is going to be used but in fact we select the best from the set
2. it conflicts semantically with TryNextFlavor , because the algo currently moves forward and tries next.

Maybe 'ReadyToStopAndUseBestFlavor' to make the name more self explanatory.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-15T21:01:20Z

Oh, apologies for not being clear.
What I meant is to replace `Stop` with `Use` _on top of_ your proposal.

That is: `whenCanBorrow: ReadyToUse` + `whenCanPreempt: TryNextFlavor`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T06:37:18Z

Got it, `whenCanBorrow: ReadyToUse + whenCanPreempt: TryNextFlavor` sounds great to me. 

wdyt @pajakd @tenzen-y ? If no objections I will just look forward for the PR

### Comment by [@ganczak-commits](https://github.com/ganczak-commits) — 2025-09-16T06:46:06Z

/assign

### Comment by [@amy](https://github.com/amy) — 2025-10-02T21:43:43Z

@ganczak-commits @mimowo To clarify...

ReadyToUse/Preempt/Borrow means... stick to the current flavor if you can fit with preemption/borrowing.
TryNextFlavor means... if your workload doesn't fit squarely within the flavor without preemption/borrowing, pick the next flavor.

Right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T12:32:23Z

Not exactly. The FlavorFungability has two phases:
1. determine the set of flavors, starting from one (TryNextFlavor expands the set, while two "ReadyToUse" close the set)
2. choose the "best" flavor within the set

Thus, the "Preempt" or "Borrow" where misleading, because even if a flavor says "Preempt" then the second phase may choose a flavor which is "Borrowing" as "best" (and vice versa). It is the new feature gate FlavorFungibilityImplicitPreferenceDefault which determines the "best" selection logic in the second phase.

cc @pajakd to keep me honest here.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-03T13:54:43Z

The original enums are misleading for many reasons. For example if `whenCanPreempt=Preempt`, `whenCanBorrow=TryNextFlavor` and we find a perfect flavor that has `(Fit,NoBorrow)` then we obviously pick it and we don't preempt (because we don't need to).

In general this API is a little bit outdated since for instance borrowing is no longer binary (and there are cases where every CQ is borrowing from some cohort). So, we have to move towards the API that can express these two-phases (restrict flavors to choose + preference) in an intuitive way. And this rename is a good step towards this.

### Comment by [@amy](https://github.com/amy) — 2025-10-03T19:25:54Z

Okay let me... repeat what y'all are saying:

Part 1: 
So when running through the list of flavors...
- `TryNextFlavor`: will construct a set of all flavors where the workload fits (or requires borrow/preemption to fit)
- Preempt/Borrow (replaced by ReadToUse): will stop at the first flavor you find that the workload fits (or requires preemption/borrow to fit)

Part 2:
FlavorFungibilityImplicitPreferenceDefault=true/false then picks out of the set of flavors you constructed above?
