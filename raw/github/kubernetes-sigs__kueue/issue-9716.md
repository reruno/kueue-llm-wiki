# Issue #9716: Reduce the sleep time between scheduling cycles when no admission

**Summary**: Reduce the sleep time between scheduling cycles when no admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9716

**Last updated**: 2026-03-09T15:39:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T13:20:33Z
- **Updated**: 2026-03-09T15:39:13Z
- **Closed**: 2026-03-09T15:39:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

When Kueue is processing multiple inadmissble workloads it needs to "drill" the CQ in the search of admissible workloads. However, the 100ms takes a substantial part of the 1s window we have for the drilling. 

The original increase to 100ms was dictated by our CI rather than users, see: https://github.com/kubernetes-sigs/kueue/pull/2102. From our experience StrictFIFO is not really used on production systems. Also, the amount of logs at 10ms backoff does not seem to grow dramatically anyway from my experiments in https://github.com/kubernetes-sigs/kueue/pull/9697

I would propose to reduce the max backoff slip to 10ms. I think this is still safe from the excessive logging perspective, while reducing the sleep to only 1% of the time between workload requeues (1s with the rate limiting done in https://github.com/kubernetes-sigs/kueue/issues/8095

**What you expected to happen**:

The sleep time between scheduling cycles should be reduced.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T13:35:02Z

/assign 
tentatively
