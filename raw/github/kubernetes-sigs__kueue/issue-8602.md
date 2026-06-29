# Issue #8602: MultiKueue: a mechanism to give up at some point

**Summary**: MultiKueue: a mechanism to give up at some point

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8602

**Last updated**: 2026-06-16T12:01:28Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-15T10:06:03Z
- **Updated**: 2026-06-16T12:01:28Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to have a mechanism which allows you to handle gracefully situations when the Workload is stuck forever because it can never get admitted on any of the workload clusters.

Some scenarios:
- the workload fits in the manager quota, but will not fit in quota for any of the worker clusters
- there is no worker cluster which requires provisioning enough nodes for the workload

I'm thinking about a time-based solution which would deactivate the workloads after a while, say 1h. The mechanism could be either specific for MultiKueue, but we may also consider something more generic for any AdmissionCheck.

**Why is this needed**:

To avoid workloads getting stuck and holding quota on the management cluster indefinitely.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:06:11Z

cc @yaroslava-serdiuk @mwielgus

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:26Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-17T11:20:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-16T12:01:24Z

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
