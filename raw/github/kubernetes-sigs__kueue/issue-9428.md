# Issue #9428: Scheduler may occasionally send multiple preemption requests to the same workload (emitting multiple events)

**Summary**: Scheduler may occasionally send multiple preemption requests to the same workload (emitting multiple events)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9428

**Last updated**: 2026-02-27T17:19:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-23T16:12:33Z
- **Updated**: 2026-02-27T17:19:33Z
- **Closed**: 2026-02-27T17:19:33Z
- **Labels**: `kind/bug`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

**What happened**:

Scheduler may issue multiple preemption requests for workloads which it already preempted.

**What you expected to happen**:

A single preemption request is sent, and a single event emitted.

**How to reproduce it (as minimally and precisely as possible)**:

I'm not sure how common this is, but we definitely observe that in longs on some deployments. 

**Anything else we need to know?**:

I think the bug is likely around this line: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/preemption/preemption.go#L173

One idea for solving is to use the in-memory "PreemptionExpectation" which are added by scheduler when preempting and removed by workload_controller when the workload is updated ("PreemptionExpectation" is observed). Before the "PreemptionExpectation" is observed the scheduler skips sending the request and emitting the event.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-23T22:03:28Z

/assign
