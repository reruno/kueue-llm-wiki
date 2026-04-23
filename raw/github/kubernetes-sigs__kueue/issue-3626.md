# Issue #3626: [Flaky E2E] Deployment should admit workloads after change queue-name if AvailableReplicas = 0

**Summary**: [Flaky E2E] Deployment should admit workloads after change queue-name if AvailableReplicas = 0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3626

**Last updated**: 2024-11-27T13:16:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-11-25T10:27:47Z
- **Updated**: 2024-11-27T13:16:05Z
- **Closed**: 2024-11-25T15:40:57Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End Suite: kindest/node:v1.28.9: [It] Deployment should admit workloads after change queue-name if AvailableReplicas = 0

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc000996960>: 
    workloads.kueue.x-k8s.io "pod-deployment-6d47d84db6-89fv2-c7e95" not found
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
            Message: "workloads.kueue.x-k8s.io \"pod-deployment-6d47d84db6-89fv2-c7e95\" not found",
            Reason: "NotFound",
            Details: {
                Name: "pod-deployment-6d47d84db6-89fv2-c7e95",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000996960>: 
    workloads.kueue.x-k8s.io "pod-deployment-6d47d84db6-89fv2-c7e95" not found
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
            Message: "workloads.kueue.x-k8s.io \"pod-deployment-6d47d84db6-89fv2-c7e95\" not found",
            Reason: "NotFound",
            Details: {
                Name: "pod-deployment-6d47d84db6-89fv2-c7e95",
                Group: "kueue.x-k8s.io",
                Kind: "workloads",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/deployment_test.go:202 @ 11/25/24 10:17:18.844
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3615/pull-kueue-test-e2e-main-1-28/1860988860012433408

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T10:38:14Z

/assign @mbobrovskyi 
PTAL

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T11:04:44Z

@mbobrovskyi the test fails pretty often, if the fix is not simple I propose to rollback the previous PR and work on it more

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T12:01:29Z

another: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3630/pull-kueue-test-e2e-main-1-29/1861011169054035968

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:16:03Z

/kind flake
