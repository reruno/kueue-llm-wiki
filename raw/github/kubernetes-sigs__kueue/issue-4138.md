# Issue #4138: [Flaky test] StatefulSet integration when StatefulSet created should allow to update the PodTemplate in StatefulSet

**Summary**: [Flaky test] StatefulSet integration when StatefulSet created should allow to update the PodTemplate in StatefulSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4138

**Last updated**: 2025-02-10T13:39:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-03T16:03:05Z
- **Updated**: 2025-02-10T13:39:59Z
- **Closed**: 2025-02-10T13:39:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 2

## Description

/kind flake 

**What happened**:

The test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4131/pull-kueue-test-e2e-main-1-29/1886439313734897664

**What you expected to happen**:

No failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat

**Anything else we need to know?**:

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:102 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:102 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:83 @ 02/03/25 15:47:42.977
}
```

Also another test " StatefulSet integration when StatefulSet created should delete all pods on scale down to zero" failed with 
```
{Expected success, but got an error:
    <*errors.StatusError | 0xc0002cd4a0>: 
    resourceflavors.kueue.x-k8s.io "sts-rf" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"sts-rf\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "sts-rf",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0002cd4a0>: 
    resourceflavors.kueue.x-k8s.io "sts-rf" already exists
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
            Message: "resourceflavors.kueue.x-k8s.io \"sts-rf\" already exists",
            Reason: "AlreadyExists",
            Details: {
                Name: "sts-rf",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 409,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:64 @ 02/03/25 15:47:42.995
}
```
I suppose this is a consequence of the first failure.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-03T16:03:12Z

cc @mbobrovskyi

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-03T16:22:54Z

/assign
