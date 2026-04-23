# Issue #9634: KEP 1618 (ObjectRetentionPolicies): kep.yaml not updated for GA promotion

**Summary**: KEP 1618 (ObjectRetentionPolicies): kep.yaml not updated for GA promotion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9634

**Last updated**: 2026-03-03T06:44:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:56:03Z
- **Updated**: 2026-03-03T06:44:45Z
- **Closed**: 2026-03-03T06:44:45Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

## Description

The `ObjectRetentionPolicies` feature was promoted to GA in v0.17, but the KEP file `keps/1618-optional-gc-of-workloads/kep.yaml` has not been updated to reflect this.

**Issues:**
1. `stage: alpha` → should be `stage: stable`
2. `latest-milestone: "v0.13"` → should be `latest-milestone: "v0.17"`
3. Missing `stable: "v0.17"` in the `milestone:` section
4. `disable-supported: true` → should be `disable-supported: false`

**Current:**
```yaml
stage: alpha
latest-milestone: "v0.13"
milestone:
  alpha: "v0.12"
  beta: "v0.13"
disable-supported: true
```

**Expected:**
```yaml
stage: stable
latest-milestone: "v0.17"
milestone:
  alpha: "v0.12"
  beta: "v0.13"
  stable: "v0.17"
disable-supported: false
```

/area feature-gates

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:56:06Z

@kannon92: The label(s) `area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9634):

>## Description
>
>The `ObjectRetentionPolicies` feature was promoted to GA in v0.17, but the KEP file `keps/1618-optional-gc-of-workloads/kep.yaml` has not been updated to reflect this.
>
>**Issues:**
>1. `stage: alpha` → should be `stage: stable`
>2. `latest-milestone: "v0.13"` → should be `latest-milestone: "v0.17"`
>3. Missing `stable: "v0.17"` in the `milestone:` section
>4. `disable-supported: true` → should be `disable-supported: false`
>
>**Current:**
>```yaml
>stage: alpha
>latest-milestone: "v0.13"
>milestone:
>  alpha: "v0.12"
>  beta: "v0.13"
>disable-supported: true
>```
>
>**Expected:**
>```yaml
>stage: stable
>latest-milestone: "v0.17"
>milestone:
>  alpha: "v0.12"
>  beta: "v0.13"
>  stable: "v0.17"
>disable-supported: false
>```
>
>/area feature-gates


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
