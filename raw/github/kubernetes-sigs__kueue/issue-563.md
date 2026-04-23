# Issue #563: Use global Kueue context for field indexing

**Summary**: Use global Kueue context for field indexing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/563

**Last updated**: 2023-02-15T14:58:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-02-14T17:03:40Z
- **Updated**: 2023-02-15T14:58:26Z
- **Closed**: 2023-02-15T14:58:26Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use global Kueue context for field indexing, instead of the context.Background()

**Why is this needed**:

To make sure the indexing is cancelled as soon as the Kueue context is cancelled.
This is a follow up issue for the discussion: https://github.com/kubernetes-sigs/kueue/pull/561#discussion_r1105890071
