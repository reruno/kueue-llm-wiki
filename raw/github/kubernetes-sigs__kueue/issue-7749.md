# Issue #7749: Documentation for reclaimWithinCohort for Fair Sharing is misleading

**Summary**: Documentation for reclaimWithinCohort for Fair Sharing is misleading

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7749

**Last updated**: 2026-04-10T10:18:19Z

---

## Metadata

- **State**: open
- **Author**: [@pajakd](https://github.com/pajakd)
- **Created**: 2025-11-19T08:03:39Z
- **Updated**: 2026-04-10T10:18:19Z
- **Closed**: —
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption under "reclaimWithinCohort" we write: `Any: if the pending Workload fits within the nominal quota of its ClusterQueue, preempt any Workload in the cohort, irrespective of priority.`

This is not correct in Fair Sharing because "canPreemptWhileBorrowing" allows to preempt even if the workload does not fit within the nominal quota.

https://github.com/kubernetes-sigs/kueue/blob/3e422174db7c555ba4e9a5dbe17b3391744420cc/pkg/scheduler/flavorassigner/flavorassigner.go#L948-L959

**Why is this needed**:

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-17T08:14:10Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T08:20:24Z

/remove-lifecycle stale

### Comment by [@sivaramsingana](https://github.com/sivaramsingana) — 2026-04-07T09:13:46Z

Hi , I would like to help fix the misleading `reclaimWithinCohort`. Could you suggest replacement paragraphs for the `reclaimWithinCohort`

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-07T09:37:29Z

cc @pajakd

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-10T10:18:16Z

/remove-kind cleanup
/kind documentation
