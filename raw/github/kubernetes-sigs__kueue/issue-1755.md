# Issue #1755: Introduce the docsy style Note

**Summary**: Introduce the docsy style Note

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1755

**Last updated**: 2024-07-22T14:50:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-02-19T09:49:53Z
- **Updated**: 2024-07-22T14:50:09Z
- **Closed**: 2024-07-22T14:50:09Z
- **Labels**: `help wanted`, `kind/cleanup`, `kind/documentation`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->
**What would you like to be cleaned**:
It would be better to replace a simple markdown style Note with the docsy style shortcode.

The sample of Docsy style: https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/tasks/setup_sequential_admission.md#enabling-waitforpodsready

**Why is this needed**:
The shortcode could be emphasize the Notes.

/kind documentation

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-16T20:51:03Z

Is the ask to go through all of the documentation and find the cases where we are not using a Docsy alert when it would be useful?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-21T16:43:32Z

> Is the ask to go through all of the documentation and find the cases where we are not using a Docsy alert when it would be useful?

I meant the I would propose to replace the GitHub style Notes with Docsy style once:

GitHub Style: https://github.com/kubernetes-sigs/kueue/blob/0db23a7d8431b25ea77281fc6b7504db247c34dc/site/content/en/docs/installation/_index.md?plain=1#L149-L151

Doccy Style: https://github.com/kubernetes-sigs/kueue/blob/0db23a7d8431b25ea77281fc6b7504db247c34dc/site/content/en/docs/tasks/manage/setup_sequential_admission.md?plain=1#L53-L61

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-21T20:08:32Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-21T20:08:34Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1755):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-19T08:45:56Z

/assign
