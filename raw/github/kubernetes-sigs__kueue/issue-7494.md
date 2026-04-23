# Issue #7494: Better support for LeaderWorkerSet in Balanced TAS

**Summary**: Better support for LeaderWorkerSet in Balanced TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7494

**Last updated**: 2026-04-20T05:46:54Z

---

## Metadata

- **State**: open
- **Author**: [@pajakd](https://github.com/pajakd)
- **Created**: 2025-11-03T07:26:47Z
- **Updated**: 2026-04-20T05:46:54Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In Balanced Placement algorithm in TAS, there is only basic support for LeaderWorkerSet. The threshold value calculation and pruning logic leaves space for leader on each node, which is suboptimal. 
https://github.com/kubernetes-sigs/kueue/pull/6851#discussion_r2481622745

Also, consider making the pruning reversible to enable fallback to BestFit at later stages of the Balanced algorithm.

**Why is this needed**:
It would result in more balanced placement for LWS.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:38:58Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:55Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:46:51Z

/remove-lifecycle rotten
