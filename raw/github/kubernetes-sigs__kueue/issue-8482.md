# Issue #8482: Operation cannot be fulfilled on workloads.kueue.x-k8s.io, the object has been modified

**Summary**: Operation cannot be fulfilled on workloads.kueue.x-k8s.io, the object has been modified

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8482

**Last updated**: 2026-01-10T12:23:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@TaylorTrz](https://github.com/TaylorTrz)
- **Created**: 2026-01-09T01:45:37Z
- **Updated**: 2026-01-10T12:23:40Z
- **Closed**: 2026-01-10T12:23:39Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Integrate pod support into kueue, following a  instruction by this link:
https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/

However, a plain pod was killed instantially after created, and then event shows message like:

```
message: Missing Workload; unable to restore pod templates
```

And kueue-controller-manager error out with:

```
Operation cannot be fulfilled on workloads.kueue.x-k8s.io, the object has been modified
```


**What you expected to happen**:

The plain pod's state was expected to be `Running` rather than `Terminating`.


**How to reproduce it (as minimally and precisely as possible)**:

1. Deploying kueue by helm template, while `managedJobsNamespaceSelector` and  `integrations` were modified:

```yaml
controllerManagerConfigYaml: |-
  apiVersion: config.kueue.x-k8s.io/v1beta2
  kind: Configuration
  managedJobsNamespaceSelector:
    matchExpressions:
      - key: kubernetes.io/metadata.name
        operator: NotIn
        values: [ kube-system, kueue-system ]
  integrations:
    frameworks:
    - "pod"
    - "deployment"
    - "statefulset"
    - "leaderworkerset.x-k8s.io/leaderworkerset"
```

2. Applying a plain pod into k8s cluster, with label `kueue.x-k8s.io/queue-name: user-queue`:

```
---
apiVersion: v1
kind: Pod
metadata:
  name: gpu-kueue-pod-2
  labels:
     kueue.x-k8s.io/queue-name: user-queue
spec:
  restartPolicy: Always
  containers:
    - name: test
      image: docker.inspur.com:5000/library/cke/kubernetes/pause:3.8
      resources:
        limits:
          cpu: 10m
          memory: 256Mi

# kubectl apply  -f pod-example.yaml
pod/gpu-kueue-pod-1 created
```

3. Watching pod and workloads, the pod and workload were created, and instantly terminated.

```
# kubectl get po -w
NAME       READY   STATUS    RESTARTS   AGE
vllm-0     1/1     Running   0          17h
vllm-0-0   1/1     Running   0          17h
gpu-kueue-pod-2   0/1     Pending       0          0s
gpu-kueue-pod-2   0/1     Pending       0          0s
gpu-kueue-pod-2   0/1     Pending       0          0s
gpu-kueue-pod-2   0/1     Terminating   0          0s
gpu-kueue-pod-2   0/1     Terminating   0          0s
gpu-kueue-pod-2   0/1     Terminating   0          0s
gpu-kueue-pod-2   1/1     Terminating   0          14s
gpu-kueue-pod-2   0/1     Terminating   0          15s
gpu-kueue-pod-2   0/1     Terminating   0          16s
gpu-kueue-pod-2   0/1     Terminating   0          16s

# kubectl get workloads -w
NAME                           QUEUE            RESERVED IN   ADMITTED   FINISHED   AGE
job-sample-job-l88rg-9a1c1     user-queue                                           12h
leaderworkerset-vllm-0-68909   user-queue-gpu                                       17h
pod-gpu-kueue-pod-2-09669      user-queue                                           0s
pod-gpu-kueue-pod-2-09669      user-queue                                           0s
pod-gpu-kueue-pod-2-09669      user-queue                                           0s
pod-gpu-kueue-pod-2-09669      user-queue                                           16s
```

4. Watching k8s event, pod stopped with message `Missing Workload; unable to restore pod templates`:

```
# kubectl get events  --sort-by {.lastTimestamp}  -w
0s          Normal    Pulled                    pod/gpu-kueue-pod-2   Container image "docker.inspur.com:5000/library/cke/kubernetes/pause:3.8" already present on machine
0s          Normal    Created                   pod/gpu-kueue-pod-2   Created container test
0s          Normal    Started                   pod/gpu-kueue-pod-2   Started container test
0s          Normal    Killing                   pod/gpu-kueue-pod-2   Stopping container test
0s          Normal    Scheduled                 pod/gpu-kueue-pod-2   Successfully assigned default/gpu-kueue-pod-2 to master01
0s          Normal    Stopped                   pod/gpu-kueue-pod-2   Missing Workload; unable to restore pod templates
0s          Normal    CreatedWorkload           pod/gpu-kueue-pod-2   Created Workload: default/pod-gpu-kueue-pod-2-09669
0s          Normal    Pulled                    pod/gpu-kueue-pod-2   Container image "docker.inspur.com:5000/library/cke/kubernetes/pause:3.8" already present on machine
0s          Normal    Created                   pod/gpu-kueue-pod-2   Created container test
0s          Normal    Started                   pod/gpu-kueue-pod-2   Started container test
61m         Normal    Starting                  node/worker02-h20
0s          Normal    Killing                   pod/gpu-kueue-pod-2   Stopping container test
```

5. Collecting logs from kueue-controller-manager:

```
{"level":"Level(-2)","ts":"2026-01-09T01:36:04.554856435Z","caller":"core/workload_controller.go:151","msg":"Reconcile Workload","controller":"workload_controller","namespace":"default","name":"pod-gpu-kueue-pod-2-09669","reconcileID":"bc794311-0113-437a-865a-18d2b58cc46e"}
{"level":"error","ts":"2026-01-09T01:36:04.562144631Z","caller":"jobframework/reconciler.go:278","msg":"Removing finalizer","controller":"v1_pod","namespace":"default","name":"gpu-kueue-pod-2","reconcileID":"d0fa15d9-3ee2-4ac0-8014-8a647fb45054","job":"default/gpu-kueue-pod-2","gvk":"/v1, Kind=Pod","error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"pod-gpu-kueue-pod-2-09669\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:278\nsigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile\n\t/workspace/pkg/controller/jobs/pod/pod_controller.go:123\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:116\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:303\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
{"level":"error","ts":"2026-01-09T01:36:04.562188092Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"v1_pod","namespace":"default","name":"gpu-kueue-pod-2","reconcileID":"d0fa15d9-3ee2-4ac0-8014-8a647fb45054","error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"pod-gpu-kueue-pod-2-09669\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
{"level":"Level(-2)","ts":"2026-01-09T01:36:05.513467937Z","caller":"core/localqueue_controller.go:115","msg":"Reconcile LocalQueue","controller":"localqueue_controller","namespace":"default","name":"user-queue","reconcileID":"0a2abe5d-e764-4433-8f97-e4e1da4da3e0"}
{"level":"Level(-2)","ts":"2026-01-09T01:36:05.513530132Z","caller":"core/clusterqueue_controller.go:178","msg":"Reconcile ClusterQueue","controller":"clusterqueue_controller","namespace":"","name":"cluster-queue","reconcileID":"4af41005-39f8-4019-878c-64dabf18c021"}
{"level":"error","ts":"2026-01-09T01:36:05.523468606Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"clusterqueue_controller","namespace":"","name":"cluster-queue","reconcileID":"4af41005-39f8-4019-878c-64dabf18c021","error":"ClusterQueue.kueue.x-k8s.io \"cluster-queue\" is invalid: spec.flavorFungibility.whenCanBorrow: Unsupported value: \"MayStopSearch\": supported values: \"Borrow\", \"TryNextFlavor\"","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
{"level":"Level(-2)","ts":"2026-01-09T01:36:05.525527897Z","logger":"localqueue-reconciler","caller":"core/localqueue_controller.go:173","msg":"Queue update event","localQueue":{"name":"user-queue","namespace":"default"}}
{"level":"Level(-2)","ts":"2026-01-09T01:36:05.526243535Z","caller":"core/localqueue_controller.go:115","msg":"Reconcile LocalQueue","controller":"localqueue_controller","namespace":"default","name":"user-queue","reconcileID":"bec511c7-a594-4152-aecf-55ea9d55b645"}
```



**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
```
Major:"1", Minor:"25", GitVersion:"v1.25.4-1"
```

- Kueue version (use `git describe --tags --dirty --always`):
```
Chart Release: kueue-0.11.9
```

- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
```
cmd: hostnamectl  | egrep 'Operating System|Kernel'
--------------------------------------------------
  Operating System: Ubuntu 20.04.6 LTS
            Kernel: Linux 5.4.0-216-generic

cmd: systemctl --version | head -n1
--------------------------------------------------
systemd 245 (245.4-4ubuntu3.20)

cmd: runc --version
--------------------------------------------------
runc version 1.0.0-rc10
commit: dc9208a3303feef5b3839f4323d9beb36df0a9dd
spec: 1.0.1-dev

cmd: containerd -v
--------------------------------------------------
containerd github.com/containerd/containerd v1.4.3 269548fa27e0089a8b8278fc4fc781d7f65a939b

# helm list -n kueue-system
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
kueue   kueue-system    1               2026-01-08 03:19:11.096477477 +0000 UTC deployed        kueue-0.11.9    v0.11.9
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:42:11Z

Could you please test on Kueue 0.15+? There has been many fixes since 0.11

### Comment by [@TaylorTrz](https://github.com/TaylorTrz) — 2026-01-09T15:12:46Z

> Could you please test on Kueue 0.15+? There has been many fixes since 0.11

@mimowo Thanks for your reminder. 

I have also conducted a tests on Kueue v0.15.1 with Kubernetes v1.25.4, the problem remains. 

Could you give me more hints on this?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T15:15:38Z

Can you also try some supported version of Kubernetes core (1.32+ https://kubernetes.io/releases/), there has also been many changes.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-09T16:00:08Z

Oh man this one is full of unsupported components.

[Containerd 1.4 is ancient](https://endoflife.date/containerd) and Runc 1.0 yikes..

To get support on this in upstream I do suggest following EOL docs for these components and make sure your platform is up to date.

Containerd 1.4 has lost full support 4 years ago.

### Comment by [@TaylorTrz](https://github.com/TaylorTrz) — 2026-01-10T07:38:19Z

> Can you also try some supported version of Kubernetes core (1.32+ https://kubernetes.io/releases/), there has also been many changes.

Kubernetes versions before v1.26 don’t support pod state of `SchedulingGated`, so that could actually be the main issue here?
https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/

```
# kubectl  get po
NAME                                 READY                     STATUS            RESTARTS   AGE
gpu-kueue-pod-1                    0/1     SchedulingGated                      0          5s
```

Anyway, I just successfully deployed a pod using Kueue 0.15.1 on Kubernetes v1.34. Looks like upgrading my cluster was the way to go.

```
# kubectl  version
Client Version: v1.34.1
Kustomize Version: v5.7.1
Server Version: v1.34.1

# helm list -A
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
kueue   kueue-system    1               2026-01-10 06:57:17.895741221 +0000 UTC deployed        kueue-0.15.1    v0.15.1
```

@kannon92 @mimowo Thanks for the help! Really appreciate it.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-10T12:23:34Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-10T12:23:40Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8482#issuecomment-3732546014):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
