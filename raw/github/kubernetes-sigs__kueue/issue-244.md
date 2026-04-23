# Issue #244: maybe data inconsistent when `UpdateWorkload`

**Summary**: maybe data inconsistent when `UpdateWorkload`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/244

**Last updated**: 2022-05-03T08:00:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-03T05:06:30Z
- **Updated**: 2022-05-03T08:00:02Z
- **Closed**: 2022-05-03T08:00:02Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Some confusing here: https://github.com/kubernetes-sigs/kueue/blob/4ec686fa7dde59579db3eb6ba699831e3bed18ac/pkg/cache/cache.go#L314-L334
Assuming that both oldWl and newWl's `Admission` already set, so when we run `c.cleanupAssumedState(oldWl)`,  we'll remove the oldWl from `assumedWorkloads`,  but we will not add newWl back to the `assumedWorkloads`, it seems inconsistent.
IIRC, we should handle like this:
```
	if newWl.Spec.Admission == nil {
		c.cleanupAssumedState(oldWl)
		return nil
	}
``` 
**What you expected to happen**:

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
