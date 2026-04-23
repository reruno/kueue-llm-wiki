# Issue #5175: Use replacements instead of vars

**Summary**: Use replacements instead of vars

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5175

**Last updated**: 2026-02-09T09:35:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-05-06T14:25:31Z
- **Updated**: 2026-02-09T09:35:26Z
- **Closed**: 2026-02-09T09:35:26Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@TapanManu](https://github.com/TapanManu)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

When running `kustomize build` with CertManager enabled, we see the following warning:

```
# Warning: 'vars' is deprecated. Please use 'replacements' instead. [EXPERIMENTAL] Run 'kustomize edit fix' to update your Kustomization automatically.
```

As suggested we should use 'replacements' instead.

**Why is this needed**:

To avoid using a deprecated feature, and as mentioned [here](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/vars/), it will not be included in the kustomize.config.k8s.io/v1 Kustomization API.

**How to reproduce it (as minimally and precisely as possible)**:

```
make kustomize
./bin/kustomize build ./test/e2e/config/certmanager
```

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T15:04:39Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-04T15:05:39Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T16:02:06Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-02T17:07:10Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-31T17:42:37Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-31T23:39:38Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-31T23:40:03Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-31T23:40:05Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5175):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-01T09:47:00Z

Hi, I would like to work on this issue, can someone assign this issue to me ?
@mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-01T11:21:38Z

> Hi, I would like to work on this issue, can someone assign this issue to me ?
@mbobrovskyi

Thank you 🙏

/assign @TapanManu

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-07T09:52:41Z

@mbobrovskyi I have opened the [PR](https://github.com/kubernetes-sigs/kueue/pull/9047) as a fix for the same issue, could you please have a look when you are available ? Feel free to provide any feedback.
