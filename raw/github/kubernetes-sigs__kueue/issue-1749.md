# Issue #1749: Propagate provisioning status of a ProvReq into the Workload status

**Summary**: Propagate provisioning status of a ProvReq into the Workload status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1749

**Last updated**: 2024-04-23T17:40:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-16T19:08:44Z
- **Updated**: 2024-04-23T17:40:42Z
- **Closed**: 2024-04-23T17:40:42Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Propagate the message from the Provisioned=false condition of the ProvisioningRequest into the Workload status

**Why is this needed**:

To improve visibility of why a job is still pending.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-16T19:09:32Z

/assign @PBundyra

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-16T19:09:35Z

@alculquicondor: GitHub didn't allow me to assign the following users: PBundyra.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1749#issuecomment-1949145816):

>/assign @PBundyra 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
