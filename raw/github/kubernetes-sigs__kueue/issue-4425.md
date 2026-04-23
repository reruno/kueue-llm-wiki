# Issue #4425: [Flaky unit test]  TestPreemption/preempt_newer_workloads_with_the_same_priority

**Summary**: [Flaky unit test]  TestPreemption/preempt_newer_workloads_with_the_same_priority

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4425

**Last updated**: 2025-03-04T20:03:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-27T09:20:48Z
- **Updated**: 2025-03-04T20:03:27Z
- **Closed**: 2025-03-04T16:57:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

What happened**:

The unit test flaked on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4418/pull-kueue-test-unit-main/1895031429167845376

**What you expected to happen**:

No failures

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

I tried locally to repro, but couldn't after 3k attempts (both local and the branch), using:

```
go test ./pkg/scheduler/preemption/ -race -c 
stress ./preemption.test -test.run TestPreemption
```

```
{Failed  === RUN   TestPreemption/preempt_newer_workloads_with_the_same_priority
    preemption_test.go:1562: Issued preemptions (-want,+got):
          sets.Set[string](
        - 	{"/wl2:InClusterQueue": {}},
        + 	{"/wl3:InClusterQueue": {}},
          )
--- FAIL: TestPreemption/preempt_newer_workloads_with_the_same_priority (0.09s)
}
```
Still, it failed once so it may repeat. I suppose the issue might be with rounding to 1s in the LastTransitionTime field. Maybe we just need to make 2s difference.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-27T09:20:55Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-04T15:09:46Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T20:03:24Z

/kind flake
