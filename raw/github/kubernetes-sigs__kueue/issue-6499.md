# Issue #6499: [Flaky] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload

**Summary**: [Flaky] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6499

**Last updated**: 2025-08-21T11:41:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-08T06:22:03Z
- **Updated**: 2025-08-21T11:41:07Z
- **Closed**: 2025-08-21T11:41:07Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 2

## Description



**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-13/1953503393620168704

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:
```
End To End Custom Configs handling Suite: kindest/node:v1.33.1: [It] ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload expand_less	46s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:194 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0009943c0>: 
    workloads.kueue.x-k8s.io "job-job-cebd4" not found
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
            Message: "workloads.kueue.x-k8s.io \"job-job-cebd4\" not found",
            Reason: "NotFound",
            Details: {
                Name: "job-job-cebd4",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:194 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0009943c0>: 
    workloads.kueue.x-k8s.io "job-job-cebd4" not found
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
            Message: "workloads.kueue.x-k8s.io \"job-job-cebd4\" not found",
            Reason: "NotFound",
            Details: {
                Name: "job-job-cebd4",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:195 @ 08/07/25 17:22:35.035

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T06:22:20Z

/kind flake
cc @mykysha @mbobrovskyi

### Comment by [@mykysha](https://github.com/mykysha) — 2025-08-19T15:01:36Z

/assign
