# Issue #5855: [DOC] Add a doc to explain how to enable Kueue to manage RayService

**Summary**: [DOC] Add a doc to explain how to enable Kueue to manage RayService

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5855

**Last updated**: 2025-07-08T17:56:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@weizhaowz](https://github.com/weizhaowz)
- **Created**: 2025-07-02T21:00:15Z
- **Updated**: 2025-07-08T17:56:25Z
- **Closed**: 2025-07-08T17:56:25Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 3

## Description

Kueue currently doesn't support RayService, and a [pr](https://github.com/kubernetes-sigs/kueue/pull/5664) tries to implement RayService controller, webhook and multikueue-adapter. However, this pr won't work as there is asynchronization between RayService's embedded RayCluster object and the RayCluster object created for the target RayService, and this issue cannot be fixed by Kueue or current RayService controller on KubeRay side. On the other hand, RayService's label is propagated to the RayCluster for it, so it's able to let Kueue manage a RayService through its RayCluster. Therefore, a doc is needed to explain the process.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T17:56:01Z

/kind documentation

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T17:56:20Z

/close
as completed by #5822

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-08T17:56:25Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5855#issuecomment-3049827865):

>/close
>as completed by #5822 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
