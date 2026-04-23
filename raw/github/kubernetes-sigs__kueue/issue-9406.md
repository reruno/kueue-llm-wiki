# Issue #9406: Fair sharing admission ordering does not preserve nominal-first workload priority

**Summary**: Fair sharing admission ordering does not preserve nominal-first workload priority

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9406

**Last updated**: 2026-02-26T09:06:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Created**: 2026-02-21T10:01:55Z
- **Updated**: 2026-02-26T09:06:32Z
- **Closed**: 2026-02-26T09:06:32Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

We have a multi-flavor setup with fair sharing enabled in production. We noticed that borrowing resources on one flavor affects a CQ's ability to use its nominal quota on a different flavor -- in both admission ordering and preemption.

**What you expected to happen**:

Borrowing on one flavor should not erode a CQ's nominal quota entitlement on another flavor. A workload that fits within its CQ's nominal quota should be prioritized over one that requires borrowing, regardless of the CQ's aggregate DRS from other flavors.

**How to reproduce it (as minimally and precisely as possible)**:

Three teams (each team is a CQ) share a cohort with two GPU flavors:

| | Team-A | Team-B | Team-C |
|---|---|---|---|
| h100-reserved nominal | 5 | 5 | 5 |
| a10-spot nominal | 0 | 0 | -- (not eligible) |

50 a10-spot GPUs are available in the cohort for borrowing. Fair sharing is enabled.

**Current state:**
- Team-A: 5 h100 (within nominal) + 30 a10 (borrowed)
- Team-B: 5 h100 (within nominal) + 20 a10 (borrowed)
- Team-C: 5 h100 (within nominal)

Fair sharing between Team-A and Team-B on a10-spot works well here.

One of Team-A's h100 workloads finishes. Both Team-A and Team-C have a pending h100 workload.

- Team-A's pending workload fits within nominal (4 + 1 = 5 <= 5 nominal). No borrowing needed.
- Team-C's pending workload requires borrowing (5 + 1 = 6 > 5 nominal).

The fair sharing iterator compares DRS after simulated admission. Team-A's DRS is dominated by its 30 borrowed a10-spot GPUs, making it higher than Team-C's DRS (just 1 borrowed h100). **Team-C gets the slot**, even though Team-A's workload fits within nominal and Team-C's does not.

The same applies to preemption. If Team-C were borrowing h100 capacity from Team-A's lendable quota, Team-A cannot preempt to reclaim it. So the inflated DRS from a10-spot borrowing blocks preemption as well.

**Anything else we need to know?**:

We've proposed flavor-aware DRS weights (#8902) to reduce the contribution of cheap flavors to DRS. While this helps narrow the gap, it doesn't eliminate the problem. At sufficient borrowing volume, the aggregate weighted borrowing from many cheap resources can still outweigh a small amount of expensive borrowing, preventing a team from using its own nominal quota.

Disabling fair sharing (using the classical iterator) is not a viable workaround for us. We need fair sharing enabled so that Team-A and Team-B get a fair distribution of borrowed a10-spot capacity. 

Would it be reasonable for the fair sharing iterator to also preserve the nominal-first guarantee? For example, a workload that fits within its CQ's nominal quota could be prioritized over one that requires borrowing, before falling through to DRS comparison for workloads at the same borrowing level.

I'm not sure if this should be classified as a bug or a feature request. Happy to re-label as appropriate. I'm also happy to contribute to a fix if the maintainers agree on the desired behavior.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.33.5
- Kueue version (use `git describe --tags --dirty --always`): v0.15.2
- Cloud provider or hardware configuration: Azure Kubernetes Service
- OS (e.g: `cat /etc/os-release`): Linux
