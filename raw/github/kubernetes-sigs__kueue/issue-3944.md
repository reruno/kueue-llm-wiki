# Issue #3944: Add 1.32 testing for presubmit/periodics jobs

**Summary**: Add 1.32 testing for presubmit/periodics jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3944

**Last updated**: 2025-01-13T09:22:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-01-08T19:53:19Z
- **Updated**: 2025-01-13T09:22:34Z
- **Closed**: 2025-01-13T09:22:34Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@bobsongplus](https://github.com/bobsongplus), [@Vinaychinnu](https://github.com/Vinaychinnu)
- **Comments**: 4

## Description

1.32 has been released and we should run our e2e tests against it.

https://github.com/kubernetes/test-infra/tree/master/config/jobs/kubernetes-sigs/kueue needs to have a 1.32 job.

/good-first-issue
/help

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-08T19:53:21Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3944):

>1.32 has been released and we should run our e2e tests against it.
>
>https://github.com/kubernetes/test-infra/tree/master/config/jobs/kubernetes-sigs/kueue needs to have a 1.32 job.
>
>/good-first-issue
>/help
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-08T20:24:30Z

/kind cleanup

### Comment by [@Vinaychinnu](https://github.com/Vinaychinnu) — 2025-01-09T05:23:40Z

/assign

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-13T08:37:44Z

/assign
