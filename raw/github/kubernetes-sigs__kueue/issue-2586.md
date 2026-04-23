# Issue #2586: Flaky Test: Kueue visibility server when A subject is bound to kueue-batch-admin-role Should return an appropriate error

**Summary**: Flaky Test: Kueue visibility server when A subject is bound to kueue-batch-admin-role Should return an appropriate error

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2586

**Last updated**: 2024-07-16T16:03:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-07-11T16:52:55Z
- **Updated**: 2024-07-16T16:03:29Z
- **Closed**: 2024-07-16T16:03:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The `End To End Suite: kindest/node:v1.30.0: [It] Kueue visibility server when A subject is bound to kueue-batch-admin-role Should return an appropriate error expand_less` failed.

```shell
{Expected
    <v1.StatusReason>: Forbidden
to equal
    <v1.StatusReason>: NotFound failed [FAILED] Expected
    <v1.StatusReason>: Forbidden
to equal
    <v1.StatusReason>: NotFound
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:506 @ 07/11/24 16:47:21.333
}
```

**What you expected to happen**:
Never seen these errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/mkubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2584/pull-kueue-test-e2e-main-1-30/1811439474740039680

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-11T16:53:03Z

/kind flake

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-11T17:17:00Z

cc @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-12T13:55:40Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/directory/pull-kueue-test-e2e-main-1-27/1811394213485481984

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-15T04:34:25Z

/assign
