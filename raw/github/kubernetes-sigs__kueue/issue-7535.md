# Issue #7535: Generate feature gate documentation based on `kube_features.go`

**Summary**: Generate feature gate documentation based on `kube_features.go`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7535

**Last updated**: 2025-11-05T08:38:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-11-05T08:23:01Z
- **Updated**: 2025-11-05T08:38:05Z
- **Closed**: 2025-11-05T08:38:04Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Generate feature gate documentation based on `kube_features.go`. Maybe with some make command

**Why is this needed**:
So there's no need to sync the table in the doc with the state of `kube_features` manually

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-05T08:34:33Z

I think this is duplicate of https://github.com/kubernetes-sigs/kueue/issues/5507.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:38:00Z

/close
Yes

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-05T08:38:05Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7535#issuecomment-3489946159):

>/close
>Yes


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
