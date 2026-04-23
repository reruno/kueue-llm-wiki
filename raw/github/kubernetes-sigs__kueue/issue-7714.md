# Issue #7714: [Flaky] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check

**Summary**: [Flaky] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7714

**Last updated**: 2025-11-18T08:11:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-11-17T16:50:40Z
- **Updated**: 2025-11-18T08:11:41Z
- **Closed**: 2025-11-18T08:11:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

Job Controller Suite: [It] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check 

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:615 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:615 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2454 @ 11/17/25 15:58:38.058
}
```

**What you expected to happen**:

No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7711/pull-kueue-test-integration-baseline-main/1990446599133728768

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T16:52:33Z

link to the failure
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7711/pull-kueue-test-integration-baseline-main/1990446599133728768

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T17:12:29Z

I'm not sure, but I suspect we may be setting the AdmissionCheck to ready too early here (before QuotaReservation): https://github.com/kubernetes-sigs/kueue/blob/d63846c9ef4c4c8244996e6f72b729b4ead6a0a4/test/integration/singlecluster/controller/jobs/job/job_controller_test.go#L2442-L2451

Maybe it could be then cleared by workload controller ? In any case setting the AC status before quota reservation may happen in this test, and then the behavior is undefined. 

So, while not 100% sure this would help I would add an interim step for waiting to get the quota, wdyt @mbobrovskyi ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-18T07:18:22Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T07:25:12Z

Actually, I think what is happening is the scheduler racing with the test code. 
The test code sets admissionCheck.state=Ready, but scheduler on QuotaReservation does not know that yet, so it submits SSA request (loose) to update the workload state with admissionCheck.state=Pending.

To fix I think it is enough to wait in the test code for the quota reservation (for both workloads in the test in question).
