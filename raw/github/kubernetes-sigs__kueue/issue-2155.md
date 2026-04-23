# Issue #2155: Flaky Test: Job controller interacting with scheduler when waitForPodsReady enabled when workload evicted due pods ready timeout should requeued after job status ready

**Summary**: Flaky Test: Job controller interacting with scheduler when waitForPodsReady enabled when workload evicted due pods ready timeout should requeued after job status ready

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2155

**Last updated**: 2024-05-08T08:46:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-07T15:04:55Z
- **Updated**: 2024-05-08T08:46:22Z
- **Closed**: 2024-05-08T08:46:22Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake
**What happened**:

Flaky Test, `Job controller interacting with scheduler when waitForPodsReady enabled when workload evicted due pods ready timeout should requeued after job status ready`:

```shell
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/job/job_controller_test.go:2007 with:
Expected
    <*int32 | 0xc000eb46e8>: 2
to equal
    <*int32 | 0xc000eb46ec>: 1 failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/job/job_controller_test.go:2007 with:
Expected
    <*int32 | 0xc000eb46e8>: 2
to equal
    <*int32 | 0xc000eb46ec>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/job/job_controller_test.go:2041 @ 05/07/24 12:58:46.121
}
```

**What you expected to happen**:

No happen

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2151/pull-kueue-test-integration-main/1787828665795481600

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-08T05:51:45Z

/assign
