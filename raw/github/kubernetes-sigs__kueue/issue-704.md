# Issue #704: [Flaky] ResourceFlavor controller when one clusterQueue references resourceFlavors Should delete the resourceFlavor when the corresponding clusterQueue no longer uses the resourceFlavor

**Summary**: [Flaky] ResourceFlavor controller when one clusterQueue references resourceFlavors Should delete the resourceFlavor when the corresponding clusterQueue no longer uses the resourceFlavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/704

**Last updated**: 2023-06-13T19:18:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-18T07:49:56Z
- **Updated**: 2023-06-13T19:18:01Z
- **Closed**: 2023-06-13T19:18:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@mcariatm](https://github.com/mcariatm), [@trasc](https://github.com/trasc)
- **Comments**: 15

## Description

**What happened**:

Flaky test:

```
ResourceFlavor controller when one clusterQueue references resourceFlavors Should delete the resourceFlavor when the corresponding clusterQueue no longer uses the resourceFlavor
```

```
{Timed out after 30.001s.
Expected success, but got an error:
    <*errors.StatusError | 0xc00062ca00>: 
    resourceflavors.kueue.x-k8s.io "flavor" not found
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
            Message: "resourceflavors.kueue.x-k8s.io \"flavor\" not found",
            Reason: "NotFound",
            Details: {
                Name: "flavor",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    } failed [FAILED] Timed out after 30.001s.
Expected success, but got an error:
    <*errors.StatusError | 0xc00062ca00>: 
    resourceflavors.kueue.x-k8s.io "flavor" not found
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
            Message: "resourceflavors.kueue.x-k8s.io \"flavor\" not found",
            Reason: "NotFound",
            Details: {
                Name: "flavor",
                Group: "kueue.x-k8s.io",
                Kind: "resourceflavors",
                UID: "",
                Causes: nil,
                RetryAfterSeconds: 0,
            },
            Code: 404,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/resourceflavor_controller_test.go:85 @ 04/17/23 19:11:13.438
}
```

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/703/pull-kueue-test-integration-main/1648040056281108480

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

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-18T07:58:20Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-03T15:17:04Z

We discussed this offline.
We only saw this fail once and we can't reproduce. It also doesn't show in the periodic testgrid https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main&width=20

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-03T15:17:08Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/704#issuecomment-1533230126):

>We discussed this offline.
>We only saw this fail once and we can't reproduce. It also doesn't show in the periodic testgrid https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main&width=20
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-04T07:57:53Z

/reopen
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/742/pull-kueue-test-integration-main/1654022279161450496

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-04T07:57:56Z

@mcariatm: You can't reopen an issue/PR unless you authored it or you are a collaborator.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/704#issuecomment-1534251969):

>/reopen
>https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/742/pull-kueue-test-integration-main/1654022279161450496


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-04T07:58:40Z

@alculquicondor please reopen this issue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-04T07:58:58Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-04T07:59:02Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/704#issuecomment-1534253299):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-04T12:22:15Z

(Just for reference)
Seen in #742, which doesn't change any code

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-08T09:12:32Z

Is not the same issue. I think the old one's gone. Now we received:
Message: "Operation cannot be fulfilled on clusterqueues.kueue.x-k8s.io \"foo\": the object has been modified; please apply your changes to the latest version and try again",
Code: 409

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-08T09:20:55Z

> Is not the same issue. I think the old one's gone. Now we received: Message: "Operation cannot be fulfilled on clusterqueues.kueue.x-k8s.io "foo": the object has been modified; please apply your changes to the latest version and try again", Code: 409

@mcariatm Can you share the full error log, like the description of this issue?

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-05-08T09:28:51Z

> > Is not the same issue. I think the old one's gone. Now we received: Message: "Operation cannot be fulfilled on clusterqueues.kueue.x-k8s.io "foo": the object has been modified; please apply your changes to the latest version and try again", Code: 409
> 
> @mcariatm Can you share the full error log, like the description of this issue?

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/742/pull-kueue-test-integration-main/1654022279161450496

I fixed it here :
https://github.com/kubernetes-sigs/kueue/pull/748

### Comment by [@trasc](https://github.com/trasc) — 2023-06-13T11:24:32Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-06-13T11:24:36Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/704#issuecomment-1589107632):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-06-13T11:24:41Z

/assign
