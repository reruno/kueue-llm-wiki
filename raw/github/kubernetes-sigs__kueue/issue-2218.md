# Issue #2218: Partial revert of #1695: Use a uniquely identifying selector based

**Summary**: Partial revert of #1695: Use a uniquely identifying selector based

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2218

**Last updated**: 2024-05-28T15:32:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-17T15:51:04Z
- **Updated**: 2024-05-28T15:32:47Z
- **Closed**: 2024-05-28T15:32:47Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

**What happened**:

While well intentioned, #1695 has the potential of complicating upgrades and downgrades (in case of emergency).

The labelSelector of a deployment is immutable, so upgrading requires uninstalling and re-installing Kueue (or at least uninstalling the Deployment).

So I propose a partial revert of https://github.com/kubernetes-sigs/kueue/pull/1695. The end result should be to add both old and new labels, but keep the old selector.

We'll figure a plan for a proper upgrade path in the future.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T15:51:11Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T15:51:21Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T15:53:04Z

> cc @tenzen-y

Thank you for creating this issue!

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-05-20T13:55:36Z

/assign
