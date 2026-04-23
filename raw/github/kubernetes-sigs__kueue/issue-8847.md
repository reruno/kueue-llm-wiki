# Issue #8847: Flaky Test: Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]

**Summary**: Flaky Test: Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8847

**Last updated**: 2026-02-19T08:46:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-28T06:58:08Z
- **Updated**: 2026-02-19T08:46:11Z
- **Closed**: 2026-02-19T08:45:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

`Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]`

**First observed in** (PR or commit, if known):
https://github.com/kubernetes-sigs/kueue/pull/8845

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8845/pull-kueue-test-integration-extended-release-0-16/2016398968849698816

**Failure message or logs**:

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000eca3c0>: 
    resourceflavors.kueue.x-k8s.io "on-demand" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"on-demand\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "on-demand",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000eca3c0>: 
    resourceflavors.kueue.x-k8s.io "on-demand" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"on-demand\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "on-demand",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/workload_controller_test.go:955 @ 01/28/26 06:40:03.632

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T12:43:18Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9095/pull-kueue-test-integration-extended-main/2021920831256399872

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T15:19:22Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9321/pull-kueue-test-integration-extended-main/2023776846776111104

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T08:45:15Z

/close
because this original issue was solved as https://github.com/kubernetes-sigs/kueue/issues/8809
The ` resourceflavors.kueue.x-k8s.io "on-demand" already exists` was just a follow up affected test.

The most recent issue https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9321/pull-kueue-test-integration-extended-main/2023776846776111104 is a different assert
```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
Expected
    <float64>: 1
to equal
    <float64>: 0 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
Expected
    <float64>: 1
to equal
    <float64>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/workload_controller_test.go:1043 @ 02/17/26 15:17:39.147
}
```

, let me open dedicated issue.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-19T08:45:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8847#issuecomment-3925670080):

>/close
>because this original issue was solved as https://github.com/kubernetes-sigs/kueue/issues/8809
>The ` resourceflavors.kueue.x-k8s.io "on-demand" already exists` was just a follow up affected test.
>
>The most recent issue https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9321/pull-kueue-test-integration-extended-main/2023776846776111104 is a different assert
>```
>{Timed out after 10.000s.
>The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
>Expected
>    <float64>: 1
>to equal
>    <float64>: 0 failed [FAILED] Timed out after 10.000s.
>The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
>Expected
>    <float64>: 1
>to equal
>    <float64>: 0
>In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/workload_controller_test.go:1043 @ 02/17/26 15:17:39.147
>}
>```
>
>, let me open dedicated issue.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T08:46:11Z

Opened https://github.com/kubernetes-sigs/kueue/issues/9358, to make it clear which assert we are debugging now.
