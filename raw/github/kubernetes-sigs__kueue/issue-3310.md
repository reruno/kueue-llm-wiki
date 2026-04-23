# Issue #3310: [Flaky e2e test] Stateful set integration when Single CQ should admit group that fits

**Summary**: [Flaky e2e test] Stateful set integration when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3310

**Last updated**: 2024-10-29T07:44:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-10-24T16:10:10Z
- **Updated**: 2024-10-29T07:44:56Z
- **Closed**: 2024-10-29T07:44:56Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End Suite: kindest/node:v1.28.9: [It] Stateful set integration when Single CQ should admit group that fits expand_less | 18s

```
{Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc0006e22b0>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    } failed [FAILED] Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc0006e22b0>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:130 @ 10/24/24 16:04:52.823
}

```

**What you expected to happen**:
no flakes

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3305/pull-kueue-test-e2e-main-1-28/1849479995282427904

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-28T18:33:51Z

/assign
