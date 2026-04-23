# Issue #5463: [TAS] Support preemption when searching for node replacement

**Summary**: [TAS] Support preemption when searching for node replacement

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5463

**Last updated**: 2026-03-31T10:19:59Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-06-03T09:50:22Z
- **Updated**: 2026-03-31T10:19:59Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Remove ifs that have been added during #5287 to prevent preemption when searching for node replacement:

- https://github.com/kubernetes-sigs/kueue/pull/5287/files#diff-0870ec2c0ea330a7d087a6ef599905bf9b7164a0dd889d1b00ba17c31a1bfd05R482-R484

- https://github.com/kubernetes-sigs/kueue/pull/5287/files#diff-fb3d6b36d3cd727e1dd2353fb86c0aee0bfaae1c900e0f005ab913620021d551L492-R492

Populate information about nodeToReplace to function
https://github.com/kubernetes-sigs/kueue/pull/5287/files#diff-cd44f6e671ae7fdc7882224c13986f4b1b98e1ea45f65bdbcc9ae185d8e91496R490

Heavily test the changes with unit and integration tests 

**Why is this needed**:
For the feature completeness 

**Completion requirements**:
Relatively few coding changes
Lots of tests

No new API is needed

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T09:53:12Z

@PBundyra 
can you fill in `Why is this needed:`. 

Also, is this something we should consider feature or a bug? If feature, should it have API?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-03T09:56:09Z

/remove-kind feature
/kind bug

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-01T10:39:33Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-01T11:00:26Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-30T11:40:24Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-01T09:35:34Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T09:46:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-31T10:19:56Z

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
