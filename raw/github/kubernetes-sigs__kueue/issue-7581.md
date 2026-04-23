# Issue #7581: Extract a helper function workload.Finish for finishing workloads

**Summary**: Extract a helper function workload.Finish for finishing workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7581

**Last updated**: 2025-11-07T16:22:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-07T12:20:12Z
- **Updated**: 2025-11-07T16:22:55Z
- **Closed**: 2025-11-07T16:22:55Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently we mark workloads as finished from a couple of places, it would be good to have a single place, workload.Finish, analogous to workload.Evict. The helper function should use SSA by default, and use Patch when WorkloadRequestUseMergePatch is enabled.

**Why is this needed**:

To commonize the code and allow injecting custom code in one place.
This is needed for https://github.com/kubernetes-sigs/kueue/pull/7532, see https://github.com/kubernetes-sigs/kueue/pull/7532/files#r2500411357

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T12:20:38Z

cc @amy 
cc @mbobrovskyi or @mszadkow who could maybe help with that

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T12:23:48Z

cc @mwysokin

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-07T12:24:56Z

/assign
