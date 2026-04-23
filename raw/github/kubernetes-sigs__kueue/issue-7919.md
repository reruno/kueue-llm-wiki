# Issue #7919: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and LocalQueueDefaulting=false should suspend a job

**Summary**: [flaky test] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and LocalQueueDefaulting=false should suspend a job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7919

**Last updated**: 2025-11-26T19:54:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-26T17:20:28Z
- **Updated**: 2025-11-26T19:54:23Z
- **Closed**: 2025-11-26T19:54:23Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

/kind flake 

**What happened**:
failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7899/pull-kueue-test-e2e-customconfigs-main/1993718563780694016
**What you expected to happen**:
no fail
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End Custom Configs handling Suite: kindest/node:v1.34.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true and LocalQueueDefaulting=false should suspend a job expand_less	51s
{Expected success, but got an error:
    <*errors.StatusError | 0xc000bfa1e0>: 
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
    <*errors.StatusError | 0xc000bfa1e0>: 
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
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:86 @ 11/26/25 16:41:21.303
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T18:21:08Z

I have analyzed the logs, and I think the reason is that while the Deployment is ready, the old pods may be still terminating, and sometimes receive still traffic, leading to errors. I think we should wait for `Status.TerminatingReplicas` to be 0.

To try to confirm this I looked at the kubelet logs around of the time of failure: `16:41:21`: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7899/pull-kueue-test-e2e-customconfigs-main/1993718563780694016/artifacts/run-test-e2e-customconfigs-1.34.0/kind-worker2/kubelet.log

here we see the order of events:
- `16:41:21.009593` (kubelet)  the new Pod `kueue-controller-manager-bfc875747-v4pjr` is Ready
- `16:41:21.037487` (kubelet) the old Pod `kueue-controller-manager-579dfb7c48-8ddb8` receives delete
- `16:41:21.30` (test code) reports failure
- `16:41:22.043663` (kubelet)  the old Pod termination completes

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T18:21:17Z

/assign
