# Issue #8908: [Flaky] failed to delete cluster "kind"

**Summary**: [Flaky] failed to delete cluster "kind"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8908

**Last updated**: 2026-02-16T14:18:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-30T11:47:37Z
- **Updated**: 2026-02-16T14:18:02Z
- **Closed**: 2026-02-16T14:18:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@nerdeveloper](https://github.com/nerdeveloper)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

```
Switched to context "kind-kind".
Deleting cluster "kind" ...

ERROR: failed to delete cluster "kind": failed to delete nodes: command "docker rm -f -v kind-worker kind-control-plane kind-worker2" failed with error: exit status 1

Command Output: kind-control-plane
Error response from daemon: cannot remove container "kind-worker": could not kill container: tried to kill container, but did not receive an exit event
Error response from daemon: cannot remove container "kind-worker2": could not kill container: tried to kill container, but did not receive an exit event
make: *** [Makefile-test.mk:176: run-test-e2e-singlecluster-1.32.11] Error 1
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8893/pull-kueue-test-e2e-main-1-32/2017169874874273792

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

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2026-02-16T03:44:24Z

/assign
