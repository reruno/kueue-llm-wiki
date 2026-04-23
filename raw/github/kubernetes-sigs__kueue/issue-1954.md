# Issue #1954: Does ClusterQueueFromLocalQueue need lock?

**Summary**: Does ClusterQueueFromLocalQueue need lock?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1954

**Last updated**: 2024-04-15T08:05:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lowang-bh](https://github.com/lowang-bh)
- **Created**: 2024-04-06T04:42:14Z
- **Updated**: 2024-04-15T08:05:00Z
- **Closed**: 2024-04-12T15:21:21Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

As code shows, it does not lock and unlock when calling `ClusterQueueFromLocalQueue`.

```go
func (m *Manager) ClusterQueueFromLocalQueue(lqName string) (string, error) {
	if lq, ok := m.localQueues[lqName]; ok {
		return lq.ClusterQueue, nil
	}
	return "", errQueueDoesNotExist
}
```
**What you expected to happen**:
May be it need to lock first.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): master branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-04-11T14:51:36Z

In my opinion yes, but maybe @PBundyra knows more about the subject, also it can help to merge the functionality with the one of `func (m *Manager) ClusterQueueForWorkload(wl *kueue.Workload) (string, bool) `.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-04-15T08:05:00Z

Thank you for catching that. Indeed it should lock first.
