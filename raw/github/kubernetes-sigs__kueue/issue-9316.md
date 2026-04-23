# Issue #9316: Fix and re-enable the flaking test: TopologyAwareScheduling when Scaling a Job requesting TAS via workload slices should preserve topology assignment during scale-up

**Summary**: Fix and re-enable the flaking test: TopologyAwareScheduling when Scaling a Job requesting TAS via workload slices should preserve topology assignment during scale-up

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9316

**Last updated**: 2026-02-18T22:19:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-17T12:07:43Z
- **Updated**: 2026-02-18T22:19:39Z
- **Closed**: 2026-02-18T22:19:39Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 4

## Description

**Which test is flaking?**:

TopologyAwareScheduling when Scaling a Job requesting TAS via workload slices should preserve topology assignment during scale-up

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9224/pull-kueue-test-e2e-main-1-35/2023720289359106048

**Failure message or logs**:
```
{Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil failed [FAILED] Expected
    <*v1beta2.Workload | 0x0>: nil
not to be nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:643 @ 02/17/26 11:39:16.134
}
```

**Anything else we need to know?**:

recently introduced in https://github.com/kubernetes-sigs/kueue/pull/8580

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:08:17Z

/assign @sohankunkerkar 
Tentatively, who works on the TAS+Elastic Workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:12:10Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9311/pull-kueue-test-e2e-main-1-35/2023724461684953088

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:15:19Z

This seems to be too common, let me disable temporarily: https://github.com/kubernetes-sigs/kueue/pull/9317

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T17:56:25Z

/retitle Fix and re-enable the flaking test: TopologyAwareScheduling when Scaling a Job requesting TAS via workload slices should preserve topology assignment during scale-up
