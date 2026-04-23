# Issue #9028: [flaky test] Kueue secure visibility server when Capacity is maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue

**Summary**: [flaky test] Kueue secure visibility server when Capacity is maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9028

**Last updated**: 2026-02-06T20:16:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T11:56:59Z
- **Updated**: 2026-02-06T20:16:34Z
- **Closed**: 2026-02-06T20:16:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description


**Which test is flaking?**:

Kueue secure visibility server when Capacity is maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue

**Link to failed CI job or steps to reproduce locally**:


https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9017/pull-kueue-test-e2e-certmanager-main/2019591424449712128

**Failure message or logs**:
```
Kueue secure visibility server when Capacity is maxed by the admitted job [It] Should allow fetching information about pending workloads in ClusterQueue
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/visibility_test.go:72
  [FAILED] Timed out after 10.001s.
  The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/visibility_test.go:122 with:
  Expected
      <*bool | 0xc0007eaf5a>: true
  to equal
      <*bool | 0xc0007eafa0>: false
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/certmanager/visibility_test.go:123 @ 02/06/26 02:09:38.494
------------------------------

------------------------------
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T12:05:45Z

Oh I see where the flake is, consider the code: https://github.com/kubernetes-sigs/kueue/blame/main/test/e2e/certmanager/visibility_test.go#L72-L116

We aren't actually deleting the Job, but the Pods and we count on the Job to fail, but it may happen the Job controller in k8s has not created the Pods yet. In this case the request to delete pods will not to anything, and the job will continue undisturbed. This is very unlikely, but it may well happen. 

There is no issue with the sibling test, because there we are waiting for the Pods to be ready actually: https://github.com/kubernetes-sigs/kueue/blame/main/test/e2e/singlecluster/visibility_test.go#L166-L177, and so we ensure they get created.

We could either call DeleteJob before DeletePod, or wait for the Pods to be ready. Seems like calling DeleteJobs is faster, and also will achieve the intention of the test.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T17:10:54Z

/assign
Let me have some fun
