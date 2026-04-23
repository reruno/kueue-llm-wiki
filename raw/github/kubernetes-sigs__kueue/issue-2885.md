# Issue #2885: [Flaky test] E2E Pod groups when Single CQ Failed Pod can be replaced in group

**Summary**: [Flaky test] E2E Pod groups when Single CQ Failed Pod can be replaced in group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2885

**Last updated**: 2024-08-26T14:27:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-08-23T21:48:26Z
- **Updated**: 2024-08-26T14:27:31Z
- **Closed**: 2024-08-26T14:27:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky E2E Pod groups when Single CQ Failed Pod can be replaced in group test.

```
{Timed out after 5.000s.
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 5.000s.
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:229 @ 08/23/24 21:40:10.786
}
```

**What you expected to happen**:
It never happened.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2884/pull-kueue-test-e2e-main-1-30/1827095865718738944

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-23T23:52:54Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-23T23:53:31Z

/kind flake
