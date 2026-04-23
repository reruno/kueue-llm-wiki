# Issue #3473: Add documentation for ProvisioningRequestConfig retryStrategy

**Summary**: Add documentation for ProvisioningRequestConfig retryStrategy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3473

**Last updated**: 2025-05-06T13:26:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-06T10:03:38Z
- **Updated**: 2025-05-06T13:26:38Z
- **Closed**: 2025-05-06T13:26:37Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Add documentation for ProvisioningRequestConfig retryStrategy

**Why is this needed**:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T18:19:05Z

/kind documentation
/remove-kind cleanup

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-07T03:29:10Z

@PBundyra Could we refine this troubleshooting guide state transition diagram as well?

https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_provreq/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T04:05:07Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T06:46:16Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-06T07:19:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T07:27:14Z

/remove-lifecycle stale

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-06T09:28:55Z

It was basically fixed by this PR: https://github.com/kubernetes-sigs/kueue/pull/3774


> [@PBundyra](https://github.com/PBundyra) Could we refine this troubleshooting guide state transition diagram as well?
> 
> https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_provreq/

But will also need to work on this diagram

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-06T09:30:57Z

Although the diagram is still valid, so I'll close this issue. I propose adding another diagram not to the troubleshooting page, but to concepts/provisioning controller page, that shows how the admission cycle, and retries work

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-06T13:26:37Z

> Although the diagram is still valid, so I'll close this issue. I propose adding another diagram not to the troubleshooting page, but to concepts/provisioning controller page, that shows how the admission cycle, and retries work

Create a separate issue describing exactly that: https://github.com/kubernetes-sigs/kueue/issues/5172
