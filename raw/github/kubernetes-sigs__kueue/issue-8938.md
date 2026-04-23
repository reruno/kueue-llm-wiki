# Issue #8938: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created [It] Rolling update with maxSurge creates workloads for surge pods and completes successfully

**Summary**: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created [It] Rolling update with maxSurge creates workloads for surge pods and completes successfully

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8938

**Last updated**: 2026-02-03T08:53:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2026-02-02T15:20:24Z
- **Updated**: 2026-02-03T08:53:42Z
- **Closed**: 2026-02-03T08:53:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 6

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
LeaderWorkerSet integration when LeaderWorkerSet created [It] Rolling update with maxSurge creates workloads for surge pods and completes successfully

**First observed in** (PR or commit, if known):
#8935 

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8935/pull-kueue-test-e2e-main-1-34/2018329542707384320

**Failure message or logs**:
```
  STEP: Wait for the surge workloads to be created with maxSurge=2 @ 02/02/26 14:42:52.167
  STEP: Verify rolling update completes successfully with 4 replicas running @ 02/02/26 14:42:52.433
  [FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:761 @ 02/02/26 14:43:37.434
  << Timeline
  [FAILED] Timed out after 45.001s.
  The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:751 with:
  Expected
      <int32>: 3
  to equal
      <int32>: 4
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:761 @ 02/02/26 14:43:37.434
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T15:39:55Z

oh I think this test was recently added, wondering if this is due to short timeout, or the rolling update getting stuck.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-02T16:28:18Z

cc: @PannagaRao

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-02-03T00:52:44Z

Ran "Rolling update with maxSurge creates workloads for surge pods and completes successfully" 200 times - all passed without flaking . Verified that this was a timing issue and  `VeryLongTimeout` fix resolves the issue.

https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8942/pull-kueue-test-e2e-main-1-34/2018441201748807680/artifacts/run-test-e2e-singlecluster-1.34.3/junit.xml

Will create a clean PR with only the timeout change.

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-02-03T00:53:00Z

/assign @PannagaRao

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-03T08:53:35Z

/close

Fixed by #8946

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-03T08:53:41Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8938#issuecomment-3839964688):

>/close
>
>Fixed by #8946 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
