# Issue #9314: Scheduler logs wrong replica-role after failover

**Summary**: Scheduler logs wrong replica-role after failover

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9314

**Last updated**: 2026-02-23T17:31:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-17T10:42:20Z
- **Updated**: 2026-02-23T17:31:39Z
- **Closed**: 2026-02-23T17:31:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

**What you expected to happen**:
This value is only set once, upon Start:
https://github.com/kubernetes-sigs/kueue/blob/3b299a308129f840bd01f53f3a038015fbc801fc/pkg/scheduler/scheduler.go#L165-L171

If the leader fails, and a follower becomes new leader, it has the wrong log

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-17T10:49:40Z

This `Start` method should only be called once the replica is the leader. However, I was observing logs where replica-role=follower for scheduler.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-17T10:53:25Z

Perhaps a race, where failover happens, but the role tracker doesn't reflect the new value until after the `Start` method is called

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T10:56:41Z

Good point, it might be related to other issues we've seen: https://github.com/kubernetes-sigs/kueue/issues/9287 and https://github.com/kubernetes-sigs/kueue/issues/9288

cc @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-23T08:41:28Z

/assign
