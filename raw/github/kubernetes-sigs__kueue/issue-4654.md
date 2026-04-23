# Issue #4654: Log namespace to improve debuggability of  ginkgo tests

**Summary**: Log namespace to improve debuggability of  ginkgo tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4654

**Last updated**: 2025-03-19T16:24:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-17T14:20:01Z
- **Updated**: 2025-03-19T16:24:41Z
- **Closed**: 2025-03-19T16:24:41Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Log the created namspece in BeforeEach for tests which create namespaces. 

We can consider an extra helper like CreateNamespaceWithLog.

**Why is this needed**:

We have a number of flakes recently, and grepping by namespace seems quite efficient to get the logs we want.

However, currently the namespace is not logged for most test failures, so we need to figure out by timestamps, and this is time-consuming.

Example: https://github.com/kubernetes-sigs/kueue/issues/4651, or https://github.com/kubernetes-sigs/kueue/issues/4626 show issues without namespace logged. We can figure out by timestamps, but it is not convenient.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T14:20:11Z

cc @mszadkow @tenzen-y

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-17T14:21:56Z

/assign
