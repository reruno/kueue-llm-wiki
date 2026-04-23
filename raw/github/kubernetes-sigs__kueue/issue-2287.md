# Issue #2287: [kueuectl] Use the fake time instead of real in tests

**Summary**: [kueuectl] Use the fake time instead of real in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2287

**Last updated**: 2024-06-07T14:14:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-27T19:34:16Z
- **Updated**: 2024-06-07T14:14:52Z
- **Closed**: 2024-06-07T14:14:52Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Introduce the same approach as controllers like this:

https://github.com/kubernetes-sigs/kueue/blob/4b9744b29bec33bbd34e01a66f09002b478a6493/pkg/controller/core/workload_controller.go#L117

https://github.com/kubernetes-sigs/kueue/blob/4b9744b29bec33bbd34e01a66f09002b478a6493/pkg/controller/core/workload_controller_test.go#L807

Also check [this](https://github.com/kubernetes-sigs/kueue/pull/2195#discussion_r1607067637).

**Why is this needed**:

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-03T09:50:50Z

/assign
