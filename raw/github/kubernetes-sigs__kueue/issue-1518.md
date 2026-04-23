# Issue #1518: Verify shcellscript by shellcheck

**Summary**: Verify shcellscript by shellcheck

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1518

**Last updated**: 2024-03-10T10:21:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-26T08:05:12Z
- **Updated**: 2024-03-10T10:21:28Z
- **Closed**: 2024-03-09T11:23:46Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@Vandit1604](https://github.com/Vandit1604)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
It would be better to verify all shell scripts by the [spellcheck](https://github.com/koalaman/shellcheck) every PR.

**Why is this needed**:
We should have more stable shell scripts.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T08:05:25Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-26T08:05:27Z

@tenzen-y: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1518):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@jaydee029](https://github.com/jaydee029) — 2023-12-26T09:45:12Z

Hi, I would like to work on this, @tenzen-y 
do we create a ci workflow for this .

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T09:55:52Z

@jaydee029 No, we don't. We need to add a Make target like https://github.com/kubernetes-sigs/kueue/blob/b83b2448fbfb8ad263724ee53277081955d2735a/Makefile#L189-L191, then we can call the target in the Make verify target: https://github.com/kubernetes-sigs/kueue/blob/b83b2448fbfb8ad263724ee53277081955d2735a/Makefile#L194

### Comment by [@jaydee029](https://github.com/jaydee029) — 2023-12-26T09:57:12Z

okay , sure

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T09:58:46Z

> okay , sure

@jaydee029 You can take this issue by the comment as `/assign`

### Comment by [@jaydee029](https://github.com/jaydee029) — 2023-12-26T10:01:33Z

/assign

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-01-07T00:08:04Z

Hey @jaydee029, Are you still working on this?
If not, I would like to take a stab on it.

### Comment by [@jaydee029](https://github.com/jaydee029) — 2024-01-07T04:18:11Z

Go for it

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-01-08T22:47:22Z

/assign

### Comment by [@mayens](https://github.com/mayens) — 2024-01-21T21:49:16Z

Hi @Vandit1604 
Are you still working on it? If not I'm interested
Thanks

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-03-10T10:21:27Z

Hey @mayens , 
I'm working on this.
Thanks
