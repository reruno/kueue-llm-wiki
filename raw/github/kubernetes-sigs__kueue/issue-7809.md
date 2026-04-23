# Issue #7809: Use ReserveQuotaAt/AdmittedAt instead of ReserveQuota/Admitted in unit tests.

**Summary**: Use ReserveQuotaAt/AdmittedAt instead of ReserveQuota/Admitted in unit tests.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7809

**Last updated**: 2025-12-29T09:14:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-11-21T12:02:30Z
- **Updated**: 2025-12-29T09:14:37Z
- **Closed**: 2025-12-29T09:14:37Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

/good-first-issue

**What would you like to be cleaned**:

We already had a lot of issues with like https://github.com/kubernetes-sigs/kueue/issues/7803. The problem is that many tests are still using the old ReserveQuota and Admitted wrappers instead of ReserveQuotaAt and AdmittedAt.

**Why is this needed**:

It helps eliminate flaky unit tests.

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-21T12:02:32Z

@mbobrovskyi: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7809):

><!-- Please only use this template for submitting clean up requests -->
>
>/good-first-issue
>
>**What would you like to be cleaned**:
>
>We already had a lot of issues with like https://github.com/kubernetes-sigs/kueue/issues/7803. The problem is that many tests are still using the old ReserveQuota and Admitted wrappers instead of ReserveQuotaAt and AdmittedAt.
>
>**Why is this needed**:
>
>It helps eliminate flaky unit tests.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@rockygeekz](https://github.com/rockygeekz) — 2025-11-21T12:08:01Z

Hi @mbobrovskyi ,

I’d like to work on this issue and can take care of replacing ReserveQuota/Admitted with ReserveQuotaAt/AdmittedAt in the unit tests. Could you please assign this issue to me?

Thank you!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-21T12:14:49Z

/assign @rockygeekz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:03:23Z

/priority @improtant-longterm
/unassign @rockygeekz 
since this has been 1month without update.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T10:03:25Z

@mimowo: The label(s) `priority/@improtant-longterm` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7809#issuecomment-3674393567):

>/priority @improtant-longterm
>/unassign @rockygeekz 
>since this has been 1month without update.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:09:56Z

/priority @important-longterm

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T10:10:00Z

@mimowo: The label(s) `priority/@important-longterm` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7809#issuecomment-3674421792):

>/priority @important-longterm


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:12:38Z

/priority important-longterm

### Comment by [@andrewseif](https://github.com/andrewseif) — 2025-12-21T15:22:08Z

Hi @mimowo 
I would like to work on this ticket since its unassigned 😃

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-22T05:33:37Z

@andrewseif yes, please take a look at it.
