# Issue #3696: Fleky Test: TopologyAwareScheduling for MPIJob when Creating a MPIJob

**Summary**: Fleky Test: TopologyAwareScheduling for MPIJob when Creating a MPIJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3696

**Last updated**: 2024-12-02T11:21:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-12-02T06:57:33Z
- **Updated**: 2024-12-02T11:21:01Z
- **Closed**: 2024-12-02T11:21:01Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Periodic Tests failed on "End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for MPIJob when Creating a MPIJob Should place pods based on the ranks-ordering".

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc0002a99a0>: 
    resourceflavors.kueue.x-k8s.io "tas-flavor" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"tas-flavor\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "tas-flavor",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0002a99a0>: 
    resourceflavors.kueue.x-k8s.io "tas-flavor" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"tas-flavor\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "tas-flavor",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/mpijob_test.go:65 @ 12/01/24 16:48:43.896
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-tas-e2e-main/1863261324973182976

**Anything else we need to know?**:

<img width="1212" alt="Screenshot 2024-12-02 at 15 55 06" src="https://github.com/user-attachments/assets/35379c08-9016-4d48-af45-3abfeb7d8617">

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-02T06:57:39Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T07:20:23Z

/cc @mbobrovskyi @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T07:20:57Z

Seem like this is just a consequence of the failed cleanup here https://github.com/kubernetes-sigs/kueue/issues/3695

### Comment by [@mykysha](https://github.com/mykysha) — 2024-12-02T09:03:21Z

/assign
