# Issue #6017: [scheduler integration test] the "Multiple flavors can be considered for preemption" test should clean after itself

**Summary**: [scheduler integration test] the "Multiple flavors can be considered for preemption" test should clean after itself

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6017

**Last updated**: 2025-07-21T14:48:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-18T11:06:05Z
- **Updated**: 2025-07-21T14:48:29Z
- **Closed**: 2025-07-21T14:48:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 2

## Description


**What would you like to be cleaned**:

The test does not clean resources after itself: https://github.com/kubernetes-sigs/kueue/blob/05291b43116cd25ab08f537c30c3d72dd34c66d5/test/integration/singlecluster/scheduler/scheduler_test.go#L2604

**Why is this needed**:

For two reasons:
- not cleaning after itself risks subtle test interactions which are hard to debug, often only manifesting on CI when all tests are run
- it does not allow to easily run the test in a loop to detect flakes with the following wrapper (which proved to be useful identifying issues with other flaky tests):
```goalng
	for i := range 100 {
		ginkgo.FWhen(fmt.Sprintf("Multiple flavors can be considered for preemption %d", i), func() {
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-18T11:06:14Z

cc @gabesaba @amy

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-07-18T12:57:09Z

/assign
