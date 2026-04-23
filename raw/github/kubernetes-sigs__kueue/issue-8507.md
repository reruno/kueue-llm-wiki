# Issue #8507: [flaky integration test] Preemption In a single ClusterQueue Should preempt Workloads with lower priority when there is not enough quota

**Summary**: [flaky integration test] Preemption In a single ClusterQueue Should preempt Workloads with lower priority when there is not enough quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8507

**Last updated**: 2026-01-12T16:10:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-09T17:38:10Z
- **Updated**: 2026-01-12T16:10:13Z
- **Closed**: 2026-01-12T16:10:13Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

**Which test is flaking?**:

Preemption In a single ClusterQueue Should preempt Workloads with lower priority when there is not enough quota

**First observed in** (PR or commit, if known):

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8505/pull-kueue-test-integration-baseline-main/2009675285502365696
**Failure message or logs**:
```
Scheduler Suite: [It] Preemption In a single ClusterQueue Should preempt Workloads with lower priority when there is not enough quota expand_less	1m33s
{Timed out after 45.005s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:121 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.005s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:121 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/preemption_test.go:88 @ 01/09/26 17:28:40.003

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-11T06:03:59Z

/assign
