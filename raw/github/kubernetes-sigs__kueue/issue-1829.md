# Issue #1829: Flaky integration test "RayCluster Job controller interacting with scheduler Should schedule jobs as they fit in their ClusterQueue"

**Summary**: Flaky integration test "RayCluster Job controller interacting with scheduler Should schedule jobs as they fit in their ClusterQueue"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1829

**Last updated**: 2024-03-15T17:32:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-13T09:29:01Z
- **Updated**: 2024-03-15T17:32:26Z
- **Closed**: 2024-03-15T17:32:26Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
/kind flake

**What happened**:

The test failed: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1827/pull-kueue-test-integration-main/1767837105611870208.

**What you expected to happen**:

The test should pass consistently.

**How to reproduce it (as minimally and precisely as possible)**:

Not sure, probably repeat the test.

**Anything else we need to know?**:

It failed on PR not related to this test. Passed after retry.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-13T10:55:10Z

cc @andrewsykim @vicentefb

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T16:30:48Z

This happened: https://github.com/kubernetes-sigs/kueue/pull/1838

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1838/pull-kueue-test-integration-main/1768311737443946496
