# Issue #2920: Flaky End To End Suite: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job

**Summary**: Flaky End To End Suite: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2920

**Last updated**: 2024-08-28T15:43:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-08-28T05:05:27Z
- **Updated**: 2024-08-28T15:43:04Z
- **Closed**: 2024-08-28T15:43:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky End to End Test on "End To End Suite: kindest/node:v1.29.4: [It] Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue"

```shell
{Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/visibility_test.go:174 @ 08/27/24 21:24:32.932
}
```

**What you expected to happen**:

Any errors have never been seen.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-29/1828542136862117888

<img width="1016" alt="Screenshot 2024-08-28 at 14 04 41" src="https://github.com/user-attachments/assets/a9bb8bd0-389f-49b5-93ba-831c1a5c2a19">

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-28T05:05:35Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-28T06:08:23Z

/assign
