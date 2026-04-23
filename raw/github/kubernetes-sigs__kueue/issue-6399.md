# Issue #6399: [MultiKueue test] The connection to a worker cluster is unreliable makes cluster not working properly

**Summary**: [MultiKueue test] The connection to a worker cluster is unreliable makes cluster not working properly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6399

**Last updated**: 2025-08-12T13:41:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-04T07:37:21Z
- **Updated**: 2025-08-12T13:41:10Z
- **Closed**: 2025-08-12T13:41:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

**What happened**:

This test leaves the cluster not working properly, if there are any tests executing after it they flake.

**What you expected to happen**:

The test should leave the cluster in usable state.

**How to reproduce it (as minimally and precisely as possible)**:

see https://github.com/kubernetes-sigs/kueue/issues/6386

**Anything else we need to know?**:

Maybe we could call AwaitForAvailablity on both workers and manager clusters.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T07:37:47Z

cc @mszadkow @mbobrovskyi it will be great to fix this

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-05T12:11:34Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-05T12:12:55Z

I believe I found the fix.
I tested back to back 10 times the mentioned test.
The problem was that kube-system components were still in CrashLoopBackoff.
The fix includes the need for checking that.
PR is on its way.
