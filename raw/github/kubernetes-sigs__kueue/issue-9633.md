# Issue #9633: KEP 2936 (LocalQueueDefaulting): stage not updated for GA promotion

**Summary**: KEP 2936 (LocalQueueDefaulting): stage not updated for GA promotion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9633

**Last updated**: 2026-03-03T06:44:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:55:59Z
- **Updated**: 2026-03-03T06:44:44Z
- **Closed**: 2026-03-03T06:44:44Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

## Description

The `LocalQueueDefaulting` feature was promoted to GA in v0.17, but the KEP file `keps/2936-local-queue-defaulting/kep.yaml` still has `stage: alpha` instead of `stage: stable`.

**Current:**
```yaml
stage: alpha
```

**Expected:**
```yaml
stage: stable
```

The `latest-milestone`, `milestone`, and `disable-supported` fields are already correct.

/area feature-gates

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:56:02Z

@kannon92: The label(s) `area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9633):

>## Description
>
>The `LocalQueueDefaulting` feature was promoted to GA in v0.17, but the KEP file `keps/2936-local-queue-defaulting/kep.yaml` still has `stage: alpha` instead of `stage: stable`.
>
>**Current:**
>```yaml
>stage: alpha
>```
>
>**Expected:**
>```yaml
>stage: stable
>```
>
>The `latest-milestone`, `milestone`, and `disable-supported` fields are already correct.
>
>/area feature-gates


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
