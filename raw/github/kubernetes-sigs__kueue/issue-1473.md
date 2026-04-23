# Issue #1473: Add in-scope/out-scope subsections to SECURITY-INSIGHTS.yml

**Summary**: Add in-scope/out-scope subsections to SECURITY-INSIGHTS.yml

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1473

**Last updated**: 2024-09-18T15:46:12Z

---

## Metadata

- **State**: open
- **Author**: [@psschwei](https://github.com/psschwei)
- **Created**: 2023-12-15T21:35:58Z
- **Updated**: 2024-09-18T15:46:12Z
- **Closed**: —
- **Labels**: `help wanted`, `kind/cleanup`, `sig/release`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

`#SecuritySlam`

**What would you like to be cleaned**:

When the SECURITY-INSIGHTS.yml file was initially created in https://github.com/kubernetes-sigs/kueue/pull/1469, the in-scope / out-scope subsections of the vulnerability-reporting section were omitted, as it was not entirely clear which of the [OWASP Top 10](https://owasp.org/Top10/) were in/out of scope. Someone with more knowledge of the project should update the SECURITY-INSIGHTS.yml file to include this section.

**Why is this needed**:

Adding this section will improve the project's score on the CLOMonitor site.

/sig release

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-14T22:07:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T22:55:12Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-12T23:13:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T17:00:47Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-11T17:40:32Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T15:46:08Z

/remove-lifecycle stale
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-18T15:46:10Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1473):

>/remove-lifecycle stale
>/help
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
