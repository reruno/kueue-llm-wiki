# Issue #9178: [Flaky e2e]  MultiKueue when Creating a multikueue admission check Should sync a LeaderWorkerSet and run replicas on worker cluster

**Summary**: [Flaky e2e]  MultiKueue when Creating a multikueue admission check Should sync a LeaderWorkerSet and run replicas on worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9178

**Last updated**: 2026-02-17T09:27:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-02-12T16:08:07Z
- **Updated**: 2026-02-17T09:27:13Z
- **Closed**: 2026-02-17T09:27:13Z
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
End To End MultiKueue Suite: kindest/node:v1.35.0: [It] MultiKueue when Creating a multikueue admission check Should sync a LeaderWorkerSet and run replicas on worker cluster

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9172/pull-kueue-test-e2e-multikueue-main/2021972406486175744

**Failure message or logs**:
```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:126 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:126 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:543 @ 02/12/26 15:53:19.479
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:48:29Z

/area multikueue
