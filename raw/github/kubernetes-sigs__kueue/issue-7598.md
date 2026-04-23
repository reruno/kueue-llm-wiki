# Issue #7598: Add option to enable fair-sharing at the root cohort level

**Summary**: Add option to enable fair-sharing at the root cohort level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7598

**Last updated**: 2026-04-18T11:15:58Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-11-10T18:36:02Z
- **Updated**: 2026-04-18T11:15:58Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add an option to enable fair sharing at the (root-) cohort level (unless it is possible to extend it to non-root cohorts as well). 

**Why is this needed**:
Today, this option is only available at the cluster level in the Kueue controller config, which means all the cohorts in the cluster are enabled for fair-sharing and there is no control to disable for specific cohorts. There are use cases where we do not want any fair sharing preemptions to happen when different clusterqueues and cohorts are borrowing resources.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:35:35Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:55Z

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
