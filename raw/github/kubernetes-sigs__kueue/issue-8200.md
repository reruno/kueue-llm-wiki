# Issue #8200: [flaky test] MultiKueue when Connection via ClusterProfile no plugins Should be able to use ClusterProfile as way to connect worker cluster

**Summary**: [flaky test] MultiKueue when Connection via ClusterProfile no plugins Should be able to use ClusterProfile as way to connect worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8200

**Last updated**: 2025-12-12T18:21:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-12T10:28:39Z
- **Updated**: 2025-12-12T18:21:17Z
- **Closed**: 2025-12-12T18:21:17Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 4

## Description


**What happened**:

flaked on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8198/pull-kueue-test-e2e-multikueue-release-0-15/1999416601102782464

**What you expected to happen**:
no flake
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End MultiKueue Suite: kindest/node:v1.34.0: [It] MultiKueue when Connection via ClusterProfile no plugins Should be able to use ClusterProfile as way to connect worker cluster expand_less	54s
{Expected success, but got an error:
    <*errors.StatusError | 0xc000b27900>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000b27900>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:171 @ 12/12/25 10:12:20.96
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T10:28:54Z

/kind flake
cc @mszadkow @sohankunkerkar ptal

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-12T15:18:23Z

I think https://github.com/kubernetes-sigs/kueue/pull/8220 should address this issue as well.
I'm assigning this issue o myself for now.

/assign @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-12T18:21:11Z

https://github.com/kubernetes-sigs/kueue/pull/8220 has merged now.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-12T18:21:17Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8200#issuecomment-3647629443):

>https://github.com/kubernetes-sigs/kueue/pull/8220 has merged now.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
