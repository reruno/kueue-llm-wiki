# Issue #9301: [Flaky E2E] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSe

**Summary**: [Flaky E2E] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and ManagedJobsNamespaceSelectorAlwaysRespected=false should not suspend Jobs from unmanaged JobSe

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9301

**Last updated**: 2026-02-17T03:48:32Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-17T03:48:32Z
- **Updated**: 2026-02-17T03:48:32Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

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
