# Issue #3709: Node has `node.kubernetes.io/not-ready` taint in integration tests even if the Node is ready

**Summary**: Node has `node.kubernetes.io/not-ready` taint in integration tests even if the Node is ready

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3709

**Last updated**: 2024-12-04T12:15:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-12-02T16:16:14Z
- **Updated**: 2024-12-04T12:15:03Z
- **Closed**: 2024-12-04T12:15:03Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In the integration tests nodes have `node.kubernetes.io/not-ready` taint even if in their status `Ready` condition is set to `true` 

**What you expected to happen**:
Nodes didn't have the taint

**How to reproduce it (as minimally and precisely as possible)**:
Run newly added integration test from this [PR](https://github.com/kubernetes-sigs/kueue/pull/3708/files#diff-f24b50c55e86bbae151e985e718b4280d2585110e1b692c579a4a0c6c191036d) with toleration deleted 

**Anything else we need to know?**:
I believe we should add util function that removes the taint based on `Ready` condition

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-02T16:16:27Z

/cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-04T08:27:12Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T08:29:12Z

> I believe we should add util function that removes the taint based on Ready condition

Or a function `createNode` which does 3 things: (1) creates the node, (2) updates status based on the object, (3) removes the taint if the node is Ready
