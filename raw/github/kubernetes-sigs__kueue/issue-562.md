# Issue #562: validate the queue-name annotation

**Summary**: validate the queue-name annotation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/562

**Last updated**: 2023-02-15T18:12:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-02-14T16:12:18Z
- **Updated**: 2023-02-15T18:12:35Z
- **Closed**: 2023-02-15T18:12:35Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add validation to the queue-name annotation, similarly as to the parent-workload annotation.
Discussion comment: https://github.com/kubernetes-sigs/kueue/pull/561#discussion_r1105916498

**Why is this needed**:

To make sure that only valid CRD names are used as values to the annotation
