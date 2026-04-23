# Issue #874: Chart misses settings for securitycontext

**Summary**: Chart misses settings for securitycontext

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/874

**Last updated**: 2023-07-04T11:20:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bh-tt](https://github.com/bh-tt)
- **Created**: 2023-06-19T10:13:13Z
- **Updated**: 2023-07-04T11:20:56Z
- **Closed**: 2023-07-04T11:20:56Z
- **Labels**: `kind/feature`
- **Assignees**: [@bh-tt](https://github.com/bh-tt)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
The chart has a fixed securityContext for the manager, which only sets allowPrivilegeEscalation to false. There are several more hardening settings to apply, like running as a specific user and enforcing a readOnlyRootFilesystem.
**Why is this needed**:
It is best practice to harden pods as much as possible, especially when it comes to controllers
**Completion requirements**:
Support a `.controllerManager.manager.podSecurityContext` and `.controllerManager.manager.securityContext` field whose value is simply inserted into the pod spec. The default can stay the same as now but will be defined in the chart values instead of the template. This allows compatibility with any future additions as well.

## Discussion

### Comment by [@bh-tt](https://github.com/bh-tt) — 2023-06-19T12:02:17Z

I'd be willing to supply a PR of course.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-19T13:06:12Z

Thanks, feel free to assign it to yourself and send a PR

### Comment by [@bh-tt](https://github.com/bh-tt) — 2023-06-19T13:07:24Z

/assign me

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-06-19T13:07:25Z

@bh-tt: GitHub didn't allow me to assign the following users: me.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/874#issuecomment-1597161681):

>/assign me


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@bh-tt](https://github.com/bh-tt) — 2023-06-19T13:07:46Z

/assign @bh-tt

### Comment by [@bh-tt](https://github.com/bh-tt) — 2023-06-20T11:55:36Z

See #878
