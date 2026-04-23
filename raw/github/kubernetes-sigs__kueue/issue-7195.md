# Issue #7195: TrainJob is missing rbac for batch-admin or batch-user

**Summary**: TrainJob is missing rbac for batch-admin or batch-user

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7195

**Last updated**: 2025-10-07T16:37:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-10-07T14:17:55Z
- **Updated**: 2025-10-07T16:37:02Z
- **Closed**: 2025-10-07T16:37:02Z
- **Labels**: _none_
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 10

## Description

When we onboard a new controller, we need to add rbac for admin and user roles.

We should add TrainJob rbac [here](https://github.com/kubernetes-sigs/kueue/tree/main/config/components/rbac).

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T14:18:16Z

cc @tenzen-y @kaisoz @mimowo @astefanutti @andreyvelich

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T14:22:16Z

Oh, good spot! Would you like to provide a fix?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T14:29:51Z

Does a kueue admin just need TrainJob permissions?

I wasn't sure about clustertrainingruntimes or traininingruntimes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T14:33:03Z

Good question. I'm also not clear about users if they should see the cluster scope resources.

I guess we could start on the conservative side and only allow seeing namespaced objects.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T14:33:24Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T14:39:29Z

PR is up. https://github.com/kubernetes-sigs/kueue/pull/7196

We should carry this to 0.14.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-10-07T14:46:51Z

Thanks for reporting this @kannon92!

>Good question. I'm also not clear about users if they should see the cluster scope resources.

Any concerns to give users read permission over ClusterTrainingRuntime even tho it is cluster-scoped ?
Yes, we will require to create ClusterRoleBinding for that.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T14:50:32Z

> Any concerns to give users read permission over ClusterTrainingRuntime even tho it is cluster-scoped ?

Generally cluster resources are cluster admin restricted. We don't give users read permissions for Kueue cluster resources either.

A kueue admin usually only has the rights to view cluster resources (see https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac/clusterqueue_viewer_role.yaml)

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-10-07T14:54:35Z

So it looks like we can leverage `clusterqueue-viewer-role` to read information from the ClusterTrainingRuntime, right ?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-07T15:02:36Z

> So it looks like we can leverage `clusterqueue-viewer-role` to read information from the ClusterTrainingRuntime, right ?

No, that role only gives a batch-admin access to read ClusterQueues.
