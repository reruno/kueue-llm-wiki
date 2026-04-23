# Issue #6227: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Summary**: [Flaky] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6227

**Last updated**: 2025-08-01T17:57:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-07-29T06:48:41Z
- **Updated**: 2025-08-01T17:57:38Z
- **Closed**: 2025-08-01T17:57:38Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at Cohort level should preempt a workload from LQ with higher recent usage

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:431 with:
Not enough workloads are preempted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:431 with:
Not enough workloads are preempted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:508 @ 07/28/25 09:04:04.895
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5174/pull-kueue-test-integration-baseline-main/1949754497840451584

**Anything else we need to know?**:

/kind flake

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T06:59:44Z

cc @PBundyra ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T14:24:31Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6283/pull-kueue-test-integration-baseline-main/1950559248463171584

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-30T15:07:32Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T10:51:04Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6297/pull-kueue-test-integration-baseline-main/1950867693955452928

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-31T11:50:56Z

> https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6297/pull-kueue-test-integration-baseline-main/1950867693955452928

Actually, this is a different test. I've opened #6324.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T09:50:14Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1951171153938616320
happened on nightly

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-01T11:53:49Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6345/pull-kueue-test-integration-baseline-main/1951184148903235584
