# Issue #9520: [flake] tas-scheduling-perf CI hangs

**Summary**: [flake] tas-scheduling-perf CI hangs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9520

**Last updated**: 2026-02-27T06:08:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-02-26T12:55:14Z
- **Updated**: 2026-02-27T06:08:04Z
- **Closed**: 2026-02-27T06:08:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@ASverdlov](https://github.com/ASverdlov)
- **Comments**: 2

## Description

**Which test is flaking?**:
See https://prow.k8s.io/job-history/gs/kubernetes-ci-logs/pr-logs/directory/pull-kueue-test-tas-scheduling-perf-main

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9386/pull-kueue-test-tas-scheduling-perf-main/2024788777733459968
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9512/pull-kueue-test-tas-scheduling-perf-main/2026966387070603264

**Failure message or logs**:
```
```

**Anything else we need to know?**:

## Discussion

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-26T19:34:40Z

Cross-posting from a discussion under https://github.com/kubernetes-sigs/kueue/pull/9495.

All the failures have one thing in common, an error like this:
```
2026-02-26T05:42:11.004586223Z	INFO	controller-runtime.cache	cache/reflector.go:578	Warning: watch ended with error	{"reflector": "sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:128", "type": "*v1beta2.Workload", "err": "very short watch: sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:128: Unexpected watch close - watch lasted less than a second and no items received"}
```

Likely scenario:
1. After this "watch close" some workloads were fast to be created and admitted by minimalkueue.
2. For them Create event should've fired after a relist from controller-runtime (and no subsequent Update will be available, since they're already admitted at that time).
3. But the workload finishing controller predicate ignores Create events: https://github.com/kubernetes-sigs/kueue/blob/main/test/performance/scheduler/runner/controller/controller.go#L84
4. So those workloads are admitted in time, but will never be finished.

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-27T00:38:15Z

/assign
