# Issue #5291: Scheduling Cycle not Filtering Workloads with nil-CQ

**Summary**: Scheduling Cycle not Filtering Workloads with nil-CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5291

**Last updated**: 2025-05-20T12:37:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-05-20T10:31:37Z
- **Updated**: 2025-05-20T12:37:17Z
- **Closed**: 2025-05-20T12:37:17Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba), [@PBundyra](https://github.com/PBundyra)
- **Comments**: 4

## Description

**What happened**:
Unit and integration tests pass, even when following lines are deleted: https://github.com/kubernetes-sigs/kueue/blob/7da8e0a2ea64c026ed3daf28aec63d711c1d1f72/pkg/scheduler/scheduler.go#L361-L362

A bug noted in https://github.com/kubernetes-sigs/kueue/issues/4959#issuecomment-2831045590 was fixed by #5138, but this does not seem to cover all the cases (FairSharing=true). Additionally, there is some undefined behavior, as we are running normal scheduling logic with CQ=nil

**What you expected to happen**:
The line which checks for nil-cq should prevent that workload from hitting the normal scheduling path. Additionally, other workloads with an inadmissibleMsg should not be considered for scheduling (only requeued)

Once we get entries (step 3), we split that list into "validEntries" and "invalidEntries". We only pass validEntries to the iterator, while requeueing invalidEntries

https://github.com/kubernetes-sigs/kueue/blob/7da8e0a2ea64c026ed3daf28aec63d711c1d1f72/pkg/scheduler/scheduler.go#L198-L202

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:32:18Z

Also see https://github.com/kubernetes-sigs/kueue/pull/5287#issuecomment-2893436998

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:32:39Z

/assign @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T10:38:08Z

@gabesaba can you please untangle the issue. I have a feeling it mixes a nil-pointer exception bug in case of fair sharing (needs minimal fix + test and cherry-picking) with the readability cleanups (can be ambitious, but no cherry-picks). My view on this:

> Unit and integration tests pass, even when following lines are deleted:

This is not a bug, it is a missing gap in testing (cleanup).

> A bug noted in https://github.com/kubernetes-sigs/kueue/issues/4959#issuecomment-2831045590 was fixed by https://github.com/kubernetes-sigs/kueue/pull/5138, but this does not seem to cover all the cases (FairSharing=true). Additionally, there is some undefined behavior, as we are running normal scheduling logic with CQ=nil

This is a bug which should be fixed with minimal diff and cherry-picked.

> Once we get entries (step 3), we split that list into "validEntries" and "invalidEntries". We only pass validEntries to the iterator, while requeueing invalidEntries

This seems like a cleanup. I would prefer not to need to cherry-pick this.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T12:03:49Z

/assign
