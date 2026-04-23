# Issue #8501: Implement UTs for WorkloadReconciler predicate functions

**Summary**: Implement UTs for WorkloadReconciler predicate functions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8501

**Last updated**: 2026-04-09T17:25:31Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-09T15:08:16Z
- **Updated**: 2026-04-09T17:25:31Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I'd propose implementing UTs for the WorkloadReconciler predicate functions (`Create`, `Update`, ...).

https://github.com/kubernetes-sigs/kueue/blob/b7fdcd4e636c5cc15dd85289e75efa66f60a70a9/pkg/controller/core/workload_controller.go#L805

https://github.com/kubernetes-sigs/kueue/blob/b7fdcd4e636c5cc15dd85289e75efa66f60a70a9/pkg/controller/core/workload_controller.go#L839

https://github.com/kubernetes-sigs/kueue/blob/b7fdcd4e636c5cc15dd85289e75efa66f60a70a9/pkg/controller/core/workload_controller.go#L873

https://github.com/kubernetes-sigs/kueue/blob/b7fdcd4e636c5cc15dd85289e75efa66f60a70a9/pkg/controller/core/workload_controller.go#L1007

**Why is this needed**:

The WorkloadReconciler predicates are very complicated, but we have no UT. So, I believe that adding UTs stabilizes the workload controller.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T15:08:31Z

cc @mimowo @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T15:14:01Z

cc @Singularity23x0 who is currently working on the related refactoring as https://github.com/kubernetes-sigs/kueue/issues/5310

Generally the idea is to reduce the amount of code in the event handlers and move the logic to Reconcile.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T15:20:59Z

> cc [@Singularity23x0](https://github.com/Singularity23x0) who is currently working on the related refactoring as [#5310](https://github.com/kubernetes-sigs/kueue/issues/5310)
> 
> Generally the idea is to reduce the amount of code in the event handlers and move the logic to Reconcile.

Thank you for sharing that. I guess that we still have predicates even after moving some logic to reconcilers.
Or do @mimowo you assume that we completely remove WorkloadReconciler predicates?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T16:26:15Z

We will still have some code there for sure, but maybe adding the tests now (before refactoring) will mean the need to rewrite them. I think improving the integration tests before the refactoring would be particularly useful to ensure nothing breaks in the process.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T16:48:40Z

> We will still have some code there for sure, but maybe adding the tests now (before refactoring) will mean the need to rewrite them. I think improving the integration tests before the refactoring would be particularly useful to ensure nothing breaks in the process.

I don't request to add UTs before refactoring. We can work on that after predicates refacotring for sure.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-09T17:25:24Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
