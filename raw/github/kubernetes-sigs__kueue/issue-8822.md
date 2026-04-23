# Issue #8822: [flaky test] Scheduler when ClusterQueue head has inadmissible workload workload which fits behind ClusterQueue head is able to admit

**Summary**: [flaky test] Scheduler when ClusterQueue head has inadmissible workload workload which fits behind ClusterQueue head is able to admit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8822

**Last updated**: 2026-01-27T16:29:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T14:32:01Z
- **Updated**: 2026-01-27T16:29:55Z
- **Closed**: 2026-01-27T16:29:55Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

**Which test is flaking?**:

Scheduler when ClusterQueue head has inadmissible workload workload which fits behind ClusterQueue head is able to admit

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2016142045285978112
**Failure message or logs**:
```
Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload workload which fits behind ClusterQueue head is able to admit [feature:fairsharing] expand_less	16s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:808 with:
Expected
    <float64>: 1000
to equal
    <float64>: 0 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:808 with:
Expected
    <float64>: 1000
to equal
    <float64>: 0
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:908 @ 01/27/26 13:53:31.486
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T14:32:26Z

cc @sohankunkerkar @mbobrovskyi  it looks similar to the recenly fixed bug

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T15:07:35Z

@mimowo Yup, we need a similar fix for that test too.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T15:07:40Z

/assign
