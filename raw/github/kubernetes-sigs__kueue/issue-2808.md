# Issue #2808: [Flaky test] JobSet controller when basic setup Should finish the preemption when the jobset becomes inactive

**Summary**: [Flaky test] JobSet controller when basic setup Should finish the preemption when the jobset becomes inactive

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2808

**Last updated**: 2024-08-12T16:41:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-09T10:59:29Z
- **Updated**: 2024-08-12T16:41:41Z
- **Closed**: 2024-08-12T16:41:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

/kind flake 

**What happened**:

This test "JobSet controller when basic setup Should finish the preemption when the jobset becomes inactive" failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2807/pull-kueue-test-integration-main/1821856009056948224
It passed after re-try.

**What you expected to happen**:

No random failures.

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build on CI.

**Anything else we need to know?**:

The error message:
```
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:312 with:
Expected
    <bool>: false
to be true failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:312 with:
Expected
    <bool>: false
to be true
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:313 @ 08/09/24 10:36:28.164
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-09T10:59:41Z

/cc @trasc @mbobrovskyi

### Comment by [@trasc](https://github.com/trasc) — 2024-08-12T08:38:34Z

/assign
