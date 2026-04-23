# Issue #5062: [Failing test] Workload controller with scheduler when the queue has admission check strategies the workload should have appropriate AdditionalChecks added [slow]

**Summary**: [Failing test] Workload controller with scheduler when the queue has admission check strategies the workload should have appropriate AdditionalChecks added [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5062

**Last updated**: 2025-04-24T05:40:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-22T06:43:44Z
- **Updated**: 2025-04-24T05:40:32Z
- **Closed**: 2025-04-24T05:40:32Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

**What happened**:

The test fails regularly since 17/18 April:

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main

![Image](https://github.com/user-attachments/assets/24495b5f-e2c7-4cc6-a0c3-c97a3cebed4c)

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1914564666319704064
**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci build

**Anything else we need to know?**:

This test does not block presubmits as it is categorized as "slow", likely this is related:
 https://github.com/kubernetes-sigs/kueue/pull/4911

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-22T06:44:17Z

cc @mbobrovskyi 
/assign @vladikkuzn 
tentatively as this seems related to the PR #4911, but I'm not sure
