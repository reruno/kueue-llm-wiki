# Issue #1700: MultiKueue e2e test flaky on startup

**Summary**: MultiKueue e2e test flaky on startup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1700

**Last updated**: 2024-02-12T13:26:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-02-07T16:18:53Z
- **Updated**: 2024-02-12T13:26:05Z
- **Closed**: 2024-02-09T15:15:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

e2e test failed on docs PR.

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

 https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1684/pull-kueue-test-e2e-main-1-29/1755244756142657536


**Anything else we need to know?**:

This is the message:
```
> Enter [BeforeEach] MultiKueue - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:69 @ 02/07/24 15:11:34.098
[FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0001406e0>: 
    Internal error occurred: failed calling webhook "vadmissioncheck.kb.io": failed to call webhook: the server could not find the requested resource
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
            Message: "Internal error occurred: failed calling webhook \"vadmissioncheck.kb.io\": failed to call webhook: the server could not find the requested resource",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vadmissioncheck.kb.io\": failed to call webhook: the server could not find the requested resource",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
```
The fix to startup Kueue was recently done: https://github.com/kubernetes-sigs/kueue/pull/1676
This seems similar, but slightly different, because this time the kueue logs show one of the managers was killed `kueue-controller-manager-57858fc6bb-xvbgg` and restarted after 1min, probably hitting some timeout (https://storage.googleapis.com/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1684/pull-kueue-test-e2e-main-1-29/1755244756142657536/artifacts/run-test-multikueue-e2e-1.29.0/kind-manager-kueue-system-pods.log):

```
Name:             kueue-controller-manager-57858fc6bb-xvbgg
Namespace:        kueue-system
Priority:         0
Service Account:  kueue-controller-manager
Node:             kind-manager-control-plane/172.18.0.2
Start Time:       Wed, 07 Feb 2024 15:08:35 +0000
Labels:           control-plane=controller-manager
                  pod-template-hash=57858fc6bb
Annotations:      kubectl.kubernetes.io/default-container: manager
Status:           Running
IP:               10.244.0.6
IPs:
  IP:           10.244.0.6
Controlled By:  ReplicaSet/kueue-controller-manager-57858fc6bb
Containers:
  manager:
    Container ID:  containerd://7faccc1023e13b4e48ad495114e48c739b7cd1a23750426a24070e535c9bf7a9
    Image:         gcr.io/k8s-staging-kueue/kueue:v0.6.0-rc.1-37-gdba0454
    Image ID:      docker.io/library/import-2024-02-07@sha256:17e63be0a74e8ee4f7ba279e23f7a46945f4aab52f628c89f1de3aa3b2d0d574
    Ports:         8082/TCP, 9443/TCP
    Host Ports:    0/TCP, 0/TCP
    Command:
      /manager
    Args:
      --config=/controller_manager_config.yaml
      --zap-devel
      --zap-log-level=3
      --feature-gates=VisibilityOnDemand=true,MultiKueue=true
    State:          Running
      Started:      Wed, 07 Feb 2024 15:10:37 +0000
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Wed, 07 Feb 2024 15:08:36 +0000
      Finished:     Wed, 07 Feb 2024 15:10:36 +0000
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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-07T16:19:57Z

/kind flake
/cc @alculquicondor @trasc @tenzen-y 
This seems a slightly different scenario as before, because one of the managers was killed, not sure how common this is for now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-07T16:36:41Z

IIRC, we decided that we should increase resource requests: https://github.com/kubernetes-sigs/kueue/issues/1658#issuecomment-1917980173

Maybe we still don't increase resource requests.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-07T16:42:33Z

> Maybe we still don't increase resource requests.

I didn't update the requests indeed, not sure this would help, but we can try.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-07T17:14:46Z

Did you check the kueue-manager logs? Maybe this is a crash. The logs should be in the artifacts.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-07T17:15:21Z

/assign @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-08T07:56:57Z

> Did you check the kueue-manager logs? Maybe this is a crash. 

Yeah, I checked the logs and definitely there was a restart of the controller as shown in the description snippet of logs:
```
   Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Wed, 07 Feb 2024 15:08:36 +0000
      Finished:     Wed, 07 Feb 2024 15:10:36 +0000
```
It is not clear to me if it crashed, but it looks more like some timeout. Here are the last logs of the terminated manager:
```
2024-02-07T15:10:36.3342151Z stderr F 2024-02-07T15:10:36.334001148Z	DEBUG	controller-runtime.healthz	healthz/healthz.go:60	healthz check failed	{"checker": "readyz", "error": "webhook server has not been started yet"}
2024-02-07T15:10:36.334256941Z stderr F 2024-02-07T15:10:36.33414449Z	INFO	controller-runtime.webhook	webhook/server.go:191	Starting webhook server
2024-02-07T15:10:36.334330392Z stderr F 2024-02-07T15:10:36.334239361Z	INFO	manager/internal.go:516	Stopping and waiting for non leader election runnables
2024-02-07T15:10:36.334336152Z stderr F 2024-02-07T15:10:36.334071679Z	INFO	controller-runtime.healthz	healthz/healthz.go:128	healthz check failed	{"statuses": [{}]}
2024-02-07T15:10:36.334581154Z stderr F 2024-02-07T15:10:36.334390832Z	INFO	cert-rotation	rotator/rotator.go:306	stopping cert rotator controller
2024-02-07T15:10:36.334592184Z stderr F 2024-02-07T15:10:36.334442433Z	INFO	controller/controller.go:240	Shutdown signal received, waiting for all workers to finish	{"controller": "cert-rotator"}
2024-02-07T15:10:36.334596414Z stderr F 2024-02-07T15:10:36.334474883Z	INFO	controller/controller.go:242	All workers finished	{"controller": "cert-rotator"}
2024-02-07T15:10:36.334605584Z stderr F 2024-02-07T15:10:36.334501463Z	INFO	manager/internal.go:520	Stopping and waiting for leader election runnables
2024-02-07T15:10:36.334609054Z stderr F 2024-02-07T15:10:36.334547314Z	INFO	manager/internal.go:526	Stopping and waiting for caches
2024-02-07T15:10:36.334919938Z stderr F 2024-02-07T15:10:36.334769556Z	INFO	manager/internal.go:530	Stopping and waiting for webhooks
2024-02-07T15:10:36.334970688Z stderr F 2024-02-07T15:10:36.334831817Z	INFO	manager/internal.go:533	Stopping and waiting for HTTP servers
2024-02-07T15:10:36.334976048Z stderr F 2024-02-07T15:10:36.334860157Z	INFO	controller-runtime.metrics	server/server.go:231	Shutting down metrics server with timeout of 1 minute
2024-02-07T15:10:36.335094619Z stderr F 2024-02-07T15:10:36.334934448Z	INFO	manager/server.go:43	shutting down server	{"kind": "health probe", "addr": "[::]:8081"}
2024-02-07T15:10:36.33516266Z stderr F 2024-02-07T15:10:36.335072179Z	INFO	manager/internal.go:537	Wait completed, proceeding to shutdown the manager
2024-02-07T15:10:36.335286371Z stderr F 2024-02-07T15:10:36.33514391Z	ERROR	setup	kueue/main.go:189	Could not run manager	{"error": "open /tmp/k8s-webhook-server/serving-certs/tls.crt: no such file or directory"}
2024-02-07T15:10:36.335292771Z stderr F main.main
2024-02-07T15:10:36.335295992Z stderr F 	/workspace/cmd/kueue/main.go:189
2024-02-07T15:10:36.335298912Z stderr F runtime.main
2024-02-07T15:10:36.335301482Z stderr F 	/usr/local/go/src/runtime/proc.go:267
```

### Comment by [@trasc](https://github.com/trasc) — 2024-02-09T07:14:18Z

/reopen 

For time-out and potentially resource changes

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-09T07:14:22Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1700#issuecomment-1935437657):

>/reopen 
>
>For time-out and potentially resource changes


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-09T07:22:35Z

Indeed, the failures may still happen currently, like this one: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1707/pull-kueue-test-e2e-main-1-27/1755619946483683328

### Comment by [@trasc](https://github.com/trasc) — 2024-02-09T10:28:31Z

#1710 opened , now we log the time it takes to wait for the clusters to be ready, we can use this info to adapt the timeout in the future. (on my local setup it kake 58 - 105 sec).

@tenzen-y  Regarding the resources , we are currently requesting 10CPU and 10G  , do we need more?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-09T15:19:45Z

@alculquicondor I think we should cherry-pick https://github.com/kubernetes-sigs/kueue/pull/1707 and https://github.com/kubernetes-sigs/kueue/pull/1710. Especially 1707, because it may affect users.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T15:29:07Z

The impact is minimal, users will be able to retry.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-09T15:33:54Z

> The impact is minimal, users will be able to retry.

Potentially, but it might be an annoyance. Also, if we run the e2e tests for Kueue historical release they may be flaking, and each failure may cause people to look / investigate, even briefly, just to confirm "this is known issue".

### Comment by [@trasc](https://github.com/trasc) — 2024-02-09T15:39:06Z

#1713 done for #1707 (sice the bot was able to do it)

#1710 will need manual work, and since the two major players involved in triggering this HA + MultiKueue are not 0.5 we can skip #1710

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-12T13:26:04Z

> #1710 opened , now we log the time it takes to wait for the clusters to be ready, we can use this info to adapt the timeout in the future. (on my local setup it kake 58 - 105 sec).
> 
> @tenzen-y Regarding the resources , we are currently requesting 10CPU and 10G , do we need more?

@trasc As I can see the metrics, the resources should be enough: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=periodic-kueue-test-e2e-main-1-28&var-build=All&refresh=30s

So, Increasing resources should not be needed. Thanks for this fixing.
