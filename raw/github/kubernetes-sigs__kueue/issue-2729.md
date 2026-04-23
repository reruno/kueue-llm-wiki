# Issue #2729: Flaky Test: Pod groups when Single CQ Failed Pod can be replaced in group

**Summary**: Flaky Test: Pod groups when Single CQ Failed Pod can be replaced in group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2729

**Last updated**: 2024-07-31T15:35:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-07-31T05:24:07Z
- **Updated**: 2024-07-31T15:35:44Z
- **Closed**: 2024-07-31T15:35:44Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky Test for  `End To End Suite: kindest/node:v1.27.13: [It] Pod groups when Single CQ Failed Pod can be replaced in group`.

```shell
{Timed out after 5.001s.
Expected
    <v1.PodPhase>: Pending
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 5.001s.
Expected
    <v1.PodPhase>: Pending
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:220 @ 07/29/24 04:13:50.231
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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-31T05:24:32Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-31T06:24:54Z

/assign
