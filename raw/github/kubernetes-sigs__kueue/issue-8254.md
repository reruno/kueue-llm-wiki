# Issue #8254: sed: can't read plugin.yaml: No such file or directory

**Summary**: sed: can't read plugin.yaml: No such file or directory

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8254

**Last updated**: 2025-12-16T10:56:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-12-16T06:58:03Z
- **Updated**: 2025-12-16T10:56:18Z
- **Closed**: 2025-12-16T10:56:18Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

I’ve seen this issue more than three times. It looks like a network issue, but it happens quite often:

```
sed: can't read plugin.yaml: No such file or directory
Failed to install helm-unittest
For support, go to https://github.com/helm-unittest/helm-unittest/blob/main/FAQ.md
Error: plugin install hook for "unittest" exited with error
make[2]: *** [Makefile-deps.mk:111: helm] Error 1
make[2]: Leaving directory '/home/prow/go/src/sigs.k8s.io/kueue'
make[1]: *** [Makefile:60: /home/prow/go/src/sigs.k8s.io/kueue/cmd/experimental/kueue-populator/../../../bin/helm] Error 2
make[1]: Leaving directory '/home/prow/go/src/sigs.k8s.io/kueue/cmd/experimental/kueue-populator'
make: *** [Makefile:449: kueue-populator-verify] Error 2
```

**What you expected to happen**:
No issue

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8253/pull-kueue-populator-verify-main/2000820428418846720

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T08:34:26Z

Looks like we are affected by https://github.com/helm-unittest/helm-unittest/issues/790

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-16T10:41:46Z

/remove-kind flake
