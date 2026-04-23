# Issue #1619: Add the possibility to add custom annotations to manager pods via helm chart

**Summary**: Add the possibility to add custom annotations to manager pods via helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1619

**Last updated**: 2024-04-24T11:58:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2024-01-19T11:50:46Z
- **Updated**: 2024-04-24T11:58:11Z
- **Closed**: 2024-04-24T11:58:11Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: [@tozastation](https://github.com/tozastation)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to be able to add additional annotations to the pod via the helm chart

**Why is this needed**:

In order to be able to enable automatic scraping via prometheus (without the CRDs) additional annotations are needed:

```
        prometheus.io/path: /metrics
        prometheus.io/port: '8080'
        prometheus.io/scrape: 'true'
```

Could be a potential fix for #663 as well (because port 8080 is the unprotected port for metrics)

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-18T12:18:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-19T06:09:57Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-19T06:10:39Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-19T06:10:41Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1619):

>/good-first-issue
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tozastation](https://github.com/tozastation) — 2024-04-22T12:04:36Z

/assign
