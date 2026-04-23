# Issue #5338: [AFS] Add e2e baseline test for Admission Fair Sharing

**Summary**: [AFS] Add e2e baseline test for Admission Fair Sharing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5338

**Last updated**: 2025-08-25T11:32:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-05-26T08:56:04Z
- **Updated**: 2025-08-25T11:32:52Z
- **Closed**: 2025-08-25T11:32:52Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add e2e baseline test for Admission Fair Sharing into the `test/e2e/customconfigs`. The scenario could look like this:
- Create 2 LQs pointing to the same CQ
- Saturate quota with workloads coming from lq-a
- Create more workloads from lq-a
- Create a workload from lq-b
- Finish some of running workloads
- Observe workload from lq-b is admitted even it was submitted later than workloads from lq-a

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T09:13:53Z

/remove-kind feature
/kind cleanup

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-24T09:19:59Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-08-25T11:32:52Z

After second consideration I think integration test are perfectly enough. This feature doesn't involve interacting with any external controller (e.g. batch job controller), so there not much value in e2e tests
