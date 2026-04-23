# Issue #7612: Cleanup logging for Job MultiKueue adapter

**Summary**: Cleanup logging for Job MultiKueue adapter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7612

**Last updated**: 2025-11-12T18:43:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-12T11:20:58Z
- **Updated**: 2025-11-12T18:43:42Z
- **Closed**: 2025-11-12T18:43:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Cleanup this line (use logger) https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_multikueue_adapter.go#L54 instead of printing to console

**Why is this needed**:

To use logging consistently

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T11:21:08Z

cc @yaroslava-serdiuk @ichekrygin
