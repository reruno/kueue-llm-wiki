# Issue #8302: MultiKueue should redo the admission process once the workload looses Admission in the worker cluster

**Summary**: MultiKueue should redo the admission process once the workload looses Admission in the worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8302

**Last updated**: 2026-01-15T13:36:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-12-17T13:51:35Z
- **Updated**: 2026-01-15T13:36:30Z
- **Closed**: 2026-01-15T10:01:38Z
- **Labels**: `kind/bug`, `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

**What happened**:

Currently only the cluster that previously run the workload tries to readmit the workload.

**What you expected to happen**:

If a MK workload looses admission (due to preemption, node failure, etc), it should get back to the MK admission process and be attempted on multiple clusters.

**How to reproduce it (as minimally and precisely as possible)**:

Preempt MK workload at the worker cluster level.

**Anything else we need to know?**:

It is a generalization of #8089

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:19:06Z

/area multikueue
/priority important-soon

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-02T07:43:55Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-07T13:14:00Z

Clarified with @mimowo on sync meeting:
Eviction on the worker should restart the admission on the manager.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T13:36:27Z

/kind feature
Handling as a feature (no backporting of https://github.com/kubernetes-sigs/kueue/pull/8477) for now, because this behavior is actually unspecified in the KEP. 

I'm happy to cherrypick in the future if someone raises this as a blocker for them (there is no API change, and we have a feature gate so it should be relatively safe), so let me know.
