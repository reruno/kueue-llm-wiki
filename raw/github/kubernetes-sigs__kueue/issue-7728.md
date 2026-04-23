# Issue #7728: TAS: nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution is ignored

**Summary**: TAS: nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution is ignored

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7728

**Last updated**: 2025-11-26T17:58:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-18T12:27:05Z
- **Updated**: 2025-11-26T17:58:36Z
- **Closed**: 2025-11-26T17:58:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 4

## Description

**What happened**:

When we create a Workload the nodeAffinity. is not respected by TAS.

Here we could follow the implementation for nodeSelectors, as here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L719-L728

Supporting `preferredDuringSchedulingIgnoredDuringExecution` is more subtle, and is not part of the issue.

**What you expected to happen**:

nodeAffnity.requiredDuringSchedulingIgnoredDuringExecution. to be respected by TAS,

**How to reproduce it (as minimally and precisely as possible)**:

Schedule a workload using the construction below, example:

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: instance-type
          operator: In
          values:
          - high-mem-xlarge
          - high-mem-2xlarge
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T12:30:43Z

cc @mwysokin @mbobrovskyi @vladikkuzn

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-20T16:26:51Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-24T10:07:08Z

/unassign

### Comment by [@kshalot](https://github.com/kshalot) — 2025-11-24T10:12:42Z

/assign
