# Issue #1335: Support Kuberay v1 CRDs

**Summary**: Support Kuberay v1 CRDs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1335

**Last updated**: 2024-04-02T17:50:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@andrewsykim](https://github.com/andrewsykim)
- **Created**: 2023-11-15T16:03:13Z
- **Updated**: 2024-04-02T17:50:12Z
- **Closed**: 2024-04-02T17:50:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 6

## Description

**What would you like to be added**:

Kuberay released v1.0.0 last week, which introduces v1 version for their CRDs. We should ensure that v1 RayJobs (and soon RayClusters) can be supported with Kueue.

**Why is this needed**:

To support future versions of kuberay APIs

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-15T16:04:47Z

Does kuberay provide conversion webhooks?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-11-15T16:34:24Z

> Does kuberay provide conversion webhooks?

No it does not :(

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-15T16:45:41Z

> > Does kuberay provide conversion webhooks?
> 
> No it does not :(

I see... Maybe, we need to implement a job controller for RayJob v1 separate from v1alpha1 :(

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-07T16:25:18Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-06T17:06:52Z

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

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-06T17:32:09Z

/remove-lifecycle stale
