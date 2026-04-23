# Issue #5898: [flaky test] AFS integration test makes Kueue panic / crash

**Summary**: [flaky test] AFS integration test makes Kueue panic / crash

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5898

**Last updated**: 2025-07-10T13:05:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-08T08:01:43Z
- **Updated**: 2025-07-10T13:05:30Z
- **Closed**: 2025-07-10T13:05:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 3

## Description

/kind flake

**What happened**:

Example failed build where Kueue paniced: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1942472892331593728

**What you expected to happen**:

No failures

**How to reproduce it (as minimally and precisely as possible)**:

run on CI

**Anything else we need to know?**:

```
[1mOutput from proc 4:[0m
  E0708 06:52:34.098576   34127 panic.go:262] "Observed a panic" panic="runtime error: invalid memory address or nil pointer dereference" panicGoValue="\"invalid memory address or nil pointer dereference\"" stacktrace=<
  	goroutine 229 [running]:
  	k8s.io/apimachinery/pkg/util/runtime.logPanic({0x352b1d0, 0xc00138e090}, {0x2e22860, 0x47a1ef0})
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:132 +0xdd
  	k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x352cab8, 0xc00049c000}, {0x2e22860, 0x47a1ef0}, {0x0, 0x0, 0x4b5652?})
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:107 +0x185
  	k8s.io/apimachinery/pkg/util/runtime.HandleCrashWithContext({0x352cab8, 0xc00049c000}, {0x0, 0x0, 0x0})
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:78 +0x69
  	panic({0x2e22860?, 0x47a1ef0?})
  		/usr/local/go/src/runtime/panic.go:792 +0x132
  	sigs.k8s.io/kueue/pkg/workload.(*Info).CalcLocalQueueFSUsage(0xc000782e80, {0x352b1d0, 0xc000bc9c80}, {0x3539bc0, 0xc0001f1710}, 0x0)
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/workload/workload.go:310 +0x1d3
  	sigs.k8s.io/kueue/pkg/cache.(*Cache).snapshotClusterQueue(0xc000492700, {0x352b1d0, 0xc000bc9c80}, 0xc000992800)
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/cache/snapshot.go:194 +0x1173
  	sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc000492700, {0x352b1d0, 0xc000bc9c80})
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/cache/snapshot.go:142 +0xee8
  	sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc0006400a0, {0x352b1d0, 0xc000a48120})
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:193 +0x397
  	sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:43 +0x59
  	k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1({0xc000120380?, 0x0?})
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x2f
  	k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1({0x352cab8, 0xc00049c000}, 0xc000067ec8)
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255 +0x9d
  	k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext({0x352cab8, 0xc00049c000}, 0xc000067ec8, {0x350a5c0, 0xc000516030}, 0x0)
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256 +0xee
  	k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00035df10, {0x350a5c0, 0xc000516030}, 0x0, 0xc00049c000)
  		/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x8b
  	sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x352b1d0, 0xc000a48120}, 0xc00100e1c0, {0x351f020, 0xc000d8a008})
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:42 +0x145
  	sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x352b1d0, 0xc000a48120}, 0xc00100e1c0)
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:34 +0xca
  	created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 103
  		/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:148 +0x234
   >
  panic: runtime error: invalid memory address or nil pointer dereference [recovered]
  	panic: runtime error: invalid memory address or nil pointer dereference
  [signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x29fac53]

  goroutine 229 [running]:
  k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x352cab8, 0xc00049c000}, {0x2e22860, 0x47a1ef0}, {0x0, 0x0, 0x4b5652?})
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:114 +0x23a
  k8s.io/apimachinery/pkg/util/runtime.HandleCrashWithContext({0x352cab8, 0xc00049c000}, {0x0, 0x0, 0x0})
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:78 +0x69
  panic({0x2e22860?, 0x47a1ef0?})
  	/usr/local/go/src/runtime/panic.go:792 +0x132
  sigs.k8s.io/kueue/pkg/workload.(*Info).CalcLocalQueueFSUsage(0xc000782e80, {0x352b1d0, 0xc000bc9c80}, {0x3539bc0, 0xc0001f1710}, 0x0)
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/workload/workload.go:310 +0x1d3
  sigs.k8s.io/kueue/pkg/cache.(*Cache).snapshotClusterQueue(0xc000492700, {0x352b1d0, 0xc000bc9c80}, 0xc000992800)
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/cache/snapshot.go:194 +0x1173
  sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc000492700, {0x352b1d0, 0xc000bc9c80})
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/cache/snapshot.go:142 +0xee8
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc0006400a0, {0x352b1d0, 0xc000a48120})
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:193 +0x397
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:43 +0x59
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1({0xc000120380?, 0x0?})
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x2f
  k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1({0x352cab8, 0xc00049c000}, 0xc000067ec8)
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255 +0x9d
  k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext({0x352cab8, 0xc00049c000}, 0xc000067ec8, {0x350a5c0, 0xc000516030}, 0x0)
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256 +0xee
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00035df10, {0x350a5c0, 0xc000516030}, 0x0, 0xc00049c000)
  	/home/prow/go/src/kubernetes-sigs/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x8b
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x352b1d0, 0xc000a48120}, 0xc00100e1c0, {0x351f020, 0xc000d8a008})
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:42 +0x145
  sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x352b1d0, 0xc000a48120}, 0xc00100e1c0)
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/util/wait/backoff.go:34 +0xca
  created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 103
  	/home/prow/go/src/kubernetes-sigs/kueue/pkg/scheduler/scheduler.go:148 +0x234
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T08:04:37Z

cc @mbobrovskyi @mwysokin

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-08T14:43:14Z

/assign @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-10T11:47:38Z

the panic repeated here: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1943016480144625664
