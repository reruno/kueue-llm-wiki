# Issue #1027: [Flaky] Job controller interacting with scheduler Should unsuspend job iff localQueue is in the same namespace

**Summary**: [Flaky] Job controller interacting with scheduler Should unsuspend job iff localQueue is in the same namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1027

**Last updated**: 2023-08-08T21:59:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-31T13:27:07Z
- **Updated**: 2023-08-08T21:59:51Z
- **Closed**: 2023-08-08T21:59:51Z
- **Labels**: `kind/bug`
- **Assignees**: [@achernevskii](https://github.com/achernevskii)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The integration test `Job controller interacting with scheduler Should unsuspend job iff localQueue is in the same namespace` failed.

Error was:

```
resourceflavors.kueue.x-k8s.io \"spot-untainted\" already exists
```

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1025/pull-kueue-test-integration-main/1686002784710692864

**Anything else we need to know?**:

This is probably a similar cause as https://github.com/kubernetes-sigs/kueue/pull/1018

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-08-03T20:29:12Z

/assign
