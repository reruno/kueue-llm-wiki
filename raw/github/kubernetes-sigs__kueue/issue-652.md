# Issue #652: Can we use tfjob or pytorchjob in kueue?

**Summary**: Can we use tfjob or pytorchjob in kueue?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/652

**Last updated**: 2023-03-29T02:20:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2023-03-20T11:46:55Z
- **Updated**: 2023-03-29T02:20:29Z
- **Closed**: 2023-03-20T12:06:04Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->
Kueue automatically creates a Workload for MPI Job and Job. Will it create workload for tfjob or pytorchjob?

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-20T12:05:59Z

@KunWuLuan Thank you for creating this issue!

We haven’t supported TFJob and PyTorchJob, yet.
You can keep tracking the feature in #297.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-20T12:06:05Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/652#issuecomment-1476105843):

>@KunWuLuan Thank you for creating this issue!
>
>We haven’t support TFJob and PyTorchJob, yet.
>You can keep tracking the feature in #297.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-20T13:20:57Z

We are currently blocked on this https://github.com/kubeflow/common/pull/196

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-03-29T02:20:29Z

Ok, thanks for help : )
