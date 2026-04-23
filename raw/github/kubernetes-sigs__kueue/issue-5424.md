# Issue #5424: Flavor Fungibility Prefers Fit over NoBorrow

**Summary**: Flavor Fungibility Prefers Fit over NoBorrow

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5424

**Last updated**: 2025-07-24T14:44:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-05-30T13:27:51Z
- **Updated**: 2025-07-24T14:44:29Z
- **Closed**: 2025-07-24T14:44:29Z
- **Labels**: `kind/feature`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 6

## Description

**What would you like to be added**:
Flavor assigner implicitly prefers (`Fit`, `Borrow`) over (`Preempt`, `NoBorrow`)

Customers may want to express that it is more important for their workload to fit within nominal quota (and therefore be un-preemptable) than upgrading from `Preempt` to `Fit`

**Why is this needed**:
- Suppose two flavors, with capacity for 1 workload each
  - Flavor1: capacity provided by cq-2
  - Flavor2: capacity provided by cq-1
- Suppose `FlavorFungibility.whenCanBorrow=TryNextFlavor`
- Suppose two CQs, both with `ReclaimWithinCohort=Any`, `WithinClusterQueue=LowerPriority`

Then we create 3 workloads in order:
1) cq-1: a low-priority workload schedules into into `Flavor2`, since (`Fit`, `NoBorrow`)
2) cq-1: a high-priority workload schedules into Flavor1, as (`Fit`, `Borrow`) > (`Preempt`, `NoBorrow`)
3) cq-2: a low-priority workload preempts the high-priority workload from cq-1 in Flavor1, as it is reclaiming its quota

The user might expect that, during step 2, the high-priority workload preempts the low-priority workload, so that it can run within nominal quota and be safe from preemptions in the future.

The scope of this task is to propose an API which would allow user to express this preference, and to implement this change in the code

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T16:00:45Z

@gabesaba Do you assume the flavor assigner prioritizes the `whenCanPreempt` rather than `whenCanBorrow`?
 In that case, do you expect adding a new API to specify which mode (`whenCanPreempt`) and (`whenCanborrow`) should be evaluated first?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T17:17:13Z

> The user might expect that, during step 2, the high-priority workload preempts the low-priority workload, so that it can run within nominal quota and be safe from preemptions in the future.

Isn't this achievable already with the current API:
```yaml
flavorFungibility:
  whenCanBorrow: TryNextFlavor
  whenCanPreempt: Preempt
```
or it works, but there are other drawbacks?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-02T09:12:06Z

> > The user might expect that, during step 2, the high-priority workload preempts the low-priority workload, so that it can run within nominal quota and be safe from preemptions in the future.
> 
> Isn't this achievable already with the current API:
> 
> flavorFungibility:
>   whenCanBorrow: TryNextFlavor
>   whenCanPreempt: Preempt
> or it works, but there are other drawbacks?

With the current API, no. It tries the 2nd flavor, and even if the 2nd flavor doesn't require borrowing, it decides 1st flavor is better since it `Fit`, while the 2nd flavor is `Preempt`. Hence the issue description: Flavor assigner implicitly prefers (Fit, Borrow) over (Preempt, NoBorrow)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-02T09:15:07Z

> [@gabesaba](https://github.com/gabesaba) Do you assume the flavor assigner prioritizes the `whenCanPreempt` rather than `whenCanBorrow`? In that case, do you expect adding a new API to specify which mode (`whenCanPreempt`) and (`whenCanborrow`) should be evaluated first?

As stated in my response to @mimowo's comment: even if only whenCanBorrow=TryNextFlavor, we implicitly prefer `Fit` over `Preempt`, regardless of borrowing status. I think that the issue is a little more general than just the order of evaluation

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T14:48:47Z

> > [@gabesaba](https://github.com/gabesaba) Do you assume the flavor assigner prioritizes the `whenCanPreempt` rather than `whenCanBorrow`? In that case, do you expect adding a new API to specify which mode (`whenCanPreempt`) and (`whenCanborrow`) should be evaluated first?
> 
> As stated in my response to [@mimowo](https://github.com/mimowo)'s comment: even if only whenCanBorrow=TryNextFlavor, we implicitly prefer `Fit` over `Preempt`, regardless of borrowing status. I think that the issue is a little more general than just the order of evaluation

Thank you for describing that. So, I guess that we might need to support new flavor fungibility (preference selection ways).

### Comment by [@pajakd](https://github.com/pajakd) — 2025-07-03T08:02:11Z

/assign
