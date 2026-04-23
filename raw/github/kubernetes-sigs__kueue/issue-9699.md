# Issue #9699: Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at Cohort level should promote a workload from LQ with lower recent usage [feature:fairsharing, feature:admissionfairsharing, slow]

**Summary**: Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at Cohort level should promote a workload from LQ with lower recent usage [feature:fairsharing, feature:admissionfairsharing, slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9699

**Last updated**: 2026-03-06T20:52:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-03-06T06:49:08Z
- **Updated**: 2026-03-06T20:52:54Z
- **Closed**: 2026-03-06T20:52:54Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at Cohort level should promote a workload from LQ with lower recent usage [feature:fairsharing, feature:admissionfairsharing, slow] 

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9698/pull-kueue-test-integration-extended-main/2029799377802891264

**Failure message or logs**:
```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:408 with:
Unexpected workloads are admitted
Expected
    <[]types.NamespacedName | len:0, cap:1>: []
to equal
    <[]types.NamespacedName | len:1, cap:1>: [
        {
            Namespace: "core-fwhpt",
            Name: "workload-cnqpk",
        },
    ] failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:408 with:
Unexpected workloads are admitted
Expected
    <[]types.NamespacedName | len:0, cap:1>: []
to equal
    <[]types.NamespacedName | len:1, cap:1>: [
        {
            Namespace: "core-fwhpt",
            Name: "workload-cnqpk",
        },
    ]
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:1375 @ 03/06/26 06:21:19.157
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-06T20:52:54Z

Fixed in https://github.com/kubernetes-sigs/kueue/pull/9698
