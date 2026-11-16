# Issue #5322: [TAS] Investigate if `domain.id` for type `leafDomain` can have the full path to the root instead of hostname only

**Summary**: [TAS] Investigate if `domain.id` for type `leafDomain` can have the full path to the root instead of hostname only

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5322

**Last updated**: 2026-11-10T10:08:51Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-05-23T12:00:16Z
- **Updated**: 2026-11-10T10:08:51Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
If the lowest level of topology is node's hostname we have a special logic that changes leaf's domain.id into hostname instead of full path to the root like for other domains https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/tas_flavor_snapshot.go#L147-L149

Investigate if this is indeed needed, or could be cleaned-up so we have more consistency

If cleaned-up add util function that `HasPrefix` that takes two `TopologyDomainID` as input and use it `belongsToRequiredDomain` function
**Why is this needed**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-23T12:00:28Z

cc @mimowo @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-23T14:36:27Z

I support this

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-21T15:26:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T15:29:05Z

+1

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-19T15:55:14Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-19T16:11:35Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-22T12:34:02Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-22T13:28:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-21T14:05:37Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-23T02:40:30Z

/remove-lifecycle rotten

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-12T10:00:23Z

I found a correctness case on current main while investigating this issue.

During TAS node replacement, `belongsToRequiredDomain` uses a raw string-prefix comparison. When the required domain is `b1,rack-a`, a sibling leaf such as `b1,rack-ab,x3` is incorrectly accepted. This can move a replacement Pod outside the required rack.

I have a regression test that fails without a component-boundary-aware comparison and passes with a `TopologyDomainID` `HasPrefix` helper.

I would like to work on this focused comparison fix and its tests. I do not plan to change the representation of all leaf domain IDs in the same PR.

AI disclosure: I used an AI coding assistant to help trace the code path and develop the reproduction, and I verified the behavior and tests locally.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-11-10T10:08:48Z

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
