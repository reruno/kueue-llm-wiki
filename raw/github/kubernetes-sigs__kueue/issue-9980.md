# Issue #9980: Include real queue position in the scheduling cycle debug logs and improve corresponding metrics

**Summary**: Include real queue position in the scheduling cycle debug logs and improve corresponding metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9980

**Last updated**: 2026-03-18T12:52:50Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-03-18T12:52:50Z
- **Updated**: 2026-03-18T12:52:50Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What would you like to be added**:

Information how deep the scheduler was able to get into Kueue. That could be proxied by amount of inadmissible workloads form the given CQ.

Also consider creating a gauge metrics that explains how many workloads were processed before readmission is triggered for a CQ. 

**Why is this needed**:

It is hard to debug how deep the scheduler goes into CQ and why some workloads are not being reached. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.
