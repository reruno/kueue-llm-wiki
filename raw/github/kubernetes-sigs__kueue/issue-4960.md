# Issue #4960: [Cohort] Reconcile Skipped when FairSharing Weight Updated

**Summary**: [Cohort] Reconcile Skipped when FairSharing Weight Updated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4960

**Last updated**: 2025-04-14T15:27:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-04-14T14:11:34Z
- **Updated**: 2025-04-14T15:27:09Z
- **Closed**: 2025-04-14T15:27:09Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What happened**:
When updating FairSharing weight, we filter out Cohort updates that are only updating the FairSharing weight

https://github.com/kubernetes-sigs/kueue/blob/ebe37a32cd69f1e2d4215562716f35751ac03a4c/pkg/controller/core/cohort_controller.go#L113-L117

- Kueue version: 0.11.3
