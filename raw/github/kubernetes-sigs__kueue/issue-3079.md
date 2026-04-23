# Issue #3079: [Flaky integration test] Provisioning when A workload is using a provision admission check Should set the condition rejected when the provision fails

**Summary**: [Flaky integration test] Provisioning when A workload is using a provision admission check Should set the condition rejected when the provision fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3079

**Last updated**: 2024-10-01T16:05:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-17T14:13:26Z
- **Updated**: 2024-10-01T16:05:52Z
- **Closed**: 2024-10-01T16:05:52Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

/kind flake

**What happened**:

An test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3078/pull-kueue-test-integration-main/1836042561878233088

**What you expected to happen**:

No random failure.


**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build.

**Anything else we need to know?**:

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:471 with:
Expected
    <v1beta1.CheckState>: Pending
to equal
    <v1beta1.CheckState>: Rejected failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:471 with:
Expected
    <v1beta1.CheckState>: Pending
to equal
    <v1beta1.CheckState>: Rejected
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:472 @ 09/17/24 14:06:35.18
}
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-17T14:19:54Z

/cc @mbobrovskyi @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-01T06:52:27Z

/assign
