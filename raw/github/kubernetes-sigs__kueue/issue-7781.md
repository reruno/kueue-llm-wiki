# Issue #7781: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSet

**Summary**: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7781

**Last updated**: 2025-11-20T20:28:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-20T12:28:22Z
- **Updated**: 2025-11-20T20:28:34Z
- **Closed**: 2025-11-20T20:28:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 5

## Description

/kind flake 

**What happened**:
failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7655/pull-kueue-test-e2e-customconfigs-main/1991476538075254784
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSet expand_less	2m8s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:159 with:
Expected
    <string>: 
to equal
    <string>: Completed failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:159 with:
Expected
    <string>: 
to equal
    <string>: Completed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:160 @ 11/20/25 12:13:21.036
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-customconfigs-1.34.0%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F7655%2Fpull-kueue-test-e2e-customconfigs-main%2F1991476538075254784%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7655/pull-kueue-test-e2e-customconfigs-main/1991476538075254784&lensIndex=2#)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T12:28:48Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T12:34:55Z

cc @MaysaMacedo

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T13:16:50Z

Should we just increase timeout for JobSet to go complete?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T13:18:06Z

> Should we just increase timeout for JobSet to go complete?

If this helps based on the logs then sure

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T18:15:34Z

/assign

I opened up https://github.com/kubernetes-sigs/kueue/pull/7784.
