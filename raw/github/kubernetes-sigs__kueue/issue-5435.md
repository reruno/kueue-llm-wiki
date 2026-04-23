# Issue #5435: The "should update workload TopologyAssignment when node fails" test takes 32s

**Summary**: The "should update workload TopologyAssignment when node fails" test takes 32s

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5435

**Last updated**: 2025-06-02T12:30:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-02T07:47:34Z
- **Updated**: 2025-06-02T12:30:38Z
- **Closed**: 2025-06-02T12:30:38Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This test takes >30s because we are waiting for [NodeFailureDelay](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/tas/constants.go#L29) =30s

See: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1929423477341687808

I consider this technical debt we took during release, but we should follow up.


We should add an option to the nodeFailureReconciler code with the timeout, and minimal value should be passed for integration tests, say 10ms, when building the controllers for integration tests [here](https://github.com/kubernetes-sigs/kueue/blob/c5bbc5577b72a430b998d9d6991bba5ed1f9d445/test/integration/singlecluster/tas/suite_test.go#L91).


**Why is this needed**:

To do not waste 30s on every build unnecessarily.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T07:49:36Z

cc @tenzen-y @pajakd @PBundyra @mbobrovskyi @mszadkow PTAL

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-02T08:23:25Z

My guess is that even in L1018 we update the lastTransitionTime in order to not wait 30s, the update doesn't apply as we don't change anything else in the condition (e.g. message). As a fix I propose checking if changing message would decrease the waiting time

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-02T08:23:56Z

I also suggest cleaning up lines L994-L1000 and using `SetNodeCondition` instead

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T09:27:46Z

I see, I'm ok either with parametrizing the  controller timeout, or with that alternative approach or updating LastTransitionTime.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-02T10:06:17Z

/assign
