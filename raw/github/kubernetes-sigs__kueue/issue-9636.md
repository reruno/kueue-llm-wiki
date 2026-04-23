# Issue #9636: KEP 1834 (PropagateBatchJobLabelsToWorkload): kep.yaml not updated for GA promotion

**Summary**: KEP 1834 (PropagateBatchJobLabelsToWorkload): kep.yaml not updated for GA promotion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9636

**Last updated**: 2026-03-03T06:44:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:56:11Z
- **Updated**: 2026-03-03T06:44:45Z
- **Closed**: 2026-03-03T06:44:45Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 2

## Description

## Description

The `PropagateBatchJobLabelsToWorkload` feature was promoted to GA in v0.17, but the KEP file `keps/1834-copy-labels-into-workload/kep.yaml` has not been updated to reflect this.

**Issues:**
1. `stage: beta` → should be `stage: stable`
2. `latest-milestone: "v0.7"` → should be `latest-milestone: "v0.17"`
3. Missing `stable: "v0.17"` in the `milestone:` section

**Current:**
```yaml
stage: beta
latest-milestone: "v0.7"
milestone:
  alpha: "v0.7"
  beta: "v0.7"
```

**Expected:**
```yaml
stage: stable
latest-milestone: "v0.17"
milestone:
  alpha: "v0.7"
  beta: "v0.7"
  stable: "v0.17"
```

/area feature-gates

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:56:14Z

@kannon92: The label(s) `area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9636):

>## Description
>
>The `PropagateBatchJobLabelsToWorkload` feature was promoted to GA in v0.17, but the KEP file `keps/1834-copy-labels-into-workload/kep.yaml` has not been updated to reflect this.
>
>**Issues:**
>1. `stage: beta` → should be `stage: stable`
>2. `latest-milestone: "v0.7"` → should be `latest-milestone: "v0.17"`
>3. Missing `stable: "v0.17"` in the `milestone:` section
>
>**Current:**
>```yaml
>stage: beta
>latest-milestone: "v0.7"
>milestone:
>  alpha: "v0.7"
>  beta: "v0.7"
>```
>
>**Expected:**
>```yaml
>stage: stable
>latest-milestone: "v0.17"
>milestone:
>  alpha: "v0.7"
>  beta: "v0.7"
>  stable: "v0.17"
>```
>
>/area feature-gates


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-02T19:22:35Z

sorry my agent spammed this a little more than I'd like.

I will open up a PR address all the KEP metadata cleanup as I don't think this needs to be done as one PR each.
