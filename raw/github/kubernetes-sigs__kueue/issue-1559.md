# Issue #1559: Flaky test for single pod integration

**Summary**: Flaky test for single pod integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1559

**Last updated**: 2024-01-09T00:04:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-08T20:05:09Z
- **Updated**: 2024-01-09T00:04:02Z
- **Closed**: 2024-01-08T20:19:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 6

## Description

**What happened**:

```
Expected pod to be deleted
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/pod/pod_controller_test.go:297 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc00102f5e0>: 
    pods "test-pod" not found
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
            Message: "pods \"test-pod\" not found",
            Reason: "NotFound",
            Details: {Name: "test-pod", Group: "", Kind: "pods", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 404,
        },
    }
```

**What you expected to happen**:

It looks like the Pod was actually deleted, but somehow the check is wrong.

**How to reproduce it (as minimally and precisely as possible)**:

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main&width=20

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-08T20:06:23Z

cc @achernevskii
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-08T20:12:27Z

@alculquicondor Isn't this duplicated with #1501?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-08T20:13:59Z

And then, I fixed it in #1547

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-08T20:19:47Z

Oops, sorry, I forgot to check for existing issues

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-08T20:19:51Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1559#issuecomment-1881762012):

>Oops, sorry, I forgot to check for existing issues
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-09T00:04:00Z

/kind flake
