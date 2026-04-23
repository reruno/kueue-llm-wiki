# Issue #9473: [flaky test] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast

**Summary**: [flaky test] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9473

**Last updated**: 2026-03-09T07:59:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-02-25T12:42:06Z
- **Updated**: 2026-03-09T07:59:13Z
- **Closed**: 2026-03-09T07:59:13Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@falconlee236](https://github.com/falconlee236)
- **Comments**: 4

## Description

**Which test is flaking?**:

`LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast`

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9450/pull-kueue-test-e2e-main-1-33/2026622621155594240

**Failure message or logs**:
```
• [FAILED] [49.027 seconds]
LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast [It] LeaderReadyStartupPolicy [area:singlecluster, feature:leaderworkerset]
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:500
  Timeline >>
  "level"=0 "msg"="Created namespace" "namespace"="lws-e2e-b4r6s"
  STEP: Create a LeaderWorkerSet @ 02/25/26 11:56:42.21
  STEP: Waiting for replicas is ready @ 02/25/26 11:56:42.222
  STEP: Check workload is created @ 02/25/26 11:56:44.262
  STEP: Scale up LeaderWorkerSet @ 02/25/26 11:56:44.266
  STEP: Scale down LeaderWorkerSet @ 02/25/26 11:56:44.283
  STEP: Waiting for replicas is ready @ 02/25/26 11:56:44.303
  STEP: Check workload for group 1 is still exist @ 02/25/26 11:56:44.308
  STEP: Check workload for group 2 is released @ 02/25/26 11:56:44.313
  [FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:478 @ 02/25/26 11:57:29.314
  << Timeline
  [FAILED] Timed out after 45.001s.
  The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:126 with:
  Error matcher expects an error.  Got:
      <nil>: nil
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:478 @ 02/25/26 11:57:29.314
```

**Anything else we need to know?**:

## Discussion

### Comment by [@j-skiba](https://github.com/j-skiba) — 2026-02-25T12:43:30Z

found here - https://github.com/kubernetes-sigs/kueue/pull/9450

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-04T03:50:50Z

Can I follow up this issue?  @j-skiba 
/assign

### Comment by [@j-skiba](https://github.com/j-skiba) — 2026-03-04T06:37:19Z

@falconlee236 yes, sure

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T12:48:21Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-16-1-33/2029614059627745280
another occurrence
