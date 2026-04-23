# Issue #6879: Flaky E2E Test: deployments.apps "mpi-operator" not found

**Summary**: Flaky E2E Test: deployments.apps "mpi-operator" not found

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6879

**Last updated**: 2025-09-18T10:47:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-09-17T07:37:10Z
- **Updated**: 2025-09-18T10:47:27Z
- **Closed**: 2025-09-18T10:47:26Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:
End To End MultiKueue Suite: kindest/node:v1.34.0: [BeforeSuite]  deployments.apps "mpi-operator" not found

```
{Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:262 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0007f7c20>: 
    deployments.apps "mpi-operator" not found
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
            Message: "deployments.apps \"mpi-operator\" not found",
            Reason: "NotFound",
            Details: {Name: "mpi-operator", Group: "apps", Kind: "deployments", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 404,
        },
    } failed [FAILED] Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:262 with:
Expected success, but got an error:
    <*errors.StatusError | 0xc0007f7c20>: 
    deployments.apps "mpi-operator" not found
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
            Message: "deployments.apps \"mpi-operator\" not found",
            Reason: "NotFound",
            Details: {Name: "mpi-operator", Group: "apps", Kind: "deployments", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 404,
        },
    }
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/suite_test.go:305 @ 09/17/25 07:28:41.458
}
```

**What you expected to happen**:
No issues.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6876/pull-kueue-test-e2e-multikueue-main/1968211494675943424

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T10:47:21Z

/close
Looks like it should be addressed with https://github.com/kubernetes-sigs/kueue/issues/6889

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T10:47:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6879#issuecomment-3306773460):

>/close
>Looks like it should be addressed with https://github.com/kubernetes-sigs/kueue/issues/6889


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
