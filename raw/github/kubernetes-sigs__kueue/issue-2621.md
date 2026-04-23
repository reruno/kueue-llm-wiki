# Issue #2621: Flaky Test: Kueue when Creating a Job With Queueing Should readmit preempted job with workloadPriorityClass into a separate flavor

**Summary**: Flaky Test: Kueue when Creating a Job With Queueing Should readmit preempted job with workloadPriorityClass into a separate flavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2621

**Last updated**: 2024-07-16T10:41:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-07-16T09:54:30Z
- **Updated**: 2024-07-16T10:41:04Z
- **Closed**: 2024-07-16T10:41:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky Test for `End To End Suite: kindest/node:v1.29.4: [It] Kueue when Creating a Job With Queueing Should readmit preempted job with workloadPriorityClass into a separate flavor`.

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc00029a820>: 
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
    <*errors.StatusError | 0xc00029a820>: 
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
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:99 @ 07/16/24 09:35:23.344
}
```

**What you expected to happen**:

Errors never has been seen.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2619/pull-kueue-test-e2e-release-0-7-1-29/1813144006800969728

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-16T09:54:45Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-16T10:25:08Z

/assign
