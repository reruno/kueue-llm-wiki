# Issue #2437: Deprecate the `retryDelayMinutes` from the AdmissionCheck API

**Summary**: Deprecate the `retryDelayMinutes` from the AdmissionCheck API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2437

**Last updated**: 2024-10-09T10:50:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-18T12:25:09Z
- **Updated**: 2024-10-09T10:50:24Z
- **Closed**: 2024-10-09T10:50:24Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Deprecate the `retryDelayMinutes` from the AdmissionCheck API

**Why is this needed**:
It is not used anywhere in the codebase

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-16T13:15:36Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-16T13:32:58Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-17T13:31:01Z

I'm wondering if we can provide the v1beta2 AdmissionCheck API since we can easily provide the conversion webhooks between v1beta1 and v1beta2 AdmissionChecks.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-07T07:27:17Z

/assign
