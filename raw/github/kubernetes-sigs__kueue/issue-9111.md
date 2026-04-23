# Issue #9111: Parallel make verify produces interleaved/messy output, making failed target errors hard to find

**Summary**: Parallel make verify produces interleaved/messy output, making failed target errors hard to find

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9111

**Last updated**: 2026-02-12T04:30:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-11T09:52:06Z
- **Updated**: 2026-02-12T04:30:01Z
- **Closed**: 2026-02-12T04:30:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

After we introduce parallel `verify`, the output from multiple targets becomes interleaved.
If some targets fail, the error messages are scattered throughout the log and mixed with output from other targets (still running or successful). This makes it very difficult to locate and read the actual errors.

Here is a real-world example from a recent Prow job where the problem is visible:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9095/pull-kueue-verify-main/2021228992547262464

**Why is this needed**:

Easier debugging of failures during parallel verify runs.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-11T09:52:14Z

/cc @vladikkuzn

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-02-11T15:58:30Z

/assign
