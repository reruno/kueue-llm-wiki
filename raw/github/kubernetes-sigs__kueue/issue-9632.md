# Issue #9632: PropagateBatchJobLabelsToWorkload GA entry missing LockToDefault: true

**Summary**: PropagateBatchJobLabelsToWorkload GA entry missing LockToDefault: true

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9632

**Last updated**: 2026-03-03T06:44:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:55:07Z
- **Updated**: 2026-03-03T06:44:37Z
- **Closed**: 2026-03-03T06:44:37Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

## Description

The `PropagateBatchJobLabelsToWorkload` feature was promoted to GA in v0.17, but its feature gate entry in `pkg/features/kube_features.go` (line 398) is missing `LockToDefault: true`.

**Current:**
```go
PropagateBatchJobLabelsToWorkload: {
    {Version: version.MustParse("0.15"), Default: true, PreRelease: featuregate.Beta},
    {Version: version.MustParse("0.17"), Default: true, PreRelease: featuregate.GA},
},
```

**Expected:**
```go
PropagateBatchJobLabelsToWorkload: {
    {Version: version.MustParse("0.15"), Default: true, PreRelease: featuregate.Beta},
    {Version: version.MustParse("0.17"), Default: true, PreRelease: featuregate.GA, LockToDefault: true}, // remove in 0.19
},
```

All other features promoted to GA in v0.17 (HierarchicalCohorts, LendingLimit, MultiKueueBatchJobWithManagedBy, LocalQueueDefaulting, ObjectRetentionPolicies, SanitizePodSets) have `LockToDefault: true` set correctly.

/area feature-gates

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:55:10Z

@kannon92: The label(s) `area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9632):

>## Description
>
>The `PropagateBatchJobLabelsToWorkload` feature was promoted to GA in v0.17, but its feature gate entry in `pkg/features/kube_features.go` (line 398) is missing `LockToDefault: true`.
>
>**Current:**
>```go
>PropagateBatchJobLabelsToWorkload: {
>    {Version: version.MustParse("0.15"), Default: true, PreRelease: featuregate.Beta},
>    {Version: version.MustParse("0.17"), Default: true, PreRelease: featuregate.GA},
>},
>```
>
>**Expected:**
>```go
>PropagateBatchJobLabelsToWorkload: {
>    {Version: version.MustParse("0.15"), Default: true, PreRelease: featuregate.Beta},
>    {Version: version.MustParse("0.17"), Default: true, PreRelease: featuregate.GA, LockToDefault: true}, // remove in 0.19
>},
>```
>
>All other features promoted to GA in v0.17 (HierarchicalCohorts, LendingLimit, MultiKueueBatchJobWithManagedBy, LocalQueueDefaulting, ObjectRetentionPolicies, SanitizePodSets) have `LockToDefault: true` set correctly.
>
>/area feature-gates


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
