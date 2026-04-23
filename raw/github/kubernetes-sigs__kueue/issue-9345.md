# Issue #9345: [FairSharing] Scheduler chooses workload resulting in unbalanced DRS

**Summary**: [FairSharing] Scheduler chooses workload resulting in unbalanced DRS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9345

**Last updated**: 2026-02-20T17:09:01Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-18T15:50:07Z
- **Updated**: 2026-02-20T17:09:01Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:
During each scheduling cycle, we consider at most 1 workload from each CQ. In certain scenarios, this results in Kueue making scheduling decisions leading to an unfair DominantResourceShare (DRS).

Consider the following scenario:

```
- Root Cohort (4 GPU)
  - CQ-A (0 GPU)
  - CQ-B (0 GPU)
```

Suppose that each workload requests 1 GPU, and that this sequence of events occur:

```
t0: create a0, a1
t1: a0, a1 schedule; DRS(CQ-A): 500
t2: create a2, b0, b1
t3: a2, b0 schedule; DRS(CQ-A): 750, DRS(CQ-B): 250
```
**What you expected to happen**:

The "correct" scheduling decision would have been to schedule both workloads from CQ-B. Many other variations of this can occur (workloads in 1 queue request more resources; another queue has a lower FairSharing weight), but it boils down to the fact that the right scheduling order should be to go deeper into 1 CQ, before scheduling a workload from the other CQ.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
This problem is less pronounced as long as preemption is possible.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2026-02-19T21:25:33Z

@gabesaba What does this mean in practice? Like is it a brief period of preemptions while the tree is balancing correctly?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-20T09:52:11Z

> [@gabesaba](https://github.com/gabesaba) What does this mean in practice? Like is it a brief period of preemptions while the tree is balancing correctly?

Exactly. As long as preemptions are enabled and completed quickly, this is not a big issue. If preemptions are disabled, however, then this issue can result in longer lasting unfairness.

### Comment by [@amy](https://github.com/amy) — 2026-02-20T17:09:01Z

@gabesaba I see. To clarify... when would the DRS tree be used then? Is this for something like admission fairsharing + preemption off?
