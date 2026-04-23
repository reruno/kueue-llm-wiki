# Issue #8937: [Flaky MultiKueue E2E] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster (webhooks)

**Summary**: [Flaky MultiKueue E2E] MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster (webhooks)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8937

**Last updated**: 2026-02-16T10:49:22Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-02T15:15:23Z
- **Updated**: 2026-02-16T10:49:22Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 9

## Description

**Which test is flaking?**:

MultiKueue when Connection via ClusterProfile with plugins Should be able to use ClusterProfile as way to connect worker cluster (webhooks)

**First observed in** (PR or commit, if known):
don't know
**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2017955730673373184

**Failure message or logs**:
```
  "level"=0 "msg"="Kueue configuration updated" "took"="25.551143234s"
  �[38;5;9m[FAILED]�[0m in [BeforeEach] - /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514 �[38;5;243m@ 02/01/26 14:01:51.547�[0m
  �[1mSTEP:�[0m reverting the configuration �[38;5;243m@ 02/01/26 14:01:51.554�[0m
  Exporting logs for cluster "kind-manager" to:
  /logs/artifacts/run-test-multikueue-e2e-1.34.0
  "level"=0 "msg"="Deployment status condition before the restart" "type"="Progressing" "status"="True" "reason"="NewReplicaSetAvailable"
  �[1mSTEP:�[0m Waiting for availability of deployment: "kueue-system/kueue-controller-manager" �[38;5;243m@ 02/01/26 14:02:16.583�[0m
  "level"=0 "msg"="Deployment is available in the cluster" "deployment"={"name"="kueue-controller-manager" "namespace"="kueue-system"} "waitingTime"="3.503811ms"
  �[1mSTEP:�[0m Waiting for deployment to have only available replicas: "kueue-system/kueue-controller-manager" �[38;5;243m@ 02/01/26 14:02:16.587�[0m
  "level"=0 "msg"="Deployment has only available replicas in the cluster" "deployment"={"name"="kueue-controller-manager" "namespace"="kueue-system"} "waitingTime"="3.618004ms"
  �[1mSTEP:�[0m Waiting for leader election lease "kueue-system/c1f6bfd2.kueue.x-k8s.io" �[38;5;243m@ 02/01/26 14:02:16.59�[0m
�[38;5;9m• [FAILED] [54.942 seconds]�[0m
�[0mMultiKueue �[38;5;9m�[1mwhen Connection via ClusterProfile no plugins [BeforeEach] �[0muses ClusterProfile as way to connect worker cluster�[0m
  �[38;5;9m[BeforeEach]�[0m �[38;5;243m/home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1512�[0m
  �[38;5;243m[It] /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1522�[0m

  �[38;5;9m[FAILED] Expected success, but got an error:
      <*errors.StatusError | 0xc0009855e0>: 
      conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
              Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
              Reason: "",
              Details: nil,
              Code: 500,
          },
      }�[0m
  �[38;5;9mIn �[1m[BeforeEach]�[0m�[38;5;9m at: �[1m/home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514�[0m �[38;5;243m@ 02/01/26 14:01:51.547�[0m
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T15:57:57Z

I think what might have happened here is that we observed spec.Replicas=1; status.AvailableReplicas=1, but the test informer could still see 2 Ready Pods. As a consequence it checked against 2 ready endpoints, and there was still a stale endpoint, allowing for the bad request.

I think this is possible, becuase in the [API server logs](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2017955730673373184/artifacts/run-test-multikueue-e2e-1.34.0/kind-manager-control-plane/pods/kube-system_kube-apiserver-kind-manager-control-plane_6fad80801f035a85852bc5734801effd/kube-apiserver/0.log) I can see the endpoints being updated only at `2026-02-01T14:02:05.429750461Z` (before the update), then at `2026-02-01T14:02:16.438366701Z` (just around the failure, but hard to say super precisely if before of after).

I would propose to make sure the set of Ready Pods is of size 1 also, then we can be sure we have only 1 endpoint.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T16:11:08Z

ptal: https://github.com/kubernetes-sigs/kueue/pull/8939

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-03T18:10:34Z

should be addressed by https://github.com/kubernetes-sigs/kueue/pull/8941

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-03T18:10:41Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-03T18:10:47Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8937#issuecomment-3842864129):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T23:02:26Z

Again this at release-0.15 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2022668151992356864

/reopen

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000a73220>: 
    conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000a73220>: 
    conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
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
            Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [BeforeEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514 @ 02/14/26 14:05:51.599
}
```

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-14T23:02:32Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8937#issuecomment-3902750525):

>Again this at release-0.15 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2022668151992356864
>
>/reopen
>
>```shell
>{Expected success, but got an error:
>    <*errors.StatusError | 0xc000a73220>: 
>    conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
>    {
>        ErrStatus: {
>            TypeMeta: {Kind: "", APIVersion: ""},
>            ListMeta: {
>                SelfLink: "",
>                ResourceVersion: "",
>                Continue: "",
>                RemainingItemCount: nil,
>            },
>            Status: "Failure",
>            Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
>            Reason: "",
>            Details: nil,
>            Code: 500,
>        },
>    } failed [FAILED] Expected success, but got an error:
>    <*errors.StatusError | 0xc000a73220>: 
>    conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
>    {
>        ErrStatus: {
>            TypeMeta: {Kind: "", APIVersion: ""},
>            ListMeta: {
>                SelfLink: "",
>                ResourceVersion: "",
>                Continue: "",
>                RemainingItemCount: nil,
>            },
>            Status: "Failure",
>            Message: "conversion webhook for kueue.x-k8s.io/v1beta2, Kind=MultiKueueCluster failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
>            Reason: "",
>            Details: nil,
>            Code: 500,
>        },
>    }
>In [BeforeEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:1514 @ 02/14/26 14:05:51.599
>}
>```


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T08:40:42Z

This seems the only test now failing which restarts Kueue configuration. What makes it different is that we are changing two things at the same time: Kueue configuration and deployment configuration. I'm wondering if it would be easier to debug, and likely fix the issue if we wait for the Deployment to be fully ready before proceeding with configuration upgrade. 

Wdyt @mbobrovskyi , to introduce the wait for the deployment available before configuration change?

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:49:20Z

/area multikueue
