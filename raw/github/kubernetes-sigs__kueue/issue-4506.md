# Issue #4506: Flaky Test: Topology Aware Scheduling when Delete Topology when ResourceFlavor exist should not allow to delete topology

**Summary**: Flaky Test: Topology Aware Scheduling when Delete Topology when ResourceFlavor exist should not allow to delete topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4506

**Last updated**: 2025-03-07T21:23:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-05T19:41:50Z
- **Updated**: 2025-03-07T21:23:48Z
- **Closed**: 2025-03-07T21:23:48Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Failed `TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Delete Topology when ResourceFlavor exist should not allow to delete topology` in periodic CI.

```shell
{Failed after 0.258s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:116 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc000d806e0>: 
    topologies.kueue.x-k8s.io "topology" not found
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
            Message: "topologies.kueue.x-k8s.io \"topology\" not found",
            Reason: "NotFound",
            Details: {
                Name: "topology",
                Group: "kueue.x-k8s.io",
                Kind: "topologies",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Failed after 0.258s.
The function passed to Consistently failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:116 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc000d806e0>: 
    topologies.kueue.x-k8s.io "topology" not found
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
            Message: "topologies.kueue.x-k8s.io \"topology\" not found",
            Reason: "NotFound",
            Details: {
                Name: "topology",
                Group: "kueue.x-k8s.io",
                Kind: "topologies",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:118 @ 03/05/25 18:31:18.676
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1897350448038285312

<img width="1315" alt="Image" src="https://github.com/user-attachments/assets/40f53d21-e068-44a9-bf4c-210243c217f6" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-05T19:41:58Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-06T10:11:35Z

/assign
