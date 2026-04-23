# Issue #1187: Validate workload PodSetUpdates

**Summary**: Validate workload PodSetUpdates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1187

**Last updated**: 2023-10-24T19:23:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-10-09T13:59:44Z
- **Updated**: 2023-10-24T19:23:16Z
- **Closed**: 2023-10-24T19:23:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 5

## Description

**What happened**:

It is possible to set workload PodSetUpdates with invalid values, resulting in errors during workload admission.

**What you expected to happen**:

Fail fast on modifications to `workload.PodSetUpdates` which are performed by external controllers.

Validated things:
- `PodSetUpdates.name` should be a valid pod set name
- `PodSetUpdates.tolerations` should a valid list of tolerations, see https://github.com/kubernetes/kubernetes/blob/57d3cc66050545d7fefb0841e750a0a41df14144/pkg/apis/core/validation/validation.go#L3749
- validate annotations and labels, see: https://github.com/kubernetes/kubernetes/blob/57d3cc66050545d7fefb0841e750a0a41df14144/pkg/apis/core/validation/validation.go#L126

Proposed solution: workload webhook.

Part of  #1145

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-10-09T14:00:15Z

FYI @mwielgus @trasc 
/assign @stuton

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-09T14:00:17Z

@mimowo: GitHub didn't allow me to assign the following users: stuton.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1187#issuecomment-1753072189):

>FYI @mwielgus @trasc 
>/assign @stuton 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2023-10-11T14:47:59Z

FYI @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-11T15:15:17Z

+1

### Comment by [@stuton](https://github.com/stuton) — 2023-10-13T13:14:31Z

/assign
