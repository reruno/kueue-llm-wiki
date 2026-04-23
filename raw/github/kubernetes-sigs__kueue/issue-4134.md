# Issue #4134: Differentiate usage by previous podsets and current podsets in messages presented to user

**Summary**: Differentiate usage by previous podsets and current podsets in messages presented to user

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4134

**Last updated**: 2025-10-16T10:36:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-02-03T14:13:04Z
- **Updated**: 2025-10-16T10:36:05Z
- **Closed**: 2025-10-16T10:36:05Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@iomarsayed](https://github.com/iomarsayed)
- **Comments**: 9

## Description

**What would you like to be cleaned**:
During flavor assignment, we pass assigned podset usage - `assignmentUsage[fr]` - and current podset usage -`val` - to fitsResourceQuota - [code](https://github.com/kubernetes-sigs/kueue/blob/14e2ca76af24ac576bb21808dd2538971de6ced3/pkg/scheduler/flavorassigner/flavorassigner.go#L475). We may consider separating these for logging purposes. Note the confusing condition message in https://github.com/kubernetes-sigs/kueue/issues/3909#issue-2758429752: 

```
couldn't assign flavors to pod set master
...
insufficient quota for nvidia.com/gpu in flavor single-node-h100, request > maximum capacity (24 > 16)
```
While this podset only requests 8 GPUs.

**Why is this needed**:
Misleading messages presented to user

/cc @mimowo

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T23:04:09Z

+1

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-05T23:19:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:04:42Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T07:02:35Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-03T07:04:34Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-08T12:56:22Z

/remove-lifecycle rotten

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-09-30T13:15:20Z

/assign

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-08T07:20:54Z

@gabesaba I have reproduced the scenario similar to what's reported in here:
https://github.com/kubernetes-sigs/kueue/issues/3909#issue-2758429752

Things were a bit confusing so I want to make sure I am understanding correctly the following:
1. The issue reports that preemption doesn't happen, while it is not reported here. I reviewed actual logs to discover that preemption is working as expected. so there is nothing to fix other than misleading log messages.
2. We need to modify the messages, such that to output pod-set quota and not the total workload quota, is that correct?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-08T08:08:50Z

Correct, the scope is just to fix the log message. The other bug is out of scope (and not reproducible?)

I would suggest presenting both quantities: the podset total, and the workload total, something like:

```
insufficient quota for nvidia.com/gpu in flavor single-node-h100, previous requests (16) + current podset request (8)  > maximum capacity (16)
```
