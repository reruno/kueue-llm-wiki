# Issue #2073: Single cluster e2e tests for pods fail to start occasionally

**Summary**: Single cluster e2e tests for pods fail to start occasionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2073

**Last updated**: 2024-07-08T11:20:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-26T07:58:52Z
- **Updated**: 2024-07-08T11:20:52Z
- **Closed**: 2024-07-08T11:20:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

/kind flake

**What happened**:

Failure on an unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2071/pull-kueue-test-e2e-main-1-28/1783763066844876800

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build, and it will fail occasionally.

The error suggests the webhooks are not ready yet.
```
{Expected success, but got an error:
    <*errors.StatusError | 0xc00029cbe0>: 
    Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": read tcp 172.18.0.3:40472->10.244.1.3:9443: read: connection reset by peer
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
            Message: "Internal error occurred: failed calling webhook \"mjob.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s\": read tcp 172.18.0.3:40472->10.244.1.3:9443: read: connection reset by peer",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"mjob.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s\": read tcp 172.18.0.3:40472->10.244.1.3:9443: read: connection reset by peer",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00029cbe0>: 
    Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": read tcp 172.18.0.3:40472->10.244.1.3:9443: read: connection reset by peer
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-17T17:49:07Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2412/pull-kueue-test-e2e-main-1-27/1802757113089363968

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-07-08T08:39:24Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-07-08T11:16:31Z

The kueue-controller-manager was down due to panic - fixed [here](https://github.com/kubernetes-sigs/kueue/pull/2461/files), thus webhook can not be handled. 
Failed test:
```
> Enter [It] Should suspend a job when its checks become invalid - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:433 @ 04/26/24 07:45:26.034
[FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00029cbe0>: 
    Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": read tcp 172.18.0.3:40472->10.244.1.3:9443: read: connection reset by peer
```

Panic on queue-controller-manager:
```
2024-04-26T07:45:26.030448574Z stderr F 2024-04-26T07:45:26.030324533Z	INFO	controller/controller.go:115	Observed a panic in reconciler: runtime error: invalid memory address or nil pointer dereference	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"cluster-queue"}, "namespace": "", "name": "cluster-queue", "reconcileID": "b50f4365-3ff5-4a70-8a82-9f9b113f4694"}
```

As mentioned this has been already fixed.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-08T11:20:47Z

@mszadkow thank you for the investigation. sounds great.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-08T11:20:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2073#issuecomment-2213747032):

>@mszadkow thank you for the investigation. sounds great.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
