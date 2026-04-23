# Issue #5275: Kueue should provide RBAC permissions for cohorts OOTB

**Summary**: Kueue should provide RBAC permissions for cohorts OOTB

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5275

**Last updated**: 2025-06-02T12:37:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-19T06:50:05Z
- **Updated**: 2025-06-02T12:37:07Z
- **Closed**: 2025-06-02T12:37:06Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 5

## Description

**What happened**:

I noticed that Kueue does not provide RBAC permissions for Cohort API to update & read by admis.

**What you expected to happen**:

Kueue provides the RBAC natively as for other cluster-scoped resources (ClusterQueue, ResourceFlavor, Topology).

**How to reproduce it (as minimally and precisely as possible)**:

Execute a request authenticated as a Kueue batch admin.

**Anything else we need to know?**:

It is not a critical bugs - administrators can easily provide the necessary RBAC, but I think we should strive for consistency, following the principle of least surprise.

See for comparison RBAC for ResourceFlavor: 

https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/resourceflavor_editor_role.yaml

https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/resourceflavor_viewer_role.yaml

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T06:50:21Z

cc @gabesaba @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T06:50:30Z

cc @tenzen-y

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-05-27T14:17:49Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-02T12:37:02Z

/close

Due to fixed on https://github.com/kubernetes-sigs/kueue/pull/5431.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-02T12:37:06Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5275#issuecomment-2930479544):

>/close
>
>Due to fixed on https://github.com/kubernetes-sigs/kueue/pull/5431.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
