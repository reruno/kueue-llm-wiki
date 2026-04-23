# Issue #412: Add Job webhook to mark them as suspended on creation

**Summary**: Add Job webhook to mark them as suspended on creation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/412

**Last updated**: 2022-11-24T19:20:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-10-07T11:37:40Z
- **Updated**: 2022-11-24T19:20:06Z
- **Closed**: 2022-11-24T19:20:06Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 3

## Description

**What would you like to be added**:

A webhook for batch/v1.Job that marks them as suspended, respecting the configuration of [`.manageJobsWithoutQueueName`]( https://github.com/kubernetes-sigs/kueue/blob/15ec4631afb3a788c45689f4e7c4305385e51e5f/apis/config/v1alpha2/configuration_types.go#L44)

**Why is this needed**:

To prevent the job controller from creating unauthorized pods, even if temporary.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-07T11:37:46Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-07T11:37:47Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/412):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-09T06:59:36Z

/assign
