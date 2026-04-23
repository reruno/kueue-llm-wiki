# Issue #6959: Replace `WithStrict(strict bool)` with `WithLoose()`

**Summary**: Replace `WithStrict(strict bool)` with `WithLoose()`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6959

**Last updated**: 2025-09-24T05:42:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-23T12:20:36Z
- **Updated**: 2025-09-24T05:42:18Z
- **Closed**: 2025-09-24T05:42:18Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to replace the following `WithStrict(bool)` with `WithLoose()`

https://github.com/kubernetes-sigs/kueue/blob/2faadda3e0827ef19195bb01d9966a4b7ddcea20/pkg/util/client/client.go#L57-L73

**Why is this needed**:

As I mentioned in https://github.com/kubernetes-sigs/kueue/pull/6842#discussion_r2372127893, the usage will be more simple which could just call `WithLoose()` w/o any argument.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T12:20:44Z

cc @mszadkow @mimowo
