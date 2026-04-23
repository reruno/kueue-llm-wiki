# Issue #9034: [flake] End To End Suite: kindest/node:v1.34.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Summary**: [flake] End To End Suite: kindest/node:v1.34.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9034

**Last updated**: 2026-02-17T12:51:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T15:33:28Z
- **Updated**: 2026-02-17T12:51:18Z
- **Closed**: 2026-02-17T12:51:17Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 6

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
End To End Suite: kindest/node:v1.34.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-34/2019767930811584512

**Failure message or logs**:
```
End To End Suite: kindest/node:v1.34.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy expand_less	49s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:486 @ 02/06/26 14:03:20.927
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T17:10:33Z

cc @mbobrovskyi @sohankunkerkar, any ideas?

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-02-06T21:17:42Z

/assign @PannagaRao

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-06T22:10:56Z

 While going through the logs, it looks like this is a controller bug in the LWS reconciler. The workload for replica group 2 never gets deleted after scale-down. There seems to be a race condition in filterWorkloads(). I will let @PannagaRao figure that out.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-16T06:15:43Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9264/pull-kueue-test-e2e-release-0-15-1-33/2023273959285329920.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T12:51:12Z

/close 
Addressed by https://github.com/kubernetes-sigs/kueue/pull/9135

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-17T12:51:18Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9034#issuecomment-3914540051):

>/close 
>Addressed by https://github.com/kubernetes-sigs/kueue/pull/9135


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
