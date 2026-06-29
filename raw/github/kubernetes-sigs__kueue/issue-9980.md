# Issue #9980: Include real queue position in the scheduling cycle debug logs and improve corresponding metrics

**Summary**: Include real queue position in the scheduling cycle debug logs and improve corresponding metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9980

**Last updated**: 2026-06-16T13:06:28Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-03-18T12:52:50Z
- **Updated**: 2026-06-16T13:06:28Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What would you like to be added**:

Information how deep the scheduler was able to get into Kueue. That could be proxied by amount of inadmissible workloads form the given CQ.

Also consider creating a gauge metrics that explains how many workloads were processed before readmission is triggered for a CQ. 

**Why is this needed**:

It is hard to debug how deep the scheduler goes into CQ and why some workloads are not being reached. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-16T13:06:25Z

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
