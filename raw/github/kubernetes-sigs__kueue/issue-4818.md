# Issue #4818: Reduce Verbosity of Scheduler Unit Tests

**Summary**: Reduce Verbosity of Scheduler Unit Tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4818

**Last updated**: 2025-08-13T18:15:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-28T13:43:20Z
- **Updated**: 2025-08-13T18:15:09Z
- **Closed**: 2025-08-13T18:15:09Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

**What would you like to be cleaned**:
Test definition of https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler_test.go is super verbose. Refactor/cleanup to make these more expressive with less code. At the very least, we should get rid of having to define LocalQueues, but I imagine that there are other low-hanging fruit.

See https://github.com/kubernetes-sigs/kueue/pull/4695 for inspiration. Additionally, use judgement to see if there are other ways to improve.

**Why is this needed**:
New tests are hard to write, and existing tests are painful to read

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-05-13T08:19:35Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-11T09:03:46Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T09:05:30Z

/remove-lifecycle stale
What is the status @IrvingMg ?

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-08-11T10:49:13Z

> What is the status [@IrvingMg](https://github.com/IrvingMg) ?

I haven't had the capacity to work on this yet, but I can take it on now.
