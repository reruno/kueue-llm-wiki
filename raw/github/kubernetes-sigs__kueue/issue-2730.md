# Issue #2730: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Summary**: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2730

**Last updated**: 2024-08-01T09:26:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-07-31T05:26:00Z
- **Updated**: 2024-08-01T09:26:30Z
- **Closed**: 2024-08-01T09:26:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky Test for `End To End Suite: kindest/node:v1.27.13: [It] Pod groups when Single CQ should allow to preempt the lower priority group`.

```shell
{Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 2 failed [FAILED] Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:502 @ 07/29/24 04:14:14.925
}
```

**What you expected to happen**:
It never happened any errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1817773432788488192

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-31T05:26:07Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-31T07:09:58Z

/assign
