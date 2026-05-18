# Issue #9301: [Flaky E2E] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSe

**Summary**: [Flaky E2E] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSe

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9301

**Last updated**: 2026-05-11T07:27:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-17T03:48:32Z
- **Updated**: 2026-05-11T07:27:51Z
- **Closed**: 2026-05-11T07:27:49Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
End To End Custom Configs handling Suite: kindest/node:v1.35.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSet 

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-15/2023574537966194688

**Failure message or logs**:
```
{Expected success, but got an error:
    <*errors.StatusError | 0xc00068ea00>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00068ea00>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [AfterEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:86 @ 02/17/26 02:05:23.042
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T07:27:45Z

/close
Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-11T07:27:50Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9301#issuecomment-4418425443):

>/close
>Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
