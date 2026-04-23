# Issue #9504: Flaky E2E test: TopologyAwareScheduling for TrainJob when Creating a TrainJob Should place pods in podset slices with two-level scheduling based on the ranks-ordering

**Summary**: Flaky E2E test: TopologyAwareScheduling for TrainJob when Creating a TrainJob Should place pods in podset slices with two-level scheduling based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9504

**Last updated**: 2026-03-02T10:50:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-26T06:02:53Z
- **Updated**: 2026-03-02T10:50:15Z
- **Closed**: 2026-03-02T10:50:15Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

End To End TAS Suite: kindest/node:v1.35.0: [It] TopologyAwareScheduling for TrainJob when Creating a TrainJob Should place pods in podset slices with two-level scheduling based on the ranks-ordering 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9501/pull-kueue-test-e2e-tas-release-0-16/2026834045899378688

**Failure message or logs**:

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc00029ae60>: 
    admission webhook "vtrainjob.kb.io" denied the request: runtime 'test-trainingruntime' not found
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
            Message: "admission webhook \"vtrainjob.kb.io\" denied the request: runtime 'test-trainingruntime' not found",
            Reason: "Forbidden",
            Details: nil,
            Code: 403,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00029ae60>: 
    admission webhook "vtrainjob.kb.io" denied the request: runtime 'test-trainingruntime' not found
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
            Message: "admission webhook \"vtrainjob.kb.io\" denied the request: runtime 'test-trainingruntime' not found",
            Reason: "Forbidden",
            Details: nil,
            Code: 403,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/tas/trainjob_test.go:190 @ 02/26/26 01:57:04.824
}
```

**Anything else we need to know?**:
