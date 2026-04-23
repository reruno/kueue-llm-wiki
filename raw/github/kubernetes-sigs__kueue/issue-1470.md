# Issue #1470: Add dependencies/sbom section to SECURITY-INSIGHTS.yml

**Summary**: Add dependencies/sbom section to SECURITY-INSIGHTS.yml

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1470

**Last updated**: 2024-06-21T18:54:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@psschwei](https://github.com/psschwei)
- **Created**: 2023-12-15T21:11:14Z
- **Updated**: 2024-06-21T18:54:56Z
- **Closed**: 2024-06-21T18:54:56Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`, `sig/release`
- **Assignees**: [@mwysokin](https://github.com/mwysokin)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting clean up requests -->

`#SecuritySlam`

**What would you like to be cleaned**:

When the SECURITY-INSIGHTS.yml file was initially created in #1469, the dependencies/sbom section was omitted, as the project was not creating sboms at that time. Once sboms are being created, the SECURITY-INSIGHTS.yml file should be updated to include this section.

**Why is this needed**:

Adding this section will improve the project's score on the CLOMonitor site.

## Discussion

### Comment by [@psschwei](https://github.com/psschwei) — 2023-12-15T21:14:50Z

/sig release

### Comment by [@psschwei](https://github.com/psschwei) — 2023-12-15T22:50:01Z

xref #1467

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-14T23:07:51Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-15T02:39:01Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-13T03:17:53Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T16:50:33Z

/remove-lifecycle stale
/help

see also: https://github.com/ossf/security-insights-spec/blob/main/specification.md#dependencies

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-13T16:50:35Z

@tenzen-y: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1470):

>/remove-lifecycle stale
>/help
>
>see also: https://github.com/ossf/security-insights-spec/blob/main/specification.md#dependencies


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T16:50:55Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-13T16:50:58Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1470):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-06-19T10:53:45Z

Hi Everyone!

Please excuse my ignorance as I'm completely new to the project and I might not understand fully the scope for this task 🙇 
Is there anything else that needs to be done other than #2443 since #1467 has been completed. The necessary artifact is present on the release page https://github.com/kubernetes-sigs/kueue/releases/tag/v0.7.0.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-06-21T15:31:50Z

/assign
