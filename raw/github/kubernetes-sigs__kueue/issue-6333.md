# Issue #6333: TAS: Follow the DUMP principle in node_failure_controller UTs

**Summary**: TAS: Follow the DUMP principle in node_failure_controller UTs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6333

**Last updated**: 2025-08-29T09:15:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-07-31T15:36:48Z
- **Updated**: 2025-08-29T09:15:12Z
- **Closed**: 2025-08-29T09:15:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to dump the test data in https://github.com/kubernetes-sigs/kueue/blob/7afe46898218e1508056dd3344b755c06d183a1d/pkg/controller/tas/node_failure_controller_test.go

We could define the following base node object inside of TestNodeFailureReconciler:

```go
baseNode := testingnode.MakeNode(name).
			StatusConditions(corev1.NodeCondition{
				Type:               corev1.NodeReady,
				Status:             readyStatus,
				LastTransitionTime: metav1.NewTime(clock.Now().Add(-transitionTimeOffset)),
			})
```

Then each test case clones the `baseNode`, and update case specific parameters by wrapper functions in the following:

```go
baseNode.Clone().
	StatusConditions(xyz)
```

**Why is this needed**:

We should follow the DUMP principle instead of DRY principle in tests.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-31T15:37:02Z

cc @mimowo @PBundyra @pajakd

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T15:40:53Z

Thank you for opening, yes it will benefit the project long term

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-08-27T22:22:52Z

/assign
