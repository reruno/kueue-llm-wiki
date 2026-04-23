# Issue #753: [DOC] add helm chart support to installation

**Summary**: [DOC] add helm chart support to installation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/753

**Last updated**: 2023-07-21T20:16:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-05-09T03:28:27Z
- **Updated**: 2023-07-21T20:16:09Z
- **Closed**: 2023-07-21T20:16:09Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 10

## Description

We can install kueue via helm chart https://github.com/kubernetes-sigs/kueue/pull/664 now.
/kind documentation
cc @Gekko0114

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-09T03:30:41Z

/remove-kind feature

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-26T00:36:48Z

/reopen

We are still missing the documentation for the website.
Although we might have to wait until we have the release?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-26T00:36:52Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/753#issuecomment-1563665772):

>/reopen
>
>We are still missing the documentation for the website.
>Although we might have to wait until we have the release?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-05-26T00:45:12Z

After releasing, we might need to change README.md again.
Also we have to check whether charts are released correctly

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-10T12:26:46Z

We included a helm chart in the release.
Let's document how to install from there in the website.

Any volunteers?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-17T07:48:43Z

/assign @BinL233

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-17T07:48:45Z

@kerthcet: GitHub didn't allow me to assign the following users: BinL233.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/753#issuecomment-1637541183):

>/assign @BinL233 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-17T08:48:33Z

Seems we didn't upload our helm charts to artifact hub, do we have any plan?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-17T12:32:43Z

We only included the chart in the release https://github.com/kubernetes-sigs/kueue/releases/tag/v0.4.0

Other than that, we should look into uploading the chart to registry.k8s.io. I think it might just work if we follow the same process as for images https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-17T12:34:45Z

Opened #990 for that
