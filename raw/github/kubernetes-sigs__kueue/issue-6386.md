# Issue #6386: [MultiKueue flake] MultiKueue with custom configs when Dispatcher Incremental mode Should run a job on worker if admitted

**Summary**: [MultiKueue flake] MultiKueue with custom configs when Dispatcher Incremental mode Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6386

**Last updated**: 2025-11-14T18:46:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-04T05:58:52Z
- **Updated**: 2025-11-14T18:46:21Z
- **Closed**: 2025-11-14T18:46:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

failure
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6385/pull-kueue-test-e2e-multikueue-main/1952242863169343488

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:


ci

**Anything else we need to know?**:
```
{Expected success, but got an error:
    <*errors.StatusError | 0xc000bcd180>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000bcd180>: 
    Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe
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
            Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": write tcp 172.18.0.5:33638->10.244.1.7:9443: write: broken pipe",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/customconfigs_test.go:109 @ 08/04/25 05:55:37.68
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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T05:58:58Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T05:59:02Z

cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T06:01:16Z

Oh, this started to flake again after splitting out the tests into files, because "when The connection to a worker cluster is unreliable" was running first. This test is clearly the culprit as it does not clear the cluster after itself properly. 

As a temporary measure we could revert https://github.com/kubernetes-sigs/kueue/pull/6356

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T07:37:29Z

fyi: https://github.com/kubernetes-sigs/kueue/issues/6399

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T09:02:07Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:51:04Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:51:30Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-main/1988378724294201344

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T18:46:15Z

/close
seeing webhook failures it looks likely solved by https://github.com/kubernetes-sigs/kueue/pull/7666

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-14T18:46:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6386#issuecomment-3534112688):

>/close
>seeing webhook failures it looks likely solved by https://github.com/kubernetes-sigs/kueue/pull/7666


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
