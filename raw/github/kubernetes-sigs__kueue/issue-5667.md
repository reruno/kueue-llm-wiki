# Issue #5667: kueueviz supports Hierarchical Cohorts

**Summary**: kueueviz supports Hierarchical Cohorts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5667

**Last updated**: 2026-03-09T20:05:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@utam0k](https://github.com/utam0k)
- **Created**: 2025-06-17T06:25:55Z
- **Updated**: 2026-03-09T20:05:15Z
- **Closed**: 2026-03-09T20:05:15Z
- **Labels**: `area/dashboard`
- **Assignees**: [@utam0k](https://github.com/utam0k), [@samzong](https://github.com/samzong)
- **Comments**: 11

## Description

Kueueviz shows cohorts, but it's flat. It'd be better to show the hierarchy. If it'll need the design docs, please tell me 🙏

## Discussion

### Comment by [@utam0k](https://github.com/utam0k) — 2025-06-17T06:26:28Z

/cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-17T06:45:16Z

cc @akram @kannon92 wdyt? 

I think maybe we don't need full design,  but some quick mockups would be helpful for discussion

### Comment by [@akram](https://github.com/akram) — 2025-06-17T06:51:18Z

@utam0k that would be a great addition especially now that `CohortTree` is a feature. A quick mockup would be enough to start the discussion, agreed 👍🏼

### Comment by [@utam0k](https://github.com/utam0k) — 2025-06-17T06:55:15Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T08:07:19Z

/kind dashboard

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-18T08:53:46Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T09:01:36Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T09:40:08Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T09:46:15Z

/remove-lifecycle stale

### Comment by [@samzong](https://github.com/samzong) — 2026-03-06T15:53:41Z

/assign I can take it.

### Comment by [@samzong](https://github.com/samzong) — 2026-03-06T15:55:04Z

/assign
