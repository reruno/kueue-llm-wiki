# Issue #1445: Non-leading replica fails due to not started cert-controller

**Summary**: Non-leading replica fails due to not started cert-controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1445

**Last updated**: 2023-12-27T14:00:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2023-12-12T18:14:13Z
- **Updated**: 2023-12-27T14:00:06Z
- **Closed**: 2023-12-22T09:43:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 22

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If I run two replicas the manager crashes after a while, it looks like that the healthiness probe fails and restarts the pod

**What you expected to happen**:

Both pods as running fine

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

```log
I1212 18:02:44.725166 1 leaderelection.go:250] attempting to acquire leader lease kueue-system/c1f6bfd2.kueue.x-k8s.io...
{"level":"info","ts":"2023-12-12T18:02:44.725142061Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *v1.Secret"}
{"level":"info","ts":"2023-12-12T18:02:44.726132561Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2023-12-12T18:02:44.726421287Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2023-12-12T18:02:44.726453798Z","caller":"controller/controller.go:186","msg":"Starting Controller","controller":"cert-rotator"}
{"level":"error","ts":"2023-12-12T18:04:44.726776367Z","caller":"controller/controller.go:203","msg":"Could not wait for Cache to sync","controller":"cert-rotator","error":"failed to wait for cert-rotator caches to sync: timed out waiting for cache to be synced for Kind *v1.Secret","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:203\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:208\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:234\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/runnable_group.go:223"}
{"level":"info","ts":"2023-12-12T18:04:44.72690754Z","caller":"manager/internal.go:516","msg":"Stopping and waiting for non leader election runnables"}
{"level":"info","ts":"2023-12-12T18:04:44.72693391Z","caller":"manager/internal.go:520","msg":"Stopping and waiting for leader election runnables"}
{"level":"error","ts":"2023-12-12T18:04:44.726934751Z","caller":"manager/internal.go:490","msg":"error received after stop sequence was engaged","error":"failed waiting for reader to sync","errorVerbose":"failed waiting for reader to sync\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:258\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/runnable_group.go:223\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_amd64.s:1650","stacktrace":"sigs.k8s.io/controller-runtime/pkg/manager.(*controllerManager).engageStopProcedure.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/internal.go:490"}
{"level":"info","ts":"2023-12-12T18:04:44.72773714Z","caller":"manager/internal.go:526","msg":"Stopping and waiting for caches"}
{"level":"info","ts":"2023-12-12T18:04:44.727923434Z","caller":"manager/internal.go:530","msg":"Stopping and waiting for webhooks"}
{"level":"info","ts":"2023-12-12T18:04:44.727976656Z","caller":"manager/internal.go:533","msg":"Stopping and waiting for HTTP servers"}
{"level":"info","ts":"2023-12-12T18:04:44.727990216Z","logger":"controller-runtime.metrics","caller":"server/server.go:231","msg":"Shutting down metrics server with timeout of 1 minute"}
{"level":"info","ts":"2023-12-12T18:04:44.727998496Z","caller":"manager/server.go:43","msg":"shutting down server","kind":"health probe","addr":"[::]:8081"}
{"level":"info","ts":"2023-12-12T18:04:44.728063958Z","caller":"manager/internal.go:537","msg":"Wait completed, proceeding to shutdown the manager"}
{"level":"error","ts":"2023-12-12T18:04:44.728084368Z","logger":"setup","caller":"kueue/main.go:182","msg":"Could not run manager","error":"failed to wait for cert-rotator caches to sync: timed out waiting for cache to be synced for Kind *v1.Secret","stacktrace":"main.main\n\t/workspace/cmd/kueue/main.go:182\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:267"}
```

**Environment**:
- Kubernetes version (use `kubectl version`): Server Version: v1.28.3-eks-4f4795d
- Kueue version (use `git describe --tags --dirty --always`): v0.5.1
- Cloud provider or hardware configuration: EKS
- OS (e.g: `cat /etc/os-release`): bottlerocket os
- Kernel (e.g. `uname -a`):
- Install tools: helm
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-12T19:00:50Z

/assign @trasc

### Comment by [@kbakk](https://github.com/kbakk) — 2023-12-13T08:47:29Z

