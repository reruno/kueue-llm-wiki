# Issue #9934: Use assertMsg for helpers in test/util/util.go

**Summary**: Use assertMsg for helpers in test/util/util.go

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9934

**Last updated**: 2026-03-26T18:02:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-17T08:40:31Z
- **Updated**: 2026-03-26T18:02:23Z
- **Closed**: 2026-03-26T18:02:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to use the new assertMsg for all helpers. 

We can deliver in multiple PRs, for example, one PR could be the workload-related helpers.

**Why is this needed**:

It proves to be very effective tool for debugging.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T08:40:41Z

cc @reruno @mbobrovskyi

### Comment by [@reruno](https://github.com/reruno) — 2026-03-17T08:43:25Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T10:59:53Z

I would appreciate the first PR to do it for ExpectWorkloadsToBeAdmitted, because this function is a very useful helper used in many tests. I already debug/write some tests using it.
