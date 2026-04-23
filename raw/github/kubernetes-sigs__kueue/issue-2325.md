# Issue #2325: Add a hugo template to highlight minimum supported version

**Summary**: Add a hugo template to highlight minimum supported version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2325

**Last updated**: 2024-07-09T14:59:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-29T18:33:22Z
- **Updated**: 2024-07-09T14:59:05Z
- **Closed**: 2024-07-09T14:59:05Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@ivange94](https://github.com/ivange94)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Some reusable block that looks similar to the following:

![image](https://github.com/kubernetes-sigs/kueue/assets/1299064/070e42d8-ffb4-494e-8f62-49d12c3a49ad)

And then use that for every time we mention that a feature is only available in a certain version.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-29T18:33:30Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-29T18:37:05Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2325):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ivange94](https://github.com/ivange94) — 2024-05-30T02:00:50Z

Hi @alculquicondor, I would like to work on this. I'm new to the project and will appreciate some guidance on how to go about this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-30T12:36:50Z

You can probably look at this PR for inspiration https://github.com/kubernetes-sigs/kueue/pull/2006

To see your work locally, you can run `make site-server`

### Comment by [@ivange94](https://github.com/ivange94) — 2024-05-30T14:05:26Z

/assign

### Comment by [@ivange94](https://github.com/ivange94) — 2024-06-03T05:10:53Z

@alculquicondor is there somewhere that we need to use this block right now? To test this I just added it to a random page but didn't commit this change. This is how it looks like. 
<img width="806" alt="Screenshot 2024-06-01 at 6 05 09 PM" src="https://github.com/kubernetes-sigs/kueue/assets/11330494/17c039b4-96d0-4e9a-8ce6-f459c5fc30b4">

It also looks like I didn't configure my git properly so it didn't use my actual email address and the bots say I didn't sign the license agreement. Would it be okay to edit that commit and force push to my branch or should I close the current PR and create a new one?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T15:16:35Z

> It also looks like I didn't configure my git properly so it didn't use my actual email address and the bots say I didn't sign the license agreement. Would it be okay to edit that commit and force push to my branch or should I close the current PR and create a new one?

@ivange94 We're ok with either way.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T15:18:29Z

> @alculquicondor is there somewhere that we need to use this block right now? To test this I just added it to a random page but didn't commit this change. This is how it looks like.

We aim to replace the warnings/notes like the ones below.

https://kueue.sigs.k8s.io/docs/tasks/manage/setup_sequential_admission/#requeuing-strategy
