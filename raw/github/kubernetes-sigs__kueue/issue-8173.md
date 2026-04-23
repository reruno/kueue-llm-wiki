# Issue #8173: Eliminate the error prone ExpectWorkloadsToBeAdmittedCount function

**Summary**: Eliminate the error prone ExpectWorkloadsToBeAdmittedCount function

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8173

**Last updated**: 2025-12-22T08:34:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-10T18:33:34Z
- **Updated**: 2025-12-22T08:34:40Z
- **Closed**: 2025-12-22T08:34:40Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Eliminate the ExpectWorkloadsToBeAdmittedCount function from our asserts

This may require adjusting existing tests which already use it, but I think this is worth the effort in the long run. Hope no test really needs it.


**Why is this needed**:

As summarized in https://github.com/kubernetes-sigs/kueue/pull/8170/files#r2607775406


1. it makes the tests intrinsically non-deterministic, I think we should avoid such tests as much as possible
2. it is currently buggy because it actually checks the count is "equal", it just makes the check very often so it usually hits the right moment

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T18:33:48Z

cc @mykysha @mbobrovskyi @sohankunkerkar

### Comment by [@mykysha](https://github.com/mykysha) — 2025-12-10T18:41:10Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T09:54:45Z

@mykysha if eliminating the function proves complex, we can just submit the first PR to fix (2.), basically by checking the number of observed admitted workloads is >= "count", rather than "equal". 

This will already eliminate flakes related to the use of the function, then we can take more time to properly refactor the existing tests, wdyt?

### Comment by [@mykysha](https://github.com/mykysha) — 2025-12-11T09:57:21Z

Surely, the flakes are a more pressing matter here. Will do in multiple PRs then

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T07:43:44Z

I have synced with @mykysha regarding this issue and I propose the following:
1. remove the use of the function from metrics_test.go, and adjust the test to be deterministic
2. in other cases were we have non-deterministic order rename the function to ExpectAtLeastWorkloadsToBeAdmittedFromSet, and verify that (1) set of admitted is subset of input workloads, (2.) count of admitted is >= atLeastCount. This will produce better failure messages, and we will check that the admitted is subset of expected.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:38:03Z

/priority important-soon
