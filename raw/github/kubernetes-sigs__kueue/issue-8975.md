# Issue #8975: [Flaky] Scheduler when Preemption is enabled and CQs have 0 weight should not cause an infinite preemption cycle

**Summary**: [Flaky] Scheduler when Preemption is enabled and CQs have 0 weight should not cause an infinite preemption cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8975

**Last updated**: 2026-02-10T16:02:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-04T08:17:24Z
- **Updated**: 2026-02-10T16:02:02Z
- **Closed**: 2026-02-10T16:02:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

Scheduler Fair Sharing Suite: [It] Scheduler when Preemption is enabled and CQs have 0 weight should not cause an infinite preemption cycle [feature:fairsharing] 

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:798 with:
Expected
    <int>: 2
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:798 with:
Expected
    <int>: 2
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:365 @ 02/04/26 07:35:33.844
}
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/2018946258751721472

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

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-09T22:11:35Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-10T14:11:51Z

May be the same flake I noted here: https://github.com/kubernetes-sigs/kueue/pull/8726#issuecomment-3785152932
