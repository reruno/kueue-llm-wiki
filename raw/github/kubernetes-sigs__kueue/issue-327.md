# Issue #327: Make kueue image multiarch

**Summary**: Make kueue image multiarch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/327

**Last updated**: 2022-09-07T14:38:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-12T16:06:30Z
- **Updated**: 2022-09-07T14:38:41Z
- **Closed**: 2022-09-07T14:38:41Z
- **Labels**: `kind/feature`, `help wanted`, `priority/backlog`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 7

## Description

**What would you like to be added**:

Make kueue image multiarch for x86 and arm

**Why is this needed**:

To be able to run in any environment.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-12T16:06:40Z

/priority backlog
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-12T16:06:41Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/327):

>/priority backlog
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-06T18:15:15Z

@alculquicondor Hi.
I'm interested in this. Does this mean [multi-platform image](https://docs.docker.com/build/buildx/multiplatform-images/)?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T18:32:05Z

Yes :)

You need to find a way to do that from the Makefile and Dockerfile

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-06T19:02:47Z

@alculquicondor Thanks for clarifying. Can I take this?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T19:06:16Z

Yes, just write `/assign` in a comment.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-06T19:07:06Z

/assign
