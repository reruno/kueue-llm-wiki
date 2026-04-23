# Issue #8429: Performance tests are not repeatable because ResourceFlavors are not cleaned up.

**Summary**: Performance tests are not repeatable because ResourceFlavors are not cleaned up.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8429

**Last updated**: 2025-12-30T08:38:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@taehwoi](https://github.com/taehwoi)
- **Created**: 2025-12-30T06:33:05Z
- **Updated**: 2025-12-30T08:38:36Z
- **Closed**: 2025-12-30T08:38:36Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

```make run-performance-scheduler``` and their likes.
**First observed in** (PR or commit, if known):

**Link to failed CI job or steps to reproduce locally**:

**Failure message or logs**:
```
2025-12-30T15:30:06.973824+09:00        ERROR   Run generator   runner/main.go:351      generating      {"error": "resourceflavors.kueue.x-k8s.io \"rf\" already exists"}
```

**Anything else we need to know?**:
```CleanUp``` does not remove ResourceFlavor because ```CleanupLabel``` is added to nodeLabels, not metadata.Labels.

Will open a PR addressing this.
