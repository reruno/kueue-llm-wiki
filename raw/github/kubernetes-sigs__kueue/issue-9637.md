# Issue #9637: LendingLimit feature-state version tag incorrect in cluster_queue.md

**Summary**: LendingLimit feature-state version tag incorrect in cluster_queue.md

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9637

**Last updated**: 2026-03-03T17:13:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-02T18:56:16Z
- **Updated**: 2026-03-03T17:13:22Z
- **Closed**: 2026-03-03T17:13:22Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

## Description

The LendingLimit feature was promoted to GA in v0.17, but the documentation in `site/content/en/docs/concepts/cluster_queue.md` (line 361) has an incorrect version tag.

**Current:**
```
{{< feature-state state="stable" for_version="v0.18" >}}
```

**Expected:**
```
{{< feature-state state="stable" for_version="v0.17" >}}
```

/area documentation
/area feature-gates

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-02T18:56:19Z

@kannon92: The label(s) `area/documentation, area/feature-gates` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9637):

>## Description
>
>The LendingLimit feature was promoted to GA in v0.17, but the documentation in `site/content/en/docs/concepts/cluster_queue.md` (line 361) has an incorrect version tag.
>
>**Current:**
>```
>{{< feature-state state="stable" for_version="v0.18" >}}
>```
>
>**Expected:**
>```
>{{< feature-state state="stable" for_version="v0.17" >}}
>```
>
>/area documentation
>/area feature-gates


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
