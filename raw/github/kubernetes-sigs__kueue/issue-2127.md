# Issue #2127: Concurrency issues with the LocalQueue controller

**Summary**: Concurrency issues with the LocalQueue controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2127

**Last updated**: 2024-05-04T11:23:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@googs1025](https://github.com/googs1025)
- **Created**: 2024-05-04T11:15:36Z
- **Updated**: 2024-05-04T11:23:43Z
- **Closed**: 2024-05-04T11:23:43Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/queue/local_queue.go#L52

Does LocalQueue need to be locked to control concurrency?

```go
func (q *LocalQueue) update(apiQueue *kueue.LocalQueue) {
	q.ClusterQueue = string(apiQueue.Spec.ClusterQueue)
}

func (q *LocalQueue) AddOrUpdate(info *workload.Info) {
	key := workload.Key(info.Obj)
	q.items[key] = info
}

```

I think that in a controller pattern, we should use locks to control concurrency.
If necessary, I will submit a pull request to make the modifications. If not needed, I will close this issue.

## Discussion

### Comment by [@googs1025](https://github.com/googs1025) — 2024-05-04T11:22:33Z

I noticed there is a method called AddOrUpdateWorkloadWithoutLock, and I would like to understand why it doesn't require locking. I might not have understood the reasons yet. I would greatly appreciate it if someone could explain it to me. Thanks a lot!
```go
func (m *Manager) AddOrUpdateWorkloadWithoutLock(w *kueue.Workload) bool {
	qKey := workload.QueueKey(w)
	q := m.localQueues[qKey]
	if q == nil {
		return false
	}
	wInfo := workload.NewInfo(w)
	q.AddOrUpdate(wInfo)
	cq := m.clusterQueues[q.ClusterQueue]
	if cq == nil {
		return false
	}
	cq.PushOrUpdate(wInfo)
	m.reportPendingWorkloads(q.ClusterQueue, cq)
	m.Broadcast()
	return true
}

```
