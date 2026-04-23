# Issue #3069: Document ways to avoid users submitting workloads without any requests

**Summary**: Document ways to avoid users submitting workloads without any requests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3069

**Last updated**: 2026-02-12T12:30:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-09-16T14:08:00Z
- **Updated**: 2026-02-12T12:30:03Z
- **Closed**: 2026-02-12T12:30:03Z
- **Labels**: `good first issue`, `help wanted`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We should add a doc to explain how to use ValidationAdmissionPolicy to optionally forbid users from submitting workloads without any requests. 

[This page](https://kueue.sigs.k8s.io/docs/tasks/manage/enforce_job_management/setup_job_admission_policy/) should be updated to mention how one can use VAP to enforce workloads having requests.

**Why is this needed**:

Kueue tracks resource requests by the requests field in the PodTemplate. If one submits a workload without any requests specified, kueue will not report any resources used by this workload.

It would be worth mentioning this in the docs and provide an example to forbid this.
**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-16T14:08:15Z

/remove-kind feature
/kind docs
/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-16T14:08:17Z

@kannon92: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3069):

>/remove-kind feature
>/kind docs
>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-16T14:08:18Z

@kannon92: The label(s) `kind/docs` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3069#issuecomment-2353033563):

>/remove-kind feature
>/kind docs
>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-17T13:25:09Z

/kind documentation

### Comment by [@amitmaurya07](https://github.com/amitmaurya07) — 2024-10-07T03:31:28Z

Hi, I would like to work on this issue. Could you please assign this issue to me?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-07T05:54:04Z

/assign @amitmaurya07

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-14T14:07:47Z

/unassign @amitmaurya07 

Please feel free to assign yourself if you are working on this.

### Comment by [@TapanManu](https://github.com/TapanManu) — 2025-11-30T13:28:57Z

Hi @kannon92, I would like to work on this issue. However, the URL linked in the description appears to be broken/inaccessible (I am getting a 404/Permission Denied error). Could you please update it or provide the correct context? Thanks!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-30T17:47:46Z

Updated the link.
