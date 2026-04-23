# Issue #741: Document: Manage number of pods in ClusterQueues

**Summary**: Document: Manage number of pods in ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/741

**Last updated**: 2023-05-09T09:18:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-03T14:10:57Z
- **Updated**: 2023-05-09T09:18:34Z
- **Closed**: 2023-05-09T09:18:33Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

**What would you like to be cleaned**:

Document the semantics when managing number of pods in a ClusterQueue quota.

It should go in https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/

Since this is a new feature for a version that wasn't released, we shouldn't merge the documentation into the main branch, otherwise it will immediately go live. You can open PRs against the `website-release-0.4` branch.

**Why is this needed**:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T14:11:06Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-05-09T04:41:27Z

@alculquicondor I think we should manually close, #743 is closed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-09T09:18:30Z

@trasc Thanks!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-09T09:18:34Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/741#issuecomment-1539761335):

>@trasc Thanks!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
