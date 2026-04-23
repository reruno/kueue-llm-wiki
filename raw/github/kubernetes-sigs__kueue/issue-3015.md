# Issue #3015: Add integration tests for detecting CRD installed after Kueue started

**Summary**: Add integration tests for detecting CRD installed after Kueue started

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3015

**Last updated**: 2024-10-11T18:48:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-09T07:45:02Z
- **Updated**: 2024-10-11T18:48:25Z
- **Closed**: 2024-10-11T18:48:25Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be cleaned**:

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/2574. 

**Why is this needed**:

To gain confidence the mechanism works as expected since there are pieces of the code which are hard to cover with unit tests.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-09T07:45:28Z

/cc @ChristianZaccaria @varshaprasad96 @alculquicondor @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T17:11:58Z

That makes sense. Since we implemented the watcher by hand, we should keep to prove that the watcher works fine.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-09T12:51:27Z

/assign
