# Issue #9284: Simplify test case for rank-based ordering to use Job rather than JobSet

**Summary**: Simplify test case for rank-based ordering to use Job rather than JobSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9284

**Last updated**: 2026-03-11T05:09:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-16T13:22:44Z
- **Updated**: 2026-03-11T05:09:11Z
- **Closed**: 2026-03-11T05:09:11Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@0xlen](https://github.com/0xlen)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use Job rather than JobSet for the test case https://github.com/kubernetes-sigs/kueue/pull/9211/changes#diff-95ef2b4868044a4fbcc96fcda6df858f3b79548d2e4548fafcd9280114928dfcR1685

**Why is this needed**:

- To clearly show JobSet is not relevant in this scenario.
- JobSet CRD is not installed for the test so it could be a bit misleading (not possible outside of integration test)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:23:27Z

cc @j-skiba @tenzen-y not a priority, but would be nice to clean it up

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T13:27:53Z

> Use Job rather than JobSet for the test case https://github.com/kubernetes-sigs/kueue/pull/9211/changes#diff-95ef2b4868044a4fbcc96fcda6df858f3b79548d2e4548fafcd9280114928dfcR1685

that sounds reasonable.

### Comment by [@0xlen](https://github.com/0xlen) — 2026-03-08T21:30:08Z

I’d be happy to take this cleanup if it’s not already being worked on.

My understanding is that the goal is to simplify the test case in `test/integration/singlecluster/tas/tas_test.go` so it uses Job semantics instead of JobSet-specific setup, while preserving the tested behavior.

Please let me know if that matches the intended direction.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T05:29:28Z

Thank you, I dont think anyone is currently working on it.

### Comment by [@0xlen](https://github.com/0xlen) — 2026-03-09T09:30:55Z

/assign
