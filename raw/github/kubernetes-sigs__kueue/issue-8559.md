# Issue #8559: Use info/warning log level for concurrent object modification errors

**Summary**: Use info/warning log level for concurrent object modification errors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8559

**Last updated**: 2026-02-04T19:30:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-01-13T11:02:26Z
- **Updated**: 2026-02-04T19:30:32Z
- **Closed**: 2026-02-04T19:30:32Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@dkaluza](https://github.com/dkaluza)
- **Comments**: 3

## Description

**What happened**:

Currently the concurrent modification of objects are reported as errors. However, they 
happen all the time, and are relatively normal thing, leading to unnecessary noise in the logs.

```
{"level":"error","ts":"2026-01-13T10:57:04.084148714Z",
"caller":"controller/controller.go:474",
"msg":"Reconciler error","controller":"jobset","controllerGroup":"jobset.x-k8s.io","controllerKind":"JobSet","JobSet":{"name":"x-ss","namespace":"default"},"namespace":"default",
"name":"x-ss","reconcileID":"324b7d91-a3cc-4059-b186-381160adb104",
"error":"clearing admission: Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"jobset-x-ss-06b4b\": the object has been modified; please apply your changes to the latest version and try again",
"stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}```
```

**What you expected to happen**:

The information is logged at a lower level.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T12:00:03Z

The challenge is this is logged by controller-runtime, but we could probably now capture this using a custom implementation of the `logr.LogSink` (passed to LogContructor)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:23Z

/priority important-soon

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-01-14T13:59:38Z

/assign
