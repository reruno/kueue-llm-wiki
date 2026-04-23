# Issue #6129: [Flaky E2E] WaitForPodsReady with default Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeout

**Summary**: [Flaky E2E] WaitForPodsReady with default Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeout

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6129

**Last updated**: 2025-08-21T11:41:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-07-22T07:20:08Z
- **Updated**: 2025-08-21T11:41:08Z
- **Closed**: 2025-08-21T11:41:08Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Custom Configs handling Suite: kindest/node:v1.33.1: [It] WaitForPodsReady with default Timeout and a tiny RecoveryTimeout should evict and requeue workload when pod failure causes recovery timeout

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc0007a4460>: 
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
    <*errors.StatusError | 0xc0007a4460>: 
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
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/waitforpodsready_test.go:265 @ 07/21/25 15:26:45.143
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6114/pull-kueue-test-e2e-customconfigs-main/1947314745077927936

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-22T07:20:22Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T16:57:44Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5782/pull-kueue-test-e2e-customconfigs-main/1948784641288704000

### Comment by [@mykysha](https://github.com/mykysha) — 2025-07-29T12:43:54Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:04:55Z

/reopen

Even though we cherry-pick https://github.com/kubernetes-sigs/kueue/pull/6405 to 0.12 and 0.13 branches, we face this problem again:

- https://github.com/kubernetes-sigs/kueue/pull/6579
  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6579/pull-kueue-test-e2e-customconfigs-release-0-13/1955865144248504320
- https://github.com/kubernetes-sigs/kueue/pull/6578
  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6578/pull-kueue-test-e2e-customconfigs-release-0-12/1955864994394411008

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-14T06:05:00Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6129#issuecomment-3187077237):

>/reopen
>
>Even though we cherry-pick https://github.com/kubernetes-sigs/kueue/pull/6405 to 0.12 and 0.13 branches, we face this problem again:
>
>- https://github.com/kubernetes-sigs/kueue/pull/6579
>  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6579/pull-kueue-test-e2e-customconfigs-release-0-13/1955865144248504320
>- https://github.com/kubernetes-sigs/kueue/pull/6578
>  - https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6578/pull-kueue-test-e2e-customconfigs-release-0-12/1955864994394411008


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:05:15Z

@mykysha, could you check this again?
