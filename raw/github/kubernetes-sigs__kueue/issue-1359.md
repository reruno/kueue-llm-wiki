# Issue #1359: Add integration test to show that Job continues when ProvisioningRequest is deleted

**Summary**: Add integration test to show that Job continues when ProvisioningRequest is deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1359

**Last updated**: 2023-12-15T15:52:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-11-22T16:22:30Z
- **Updated**: 2023-12-15T15:52:40Z
- **Closed**: 2023-12-15T15:52:40Z
- **Labels**: `good first issue`, `help wanted`, `triage/accepted`
- **Assignees**: [@B1F030](https://github.com/B1F030)
- **Comments**: 5

## Description

We need to ensure this scenario is covered. It is experimentally verified to be the case, but we need to prevent regressions here.

The ProvisioningRequest can be deleted, and the job is able to run because Cluster Autoscaler does not collect nodes with bound pods.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-11-22T16:23:12Z

cc @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-22T16:27:53Z

/triage accepted

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-22T16:28:04Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-11-22T16:28:06Z

@alculquicondor: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1359):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-23T09:52:10Z

/assign
I'm glad to help. Planning to do this after [KEP-1224](https://github.com/kubernetes-sigs/kueue/pull/1331).
