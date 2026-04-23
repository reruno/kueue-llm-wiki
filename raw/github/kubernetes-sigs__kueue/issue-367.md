# Issue #367: Documentation: Link to Admission points to concepts folder.

**Summary**: Documentation: Link to Admission points to concepts folder.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/367

**Last updated**: 2022-09-06T14:56:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-09-02T13:32:31Z
- **Updated**: 2022-09-06T14:56:56Z
- **Closed**: 2022-09-06T14:56:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

https://github.com/kubernetes-sigs/kueue/blob/main/docs/concepts/cluster_queue.md

In cluster_queue concepts:

```
In a process called [admission](https://github.com/kubernetes-sigs/kueue/blob/main/docs/concepts/#admission), Kueue assigns to the [Workload pod sets](https://github.com/kubernetes-sigs/kueue/blob/main/docs/concepts/workload.md#pod-sets) a flavor for each resource the pod set requests.
```

Admission is linked to a nonexistent section in the repo.  I'd be willing to open a PR but I'm unsure where it is supposed to point or if that was removed.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-02T19:24:15Z

Looking at the README.md in concepts, there is a section about Admission.  I assume this is where the doc was meant to point?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-09-05T02:35:56Z

I think so. It should be fixed.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-05T19:27:47Z

@kerthcet Thank you for pointing that out.  I have a PR to fix this now.
