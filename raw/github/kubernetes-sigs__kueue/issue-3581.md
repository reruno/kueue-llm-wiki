# Issue #3581: [Flaky multikueue e2e] MultiKueue when Creating a multikueue admission check Should run a job on worker if admitted

**Summary**: [Flaky multikueue e2e] MultiKueue when Creating a multikueue admission check Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3581

**Last updated**: 2024-12-04T10:19:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-11-18T14:29:53Z
- **Updated**: 2024-12-04T10:19:03Z
- **Closed**: 2024-12-04T10:19:03Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End MultiKueue Suite: kindest/node:v1.30.0: [It] MultiKueue when Creating a multikueue admission check Should run a job on worker if admitted

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:231 with:
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:231 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:232 @ 11/18/24 14:17:15.278
}
```

**What you expected to happen**:
No random failures

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3580/pull-kueue-test-multikueue-e2e-release-0-9/1858512622475808768

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T10:58:49Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3708/pull-kueue-test-multikueue-e2e-main/1863892287004610560

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T11:05:53Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T11:06:17Z

/assign @IrvingMg
