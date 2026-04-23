# Issue #2285: Restructure PodsReadyTimeout integration tests with short timeout

**Summary**: Restructure PodsReadyTimeout integration tests with short timeout

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2285

**Last updated**: 2024-05-30T17:16:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-27T10:26:34Z
- **Updated**: 2024-05-30T17:16:31Z
- **Closed**: 2024-05-30T17:16:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
As we discussed [here](https://github.com/kubernetes-sigs/kueue/pull/2219#discussion_r1615215775), we should use a shorter timeout (10ms) for the test cases with a single or second reconciliation and should keep using a 1s for test cases with 3 reconciliations.

For example, deactivation test cases consume 3 API calls:
 
1. [workload-controller] Set `.spec.active=false` in the Workload
2. [workload-controller] Set  `Evicted` condition
3. [jobframework controller] Stop a Job with a Requeued condition.

**Why is this needed**:
It would be better to decrease the duration for performing integration tests.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-29T15:57:25Z

/assign
