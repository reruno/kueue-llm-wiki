# Issue #7052: [flaky test] TrainJob controller interacting with scheduler Should schedule TrainJobs as they fit in their ClusterQueue

**Summary**: [flaky test] TrainJob controller interacting with scheduler Should schedule TrainJobs as they fit in their ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7052

**Last updated**: 2025-09-29T14:46:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-29T13:22:12Z
- **Updated**: 2025-09-29T14:46:21Z
- **Closed**: 2025-09-29T14:46:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 2

## Description

**What happened**:

failure on unreleated PR: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7051/pull-kueue-test-integration-baseline-main/1972648316483145728

**What you expected to happen**:
no failures
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
TrainJob Controller Suite: [It] TrainJob controller interacting with scheduler Should schedule TrainJobs as they fit in their ClusterQueue expand_less	0s
{Expected success, but got an error:
    <*errors.StatusError | 0xc00033ac80>: 
    clustertrainingruntimes.trainer.kubeflow.org "test" already exists
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "clustertrainingruntimes.trainer.kubeflow.org \"test\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "test",
                Group: "trainer.kubeflow.org",
                Kind: "clustertrainingruntimes",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00033ac80>: 
    clustertrainingruntimes.trainer.kubeflow.org "test" already exists
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "clustertrainingruntimes.trainer.kubeflow.org \"test\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "test",
                Group: "trainer.kubeflow.org",
                Kind: "clustertrainingruntimes",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/trainjob/trainjob_controller_test.go:422 @ 09/29/25 13:15:13.077
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F7051%2Fpull-kueue-test-integration-baseline-main%2F1972648316483145728%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7051/pull-kueue-test-integration-baseline-main/1972648316483145728&lensIndex=2#)
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T13:22:41Z

cc @kaisoz @mbobrovskyi ptal, looks like possibly some missing cleanup in the AfterEach?
/kind flake

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-29T13:24:08Z

/assign
