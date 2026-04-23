# Issue #8773: [Flaky] Scheduler Fair Sharing Suite.[It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits

**Summary**: [Flaky] Scheduler Fair Sharing Suite.[It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8773

**Last updated**: 2026-01-26T06:31:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-24T02:32:54Z
- **Updated**: 2026-01-26T06:31:09Z
- **Closed**: 2026-01-26T06:31:09Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits [feature:fairsharing] 

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:808 with:
Expected
    <float64>: 1000
to equal
    <float64>: 0 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:808 with:
Expected
    <float64>: 1000
to equal
    <float64>: 0
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:946 @ 01/24/26 01:53:56.822
}
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2014873675085385728

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

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-25T04:42:50Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-25T18:04:09Z

Hmm... I went through that test it looks like after preemption completes, the 2-CPU workload (priority 9) gets admitted to cq1. Since cq1 is configured as a borrower-only queue with zero local quota, it ends up borrowing the full 2 CPU from cohort-a. So, cohort-a’s capacity is reduced to 2 CPU and that becomes the total lendable amount.

The weighted share is calculated [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/fair_sharing.go#L136) using the formula `borrowing * 1000 / lendable`. With 2 CPU borrowed from 2 CPU lendable, this gives 2 * 1000 / 2 = 1000. The test was incorrectly expecting 0.

I'm surprised that it didn't get caught so far. What I imagined would have happened is the test uses Eventually which polls for 10 seconds waiting for the expected value. There is a race condition between the scheduler admitting the workload, the          CQ controller asynchronously reconciling to update the metric, and the test assertion polling for the expected value. 

In passing runs, the test's first poll catches the stale value of 0 from before admission, before the CQ controller has a chance to reconcile. Since 0 matches the (incorrect) expectation, the test passes immediately. In failing runs, the controller reconciles fast enough to update the metric to 1000 before the first poll, so the test keeps polling and eventually times out because 1000 never matches the expected. Although the logs I checked are from v0.15, I expect the same behavior to apply on main as well.

@mbobrovskyi thoughts?