I'm able to reproduce this in Kind:

```
$ kind create cluster --image kindest/node:v1.28.0
# on v0.5.1 tag in kueue repo
$ helm install  kueue charts/kueue/ --create-namespace --namespace kueue-system --set=controllerManager.replicas=2 --set=controllerManager.manager.image.tag=v0.5.1
```

The non-leader pod restarts after ~1.5 min and keeps restarting.

<details><summary>Logs:</summary>

```
{"level":"info","ts":"2023-12-13T08:43:32.418662328Z","logger":"setup","caller":"kueue/main.go:120","msg":"Initializing","gitVersion":"","gitCommit":""}
{"level":"info","ts":"2023-12-13T08:43:32.41998334Z","logger":"setup","caller":"kueue/main.go:385","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 100\n  qps: 50\ncontroller:\n  groupKindConcurrency:\n    ClusterQueue.kueue.x-k8s.io: 1\n    Job.batch: 5\n    LocalQueue.kueue.x-k8s.io: 1\n    ResourceFlavor.kueue.x-k8s.io: 1\n    Workload.kueue.x-k8s.io: 1\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\n  - kubeflow.org/mpijob\n  - ray.io/rayjob\n  - jobset.x-k8s.io/jobset\n  - kubeflow.org/mxjob\n  - kubeflow.org/paddlejob\n  - kubeflow.org/pytorchjob\n  - kubeflow.org/tfjob\n  - kubeflow.org/xgboostjob\n  podOptions:\n    namespaceSelector:\n      matchExpressions:\n      - key: kubernetes.io/metadata.name\n        operator: NotIn\n        values:\n        - kube-system\n        - kueue-system\n    podSelector: {}\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 0s\n  renewDeadline: 0s\n  resourceLock: \"\"\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 0s\nmanageJobsWithoutQueueName: false\nmetrics:\n  bindAddress: :8080\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"Level(-2)","ts":"2023-12-13T08:43:32.420171397Z","logger":"setup","caller":"kueue/main.go:136","msg":"K8S Client","qps":50,"burst":100}
{"level":"info","ts":"2023-12-13T08:43:32.43573053Z","logger":"setup","caller":"kueue/main.go:315","msg":"Probe endpoints are configured on healthz and readyz"}
{"level":"info","ts":"2023-12-13T08:43:32.435855285Z","logger":"setup","caller":"kueue/main.go:180","msg":"Starting manager"}
{"level":"info","ts":"2023-12-13T08:43:32.435892166Z","logger":"setup","caller":"kueue/main.go:217","msg":"Waiting for certificate generation to complete"}
{"level":"info","ts":"2023-12-13T08:43:32.435957174Z","caller":"manager/server.go:50","msg":"starting server","kind":"health probe","addr":"[::]:8081"}
{"level":"info","ts":"2023-12-13T08:43:32.435990491Z","logger":"controller-runtime.metrics","caller":"server/server.go:185","msg":"Starting metrics server"}
{"level":"info","ts":"2023-12-13T08:43:32.436136724Z","logger":"controller-runtime.metrics","caller":"server/server.go:224","msg":"Serving metrics server","bindAddress":":8080","secure":false}
{"level":"info","ts":"2023-12-13T08:43:32.537488746Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *v1.Secret"}
{"level":"info","ts":"2023-12-13T08:43:32.537563402Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2023-12-13T08:43:32.537578014Z","caller":"controller/controller.go:178","msg":"Starting EventSource","controller":"cert-rotator","source":"kind source: *unstructured.Unstructured"}
{"level":"info","ts":"2023-12-13T08:43:32.537587442Z","caller":"controller/controller.go:186","msg":"Starting Controller","controller":"cert-rotator"}
I1213 08:43:32.537593       1 leaderelection.go:250] attempting to acquire leader lease kueue-system/c1f6bfd2.kueue.x-k8s.io...
{"level":"error","ts":"2023-12-13T08:45:32.538752584Z","caller":"controller/controller.go:203","msg":"Could not wait for Cache to sync","controller":"cert-rotator","error":"failed to wait for cert-rotator caches to sync: timed out waiting for cache to be synced for Kind *v1.Secret","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:203\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:208\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:234\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/runnable_group.go:223"}
{"level":"info","ts":"2023-12-13T08:45:32.538943092Z","caller":"manager/internal.go:516","msg":"Stopping and waiting for non leader election runnables"}
{"level":"info","ts":"2023-12-13T08:45:32.539056196Z","caller":"manager/internal.go:520","msg":"Stopping and waiting for leader election runnables"}
{"level":"error","ts":"2023-12-13T08:45:32.539191455Z","caller":"manager/internal.go:490","msg":"error received after stop sequence was engaged","error":"failed waiting for reader to sync","errorVerbose":"failed waiting for reader to sync\ngithub.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start\n\t/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.10.0/pkg/rotator/rotator.go:258\nsigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/runnable_group.go:223\nruntime.goexit\n\t/usr/local/go/src/runtime/asm_amd64.s:1650","stacktrace":"sigs.k8s.io/controller-runtime/pkg/manager.(*controllerManager).engageStopProcedure.func1\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/manager/internal.go:490"}
{"level":"info","ts":"2023-12-13T08:45:32.541570151Z","caller":"manager/internal.go:526","msg":"Stopping and waiting for caches"}
{"level":"info","ts":"2023-12-13T08:45:32.541829866Z","caller":"manager/internal.go:530","msg":"Stopping and waiting for webhooks"}
{"level":"info","ts":"2023-12-13T08:45:32.541923813Z","caller":"manager/internal.go:533","msg":"Stopping and waiting for HTTP servers"}
{"level":"info","ts":"2023-12-13T08:45:32.541944674Z","logger":"controller-runtime.metrics","caller":"server/server.go:231","msg":"Shutting down metrics server with timeout of 1 minute"}
{"level":"info","ts":"2023-12-13T08:45:32.542043913Z","caller":"manager/server.go:43","msg":"shutting down server","kind":"health probe","addr":"[::]:8081"}
{"level":"info","ts":"2023-12-13T08:45:32.542234342Z","caller":"manager/internal.go:537","msg":"Wait completed, proceeding to shutdown the manager"}
{"level":"error","ts":"2023-12-13T08:45:32.542345851Z","logger":"setup","caller":"kueue/main.go:182","msg":"Could not run manager","error":"failed to wait for cert-rotator caches to sync: timed out waiting for cache to be synced for Kind *v1.Secret","stacktrace":"main.main\n\t/workspace/cmd/kueue/main.go:182\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:267"}
```

