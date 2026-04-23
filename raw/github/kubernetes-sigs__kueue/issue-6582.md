# Issue #6582: Plans to GA ConfigurableResourceTransformation

**Summary**: Plans to GA ConfigurableResourceTransformation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6582

**Last updated**: 2025-09-12T18:50:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2025-08-14T16:56:50Z
- **Updated**: 2025-09-12T18:50:09Z
- **Closed**: 2025-09-12T18:50:09Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 4

## Description

## Background

The resource transformation feature (`ConfigurableResourceTransformation`) is currently in beta but enabled by default.

## Problem

The OpenShift Kueue Operator wants to expose this feature to users, but our operator APIs are GA (`v1`). We cannot include `v1beta1` APIs in our GA operator due to stability concerns.

## Questions

1. **Is there a timeline for graduating the resource transformation API from `v1beta1` to `v1`?**
2. **Are any breaking changes planned before GA?**
3. **What are the blockers (if any) preventing graduation?**

## Use Case

Once the resource transformation API graduates to `v1`, we can include it as-is in the downstream operator. Until then, we'd need to copy the types locally, which creates maintenance overhead.

Any insights on the graduation timeline would be greatly appreciated!

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-08-14T16:57:03Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-14T17:03:19Z

I think this is really a duplicate of #3476.

But I am not entirely sure on your ask.

ConfigurableResourceTransformation can GA as a feature but we have not yet planned the promotion of all the APIs to V1.

So we can graduate this feature to GA but I think the config API would still be v1beta1 for the forseeable future until #3476 is planned and committed.

I also don't know if we have considered promoting the config API to V1. That I think is a separate discussion from the kueue APIs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T17:56:54Z

As @kannon92 described, at this moment, we can not graduate an entire Configuration API. But, we can graduate the FG to GA.

FG graduation is acceptable for v0.14.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T10:58:05Z

I don't see this as a blocker, but opened a documentation issue: https://github.com/kubernetes-sigs/kueue/issues/6704 I think would be useful to have
