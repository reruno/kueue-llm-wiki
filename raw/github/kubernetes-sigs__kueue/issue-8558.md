# Issue #8558: Ungater logs workload problems at Error level

**Summary**: Ungater logs workload problems at Error level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8558

**Last updated**: 2026-01-20T14:58:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-01-13T09:40:59Z
- **Updated**: 2026-01-20T14:58:55Z
- **Closed**: 2026-01-20T14:58:55Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

**What happened**:

When index is missing in pods TAS ungater writes logs with stacktraces. 

```
{"level":"error","ts":"2025-12-30T13:12:21.50416257Z","caller":"tas/topology_ungater.go:415",
"msg":"failed to read rank information from Pods","controller":"tas_topology_ungater",
"namespace":"default","name":"job-tas-pause-job-mbmwb-96750",
"reconcileID":"636593ec-79a5-4d0b-b6e9-901f0a92a304",
"error":"label not found: no label \"[batch.kubernetes.io/job-completion-index\](http://batch.kubernetes.io/job-completion-index%5C)" for Pod \"default/tas-pause-job-mbmwb-cg2nd\"",
"stacktrace":"[sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:415\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:330\nsigs.k8s.io/kueue/pkg/controller/tas
(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core
(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296](http://sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:415%5Cnsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:330%5Cnsigs.k8s.io/kueue/pkg/controller/tas.%28*topologyUngater%29.Reconcile%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:222%5Cnsigs.k8s.io/kueue/pkg/controller/core.%28*leaderAwareReconciler%29.Reconcile%5Cn%5Ct/workspace/pkg/controller/core/leader_aware_reconciler.go:77%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.Reconcile%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.reconcileHandler%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.processNextWorkItem%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.Start.func1.1%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296)"}
```

**What you expected to happen**:

TAS ungater uses lower level and doesn't write stacktraces.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T17:42:56Z

So, do you want to eliminate the stack trace in the following at all? Personally, it is still beneficial in case of debugging. 
So, what about moving the stack trace to the debug logger instead of the error log?

```
"stacktrace":"[sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable\n\t/workspace/pkg/controller/tas/topology_ungater.go:415\nsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains\n\t/workspace/pkg/controller/tas/topology_ungater.go:330\nsigs.k8s.io/kueue/pkg/controller/tas
(*topologyUngater).Reconcile\n\t/workspace/pkg/controller/tas/topology_ungater.go:222\nsigs.k8s.io/kueue/pkg/controller/core
(*leaderAwareReconciler).Reconcile\n\t/workspace/pkg/controller/core/leader_aware_reconciler.go:77\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296](http://sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:415%5Cnsigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:330%5Cnsigs.k8s.io/kueue/pkg/controller/tas.%28*topologyUngater%29.Reconcile%5Cn%5Ct/workspace/pkg/controller/tas/topology_ungater.go:222%5Cnsigs.k8s.io/kueue/pkg/controller/core.%28*leaderAwareReconciler%29.Reconcile%5Cn%5Ct/workspace/pkg/controller/core/leader_aware_reconciler.go:77%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.Reconcile%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.reconcileHandler%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.processNextWorkItem%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421%5Cnsigs.k8s.io/controller-runtime/pkg/internal/controller.%28*Controller[...]%29.Start.func1.1%5Cn%5Ct/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296)"
```

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T19:04:03Z

Are there error logs harmless? Maybe the scenario is using non-indexed k8s job in which case we dont have indexes and need to fallback to unranked?


 If so I wouldnt log stacktraces probably, even in debug. I think we can describe the situation in the log.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:33Z

/priority important-soon

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-20T10:40:06Z

/assign
