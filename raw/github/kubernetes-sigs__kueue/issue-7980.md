# Issue #7980: release-0.14: Flaky Integration Test: JobSet controller with TopologyAwareScheduling should admit workload which fits in a required topology domain

**Summary**: release-0.14: Flaky Integration Test: JobSet controller with TopologyAwareScheduling should admit workload which fits in a required topology domain

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7980

**Last updated**: 2025-11-28T08:02:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-11-28T02:29:21Z
- **Updated**: 2025-11-28T08:02:23Z
- **Closed**: 2025-11-28T08:02:23Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

- `JobSet Controller Suite: [It] JobSet controller with TopologyAwareScheduling should admit workload which fits in a required topology domain`

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:376 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:376 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go:1276 @ 11/27/25 16:05:24.335
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-14/1994072299472424960

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T02:29:29Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T07:31:02Z

/assign
