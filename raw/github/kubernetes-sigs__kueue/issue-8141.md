# Issue #8141: [flaky integration test] Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads

**Summary**: [flaky integration test] Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8141

**Last updated**: 2025-12-12T14:27:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-09T07:32:28Z
- **Updated**: 2025-12-12T14:27:46Z
- **Closed**: 2025-12-12T14:27:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 9

## Description

**What happened**:
failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1998285100025909248
**What you expected to happen**:
no fail
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Scheduler Suite: [It] Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads expand_less	12s
{Timed out after 10.010s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:356 with:
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 10.010s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:356 with:
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/preemption_test.go:598 @ 12/09/25 07:14:02.508
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-09T07:32:56Z

cc @sohankunkerkar @mbobrovskyi

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-09T13:55:54Z

/assign @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T15:57:04Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T11:57:22Z

I have analyzed the logs and I think I know what is going on. When "use-all" transitions from "admitted" to "pending" (due to eviction) then it is Deleted from "cache" and added to 'queues". These operations take the "manager" lock here: https://github.com/kubernetes-sigs/kueue/blob/9ba604919ec4733cbc0f3055c98d8e93154bdcc6/pkg/controller/core/workload_controller.go#L940-L964

However, it means there is a "gap" between L946 and L959 when the workload is removed from cache, but not yet considered queued. In this gap it is possible that scheduler:
1. take the "heads" including "preemptor" and "pending" (2 heads before "use-all" is requeued) - this requires manager lock, but it could be taken before the preemption completed
2. do snapshot of the cache but only using the "cache" lock

For (1.) and (2.) see https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L206-L224.

As a result scheduler may admit both "pending" and "preemptor".

So, I can see two options:
1. extend locking in for creating snapshot to entire "manager" - not just "cache"
2. plumb the test to make sure "pending" cannot get admitted , eg giving it size 4

I'm leaning towards (2.) because;
a) extending the locking in scheduler may be risky from performance perspective, even if it looks harmless, but we should probably have a feature gate to be safe
b) I have no users reporting about it
c) the consequences are quite limited, the "pending" workload just got admitted inverting priorities, but it can always get preempted again by "use-all" (given that "preemptor" completes)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T12:02:00Z

I'm not sure if catching the issue like this was the intention of the test. I found the PR which introduced the test https://github.com/kubernetes-sigs/kueue/pull/1866 and it seems the intention of the test was to make sure the preemption happens, not necessarily which workload gets admitted after it completes ("preemptor" only or "preemptor" and "pending").

So it seems the test was written stronger than MVP for the old bug.

Thus I'm leaning to making just test pass consistently (2.).

If we get ever user bug reported then we can consider the more  advanced fix for (1.) , but I doubt given how unlikely it is, and how limited consequences are.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T12:02:11Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T13:36:22Z

Oh, I didn't notice https://github.com/kubernetes-sigs/kueue/pull/8153 and https://github.com/kubernetes-sigs/kueue/issues/8141#issuecomment-3632399735

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-11T13:53:31Z

You're right that only extending the manager lock (Option 1) would fully fix the race. My [fix](https://github.com/kubernetes-sigs/kueue/pull/8153) narrows the window but doesn't eliminate it. Given no user reports and limited impact, adjusting the test makes sense. Thanks for the thorough analysis!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T10:38:22Z

I submitted the quick fix for the flake ptal: https://github.com/kubernetes-sigs/kueue/pull/8203
