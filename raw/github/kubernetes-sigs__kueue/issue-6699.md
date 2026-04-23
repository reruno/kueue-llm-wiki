# Issue #6699: Flaky E2E Test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label

**Summary**: Flaky E2E Test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6699

**Last updated**: 2025-10-23T12:21:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-29T19:26:06Z
- **Updated**: 2025-10-23T12:21:50Z
- **Closed**: 2025-10-23T12:19:19Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

`End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods created by a StatefulSet in the test namespace without queue-name label` failed in https://github.com/kubernetes-sigs/kueue/pull/6686

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:648 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0008886e0>: 
    workloads.kueue.x-k8s.io "statefulset-sts-18b6e" not found
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
            Message: "workloads.kueue.x-k8s.io \"statefulset-sts-18b6e\" not found",
            Reason: "NotFound",
            Details: {
                Name: "statefulset-sts-18b6e",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:648 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0008886e0>: 
    workloads.kueue.x-k8s.io "statefulset-sts-18b6e" not found
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
            Message: "workloads.kueue.x-k8s.io \"statefulset-sts-18b6e\" not found",
            Reason: "NotFound",
            Details: {
                Name: "statefulset-sts-18b6e",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:650 @ 08/29/25 19:02:47.399
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6686/pull-kueue-test-e2e-customconfigs-main/1961500167513313280

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-29T19:26:13Z

/kind flake

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-24T15:36:27Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T12:34:21Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6765/pull-kueue-test-e2e-customconfigs-main/1971185466099109888

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T11:29:14Z

This happened again.

https://github.com/kubernetes-sigs/kueue/pull/7356
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7356/pull-kueue-test-e2e-customconfigs-main/1981316427394584576

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T11:29:20Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6699#issuecomment-3436447942):

>This happened again.
>
>https://github.com/kubernetes-sigs/kueue/pull/7356
>https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7356/pull-kueue-test-e2e-customconfigs-main/1981316427394584576
>
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T11:35:59Z

It is the same test, but different assert, and I think a different root cause
```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:658 @ 10/23/25 11:18:28.239
}
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:19:09Z

> It is the same test, but different assert, and I think a different root cause
> 
> ```
> {Timed out after 45.000s.
> The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
> Expected
>     <int32>: 0
> to equal
>     <int32>: 3 failed [FAILED] Timed out after 45.000s.
> The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:657 with:
> Expected
>     <int32>: 0
> to equal
>     <int32>: 3
> In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:658 @ 10/23/25 11:18:28.239
> }
> ```

Good point, let me open another issue, thanks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:19:14Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T12:19:20Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6699#issuecomment-3436632531):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:21:50Z

Opened https://github.com/kubernetes-sigs/kueue/issues/7366
