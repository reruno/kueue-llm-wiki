# Issue #7874: Document the fair sharing scheduling and preemption algorithm for hierarchical cohorts

**Summary**: Document the fair sharing scheduling and preemption algorithm for hierarchical cohorts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7874

**Last updated**: 2026-04-20T05:47:16Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-25T10:13:19Z
- **Updated**: 2026-04-20T05:47:16Z
- **Closed**: —
- **Labels**: `priority/important-longterm`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 5

## Description

I would like to document the non-trivial algorithms for hierarchical cohorts in the context of fair sharing:
- the scheduling tournament approach https://github.com/kubernetes-sigs/kueue/blob/cc8ac4b53ce740271a7c374692e7209db1b86886/pkg/scheduler/fair_sharing_iterator.go
- the preemption alomst LCA-based approach: https://github.com/kubernetes-sigs/kueue/blob/cc8ac4b53ce740271a7c374692e7209db1b86886/pkg/scheduler/preemption/fairsharing/ordering.go

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:13:40Z

/kind documentation
cc @pajakd @tenzen-y @amy @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:53:41Z

/priority important-longterm

### Comment by [@monabil08](https://github.com/monabil08) — 2026-01-18T13:19:30Z

@mimowo can I take a stab at this one? As I was just working on setting up kueue and hit the limitation

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T14:19:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:47:14Z

/remove-lifecycle stale
