# Issue #3147: [flaky]  End To End Suite: kindest/node:v1.29.4: [It] Pod groups when Single CQ Failed Pod can be replaced in group expand_less

**Summary**: [flaky]  End To End Suite: kindest/node:v1.29.4: [It] Pod groups when Single CQ Failed Pod can be replaced in group expand_less

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3147

**Last updated**: 2024-09-30T12:42:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-09-26T13:32:47Z
- **Updated**: 2024-09-30T12:42:11Z
- **Closed**: 2024-09-30T12:42:11Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3145/pull-kueue-test-e2e-main-1-29/1839287537244311552

```
End To End Suite: kindest/node:v1.29.4: [It] Pod groups when Single CQ Failed Pod can be replaced in group expand_less	8s
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:258 with:
NotFoundError expects an error failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:258 with:
NotFoundError expects an error
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:259 @ 09/26/24 13:05:20.779
}
```
**What you expected to happen**:

Run successfully. 

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-26T14:03:47Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-26T14:46:26Z

/assign
