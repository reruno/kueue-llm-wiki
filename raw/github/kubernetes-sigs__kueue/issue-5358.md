# Issue #5358: [flaky test] WaitForPodsReady has a tiny Timeout and no RecoveryTimeout should evict and requeue workload when pods readiness timeout is surpassed

**Summary**: [flaky test] WaitForPodsReady has a tiny Timeout and no RecoveryTimeout should evict and requeue workload when pods readiness timeout is surpassed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5358

**Last updated**: 2025-12-08T17:57:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-26T15:32:12Z
- **Updated**: 2025-12-08T17:57:30Z
- **Closed**: 2025-12-08T17:57:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 8

## Description

/kind flake

**What happened**:

failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5357/pull-kueue-test-e2e-customconfigs-main/1927021441526534144

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End Custom Configs handling Suite: kindest/node:v1.32.3: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and LocalQueueDefaulting=false should suspend a job expand_less	25s
{Expected success, but got an error:
    <*errors.StatusError | 0xc0008a26e0>: 
    resourceflavors.kueue.x-k8s.io "default" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"default\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "default",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0008a26e0>: 
    resourceflavors.kueue.x-k8s.io "default" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"default\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "default",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:72 @ 05/26/25 15:27:15.647
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T15:32:27Z

cc @mykysha @mbobrovskyi ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-26T15:59:46Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:11:39Z

/reopen

Even though we cherry-picked https://github.com/kubernetes-sigs/kueue/pull/5685 to release-0.12, we face this problem again.

- https://github.com/kubernetes-sigs/kueue/pull/6578
  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6578/pull-kueue-test-e2e-customconfigs-release-0-12/1955864994394411008

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-14T06:11:43Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5358#issuecomment-3187091077):

>/reopen
>
>Even though we cherry-picked https://github.com/kubernetes-sigs/kueue/pull/5685 to release-0.12, we face this problem again.
>
>- https://github.com/kubernetes-sigs/kueue/pull/6578
>  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6578/pull-kueue-test-e2e-customconfigs-release-0-12/1955864994394411008


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:11:56Z

@mbobrovskyi Could you check this?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T06:51:13Z

```

End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] WaitForPodsReady with tiny Timeout and no RecoveryTimeout should evict and requeue workload when pods readiness timeout is surpassed expand_less	50s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/waitforpodsready_test.go:150 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc00084e500>: 
    workloads.kueue.x-k8s.io "job-job-timeout-fe254" not found
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
            Message: "workloads.kueue.x-k8s.io \"job-job-timeout-fe254\" not found",
            Reason: "NotFound",
            Details: {
                Name: "job-job-timeout-fe254",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/waitforpodsready_test.go:150 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc00084e500>: 
    workloads.kueue.x-k8s.io "job-job-timeout-fe254" not found
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
            Message: "workloads.kueue.x-k8s.io \"job-job-timeout-fe254\" not found",
            Reason: "NotFound",
            Details: {
                Name: "job-job-timeout-fe254",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/waitforpodsready_test.go:152 @ 09/10/25 22:51:21.681

There were additional failures detected after the initial failure. These are visible in the timeline
}
```
This happened again here: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-main/1965908579537915904

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T16:45:18Z

/unassign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-05T21:28:57Z

/assign @sohankunkerkar
