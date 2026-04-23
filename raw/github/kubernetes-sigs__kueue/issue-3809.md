# Issue #3809: Add validation to `config.waitForPodsReady`

**Summary**: Add validation to `config.waitForPodsReady`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3809

**Last updated**: 2025-09-08T16:59:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-12-11T10:31:55Z
- **Updated**: 2025-09-08T16:59:30Z
- **Closed**: 2025-09-08T16:59:30Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add validation for WaitForPodsReady that asserts `timeout`, `blockAdmission` and `requeuingStrategy` are defined only if `enable` is set to True

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T10:40:29Z

Hm, not sure about that. What about the use case that an admin has the feature configured and just wants to disable it temporarily and reenable quickly with the same config.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-11T13:07:41Z

We already checked the waitForPodsReady only when the waitForPodsReady is enabled here: https://github.com/kubernetes-sigs/kueue/blob/d85a79b81c906d1d17197f8d560ba11d018223ac/pkg/config/validation.go#L118-L120

So, I was not sure this validation motivation.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-11T14:06:00Z

Do we give any feedback to a user in case they configured the rest of the fields, but forgot to switch the `enable` field?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T14:20:11Z

I don't think we do, maybe we could leave some useful log or use a warning.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-11T14:23:14Z

> maybe we could leave some useful log or use a warning.

+1

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-11T14:40:01Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-12T14:44:37Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T15:01:17Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-12T08:20:59Z

/remove-lifecycle stale

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-12T08:21:55Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-12T08:21:58Z

@PBundyra: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3809):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
