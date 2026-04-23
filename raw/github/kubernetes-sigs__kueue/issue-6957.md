# Issue #6957: TAS: support hotwap for LeaderWorkerSet (PodSet Group)

**Summary**: TAS: support hotwap for LeaderWorkerSet (PodSet Group)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6957

**Last updated**: 2026-04-21T16:11:37Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-23T11:44:25Z
- **Updated**: 2026-04-21T16:11:37Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/6942#issuecomment-3323479054, the combination of TAS hotswap and LeaderWorkerSet (PodSet Group) probably doesn't work correctly.

**What you expected to happen**:

The TAS hotswap fully support every Topology representation mechanism including PodSet Group.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T11:45:00Z

cc @pajakd @mimowo @PBundyra

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-23T11:48:59Z

The reason I think it is not supported is that in this call https://github.com/kubernetes-sigs/kueue/blob/b7cd74b0424928f1da26ae150abf1c0ca7e27902/pkg/cache/scheduler/tas_flavor_snapshot.go#L517C37-L517C59
we pass nil as the argument `leaderTasPodSetRequests`

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-23T11:53:10Z

And we don't have a mechanism to search for node replacement "in sync" for both leader and the workers that might have been co-located in the failed node.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T13:29:51Z

> The reason I think it is not supported is that in this call https://github.com/kubernetes-sigs/kueue/blob/b7cd74b0424928f1da26ae150abf1c0ca7e27902/pkg/cache/scheduler/tas_flavor_snapshot.go#L517C37-L517C59
we pass nil as the argument leaderTasPodSetRequests

> And we don't have a mechanism to search for node replacement "in sync" for both leader and the workers that might have been co-located in the failed node.

Thank you for expanding that.
So, if we want to support this feature, we need to implement any mechanism to tas_flavor_snapthot, right? I guess that we might need to refactor data structure a bit to corresponding to leader and worker.

As your expectation, will it take a longer time to implement that?
If yes, we might need to mention the limitation for Hotswap and LeaderWorkerSet in documentations for v0.14.0 release.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T13:44:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-21T14:33:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T15:54:10Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-21T16:06:36Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-21T16:11:35Z

/remove-lifecycle stale
