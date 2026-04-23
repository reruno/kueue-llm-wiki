# Issue #9088: conflict with "multikueue.test" using v1

**Summary**: conflict with "multikueue.test" using v1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9088

**Last updated**: 2026-02-10T18:08:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-10T11:14:41Z
- **Updated**: 2026-02-10T18:08:02Z
- **Closed**: 2026-02-10T18:08:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```
error: Apply failed with 1 conflict: conflict with "multikueue.test" using v1: .data.controller_manager_config.yaml
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

Execute twice:

Use focus for this test case:

```
ginkgo.FIt("Should be able to use ClusterProfile as way to connect worker cluster", func() {
```

```sh
E2E_MODE=dev make kind-image-build test-multikueue-e2e
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-10T11:54:14Z

/assign
