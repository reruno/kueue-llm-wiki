# Issue #2799: Partial Admission Preemption Panic

**Summary**: Partial Admission Preemption Panic

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2799

**Last updated**: 2024-09-23T17:18:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-08-08T13:17:12Z
- **Updated**: 2024-09-23T17:18:01Z
- **Closed**: 2024-09-23T17:18:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What happened**:
While refactoring `Preemptor.GetTargets`, I encountered a panic. Furthermore, I discovered that we are not exercising the PartialAdmission preemption logic in any of our tests, and it may be broken and panicking generally.

[This test](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/scheduler_test.go#L1194) exits [here](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/scheduler.go#L467-L469), as we find a preemption target above. The PartialAdmission preemption path is not tested.

[In this test](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/scheduler_test.go#L1234), we exit [here](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/preemption/preemption.go#L111). We panic when calling `assignment.TotalRequestsFor`, as [this map](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/flavorassigner/flavorassigner.go#L166) is empty

**How to reproduce it (as minimally and precisely as possible)**:

Move this line to the top of `Preemptor.GetTargets` and observe a panic during [this test](https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/scheduler_test.go#L1234)
https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/preemption/preemption.go#L116


Delete these lines and observe that unit and integration tests still pass
https://github.com/kubernetes-sigs/kueue/blob/00111d9aada59e1a6d8d90b9847cf7451bc5be76/pkg/scheduler/scheduler.go#L477-L481

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-08-08T13:17:28Z

cc @mimowo @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-09T09:14:49Z

/assign @trasc
