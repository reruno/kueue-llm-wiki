# Issue #3821: Use kueue.x-k8s.io/resource-in-use finalizer for Topology

**Summary**: Use kueue.x-k8s.io/resource-in-use finalizer for Topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3821

**Last updated**: 2024-12-13T17:30:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-12T08:55:47Z
- **Updated**: 2024-12-13T17:30:28Z
- **Closed**: 2024-12-13T17:30:28Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What happened**:

Topology can be deleted easily at any time, even when in use.

**What you expected to happen**:

There should be some guard before accidental deletion, such as we have for ResourceFlavor - the kueue.x-k8s.io/resource-in-use finalizer. The Topology can be still deleted by admins, just requires either first deleting the ResourceFlavor, or deleting the finalizer.

**How to reproduce it (as minimally and precisely as possible)**:

Create the structure: LQ, CQ, RF, Topology. 

Now, the Topology can be deleted.

**Anything else we need to know?**:

Here is the analogous code handing the finalizer for ResourceFlavors: https://github.com/kubernetes-sigs/kueue/blob/e544dc8a447abfafb471886f9390af0a303b24d5/pkg/controller/core/resourceflavor_controller.go#L83-L108

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T08:55:59Z

cc @PBundyra @mbobrovskyi @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T08:56:31Z

cc @mwysokin

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-12T09:00:31Z

/assign
