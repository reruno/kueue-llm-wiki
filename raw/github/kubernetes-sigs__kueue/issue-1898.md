# Issue #1898: Flaky E2E test for pod groups

**Summary**: Flaky E2E test for pod groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1898

**Last updated**: 2024-03-25T22:23:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-25T17:40:51Z
- **Updated**: 2024-03-25T22:23:55Z
- **Closed**: 2024-03-25T22:23:55Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

/kind flake

It seems that sometimes there is a lingering Pod with a finalizer.

```
Pod groups when Single CQ should allow to schedule a group of diverse pods

{Timed out after 30.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:300 with:
Expected
    <nil>: nil
to be a NotFound error failed [FAILED] Timed out after 30.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:300 with:
Expected
    <nil>: nil
to be a NotFound error
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:304 @ 03/25/24 17:25:47.542
}
```

**What you expected to happen**:

No flakiness

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1888/pull-kueue-test-e2e-main-1-29/1772312509823324160

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
