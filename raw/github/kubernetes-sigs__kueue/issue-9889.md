# Issue #9889: Kueue may hit inifinite requeue loop for workloads which only specify limits without requests

**Summary**: Kueue may hit inifinite requeue loop for workloads which only specify limits without requests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9889

**Last updated**: 2026-03-18T22:49:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-16T10:37:46Z
- **Updated**: 2026-03-18T22:49:17Z
- **Closed**: 2026-03-16T21:15:40Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description


**What happened**:

Kueue may hit inifinte requeue loop for workloads which only specify limits without requests.

Such workloads loop with the `Workload no longer fits after processing another workload` even if there is enough capacity

**What you expected to happen**:

Workloads should be able to schedule as soon as there is enough capacty.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

The reason is that requeueAndUpdate does not use AdjustResources which is responsible for defaulting requests based on limits

Specifying only limits is pretty popular patter for accelarator workloads.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T10:37:50Z

/assign
tentatively as I already debugged the issue and have some repro integration test.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T10:38:23Z

cc @mwysokin

### Comment by [@jessicaxiejw](https://github.com/jessicaxiejw) — 2026-03-18T22:49:17Z

Any chance we could do a release with this fix? We are seeing this issue in our production cluster right now.
