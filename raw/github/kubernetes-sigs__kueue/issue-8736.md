# Issue #8736: [flaky integration test] Job Controller Suite: [It] Interacting with scheduler Shouldn't admit deactivated Workload after manager restart [slow]

**Summary**: [flaky integration test] Job Controller Suite: [It] Interacting with scheduler Shouldn't admit deactivated Workload after manager restart [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8736

**Last updated**: 2026-01-27T17:27:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-22T08:15:17Z
- **Updated**: 2026-01-27T17:27:52Z
- **Closed**: 2026-01-27T17:27:52Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Job Controller Suite: [It] Interacting with scheduler Shouldn't admit deactivated Workload after manager restart [slow] 
**First observed in** (PR or commit, if known):
don't know
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2013967686685429760
**Failure message or logs**:
```
Job Controller Suite: [It] Interacting with scheduler Shouldn't admit deactivated Workload after manager restart [slow] expand_less	4s
{Failed after 0.025s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2691 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0016274a0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post "https://127.0.0.1:38611/convert?timeout=30s": dial tcp 127.0.0.1:38611: connect: connection refused
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post \"https://127.0.0.1:38611/convert?timeout=30s\": dial tcp 127.0.0.1:38611: connect: connection refused",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Failed after 0.025s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2691 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0016274a0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post "https://127.0.0.1:38611/convert?timeout=30s": dial tcp 127.0.0.1:38611: connect: connection refused
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=Workload failed: Post \"https://127.0.0.1:38611/convert?timeout=30s\": dial tcp 127.0.0.1:38611: connect: connection refused",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2695 @ 01/21/26 13:44:06.088
}
```

**Anything else we need to know?**:

I think we might need to make sure the webhooks are working fine before checking the consistently. Probably using Eventually to first read the workload and check Admitted would help.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T08:24:11Z

cc @mbobrovskyi @IrvingMg @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T08:24:42Z

> {Failed after 0.025s.

suggests it very early on - just after restart before the webhooks were initialized. I guess adding some Eventually to make sure the webhooks are running could help. Maybe list all Workloads even inside the `restartManager` helper.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-22T08:35:02Z

/assign
