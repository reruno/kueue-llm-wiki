# Issue #1054: Change a way to check if the GVK is registered

**Summary**: Change a way to check if the GVK is registered

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1054

**Last updated**: 2023-09-19T18:59:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-08-11T11:17:15Z
- **Updated**: 2023-09-19T18:59:08Z
- **Closed**: 2023-09-19T18:59:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Once https://github.com/kubernetes-sigs/controller-runtime/pull/2425 commit is released, we need to use only `!meta.IsNoMatchError(err)` to check if the GVK is registered.

https://github.com/kubernetes-sigs/kueue/blob/b95d0fd979ae210e1dd6834523f3bb407db86bf8/main.go#L223-L233

**Why is this needed**:

The behavior of `mgr.GetRESTMapper().RESTMapping()` will be changed once https://github.com/kubernetes-sigs/controller-runtime/pull/2425 is released.

Follow-ups: #1046

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-12T13:41:05Z

I think this is unblocked after https://github.com/kubernetes-sigs/controller-runtime/pull/2472 is merged.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-12T14:11:57Z

> I think this is unblocked after [kubernetes-sigs/controller-runtime#2472](https://github.com/kubernetes-sigs/controller-runtime/pull/2472) is merged.

Oh, right. Thank you for the notifications!
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-14T17:01:42Z

I will bump K8s dependencies to address this issue.
