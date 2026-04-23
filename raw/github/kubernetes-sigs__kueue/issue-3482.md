# Issue #3482: TAS: may report negative values of pods in messages for non-admitted workloads

**Summary**: TAS: may report negative values of pods in messages for non-admitted workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3482

**Last updated**: 2024-11-12T11:44:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-07T13:02:49Z
- **Updated**: 2024-11-12T11:44:48Z
- **Closed**: 2024-11-12T11:44:48Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

**What happened**:

When a workload using preferred topology annotation cannot be admitted is sometimes reports negative number of pods in the status message of the workload.

**What you expected to happen**:

negative values of pods are never reported, it does not make sense.

**How to reproduce it (as minimally and precisely as possible)**:

I have a reproducible scenario, but it is yet not simplified enough to be included here. I will simplify and post.

Basically I create multiple jobs using preferred, and workload corresponding to the non-admitted job reports message like:
```
status:
  conditions:
  - lastTransitionTime: "2024-11-07T13:01:01Z"
    message: 'couldn''t assign flavors to pod set main: insufficient unused quota
      for cpu in flavor tas-flavor, 30 more needed, topology "gke-default" allows
      to fit only -18 out of 40 pod(s)'
    observedGeneration: 1
    reason: Pending
    status: "False"
    type: QuotaReserved
```

**Anything else we need to know?**:

It was reported first here: https://github.com/kubernetes-sigs/kueue/issues/3211#issuecomment-2458900114

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T13:02:55Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T13:03:20Z

/cc @tenzen-y @hy00nc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T10:46:16Z

After investigation it turns out that this is not only related to preferred - so I retitled the issue. 

The root cause is that the usage of TAS workloads is multiplied by the number of resources, because of [this loop](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/cache/clusterqueue.go#L522) which iterates over pairs of (resource, flavor). So it would add the same usage for `(cpu, tas-flavor), (memory, tas-flavor), (gpu, tas-flavor)`.

I proposed a fix https://github.com/kubernetes-sigs/kueue/pull/3490
