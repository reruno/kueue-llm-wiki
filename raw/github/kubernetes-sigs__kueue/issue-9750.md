# Issue #9750: LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should only recreate the deleted pod when policy is set to NoneRestartPolicy

**Summary**: LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should only recreate the deleted pod when policy is set to NoneRestartPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9750

**Last updated**: 2026-03-18T14:34:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T08:53:24Z
- **Updated**: 2026-03-18T14:34:34Z
- **Closed**: 2026-03-18T14:34:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

**Which test is flaking?**:
LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should only recreate the deleted pod when policy is set to NoneRestartPolicy
**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-16-1-34/2030157647042318336
**Failure message or logs**:
```

End To End Suite: kindest/node:v1.34.3: [It] LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should only recreate the deleted pod when policy is set to NoneRestartPolicy [area:singlecluster, feature:leaderworkerset] expand_less	1m24s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:1217 with:
only the deleted pod should be recreated with NoneRestartPolicy
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:1217 with:
only the deleted pod should be recreated with NoneRestartPolicy
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:1219 @ 03/07/26 06:03:28.417
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-09T10:04:40Z

/assign
