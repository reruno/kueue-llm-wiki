# Issue #2245: [kueuectl] Flaky test "Should stop a ClusterQueue Stop a ClusterQueue and drain workloads"

**Summary**: [kueuectl] Flaky test "Should stop a ClusterQueue Stop a ClusterQueue and drain workloads"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2245

**Last updated**: 2024-05-21T10:53:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-21T07:58:12Z
- **Updated**: 2024-05-21T10:53:18Z
- **Closed**: 2024-05-21T10:53:18Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

The test failed on unrelated branch https://github.com/kubernetes-sigs/kueue/pull/2239

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

Probably just repeat the build

**Anything else we need to know?**:

```
Kueuectl Suite: [It] Kueuectl Stop when Stopping a ClusterQueue Should stop a ClusterQueue Stop a ClusterQueue and drain workloads expand_less	0s
{Expected success, but got an error:
    <*errors.StatusError | 0xc0005141e0>: 
    clusterqueues.kueue.x-k8s.io "cq-1" already exists
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
            Message: "clusterqueues.kueue.x-k8s.io \"cq-1\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "cq-1",
                Group: "kueue.x-k8s.io",
                Kind: "clusterqueues",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0005141e0>: 
    clusterqueues.kueue.x-k8s.io "cq-1" already exists
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
            Message: "clusterqueues.kueue.x-k8s.io \"cq-1\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "cq-1",
                Group: "kueue.x-k8s.io",
                Kind: "clusterqueues",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/stop_test.go:87 @ 05/21/24 07:10:01.133
}
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-21T07:58:49Z

/kind flake
/assign @trasc
