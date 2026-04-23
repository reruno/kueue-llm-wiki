# Issue #4925: Add validation webhook for `Topology.spec.levels`

**Summary**: Add validation webhook for `Topology.spec.levels`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4925

**Last updated**: 2025-04-16T18:55:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@qti-haeyoon](https://github.com/qti-haeyoon)
- **Created**: 2025-04-11T06:10:52Z
- **Updated**: 2025-04-16T18:55:09Z
- **Closed**: 2025-04-16T18:55:08Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Can create a `Topology` resource without `spec.levels` but it seems required else controller can panic.

**What you expected to happen**:

Creation/Patch of `Topology` resource without `spec.levels` should be blocked.

**How to reproduce it (as minimally and precisely as possible)**:

Controller panics when I create Topology and ResourceFlavor like:
```yaml
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: wrong-topo
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: wrong-flavor
spec:
  nodeLabels:
    some-label: true
  topologyName: wrong-topo
```

```text
E0408 02:00:42.785113       1 panic.go:115] "Observed a panic" panic="runtime error: index out of range [-1]" panicGoValue="runtime.boundsError{x:-1, y:0, signed:true, code:0x0}" stacktrace=<
        goroutine 989 [running]:
        k8s.io/apimachinery/pkg/util/runtime.logPanic({0x32aaba0, 0x4de4320}, {0x2c1f080, 0xc0031fe828})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:107 +0xbc
        k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x32aaba0, 0x4de4320}, {0x2c1f080, 0xc0031fe828}, {0x4de4320, 0x0, 0x100000000440f18?})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:82 +0x5a
        k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc0022d2700?})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x105
        panic({0x2c1f080?, 0xc0031fe828?})
                /usr/local/go/src/runtime/panic.go:787 +0x132
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).lowestLevel(...)
                /workspace/pkg/cache/tas_flavor_snapshot.go:166
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).isLowestLevelNode(...)
                /workspace/pkg/cache/tas_flavor_snapshot.go:162
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).addNode(_, {{{0x25ab53f, 0x4}, {0x2e2e19a, 0x2}}, {{0xc000b9f6c8, 0x15}, {0x0, 0x0}, {0x0, ...}, ...}, ...})
                /workspace/pkg/cache/tas_flavor_snapshot.go:141 +0x7bf
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshotForNodes(0xc0000bd880, {{0x32b5fd0?, 0xc00334a840?}, 0x0?}, {0xc003356008, 0x3, 0x3?}, {0xc0035ba000, 0x25, 0x25})
                /workspace/pkg/cache/tas_flavor.go:127 +0x785
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshot(0xc0000bd880, {0x32aaac0, 0xc00148c660})
                /workspace/pkg/cache/tas_flavor.go:115 +0x68e
        sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc0008112c0, {0x32aaac0, 0xc00148c660})
                /workspace/pkg/cache/snapshot.go:127 +0x505
        sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00092e320, {0x32aaac0, 0xc00148c4e0})
                /workspace/pkg/scheduler/scheduler.go:191 +0x21b
        sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
                /workspace/pkg/util/wait/backoff.go:43 +0x2b
        k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc00000e828?)
                /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
        k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc003063f30, {0x3275820, 0xc00000e828}, 0x0, 0xc0021d7dc0)
                /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
        sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x32aaac0, 0xc00148c4e0}, 0xc0022d1e40, {0x329f9f0, 0xc0001849d0})
                /workspace/pkg/util/wait/backoff.go:42 +0xd3
        sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x32aaac0, 0xc00148c4e0}, 0xc0022d1e40)
                /workspace/pkg/util/wait/backoff.go:34 +0x8c
        created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 985
                /workspace/pkg/scheduler/scheduler.go:146 +0x131
 >
panic: runtime error: index out of range [-1] [recovered]
        panic: runtime error: index out of range [-1]

goroutine 989 [running]:
k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x32aaba0, 0x4de4320}, {0x2c1f080, 0xc0031fe828}, {0x4de4320, 0x0, 0x100000000440f18?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:89 +0xe7
k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc0022d2700?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x105
panic({0x2c1f080?, 0xc0031fe828?})
        /usr/local/go/src/runtime/panic.go:787 +0x132
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).lowestLevel(...)
        /workspace/pkg/cache/tas_flavor_snapshot.go:166
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).isLowestLevelNode(...)
        /workspace/pkg/cache/tas_flavor_snapshot.go:162
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).addNode(_, {{{0x25ab53f, 0x4}, {0x2e2e19a, 0x2}}, {{0xc000b9f6c8, 0x15}, {0x0, 0x0}, {0x0, ...}, ...}, ...})
        /workspace/pkg/cache/tas_flavor_snapshot.go:141 +0x7bf
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshotForNodes(0xc0000bd880, {{0x32b5fd0?, 0xc00334a840?}, 0x0?}, {0xc003356008, 0x3, 0x3?}, {0xc0035ba000, 0x25, 0x25})
        /workspace/pkg/cache/tas_flavor.go:127 +0x785
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshot(0xc0000bd880, {0x32aaac0, 0xc00148c660})
        /workspace/pkg/cache/tas_flavor.go:115 +0x68e
sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc0008112c0, {0x32aaac0, 0xc00148c660})
        /workspace/pkg/cache/snapshot.go:127 +0x505
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00092e320, {0x32aaac0, 0xc00148c4e0})
        /workspace/pkg/scheduler/scheduler.go:191 +0x21b
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
        /workspace/pkg/util/wait/backoff.go:43 +0x2b
k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc00000e828?)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc003063f30, {0x3275820, 0xc00000e828}, 0x0, 0xc0021d7dc0)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x32aaac0, 0xc00148c4e0}, 0xc0022d1e40, {0x329f9f0, 0xc0001849d0})
        /workspace/pkg/util/wait/backoff.go:42 +0xd3
sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x32aaac0, 0xc00148c4e0}, 0xc0022d1e40)
        /workspace/pkg/util/wait/backoff.go:34 +0x8c
created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 985
        /workspace/pkg/scheduler/scheduler.go:146 +0x131
```

**Anything else we need to know?**:

I think it's also worth to mention that panic did not happen when I removed `spec.levels` from existing `Topology` which is already being used with a `ResourceFlavor`.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.29.4
- Kueue version (use `git describe --tags --dirty --always`): v0.11.3

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-11T06:31:32Z

Wondering if this is something we could prevent with CEL. It seems possible in cases where the issue is scoped to one object, like topology.
