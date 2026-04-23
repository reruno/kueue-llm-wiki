# Issue #3683: Pod stuck on Suspend state after recreation on Pod Group.

**Summary**: Pod stuck on Suspend state after recreation on Pod Group.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3683

**Last updated**: 2024-11-29T13:46:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-11-28T16:58:26Z
- **Updated**: 2024-11-29T13:46:55Z
- **Closed**: 2024-11-29T13:46:53Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Pod stuck on Suspend state after recreation on Pod Group.

```
2024-11-28T16:41:50.25358188Z	ERROR	jobframework/reconciler.go:429	Updating reclaimable pods	{"controller": "v1_pod", "namespace": "group/sts-e2e-pbznc", "name": "statefulset-sts-18b6e", "reconcileID": "d17d280a-8c61-4ec4-9d49-27b7398d8a74", "job": "group/sts-e2e-pbznc/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod", "error": "admission webhook \"vworkload.kb.io\" denied the request: status.reclaimablePods[5949e52e]: Required value: cannot be removed"}
sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob
	/workspace/pkg/controller/jobframework/reconciler.go:429
sigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile
	/workspace/pkg/controller/jobs/pod/pod_controller.go:123
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:116
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:303
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224
2024-11-28T16:41:50.253725505Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/sts-e2e-pbznc", "name": "statefulset-sts-18b6e", "reconcileID": "d17d280a-8c61-4ec4-9d49-27b7398d8a74", "error": "admission webhook \"vworkload.kb.io\" denied the request: status.reclaimablePods[5949e52e]: Required value: cannot be removed"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224
```

**What you expected to happen**:
Pods running after recreation.

**How to reproduce it (as minimally and precisely as possible)**:
1. Create pod group.

```
kubectl apply -f kueue-pod-group.yaml
```

```
---
apiVersion: v1
kind: Pod
metadata:
  name: sample-leader
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
    args: ["30m"]
    resources:
      requests:
        cpu: "100m"
---
apiVersion: v1
kind: Pod
metadata:
  name: sample-worker
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
    args: [ "30m"]
    resources:
      requests:
        cpu: "100m"

```


```
NAME            READY   STATUS    RESTARTS   AGE
sample-leader   1/1     Running   0          1s
sample-worker   1/1     Running   0          1s
```

2. Delete one of the pod.
```
kubectl delete pod sample-worker
```

3. Remove finalizer

```
NAME            READY   STATUS    RESTARTS   AGE
sample-leader   1/1     Running   0          24s
```


4. Create pod again.

```
kubectl apply -f kueue-pod-group.yaml
```

```
NAME            READY   STATUS            RESTARTS   AGE
sample-leader   1/1     Running           0          29s
sample-worker   0/1     SchedulingGated   0          3s
```

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-28T16:58:35Z

cc: @mimowo

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-28T17:54:35Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T13:46:48Z

Actually, the fact that the replacement for a succeeded pods is suspended and gated is expected, for batch Jobs. We don't need to run a replacement if the previous task succeeded. 

I synced with @mbobrovskyi and this issue was originally motivated by the broken support for STS, but this is only a problem for "serving" workloads. For serving workloads we need to run the replacement pod even for succeeded pods. I created a dedicated issue https://github.com/kubernetes-sigs/kueue/issues/3690 to better reflect the problem.

Since the PodGroups were originally introduced for batch workloads we should not change the behavior and I proposed to introduce the "serving" annotation for PodGroups, implemented in https://github.com/kubernetes-sigs/kueue/pull/3686, so that we don't change the baseline behavior.

So, I believe we can close this issue and focus on https://github.com/kubernetes-sigs/kueue/issues/3690. I agree the error message could be better, but I think this is a separate issue. I think the  user-observable behavior is correct for batch workloads based on PodGroups.

cc @mbobrovskyi @tenzen-y 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-29T13:46:54Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3683#issuecomment-2507854821):

>Actually, the fact that the replacement for a succeeded pods is suspended and gated is expected, for batch Jobs. We don't need to run a replacement if the previous task succeeded. 
>
>I synced with @mbobrovskyi and this issue was originally motivated by the broken support for STS, but this is only a problem for "serving" workloads. For serving workloads we need to run the replacement pod even for succeeded pods. I created a dedicated issue https://github.com/kubernetes-sigs/kueue/issues/3690 to better reflect the problem.
>
>Since the PodGroups were originally introduced for batch workloads we should not change the behavior and I proposed to introduce the "serving" annotation for PodGroups, implemented in https://github.com/kubernetes-sigs/kueue/pull/3686, so that we don't change the baseline behavior.
>
>So, I believe we can close this issue and focus on https://github.com/kubernetes-sigs/kueue/issues/3690. I agree the error message could be better, but I think this is a separate issue. I think the  user-observable behavior is correct for batch workloads based on PodGroups.
>
>cc @mbobrovskyi @tenzen-y 
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
