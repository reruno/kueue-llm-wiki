# Issue #4970: Controller panics when request is zero using TAS

**Summary**: Controller panics when request is zero using TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4970

**Last updated**: 2025-04-15T06:53:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@qti-haeyoon](https://github.com/qti-haeyoon)
- **Created**: 2025-04-15T02:24:14Z
- **Updated**: 2025-04-15T06:53:07Z
- **Closed**: 2025-04-15T06:53:07Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Using TAS, pod sets that have resources with value zero (for example `nvidia.com/gpu: "0"`) panics due to `runtime error: integer divide by zero`.

```txt
E0415 02:20:30.985818       1 panic.go:241] "Observed a panic" panic="runtime error: integer divide by zero" panicGoValue="\"integer divide by zero\"" stacktrace=<
        goroutine 1012 [running]:
        k8s.io/apimachinery/pkg/util/runtime.logPanic({0x32aaba0, 0x4de4320}, {0x2905440, 0x4d4c270})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:107 +0xbc
        k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x32aaba0, 0x4de4320}, {0x2905440, 0x4d4c270}, {0x4de4320, 0x0, 0x440f18?})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:82 +0x5a
        k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc0013b9500?})
                /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x105
        panic({0x2905440?, 0x4d4c270?})
                /usr/local/go/src/runtime/panic.go:787 +0x132
        sigs.k8s.io/kueue/pkg/resources.Requests.CountIn(...)
                /workspace/pkg/resources/requests.go:126
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).fillInCounts(0xc001622b40, 0xc000d76cf0, 0xc0013f48c8, 0x0, {0xc0019e15f0, 0x2, 0x2})
                /workspace/pkg/cache/tas_flavor_snapshot.go:671 +0x685
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).findTopologyAssignment(0xc001622b40, {0xc000bfc708, 0xc000d76c00, 0x1, {0xc000f15490, 0xe}, 0x1}, 0xc0013f48c8, 0x0)
                /workspace/pkg/cache/tas_flavor_snapshot.go:425 +0x436
        sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).FindTopologyAssignmentsForFlavor(0xc001622b40, {0xc000d76c60, 0x1, 0xc0019e15f0?}, 0x0)
                /workspace/pkg/cache/tas_flavor_snapshot.go:378 +0x199
        sigs.k8s.io/kueue/pkg/cache.(*ClusterQueueSnapshot).FindTopologyAssignmentsForWorkload(0xc000b419e0, 0xc000d76bd0, 0x0)
                /workspace/pkg/cache/clusterqueue_snapshot.go:213 +0xfc
        sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).assignFlavors(0xc0013f51e8, {{0x32b5fd0?, 0xc000d76450?}, 0x0?}, {0x0?, 0x8?, 0x200000001b11520?})
                /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:441 +0x8b1
        sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).Assign(0x0?, {{0x32b5fd0?, 0xc000d76450?}, 0x248?}, {0x0?, 0xc000d76701?, 0xc0013f5068?})
                /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:378 +0x2ba
        sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getInitialAssignments(0xc00055e640, {{0x32b5fd0?, 0xc000d76450?}, 0x209e645?}, 0xc000bb2a80, 0xc0012cd4a0)
                /workspace/pkg/scheduler/scheduler.go:433 +0x1b4
        sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getAssignments(0xc000dfda20?, {{0x32b5fd0?, 0xc000d76450?}, 0xc000f15430?}, 0xc000bb2a80, 0xc0012cd4a0)
                /workspace/pkg/scheduler/scheduler.go:424 +0xa5
        sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).nominate(0xc00055e640, {0x32aaac0, 0xc0012cd290}, {0xc000ee1440, 0x1, 0x0?}, 0xc0012cd4a0)
                /workspace/pkg/scheduler/scheduler.go:371 +0xae8
        sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00055e640, {0x32aaac0, 0xc0012cd110})
                /workspace/pkg/scheduler/scheduler.go:199 +0x28e
        sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
                /workspace/pkg/util/wait/backoff.go:43 +0x2b
        k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc000c09638?)
                /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
        k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0013f5f30, {0x3275820, 0xc000c09638}, 0x0, 0xc000c369a0)
                /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
        sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x32aaac0, 0xc0012cd110}, 0xc0019f3eb0, {0x329f9f0, 0xc000a32780})
                /workspace/pkg/util/wait/backoff.go:42 +0xd3
        sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x32aaac0, 0xc0012cd110}, 0xc0019f3eb0)
                /workspace/pkg/util/wait/backoff.go:34 +0x8c
        created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 992
                /workspace/pkg/scheduler/scheduler.go:146 +0x131
 >
panic: runtime error: integer divide by zero [recovered]
        panic: runtime error: integer divide by zero

goroutine 1012 [running]:
k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x32aaba0, 0x4de4320}, {0x2905440, 0x4d4c270}, {0x4de4320, 0x0, 0x440f18?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:89 +0xe7
k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc0013b9500?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x105
panic({0x2905440?, 0x4d4c270?})
        /usr/local/go/src/runtime/panic.go:787 +0x132
sigs.k8s.io/kueue/pkg/resources.Requests.CountIn(...)
        /workspace/pkg/resources/requests.go:126
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).fillInCounts(0xc001622b40, 0xc000d76cf0, 0xc0013f48c8, 0x0, {0xc0019e15f0, 0x2, 0x2})
        /workspace/pkg/cache/tas_flavor_snapshot.go:671 +0x685
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).findTopologyAssignment(0xc001622b40, {0xc000bfc708, 0xc000d76c00, 0x1, {0xc000f15490, 0xe}, 0x1}, 0xc0013f48c8, 0x0)
        /workspace/pkg/cache/tas_flavor_snapshot.go:425 +0x436
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).FindTopologyAssignmentsForFlavor(0xc001622b40, {0xc000d76c60, 0x1, 0xc0019e15f0?}, 0x0)
        /workspace/pkg/cache/tas_flavor_snapshot.go:378 +0x199
sigs.k8s.io/kueue/pkg/cache.(*ClusterQueueSnapshot).FindTopologyAssignmentsForWorkload(0xc000b419e0, 0xc000d76bd0, 0x0)
        /workspace/pkg/cache/clusterqueue_snapshot.go:213 +0xfc
sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).assignFlavors(0xc0013f51e8, {{0x32b5fd0?, 0xc000d76450?}, 0x0?}, {0x0?, 0x8?, 0x200000001b11520?})
        /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:441 +0x8b1
sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).Assign(0x0?, {{0x32b5fd0?, 0xc000d76450?}, 0x248?}, {0x0?, 0xc000d76701?, 0xc0013f5068?})
        /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:378 +0x2ba
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getInitialAssignments(0xc00055e640, {{0x32b5fd0?, 0xc000d76450?}, 0x209e645?}, 0xc000bb2a80, 0xc0012cd4a0)
        /workspace/pkg/scheduler/scheduler.go:433 +0x1b4
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getAssignments(0xc000dfda20?, {{0x32b5fd0?, 0xc000d76450?}, 0xc000f15430?}, 0xc000bb2a80, 0xc0012cd4a0)
        /workspace/pkg/scheduler/scheduler.go:424 +0xa5
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).nominate(0xc00055e640, {0x32aaac0, 0xc0012cd290}, {0xc000ee1440, 0x1, 0x0?}, 0xc0012cd4a0)
        /workspace/pkg/scheduler/scheduler.go:371 +0xae8
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00055e640, {0x32aaac0, 0xc0012cd110})
        /workspace/pkg/scheduler/scheduler.go:199 +0x28e
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
        /workspace/pkg/util/wait/backoff.go:43 +0x2b
k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc000c09638?)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0013f5f30, {0x3275820, 0xc000c09638}, 0x0, 0xc000c369a0)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x32aaac0, 0xc0012cd110}, 0xc0019f3eb0, {0x329f9f0, 0xc000a32780})
        /workspace/pkg/util/wait/backoff.go:42 +0xd3
sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x32aaac0, 0xc0012cd110}, 0xc0019f3eb0)
        /workspace/pkg/util/wait/backoff.go:34 +0x8c
created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 992
        /workspace/pkg/scheduler/scheduler.go:146 +0x131
```

**What you expected to happen**:
No panic, should be considered as a normal workload.

**How to reproduce it (as minimally and precisely as possible)**:

Create simple ResourceFlavor and Topology:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
spec:
  nodeLabels:
    test-node: true
  topologyName: default
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: default
spec:
  levels:
    - nodeLabel: kubernetes.io/hostname
```

Then try to create a pod that requests zero gpu:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-0-gpu
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: default # assumes default queue uses default flavor
spec:
  containers:
    - name: busybox
      image: busybox:1.37
      command: ["sh", "-c", "echo Hello World"]
      resources:
        limits:
          nvidia.com/gpu: "0"
```

**Environment**:
- Kubernetes version (use `kubectl version`): v1.29.4
- Kueue version (use `git describe --tags --dirty --always`): v0.11.3

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-15T02:52:41Z

Interesting find! Are you interested in fixing this?

### Comment by [@qti-haeyoon](https://github.com/qti-haeyoon) — 2025-04-15T02:57:35Z

@kannon92 , sure! Let me try to come up with a PR.
