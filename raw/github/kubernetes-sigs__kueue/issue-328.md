# Issue #328: Validate Workload.spec.admission on webhook

**Summary**: Validate Workload.spec.admission on webhook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/328

**Last updated**: 2022-08-19T19:19:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-12T20:26:16Z
- **Updated**: 2022-08-19T19:19:53Z
- **Closed**: 2022-08-19T19:19:52Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 6

## Description

**What would you like to be added**:

The following validations should apply:

- The clusterQueue should be a valid object name.
- The list of podSetFlavors should match the podSets names.
- Each resourceName should be listed in the pod spec, although it might be too cumbersome to validate, so we could ignore it.
- Each flavorName should be a valid object name.

Also validate that, once set, the contents of the admission are immutable, except that it can be set to nil.

**Why is this needed**:

To prevent accidental misuse of this field by administrators.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-12T20:26:23Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-12T20:26:25Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/328):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T08:00:49Z

/assign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T10:13:46Z

I wonder if we should allow parts of podsets to run first when out of resources, then we can release the resources for the left podsets to run. For podgroup pods, we should have a different set of logic.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T10:15:08Z

And this can be configured.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-19T13:34:36Z

For now, we are going with the assumption that the entire Workload is all-or-nothing.
