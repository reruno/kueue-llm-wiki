# Issue #1844: RayClusters managed by RayJobs stay in suspended state

**Summary**: RayClusters managed by RayJobs stay in suspended state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1844

**Last updated**: 2024-03-15T10:06:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-03-14T17:34:00Z
- **Updated**: 2024-03-15T10:06:02Z
- **Closed**: 2024-03-15T10:06:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 4

## Description

**What happened**:

RayClusters that are created when RayJobs are admitted stay in suspended state, while they should be unsuspended and running. 

This has been first reported in https://github.com/kubernetes-sigs/kueue/pull/1802#issuecomment-1995580722.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a RayJob that can be admitted
2. Check the child RayCluster stays in suspended state

**Anything else we need to know?**:

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-rc.1-116-ga96927de-dirty

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-14T17:34:10Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T17:36:26Z

@astefanutti Is this related to https://github.com/kubernetes-sigs/kueue/issues/1829?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-14T18:50:02Z

@tenzen-y it doesn't look related at first glance. I'll try to look into it deeper when I have a moment.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T18:58:32Z

> it doesn't look related at first glance. I'll try to look into it deeper when I have a moment.

Thank you!
