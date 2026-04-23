# Issue #1369: Flaky job controller integration test

**Summary**: Flaky job controller integration test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1369

**Last updated**: 2023-12-05T01:09:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2023-11-27T11:38:48Z
- **Updated**: 2023-12-05T01:09:02Z
- **Closed**: 2023-12-05T01:09:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Job controller partial admission integration test failed

**What you expected to happen**:
Test to succeed

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1362/pull-kueue-test-integration-main/1729093850112200704

**Anything else we need to know?**:
 The linked PR does not include any changes, neither in integration tests nor job controllers.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-11-27T11:40:39Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-01T01:12:56Z

This flaky test happened: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1252/pull-kueue-test-integration-main/1730371464466534400

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-01T14:48:02Z

@stuton can you take a look?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-01T14:49:01Z

Also failed in periodic tests https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1729168625044033536

### Comment by [@stuton](https://github.com/stuton) — 2023-12-01T14:53:33Z

> @stuton can you take a look?

yes, sure

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-01T15:38:23Z

/assign stuton

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-04T15:00:16Z

/assign trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-04T15:00:27Z

/unassign stuton
