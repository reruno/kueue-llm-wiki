# Issue #7650: [flaky test] MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster

**Summary**: [flaky test] MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7650

**Last updated**: 2025-12-10T08:58:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-13T19:06:46Z
- **Updated**: 2025-12-10T08:58:51Z
- **Closed**: 2025-12-10T08:58:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description


**What happened**:

failure on unrelated branch : https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7316/pull-kueue-test-e2e-multikueue-main/1988971533585879040

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Expected success, but got an error:
    <*errors.StatusError | 0xc000d9e140>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s": dial tcp 10.244.1.8:9443: connect: connection refused
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": dial tcp 10.244.1.8:9443: connect: connection refused",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": dial tcp 10.244.1.8:9443: connect: connection refused",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000d9e140>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s": dial tcp 10.244.1.8:9443: connect: connection refused
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": dial tcp 10.244.1.8:9443: connect: connection refused",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta2-resourceflavor?timeout=10s\": dial tcp 10.244.1.8:9443: connect: connection refused",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/tas_test.go:135 @ 11/13/25 14:26:25.95
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:58:45Z

/close
Since this failed test was triggered after "The connection to a worker cluster is unreliable", and we have recently improved stability of testing after that disruptive test: https://github.com/kubernetes-sigs/kueue/pull/7666

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-10T08:58:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7650#issuecomment-3636038974):

>/close
>Since this failed test was triggered after "The connection to a worker cluster is unreliable", and we have recently improved stability of testing after that disruptive test: https://github.com/kubernetes-sigs/kueue/pull/7666


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