</details>

### Comment by [@kbakk](https://github.com/kbakk) — 2023-12-13T09:17:52Z

See the restarts on v0.5.0 as well. Not able to reproduce this on v0.4.2.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T14:37:25Z

Does it only reproduce with helm?
I wonder if this is the culprit https://github.com/kubernetes-sigs/kueue/pull/986

@yyzxw what did you base the probe configuration on?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T14:44:26Z

Maybe it is the probes implementations themselves that are wrong.
The behavior should be:
- The liveness probe should always be healthy if the pod is up.
- The readiness probe should be healthy if it's the leader

### Comment by [@woehrl01](https://github.com/woehrl01) — 2023-12-13T15:15:14Z

I've recently started using Kueue and I'm intrigued by its implementation. Given that it operates as an admission webhook, I'm wondering if there should be a redundancy system for the pods that manage the requests. Wouldn't it make sense for the non-leader pods to at least handle the admission webhooks, while the leader pod focuses also on background processing? Resulting in also returning readiness probe healthy if it's a non-leader.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T15:57:13Z

Yeah, ideally all replicas should reply to webhooks.

However, we recently introduced this feature https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-2-pending-workloads-visibility. In this case, only the leader can respond. Another alternative would be for non-leaders to also maintain the queues (we do this in kube-scheduler), so that they can also respond to api-extensions requests.

I'm not actually sure about what is the behavior that controller-runtime applies.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-14T13:11:51Z

controller-runtime exposes the `LeaderElectionRunnable` interface, so controllers can implement its `NeedLeaderElection` method to control whether the manager should start them in non-leader instances. Also managed webhooks are always started, irrespective of leader election.

