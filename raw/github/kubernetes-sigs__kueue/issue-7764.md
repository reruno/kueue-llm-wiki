# Issue #7764: Document MultiKueue support authentication to worker clusters using ClusterProfile

**Summary**: Document MultiKueue support authentication to worker clusters using ClusterProfile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7764

**Last updated**: 2025-11-25T18:14:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-19T15:34:07Z
- **Updated**: 2025-11-25T18:14:42Z
- **Closed**: 2025-11-25T18:14:42Z
- **Labels**: `kind/documentation`
- **Assignees**: [@hdp617](https://github.com/hdp617)
- **Comments**: 10

## Description

Follow up to https://github.com/kubernetes-sigs/kueue/issues/6714

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T15:34:42Z

/assign hdp617
Tentatively as the feature owner

cc @tenzen-y

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-19T15:34:44Z

@mimowo: GitHub didn't allow me to assign the following users: hdp617.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7764#issuecomment-3553370000):

>/assign hdp617
>Tentatively as the feature owner
>
>cc @tenzen-y
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T15:35:07Z

cc @hdp617

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T15:36:09Z

cc @kannon92 @mwysokin

### Comment by [@hdp617](https://github.com/hdp617) — 2025-11-19T17:04:17Z

/assign @hdp617

### Comment by [@hdp617](https://github.com/hdp617) — 2025-11-19T17:19:38Z

I'm planning to add a section e.g. "Setup MultiKueue with the ClusterProfile API" to this [doc](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/). WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T17:34:27Z

sgtm, the only hesitation I have is where to put the cloud provider specific bits

### Comment by [@hdp617](https://github.com/hdp617) — 2025-11-19T17:48:58Z

> sgtm, the only hesitation I have is where to put the cloud provider specific bits

That's a good callout. I'll keep the documentation cloud provider neutral and add links to the cloud provider specific bits (e.g. plugins), similar to the section for Open Cluster Management (OCM).

### Comment by [@hdp617](https://github.com/hdp617) — 2025-11-24T18:57:32Z

cc @knee-berts @zhang-xuebin.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T08:16:37Z

/kind documentation
