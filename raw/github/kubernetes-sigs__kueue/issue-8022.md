# Issue #8022: Make scheduling of the "stuck" pod termination reconciler more explicit

**Summary**: Make scheduling of the "stuck" pod termination reconciler more explicit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8022

**Last updated**: 2026-03-19T10:48:41Z

---

## Metadata

- **State**: open
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2025-12-01T14:55:19Z
- **Updated**: 2026-03-19T10:48:41Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be cleaned**:
As of release v0.15, there is an edge case in the implementation of [TerminatingPodReconciler](https://github.com/kubernetes-sigs/kueue/blob/65a1a41810980a725aab465076de7b8150be908d/pkg/controller/failurerecovery/pod_termination_controller.go) - if the affected node becomes tainted with `node.kubernetes.io/unreachable` after [taint existence check](https://github.com/kubernetes-sigs/kueue/blob/65a1a41810980a725aab465076de7b8150be908d/pkg/controller/failurerecovery/pod_termination_controller.go#L154-L157), the controller relies on the pods running on that node [being marked as not ready](https://github.com/kubernetes/kubernetes/blob/9998041e0ffe0dd3f2abab3b9f95505c4402bf14/pkg/controller/nodelifecycle/node_lifecycle_controller.go#L759) to re-trigger the reconciliation. This behavior could be made more explicit by watching node events or re-queueing after `node-monitor-grace-period`. Alternatively, the code could be restructured/documented/instrumented to make this dependency clear.

**Note:** With the default settings, it's unlikely that this behavior would manifest in practice. This would mean that:
1. The pod's `deletionTimestamp` is set.
2. The pod's `deletionGracePeriodSeconds` (30 seconds) elapsed.
3. The `forcefulTerminationGracePeriod` (60 seconds) elapsed.
4. The node is not unreachable.

For all 4 things to happen at the same time, either:
1. The node became reachable again and the pod shouldn't be forcefully terminated. This might happen if the node is flapping.
2. With non default settings, if the `node_monitor_grace_period` is longer than `deletionGracePeriodSeconds + forcefulTerminationGracePeriod`. Then the total grace period will elapse before the node is marked as unreachable.
3. With default settings, there may be some very obscure case where this happens (if the process is not killed by SIGKILL for example, maybe the kubelet goes down at the exact right moment etc.), but it's harder to consider here. For example:
    1. `deletionTimestamp` is set.
    2. (after 30s) `deletionGracePeriodSeconds` elapses. `SIGKILL` is sent.
    3. (after 11s) The `kubelet` pings the control plane (heartbeat). It did not manage to send the update about the processes of the pod, so from the control plane's perspective they are still terminating. The `kubelet` goes down immediately after the heartbeat.
    4. (after 49s) The `forcefulTerminationGracePeriod` elapses, the reconciler is run and stops at the [taint check which is false](https://github.com/kubernetes-sigs/kueue/blob/65a1a41810980a725aab465076de7b8150be908d/pkg/controller/failurerecovery/pod_termination_controller.go#L154-L157).
    5. (after 1s) `node_monitor_grace_period` elapses, the node is not in a ready state and the `unreachable` taint is added.

**Why is this needed**:
To make the feature more maintainable and make debugging easier in case a user encounters some unexpected behavior.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:43:20Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:19Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T10:48:38Z

/remove-lifecycle stale
