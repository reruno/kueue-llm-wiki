# Issue #8633: Testing: eliminate using Evicted in favor of EvictedAt in unit tests

**Summary**: Testing: eliminate using Evicted in favor of EvictedAt in unit tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8633

**Last updated**: 2026-02-11T14:16:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-16T12:03:33Z
- **Updated**: 2026-02-11T14:16:09Z
- **Closed**: 2026-02-11T14:16:09Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be cleaned**:

I would like to replace all uses of Evicted to EvictedAt in unit tests. Example: https://github.com/kubernetes-sigs/kueue/blob/0880bb125aada2662cb298d6910cdce30a7a9c1a/pkg/workload/workload_test.go#L1492

**Why is this needed**:

* To prevent flakes due to differing timestamps, as in unit tests we should use fake clock consistently.
* consistency with AdmittedAt or ReserveQuotaAt

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:04:45Z

cc @skools-here

### Comment by [@skools-here](https://github.com/skools-here) — 2026-01-16T13:32:04Z

While removing Evicted() from tests, I noticed eviction is represented via a status condition (WorkloadEvicted + LastTransitionTime), and there’s no EvictedAt field or builder.

For updating the remaining tests, should eviction be set explicitly via the condition each time, or would you prefer a small test helper? I can follow either approach.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T13:42:50Z

I meant to introduce the EvictedAt function on the WorkloadWrapper, similar to AdmittedAt. This function would set the Evicted condition, setting the timestamp passed as LastTransitionTime.
