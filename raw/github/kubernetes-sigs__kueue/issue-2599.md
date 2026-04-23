# Issue #2599: Flaky test: The workload's admission is removed Should restore the original node selectors

**Summary**: Flaky test: The workload's admission is removed Should restore the original node selectors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2599

**Last updated**: 2024-07-15T15:19:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-07-12T20:29:00Z
- **Updated**: 2024-07-15T15:19:11Z
- **Closed**: 2024-07-15T15:19:11Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
PyTorchJob Controller Suite: [It] Job controller interacting with scheduler when The workload's admission is removed Should restore the original node selectors

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc002021540>: 
    object is being deleted: resourceflavors.kueue.x-k8s.io "spot-untainted" already exists
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
            Message: "object is being deleted: resourceflavors.kueue.x-k8s.io \"spot-untainted\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "spot-untainted",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc002021540>: 
    object is being deleted: resourceflavors.kueue.x-k8s.io "spot-untainted" already exists
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
            Message: "object is being deleted: resourceflavors.kueue.x-k8s.io \"spot-untainted\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "spot-untainted",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/pytorchjob/pytorchjob_controller_test.go:493 @ 07/12/24 20:11:04.513
}
```

**What you expected to happen**:
Never seen these errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2598/pull-kueue-test-integration-main/1811853301533118464

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-12T20:30:59Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-15T04:33:55Z

/assign
