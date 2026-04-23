# Issue #7138: Support mutating workload priority class while running without disruption

**Summary**: Support mutating workload priority class while running without disruption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7138

**Last updated**: 2025-10-28T16:32:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-02T12:22:45Z
- **Updated**: 2025-10-28T16:32:03Z
- **Closed**: 2025-10-28T16:32:03Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be added**:

Support mutating the workload priority class label. 

Currently it is blocked here: https://github.com/kubernetes-sigs/kueue/blob/15ea4e843157cb86b443ad8ff0f5ebeed9327ef2/pkg/controller/jobframework/validation.go#L151-L157

However, it seems like a precautionary measure rather than a fundamental problem.

Once the priority is lowered we should make sure the scheduling is triggered as we may be now having a new workload that can schedule preempting the running one.

**Why is this needed**:

Sometimes users may want change priority of a running workload. They are ok if the workload gets interrupted (preempted) by the inflow of incoming workloads, but would like to avoid preemption if not needed.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T12:22:56Z

cc @mwielgus @mwysokin @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-02T13:03:21Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-02T14:07:44Z

I like this enhancement, which allows us to construct the budget-based workload management.
Let's say that we have a billing and usage management system separate from Kueue.
The external costom controllers watches the budget (billing) monitoring system, then it automatically change the WorkloadPriorityClass if the tenants use the quota with exceeding the pre-defined ones in a external Custom Resource.
