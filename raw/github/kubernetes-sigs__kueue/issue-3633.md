# Issue #3633: [Flaky test] Using cohorts for sharing unused resources Should start workloads that are under ...

**Summary**: [Flaky test] Using cohorts for sharing unused resources Should start workloads that are under ...

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3633

**Last updated**: 2024-12-09T16:00:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-25T12:22:20Z
- **Updated**: 2024-12-09T16:00:05Z
- **Closed**: 2024-12-09T16:00:05Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

/kind flake

**What happened**:

Failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3632/pull-kueue-test-integration-main/1861018475376414720

**What you expected to happen**:

No failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat on CI

**Anything else we need to know?**:

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:248 with:
Not enough workloads were admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:248 with:
Not enough workloads were admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/scheduler_test.go:1271 @ 11/25/24 12:18:31.598
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T12:22:59Z

cc @mbobrovskyi  @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-12-04T10:20:49Z

cc @mszadkow  @PBundyra

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-04T10:48:28Z

/assign
