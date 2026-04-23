# Issue #690: Set up milestone automatically for new PRs

**Summary**: Set up milestone automatically for new PRs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/690

**Last updated**: 2023-05-31T16:25:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-11T15:58:04Z
- **Updated**: 2023-05-31T16:25:48Z
- **Closed**: 2023-05-31T16:25:48Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Set the milestone v0.4 automatically for PRs in the main branch and v0.3 for the release-0.3 branch.

**Why is this needed**:

Having a milestone has two purposes:
- historical record: being able to tell when a PR was introduced.
- (potentially): block a PR from merging unless it has a milestone, to implement code-freezes later on.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-11T15:58:13Z

Rough instructions https://kubernetes.slack.com/archives/C1TU9EB9S/p1679586290890489

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-25T14:12:11Z

@ArangoGutierrez it looks like something is missing. New PRs aren't getting the tag automatically

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2023-04-25T15:00:19Z

I enabled the PROW side, I guess more is needed on this. let me check what's left, I'll be back here

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-23T19:22:00Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-23T19:22:01Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/690):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-24T12:06:12Z

It seems to be adding a milestone correctly for the `release-0.3` branch, but not `main`.
