# Issue #8958: TAS: support spreading for inference workloads based on LWS

**Summary**: TAS: support spreading for inference workloads based on LWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8958

**Last updated**: 2026-06-03T10:05:00Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-03T08:56:44Z
- **Updated**: 2026-06-03T10:05:00Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We need some form of spreading to be supported by TAS for inference workloads, based on LWS.

We don't need "strict" spreading, just the best effort is enough. The MostFreeCapacity seems to do a good job, and I have prototyped already some idea based on the MostFreeCapacity here, and it seems to work: https://github.com/kubernetes-sigs/kueue/pull/8923

**Why is this needed**:

To better support failure tolerance. Placing all LWS groups on the same pool of nodes is risky for our users.

Imagine LWS with 4 groups, each group is 4 pods. This is 16 Pods, and all of them could fit into one "rack". If the rack fails the entire LWS may fail.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T08:57:04Z

cc @PBundyra @tenzen-y @gabesaba wdyt?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-04T09:04:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-03T10:04:56Z

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
