# Issue #1379: Confusing QueueingStrategy API description

**Summary**: Confusing QueueingStrategy API description

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1379

**Last updated**: 2024-02-27T13:57:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Created**: 2023-11-29T11:01:09Z
- **Updated**: 2024-02-27T13:57:35Z
- **Closed**: 2024-02-27T13:57:35Z
- **Labels**: `kind/support`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 5

## Description

From API: 
```
type QueueingStrategy string

const (
	// StrictFIFO means that workloads are ordered strictly by creation time.
	// Older workloads that can't be admitted will block admitting newer
	// workloads even if they fit available quota.
	StrictFIFO QueueingStrategy = "StrictFIFO"

	// BestEffortFIFO means that workloads are ordered by creation time,
	// however older workloads that can't be admitted will not block
	// admitting newer workloads that fit existing quota.
	BestEffortFIFO QueueingStrategy = "BestEffortFIFO"
)
```

however in fact we use priority queueing: 
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/queue/cluster_queue_strict_fifo.go#L47

I found it confusing and doesn't correspond to the API description.

## Discussion

### Comment by [@aleksandra-malinowska](https://github.com/aleksandra-malinowska) — 2023-11-29T11:06:01Z

+1, also got confused by this. If we can't change strategy names, maybe sth like this would help?

```
	// StrictFIFO means that workloads of the same priority are ordered strictly by creation time.
	(...)
	// BestEffortFIFO means that workloads of the same priority are ordered by creation time,
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-29T11:18:22Z

We mention priority in this document: https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy
So, I guess that we missed to update the API description.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-11-29T12:04:36Z

If we can't change names, maybe worth introduce the new proper names and depreciate those ones?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-27T13:02:26Z

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

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-02-27T13:57:35Z

The comments were updated in https://github.com/kubernetes-sigs/kueue/pull/1399
