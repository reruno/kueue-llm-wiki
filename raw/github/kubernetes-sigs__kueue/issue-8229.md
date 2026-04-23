# Issue #8229: Backport RayJob autoscaling support to v0.14

**Summary**: Backport RayJob autoscaling support to v0.14

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8229

**Last updated**: 2025-12-16T18:34:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ns-sundar](https://github.com/ns-sundar)
- **Created**: 2025-12-15T06:16:03Z
- **Updated**: 2025-12-16T18:34:54Z
- **Closed**: 2025-12-16T18:34:53Z
- **Labels**: _none_
- **Assignees**: [@ns-sundar](https://github.com/ns-sundar)
- **Comments**: 4

## Description

Support for RayJob autoscaling was requested via [Issue 7605](https://github.com/kubernetes-sigs/kueue/issues/7605) and implemented via [PR 8082](https://github.com/kubernetes-sigs/kueue/pull/8082).

By default, it will be available in v0.16. This is a request to back port it to v0.14.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T06:45:04Z

I'm ok with that since this does not involve any API changes. cc @tenzen-y

### Comment by [@ns-sundar](https://github.com/ns-sundar) — 2025-12-15T17:41:42Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T18:34:48Z

/close 
as the PR are merging:
- 0.14: https://github.com/kubernetes-sigs/kueue/pull/8282
- 0.15: https://github.com/kubernetes-sigs/kueue/pull/8284

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-16T18:34:54Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8229#issuecomment-3661881219):

>/close 
>as the PR are merging:
>- 0.14: https://github.com/kubernetes-sigs/kueue/pull/8282
>- 0.15: https://github.com/kubernetes-sigs/kueue/pull/8284


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
