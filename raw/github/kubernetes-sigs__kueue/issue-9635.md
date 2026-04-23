# Issue #9635: KEP 693 (MultiKueue): kep.yaml outdated after MultiKueueBatchJobWithManagedBy GA promotion

**Summary**: KEP 693 (MultiKueue): kep.yaml outdated after MultiKueueBatchJobWithManagedBy GA promotion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9635

**Last updated**: 2026-03-03T06:44:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:56:07Z
- **Updated**: 2026-03-03T06:44:45Z
- **Closed**: 2026-03-03T06:44:45Z
- **Labels**: `area/multikueue`
- **Assignees**: _none_
- **Comments**: 1

## Description

## Description

The `MultiKueueBatchJobWithManagedBy` feature was promoted to GA in v0.17, but the KEP file `keps/693-multikueue/kep.yaml` has not been updated to reflect this.

**Issues:**
1. `latest-milestone: "v0.7"` is very outdated — should be at least `"v0.17"`
2. Missing `stable: "v0.17"` in the `milestone:` section
3. `disable-supported: true` → should be `disable-supported: false` (at least for the MultiKueueBatchJobWithManagedBy gate)

Note: This KEP covers multiple feature gates (`MultiKueue` which is still beta, and `MultiKueueBatchJobWithManagedBy` which is now GA), so the `stage` field is ambiguous. The KEP may need to be restructured or the stage may need to reflect the most advanced sub-feature.

**Current:**
```yaml
stage: beta
latest-milestone: "v0.7"
milestone:
  alpha: "v0.6"
  beta: "v0.8"
disable-supported: true
```

/area feature-gates
/area multikueue

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:56:11Z

@kannon92: The label(s) `area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9635):

>## Description
>
>The `MultiKueueBatchJobWithManagedBy` feature was promoted to GA in v0.17, but the KEP file `keps/693-multikueue/kep.yaml` has not been updated to reflect this.
>
>**Issues:**
>1. `latest-milestone: "v0.7"` is very outdated — should be at least `"v0.17"`
>2. Missing `stable: "v0.17"` in the `milestone:` section
>3. `disable-supported: true` → should be `disable-supported: false` (at least for the MultiKueueBatchJobWithManagedBy gate)
>
>Note: This KEP covers multiple feature gates (`MultiKueue` which is still beta, and `MultiKueueBatchJobWithManagedBy` which is now GA), so the `stage` field is ambiguous. The KEP may need to be restructured or the stage may need to reflect the most advanced sub-feature.
>
>**Current:**
>```yaml
>stage: beta
>latest-milestone: "v0.7"
>milestone:
>  alpha: "v0.6"
>  beta: "v0.8"
>disable-supported: true
>```
>
>/area feature-gates
>/area multikueue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
