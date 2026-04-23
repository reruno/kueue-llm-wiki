# Issue #3243: [kjobctl] Publish a dedicated image to run kjobctl slurm init container

**Summary**: [kjobctl] Publish a dedicated image to run kjobctl slurm init container

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3243

**Last updated**: 2024-12-03T13:56:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-16T07:04:16Z
- **Updated**: 2024-12-03T13:56:31Z
- **Closed**: 2024-12-03T13:56:29Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be added**:

To simplify the development of the slurm support in kjobctl. Also, not to use outdated images.
The new image could be generic for kjobctl , or specific for the slurm support (maybe `kjobctl-slurm`), to be discussed.

This is related also to https://github.com/kubernetes-sigs/kueue/issues/2778.

**Why is this needed**:

The discussion [here](https://github.com/kubernetes-sigs/kueue/pull/3072#discussion_r1800756917). 
The available images in registry.k8s.io (see https://explore.ggcr.dev/?repo=registry.k8s.io) are very limited in tooling, or old. We could not find a new image which would have: `bash` and `nslookup` (with `bind-tools`).

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-21T03:18:15Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T13:56:24Z

/close

Due to moved to separate repo https://github.com/kubernetes-sigs/kjob/issues/6.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-03T13:56:30Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3243#issuecomment-2514630280):

>/close
>
>Due to moved to separate repo https://github.com/kubernetes-sigs/kjob/issues/6.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
