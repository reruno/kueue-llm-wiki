# Issue #5161: [Flaky E2E Test]: Deployment should admit workloads after change queue-name if AvailableReplicas = 0

**Summary**: [Flaky E2E Test]: Deployment should admit workloads after change queue-name if AvailableReplicas = 0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5161

**Last updated**: 2025-05-06T06:45:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-05-05T12:23:37Z
- **Updated**: 2025-05-06T06:45:21Z
- **Closed**: 2025-05-06T06:45:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
End To End Suite: kindest/node:v1.30.10: [It] Deployment should admit workloads after change queue-name if AvailableReplicas = 0

```
{Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type QuotaReserved and status False failed [FAILED] Expected
    <[]v1.Condition | len:0, cap:0>: nil
to have condition type QuotaReserved and status False
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/deployment_test.go:168 @ 05/05/25 11:22:26.192
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5160/pull-kueue-test-e2e-main-1-30/1919348839219728384

**Anything else we need to know?**:

/kind flake

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-05T12:57:51Z

/assign
