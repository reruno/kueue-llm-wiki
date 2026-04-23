# Issue #8006: [flaky importer test] Importer when Kueue is started after import Should keep the imported pods admitted

**Summary**: [flaky importer test] Importer when Kueue is started after import Should keep the imported pods admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8006

**Last updated**: 2025-12-01T11:12:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-01T07:28:25Z
- **Updated**: 2025-12-01T11:12:58Z
- **Closed**: 2025-12-01T11:12:58Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 11

## Description

/kind flake 

**What happened**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1994479989755482112
**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Importer Suite: [It] Importer when Kueue is started after import Should keep the imported pods admitted expand_less	3s
{Expected success, but got an error:
    <*errors.StatusError | 0xc000f5bb80>: 
    pods "pod2" not found
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
            Message: "pods \"pod2\" not found",
            Reason: "NotFound",
            Details: {Name: "pod2", Group: "", Kind: "pods", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 404,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000f5bb80>: 
    pods "pod2" not found
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
            Message: "pods \"pod2\" not found",
            Reason: "NotFound",
            Details: {Name: "pod2", Group: "", Kind: "pods", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/importer/importer_test.go:149 @ 11/28/25 19:13:04.27
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T07:30:04Z

I looked at the code and I think we are missing Eventually around the updating function. It may happen that the code hasn't yet received the event about pod2, so we need to wait for it explicitly or just repeat the call to `util.SetPodsPhase(`

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-01T07:53:47Z

Yeah, this is good point, but not sure why we have `pods "pod2" not found` error.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T08:24:01Z

because we don't have any guarantee the event about the pod2 has reached Kueue since the startup - never check it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T08:25:01Z


We only check the associated Workload object is observed, but this is a different CRD. There is no guarantee events about Pods are received before Workloads or vice-versa.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:02:45Z

/close 
per https://github.com/kubernetes-sigs/kueue/pull/8007

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T09:02:52Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8006#issuecomment-3595379599):

>/close 
>per https://github.com/kubernetes-sigs/kueue/pull/8007


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:11:12Z

/reopen
As @mbobrovskyi said the issue might be more complex, because the "not found" wasn't from Kueue, but from test code which created the Pod. We should investigate the api-server logs to see if something deleted the Pod.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T09:11:18Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8006#issuecomment-3595412168):

>/reopen
>As @mbobrovskyi said the issue might be more complex, because the "not found" wasn't from Kueue, but from test code which created the Pod. We should investigate the api-server logs to see if something deleted the Pod.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:16:17Z

Actually, if the k8sClient is using cache (to be checked), which is populated based on events from API server then it is still possible to get 404 for a short while if the response is cached.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T11:12:53Z

/close
The issue is no tricky. As I synced with @mbobrovskyi https://github.com/kubernetes-sigs/kueue/issues/8006#issuecomment-3595432188 is potentially correct, but we are not sure. 

I think we are ok to close, and re-open if the issue ever re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T11:12:58Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8006#issuecomment-3595958970):

>/close
>The issue is no tricky. As I synced with @mbobrovskyi https://github.com/kubernetes-sigs/kueue/issues/8006#issuecomment-3595432188 is potentially correct, but we are not sure. 
>
>I think we are ok to close, and re-open if the issue ever re-occurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
