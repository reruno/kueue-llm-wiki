# Issue #189: Pending event should include information of which resource didn't have enough quota

**Summary**: Pending event should include information of which resource didn't have enough quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/189

**Last updated**: 2022-05-04T02:45:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-04-08T13:42:02Z
- **Updated**: 2022-05-04T02:45:32Z
- **Closed**: 2022-05-04T02:45:32Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/ux`, `kind/productionization`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 3

## Description

**What would you like to be added**:

The current message says "Workload didn't fit in the remaining quota" with no indication of which resource doesn't fit, which flavors were tried, which ones are under `min` (this is possible because there is no preemption).

**Why is this needed**:

Improves UX and allows users and administrators to understand which quotas might need to be revisited.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-08T20:43:26Z

We should also breakdown the reason by flavor, which may not fit because of:
1. no quota
2. untolerated taint 
3. non-matching affinity.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T02:01:51Z

/kind ux

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-14T08:57:49Z

/assign
