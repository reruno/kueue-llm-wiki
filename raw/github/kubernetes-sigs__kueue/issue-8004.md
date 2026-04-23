# Issue #8004: Use label filters to make it easier to run tests for specific use cases

**Summary**: Use label filters to make it easier to run tests for specific use cases

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8004

**Last updated**: 2026-01-23T14:02:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-11-30T17:21:01Z
- **Updated**: 2026-01-23T14:02:33Z
- **Closed**: 2025-12-04T14:35:00Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

When I am working on a feature or testing specific controllers, the integration tests are difficult to manage as we can only filter by folder. Ginkgo has an optional to add label-filters so we could target specific test cases across the different suites.

Ideally, we can add a label for each integration test that corresponds to what we are testing. That way, one could run the localqueue integration tests without also running the workload tests.

**Why is this needed**:

Easier to work with integration tests.

## Discussion

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-12-01T17:42:20Z

Great idea. It would be worth to have the same for the e2e tests.
