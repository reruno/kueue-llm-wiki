# Issue #4634: TAS: add perf test for scheduling with TAS

**Summary**: TAS: add perf test for scheduling with TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4634

**Last updated**: 2026-02-04T22:04:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-17T08:24:14Z
- **Updated**: 2026-02-04T22:04:33Z
- **Closed**: 2026-02-04T22:04:33Z
- **Labels**: `kind/feature`
- **Assignees**: [@ASverdlov](https://github.com/ASverdlov)
- **Comments**: 10

## Description

**What would you like to be added**:

A performance test for scheduling. 

It could be a folder in separate `test/performance/tas` next to `test/performance/scheduler` with a dedicated CI job.

One approach is to make it analogous to https://github.com/kubernetes-sigs/kueue/tree/main/test/performance/scheduler. The difference is that it will need to have nodes grouped into topology. I would like to have 3 levels: nodes, racks, blocks.

The number of each domains is parametrized, eg. 2 blocks, each block has 10 racks, each rack is 64 nodes. This gives 64*10*2=1280 nodes by default. However, the parameters can be yet tuned and discussed as we see the running times.

**Why is this needed**:

To collect data about performance of TAS. This can drive decisions about future performance improvements.

This was suggested in https://github.com/kubernetes-sigs/kueue/pull/4591#discussion_r1998155126

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T08:24:35Z

cc @tenzen-y @PBundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-17T09:03:59Z

I like this a lot. Maybe we could also assigns workloads randomly to the nodes, to test some of the functionalities? Ideally, workloads sizes should be selected based on some configurable distribution, to favor both very small and hero jobs

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-15T09:39:19Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-16T13:35:22Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-14T14:25:37Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-15T02:03:25Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-14T02:14:09Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-16T08:42:47Z

/remove-lifecycle-stale

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-01-13T17:00:14Z

/remove-lifecycle stale

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-01-13T17:03:49Z

I'd like to work on this
/assign

Maybe we can extend the `test/performance/scheduler` to handle TAS test cases as well? Otherwise, seems like there'll be lots of code duplication.

Let me try to come up with something working, and we can iterate from there.
