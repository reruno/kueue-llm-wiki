# Issue #8564: MultiKueue: performance testing

**Summary**: MultiKueue: performance testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8564

**Last updated**: 2026-02-16T10:50:34Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-13T16:35:01Z
- **Updated**: 2026-02-16T10:50:34Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**:

Performance test for MultiKueue . 

We would like to observe the rate of processing workloads assuming there are 3 (or so) worker clusters.

I imagine this is a dedicated CI job. It will be hard in OSS on kind to get beyond 3 clusters probably, or otherwise we will anyway saturate the resources of the host node running the CI job.



**Why is this needed**:

To allow detecting performance regressions in MultiKueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:01Z

/priority important-soon

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:32Z

/area multikueue
