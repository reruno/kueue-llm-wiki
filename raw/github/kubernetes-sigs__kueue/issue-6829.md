# Issue #6829: ElasticJobs: support for ProvisioningRequests

**Summary**: ElasticJobs: support for ProvisioningRequests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6829

**Last updated**: 2026-04-13T11:08:52Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-15T09:02:50Z
- **Updated**: 2026-04-13T11:08:52Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support for Provisioning requests, for example for RayClusters.

Assume scenario that user has a Workload for 5 GPUs backed by a ProvisioningRequest and wants to scale up to 10 GPUs.

Ideally "ProvisioningRequest" in ClusterAutoscaler would provide the semantic for resize.

However, we may just in Kueue consider  creating a new ProvisioningRequest for the 'delta' 5 GPU.

Maybe 

**Why is this needed**:

To support elastic Ray clusters (and other Jobs) in autoscalable environments.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T09:03:17Z

cc @mwysokin @MichalZylinski

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-14T09:14:08Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-13T09:56:42Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T11:06:24Z

/remove-lifecycle rotten
/assign @yaroslava-serdiuk 
I think she is already looking into that

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-13T11:08:50Z

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
