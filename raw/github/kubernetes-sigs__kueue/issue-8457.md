# Issue #8457: Add RuntimeHandlers and Images chain functions

**Summary**: Add RuntimeHandlers and Images chain functions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8457

**Last updated**: 2026-04-05T05:03:12Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-08T03:25:47Z
- **Updated**: 2026-04-05T05:03:12Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@falconlee236](https://github.com/falconlee236)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Follow-up https://github.com/kubernetes-sigs/kueue/pull/8452#discussion_r2669024965

I'd like to add `RuntimeHandlers` and `Images` to NodeWrapper: https://github.com/kubernetes-sigs/kueue/blob/2808fa21ddebac0569bf15a48c4399645ea35af4/pkg/util/testingjobs/node/wrappers.go#L27

Then try to use those in `TASNodeHandler_Update` test function:

https://github.com/kubernetes-sigs/kueue/blob/2808fa21ddebac0569bf15a48c4399645ea35af4/pkg/controller/tas/resource_flavor_test.go#L96-L132

**Why is this needed**:

To eliminate anonymous bypass functions from tests.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T03:25:57Z

cc @Ladicle

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T07:33:11Z

/priority important-longterm
but it would be good to clean it up as it is fresh

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-04-05T05:03:10Z

/assign