In the case of the OPA cert-controller, there is a `RequireLeaderElection` option, that's correctly set by Kueue, but I suspect there is an issue in cert-controller that makes it not taken into account, which is the root cause of that issue. I'll fix it upstream.

For the visibility extension API server, we would need to make sure it's safe to run multiple instances of ClusterQueueReconciler concurrently, or find a way to only run the read-only part?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-14T13:12:01Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-12-14T14:03:21Z

@astefanutti do you want to on this?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-14T14:07:51Z

@trasc yes I can work on it. There is only the part about the visibility API server HA, I may need your input on this. But that may be tackled separately.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:03:22Z

/unassign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:06:35Z

> For the visibility extension API server, we would need to make sure it's safe to run multiple instances of ClusterQueueReconciler concurrently, or find a way to only run the read-only part?

That might be tricky. The CQReconciler updates status based on usage. If each replica maintains the cache and queues, in theory the usage should be in sync, but we could face race conditions. Ideally we would only like to run the event handlers, but not the reconciler itself.

Is there a boolean given by the interface that can tell us whether it's the leader? Then we can just return `false` from the event handlers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:07:57Z

> In the case of the OPA cert-controller, there is a RequireLeaderElection option, that's correctly set by Kueue, but I suspect there is an issue in cert-controller that makes it not taken into account, which is the root cause of that issue. I'll fix it upstream.

Do you mean you'll fix ca-cert itself? I wonder if this somehow related to the e2e failures that we are seeing: https://github.com/kubernetes-sigs/kueue/issues/1372#issuecomment-1854746503

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:38:26Z

For the sake of truthfulness

/retitle Non-leading replica is restarted due to inaccurate probe implementation

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-14T17:17:42Z

> Is there a boolean given by the interface that can tell us whether it's the leader? Then we can just return `false` from the event handlers.

controller-runtime `Manager` interface exposes a `Elected() <-chan struct{}` method, that returns a channel that's closed only when that manager has been leader elected (or leader election is disabled). So in theory, it could be possible to pass it to the ClusterQueueReconciler, and adapt the handlers logic depending on it.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-14T17:23:33Z

> > In the case of the OPA cert-controller, there is a RequireLeaderElection option, that's correctly set by Kueue, but I suspect there is an issue in cert-controller that makes it not taken into account, which is the root cause of that issue. I'll fix it upstream.
> 
> Do you mean you'll fix ca-cert itself?

I mean I'll fix the following issue in cert-controller itself (assuming my analysis is correct), and upgrade the cert-controller dependency in Kueue:

```
Could not wait for Cache to sync","controller":"cert-rotator","error":"failed to wait for cert-rotator caches to sync: timed out waiting for cache to be synced for Kind *v1.Secret
```

> I wonder if this somehow related to the e2e failures that we are seeing: [#1372 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1372#issuecomment-1854746503)

I need to look more at how the e2e tests are setup. I'll check it once I have the fix.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-15T16:08:07Z

I've open open-policy-agent/cert-controller#166 that fixes the cache timeout issue in cert-controller.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-19T18:55:41Z

@astefanutti can you explain why the binary is terminating given the bug in cert-controller?

I thought this had something to do with the probes, but our probes just use Ping, which would return Ready/Live if the binary is able to respond to the Http request.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-19T19:14:56Z

> @astefanutti can you explain why the binary is terminating given the bug in cert-controller?
> 
> I thought this had something to do with the probes, but our probes just use Ping, which would return Ready/Live if the binary is able to respond to the Http request.

@alculquicondor right, I don't think it has something to do with the probes.

So what happens in the non-leader elected mode is the following:
- cert-controller is added to the manager (as a runnable)
- the manager starts
- the cert-controller runnable is started
- that waits for its cache to sync, but that cache is never started (because controller-runtime defaults to starting runnables only in the leader-elected instance)
- the above calls times out and returns an error
- the manager start call return an error, which is confirmed by the `Could not run manager` message
- the binary exits

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-22T09:33:04Z

A new version of cert-controller has been released with the fix, and I've open #1509 that upgrades our dependency. That fixes the non-leading replicas starting issue.

I've also open #1510 to track the work for making the visibility extension API server highly available.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T14:00:05Z

Thanks a lot for fixing this!
