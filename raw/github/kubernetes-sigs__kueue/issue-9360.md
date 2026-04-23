# Issue #9360: Report entire objects in ginkgo reports when asserts fail

**Summary**: Report entire objects in ginkgo reports when asserts fail

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9360

**Last updated**: 2026-03-11T16:03:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T08:51:27Z
- **Updated**: 2026-03-11T16:03:37Z
- **Closed**: 2026-03-11T16:03:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@laxmi-333](https://github.com/laxmi-333)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to report the entire objects in the failure report when an assert fails.

For example, an assert on the suspend field fails, I would like to see the entire Job state in the failure report.

https://github.com/kubernetes-sigs/kueue/blob/cf49633305c8df2cd7b1a2d944f488962497e304/test/util/util.go#L844

There might be not "silver bullet" solution, so we could just start by improving the "helper" utility functions for asserting. in test/util/*.

Some ideas at technical level:
- use ginkgo.HasField, to assert field, eg"spec.suspend", but it will report the entire workload
- attach the entire object as description to each assert (needs better formatter probably)

**Why is this needed**:

This will be very useful for debugging. Some historical cases which could be easier by this:
- when finalizers keep workload deletion we just see that there is no NotFoundError, but seeing finalizers would make it easier
- some race conditions caused Workload state internally invalid, eg for admissionChecks and evictions. Seeing entire workload rather than just the field would help to resolve just issues much faster

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T08:51:58Z

/remove-kind feature
/kind cleanup
cc @tenzen-y @gabesaba @mbobrovskyi @PBundyra wdyt?

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-04T04:06:22Z

@mimowo I would like to work on this.

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-04T04:06:30Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-04T06:07:58Z

Awesome, you may start with a couple of helpers to align on the approach first, and then we use the pattern more.

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-05T06:44:17Z

@mimowo Could you please provide some context about the issue to begin with?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T07:03:54Z

I think the delete helpers. Here is would be very helpful to see if the finalizers was still present.

Next I would add it to helpers for workloads wrt asserts for admission checks.
