# Issue #2247: kueuectl: "Should stop a ClusterQueue Stop a ClusterQueue and let the admitted workloads finish" flakes

**Summary**: kueuectl: "Should stop a ClusterQueue Stop a ClusterQueue and let the admitted workloads finish" flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2247

**Last updated**: 2024-05-21T16:55:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-21T08:45:52Z
- **Updated**: 2024-05-21T16:55:58Z
- **Closed**: 2024-05-21T16:55:56Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake
**What happened**:
Integration test failed on the "Kueuectl Suite: [It] Kueuectl Stop when Stopping a ClusterQueue Should stop a ClusterQueue Stop a ClusterQueue and let the admitted workloads finish".

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000afdae0>: 
    clusterqueues.kueue.x-k8s.io "cq-2" already exists
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
            Message: "clusterqueues.kueue.x-k8s.io \"cq-2\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "cq-2",
                Group: "kueue.x-k8s.io",
                Kind: "clusterqueues",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000afdae0>: 
    clusterqueues.kueue.x-k8s.io "cq-2" already exists
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
            Message: "clusterqueues.kueue.x-k8s.io \"cq-2\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "cq-2",
                Group: "kueue.x-k8s.io",
                Kind: "clusterqueues",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/stop_test.go:87 @ 05/21/24 08:32:52.012
}
```

**What you expected to happen**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2236/pull-kueue-test-integration-main/1792834177331105792

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@trasc](https://github.com/trasc) — 2024-05-21T13:29:59Z

@tenzen-y this looks to be a duplicate of #2245, Am I missing something?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-21T16:55:52Z

> @tenzen-y this looks to be a duplicate of #2245, Am I missing something?

@trasc Oh, it seems that both indicate the same verifications :)
Thank you for pointing this out!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-21T16:55:57Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2247#issuecomment-2123052946):

>> @tenzen-y this looks to be a duplicate of #2245, Am I missing something?
>
>@trasc Oh, it seems that both indicate the same verifications :)
>Thank you for pointing this out!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
