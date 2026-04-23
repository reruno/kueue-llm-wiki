# Issue #9609: [release-0.16] Flaky MPIJob E2E Test Job controller for workloads when only jobs with queue are managed Should suspend a job if the parent's workload does not exist or is not admitted

**Summary**: [release-0.16] Flaky MPIJob E2E Test Job controller for workloads when only jobs with queue are managed Should suspend a job if the parent's workload does not exist or is not admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9609

**Last updated**: 2026-03-03T15:41:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-03-02T05:32:36Z
- **Updated**: 2026-03-03T15:41:34Z
- **Closed**: 2026-03-03T15:41:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@falconlee236](https://github.com/falconlee236)
- **Comments**: 6

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

MPIJob Controller Suite: [It] Job controller for workloads when only jobs with queue are managed Should suspend a job if the parent's workload does not exist or is not admitted

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-16/2027619659972349952

**Failure message or logs**:
```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000580640>: 
    admission webhook "mjob.kb.io" denied the request: MPIJob.kubeflow.org "test-job-parent" not found
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
            Message: "admission webhook \"mjob.kb.io\" denied the request: MPIJob.kubeflow.org \"test-job-parent\" not found",
            Reason: "NotFound",
            Details: {
                Name: "test-job-parent",
                Group: "kubeflow.org",
                Kind: "MPIJob",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000580640>: 
    admission webhook "mjob.kb.io" denied the request: MPIJob.kubeflow.org "test-job-parent" not found
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
            Message: "admission webhook \"mjob.kb.io\" denied the request: MPIJob.kubeflow.org \"test-job-parent\" not found",
            Reason: "NotFound",
            Details: {
                Name: "test-job-parent",
                Group: "kubeflow.org",
                Kind: "MPIJob",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/mpijob/mpijob_controller_test.go:527 @ 02/28/26 05:54:52.453
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-02T09:49:38Z

Hi, I'm interested in this flaky test. 
I've been studying MPIJob and Kueue, and I'd like to investigate the cause.
/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T10:18:01Z

I think this is very similar to https://github.com/kubernetes-sigs/kueue/issues/9504, and the fix could be similar as in https://github.com/kubernetes-sigs/kueue/pull/9571

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-02T10:24:53Z

Thanks for the hints, @mimowo
 
I'll take a look at #9571 and #9504, and try to refactor it using util.MustCreateWithRetry as suggested.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T13:46:48Z

sgtm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T15:41:27Z

/close
as the fix pr is merged

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-03T15:41:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9609#issuecomment-3991888150):

>/close
>as the fix pr is merged
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
