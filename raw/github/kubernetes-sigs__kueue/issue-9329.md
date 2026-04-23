# Issue #9329: ElasticJobsViaWorkloadSlices: Disallow bidirectional scaling updates for multi-PodSet workloads

**Summary**: ElasticJobsViaWorkloadSlices: Disallow bidirectional scaling updates for multi-PodSet workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9329

**Last updated**: 2026-02-17T18:43:26Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-02-17T18:43:26Z
- **Updated**: 2026-02-17T18:43:26Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What happened**:  
ElasticJobsViaWorkloadSlices-enabled Jobs with multiple PodSets may incorrectly record quota usage during *bidirectional* scaling when one PodSet is scaled up and another is scaled down.

**What you expected to happen**:  
ElasticJobsViaWorkloadSlices-enabled Jobs with multiple PodSets should reject bidirectional scaling and not allow such updates.

**How to reproduce it (as minimally and precisely as possible)**:
- Create a RayCluster Job with 2 PodSets:
  - PodSet A = 2 replicas
  - PodSet B = 2 replicas
- Update the RayCluster Job to the following spec:
  - PodSet A = 3 replicas
  - PodSet B = 1 replica
- Observe the result.

## Summary

ElasticJobsViaWorkloadSlices currently supports scaling-enabled workloads by detecting scale-up or scale-down events and adjusting Workload PodSets and quota usage accordingly.

For workloads with a single PodSet, scale direction detection is trivial and unambiguous.

However, for workloads with multiple PodSets, the current detection logic can incorrectly classify bidirectional scaling updates, leading to inconsistent quota accounting and incorrect scaling behavior.

This issue proposes to explicitly disallow bidirectional scaling updates for ElasticJobsViaWorkloadSlices workloads with multiple PodSets, requiring users to perform directional scaling updates separately.

## Current behavior

ElasticJobsViaWorkloadSlices determines scale direction by comparing PodSet replica counts between the existing Workload and the updated Job spec.

Current detection logic effectively behaves as follows:

* If at least one PodSet replica count decreases, the change is classified as a **scale-down**
* Scale-down is handled by directly updating the existing Workload PodSets
* ClusterQueue quota usage is reduced accordingly as part of normal reconciliation

This behavior works correctly when scaling is strictly unidirectional:

* All PodSets scale up, OR
* All PodSets scale down

## Where this behavior fails

With multiple PodSets, it is possible for an update to include both:

* Scale-down in one PodSet
* Scale-up in another PodSet

Example:

Before:

```yaml
podSets:
- name: ps
  count: 4
- name: worker
  count: 8
```

After:

```yaml
podSets:
- name: ps
  count: 2   # scale-down
- name: worker
  count: 16  # scale-up
```

Under the current logic:

* This change is classified as a scale-down because at least one PodSet decreased
* The Workload is updated in place
* ClusterQueue quota usage is reduced prematurely
* However, the Workload simultaneously requires increased quota for the scaled-up PodSet

This leads to incorrect quota accounting and breaks the core ElasticJobsViaWorkloadSlices invariant that quota increases must be admission-controlled.

## Expected behavior

ElasticJobsViaWorkloadSlices should reject bidirectional scaling updates where:

* At least one PodSet replica count increases, **and**
* At least one PodSet replica count decreases

These updates should be rejected explicitly to preserve quota correctness and admission semantics.

## Proposed change

For workloads with ElasticJobsViaWorkloadSlices enabled and multiple PodSets:

Disallow updates where both of the following conditions are true:

* Any PodSet replica count increases
* Any PodSet replica count decreases

Such updates should be rejected with a clear validation error, or ignored with an appropriate Event explaining that bidirectional scaling is not supported.

## Recommended user workflow

Users should break bidirectional updates into two distinct updates, each with a single direction.

Example:

Initial state:

```text
ps: 4
worker: 8
```

Step 1, scale up:

```text
ps: 4
worker: 16
```

Step 2, scale down:

```text
ps: 2
worker: 16
```

The order of operations is not important, as long as each update is strictly unidirectional.

---

## Rationale

ElasticJobsViaWorkloadSlices relies on clear directional scaling semantics:

* Scale-up requires admission control and quota reservation
* Scale-down releases quota immediately

Bidirectional updates violate these assumptions and cannot be safely processed within the current WorkloadSlice and admission model.

Explicitly disallowing bidirectional updates ensures:

* Correct quota accounting
* Predictable admission behavior
* Clear and consistent scaling semantics
* Alignment with ElasticJobsViaWorkloadSlices lifecycle guarantees

## Scope

This change applies only to workloads with:

* ElasticJobsViaWorkloadSlices enabled
* Multiple PodSets

Single-PodSet workloads are unaffected.

## Additional context

ElasticJobsViaWorkloadSlices assumes directional scaling semantics and admission-controlled quota changes. Supporting bidirectional updates would require more complex admission coordination across PodSets, which is outside the scope of the current model.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
