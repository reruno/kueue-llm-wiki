# Issue #3144: [Flaky integration test] RayCluster controller Should reconcile RayClusters

**Summary**: [Flaky integration test] RayCluster controller Should reconcile RayClusters

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3144

**Last updated**: 2024-09-30T07:32:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-09-26T12:32:01Z
- **Updated**: 2024-09-30T07:32:04Z
- **Closed**: 2024-09-30T07:32:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

/kind flake

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky test on pull-kueue-test-integration-main:

RayCluster Controller Suite: [It] RayCluster controller Should reconcile RayClusters

```
{Timed out after 5.001s.
Expected
    <bool>: false
to be true failed [FAILED] Timed out after 5.001s.
Expected
    <bool>: false
to be true
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/raycluster/raycluster_controller_test.go:192 @ 09/26/24 12:00:41.972
}
```

**What you expected to happen**:
No random failure.

**How to reproduce it (as minimally and precisely as possible)**:
Repeat the build: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3143/pull-kueue-test-integration-main/1839271461601153024

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-26T12:54:28Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-26T13:02:39Z

/unassign

### Comment by [@trasc](https://github.com/trasc) — 2024-09-26T13:29:20Z

/assign
