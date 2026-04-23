# Issue #1841: Move logic to evict on Workload deactivation to the Workload controller

**Summary**: Move logic to evict on Workload deactivation to the Workload controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1841

**Last updated**: 2024-05-06T19:45:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-14T16:11:37Z
- **Updated**: 2024-05-06T19:45:42Z
- **Closed**: 2024-05-06T19:45:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The logic is currently in the job reconciler:
https://github.com/kubernetes-sigs/kueue/blob/a96927de470d985f17b03a328c33bb8547eae9a4/pkg/controller/jobframework/reconciler.go#L422-L429

**Why is this needed**:

1. The logic is fully independent of the job
2. If an integration decides not to use the job reconciler framework, they would have to re-implement this logic.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T16:27:23Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-14T16:28:22Z

First of all, I will try to investigate the reason why we added this logic to the jobs controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-28T17:56:51Z

> kueue/pkg/controller/jobframework/reconciler.go

I sought https://github.com/kubernetes-sigs/kueue/pull/1252, but I could not find any reasonable reason to put this logic on the job framework-controller.

So, I'll try to move it to the workload-controller.
