# Issue #5573: [flaky test]  Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails

**Summary**: [flaky test]  Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5573

**Last updated**: 2025-07-30T16:52:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T11:53:20Z
- **Updated**: 2025-07-30T16:52:29Z
- **Closed**: 2025-07-30T16:52:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

/kind flake

**What happened**:

[failure ](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5572/pull-kueue-test-integration-baseline-release-0-11/1932040894110765056)

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Provisioning admission check suite: [It] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails expand_less	15s
{Timed out after 10.007s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1735 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending failed [FAILED] Timed out after 10.007s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1735 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1739 @ 06/09/25 11:49:00.349
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F5572%2Fpull-kueue-test-integration-baseline-release-0-11%2F1932040894110765056%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5572/pull-kueue-test-integration-baseline-release-0-11/1932040894110765056&lensIndex=2#)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T06:59:00Z

/assign
This is likely the same issue as this https://github.com/kubernetes-sigs/kueue/issues/5129
