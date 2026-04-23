# Issue #6233: [Flaky E2E] MultiKueue with Incremental mode Should run a job on worker if admitted

**Summary**: [Flaky E2E] MultiKueue with Incremental mode Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6233

**Last updated**: 2025-08-01T12:37:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-07-29T09:13:26Z
- **Updated**: 2025-08-01T12:37:38Z
- **Closed**: 2025-08-01T12:37:38Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End MultiKueue Suite: kindest/node:v1.33.1: [It] MultiKueue with Incremental mode Should run a job on worker if admitted 

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc000b91900>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000b91900>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.7:59888->10.244.1.7:9443: write: connection reset by peer",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [BeforeAll] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:1031 @ 07/29/25 09:05:11.601
}
```

**What you expected to happen**:
No errors 

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5174/pull-kueue-test-e2e-multikueue-main/1950115850333720576

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-29T09:13:36Z

/cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T13:56:31Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6287/pull-kueue-test-e2e-multikueue-main/1950551855390003200

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T14:01:08Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6284/pull-kueue-test-e2e-multikueue-main/1950537174688468992

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-30T16:19:14Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T08:15:35Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6297/pull-kueue-test-e2e-multikueue-main/1950828015646674944

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T08:15:46Z

seems like the most common flake currently

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-07-31T09:17:11Z

Yes, there is nothing wrong with the test itself, I am 99% positive about that.
I have checked all the logs etc. every time it's the same pattern with the webhook, before the test even really starts.
However as @mbobrovskyi mentioned the other test might ruin this one's performance - 
`The connection to a worker cluster is unreliable`.
I try to move this test in the hierarchy to eliminate flakiness, but `The connection to a worker cluster is unreliable` is the one that has to be fixed.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T09:27:47Z

> I try to move this test in the hierarchy to eliminate flakiness, but The connection to a worker cluster is unreliable is the one that has to be fixed.

Because the "The connection to a worker cluster is unreliable" test breaks the connectivity between the clusters? This could make sense. If this is the case then indeed it is responsibility of this test to restore the connection and test it is ok.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T09:30:48Z

OTOH, it does not quite make sense, the test disrupts connectivity between clusters, not within a cluster. The webhook failures suggest requests failing *within* the cluster. I don't think we would directly call webhooks from external cluster.

Given how common the flake is I wouldn't assume it is network issue within cluster (these are super rare). The most likely explanation for such errors is that Kueue (which hosts the webhooks) is non-responsible (for example restarting or crashing).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T15:21:55Z

still flake https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6329/pull-kueue-test-e2e-multikueue-release-0-13/1950934478683639808

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-01T07:05:42Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6345/pull-kueue-test-e2e-multikueue-main/1951172197842161664
