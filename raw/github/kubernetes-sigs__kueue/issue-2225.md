# Issue #2225: Faky test: Pod groups when Single CQ should admit group that fits

**Summary**: Faky test: Pod groups when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2225

**Last updated**: 2024-05-21T09:00:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-17T19:07:03Z
- **Updated**: 2024-05-21T09:00:48Z
- **Closed**: 2024-05-21T09:00:48Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
Failed `End To End Suite: kindest/node:v1.28.0: [It] Pod groups when Single CQ should admit group that fits`

```shell
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:133 with:
NotFoundError expects an error failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:133 with:
NotFoundError expects an error
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:134 @ 05/17/24 17:17:58.033
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2221/pull-kueue-test-e2e-main-1-28/1791517344896389120

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-17T19:20:25Z

It also happened in the periodic tests https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1787143043464302592

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-20T10:09:36Z

/assign
