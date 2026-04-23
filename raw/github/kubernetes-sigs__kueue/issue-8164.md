# Issue #8164: website: setup dead links checker

**Summary**: website: setup dead links checker

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8164

**Last updated**: 2026-02-12T19:30:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexandear](https://github.com/alexandear)
- **Created**: 2025-12-10T11:29:55Z
- **Updated**: 2026-02-12T19:30:02Z
- **Closed**: 2026-02-12T19:30:02Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@yashnib](https://github.com/yashnib)
- **Comments**: 5

## Description

**What would you like to be cleaned**:

Set up an automated dead-link checker for the website documentation and integrate it into the CI/CD pipeline.

**Why is this needed**:

To prevent regressions like https://github.com/kubernetes-sigs/kueue/issues/7285, where multiple dead links appeared on the website.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-10T13:12:26Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-10T13:12:29Z

@kannon92: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8164):

>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@yashnib](https://github.com/yashnib) — 2025-12-14T03:14:57Z

Hi, I can implement a CI dead-link checker for the website. Please assign this to me. Thanks!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-14T03:56:33Z

/assign @yashnib

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:38:17Z

/priority important-longterm
