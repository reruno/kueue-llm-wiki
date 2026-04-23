# Issue #6149: Plain Pods cannot delete before completion

**Summary**: Plain Pods cannot delete before completion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6149

**Last updated**: 2025-07-24T03:16:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Ladicle](https://github.com/Ladicle)
- **Created**: 2025-07-23T07:07:19Z
- **Updated**: 2025-07-24T03:16:27Z
- **Closed**: 2025-07-23T23:35:32Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

When I delete Plain Pods before they are complete, the finalizer will not be removed, and the pods will remain.

**What you expected to happen**:

Plain Pods can be deleted even before they are finished. 

**How to reproduce it (as minimally and precisely as possible)**:

<details>
<summary>simple plain pods example</summary>

```bash
# pod manifest
> cat kueue-info/test.yaml
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-leader-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the leader pod" && sleep 3']
    resources:
      requests:
        cpu: 5
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-worker-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the worker pod" && sleep 2']
    resources:
      requests:
        cpu: 5

# create pods
> kubectl create -f kueue-info/test.yaml
pod/sample-leader-7lpxm created
pod/sample-worker-rkxch created

# pods have not been admitted yet
> kubectl get pods
NAME                  READY   STATUS            RESTARTS   AGE
sample-leader-7lpxm   0/1     SchedulingGated   0          14s
sample-worker-rkxch   0/1     SchedulingGated   0          14s

> kubectl kueue list workload
NAME           JOB TYPE   JOB NAME                                   LOCALQUEUE   CLUSTERQUEUE    STATUS    POSITION IN QUEUE   EXEC TIME   AGE
sample-group   pod        sample-leader-7lpxm, sample-worker-rkxch   user-queue   cluster-queue   PENDING   0                               22s

# delete pods -> failed to delete
> kubectl delete pod sample-leader-7lpxm sample-worker-rkxch
pod "sample-leader-7lpxm" deleted
pod "sample-worker-rkxch" deleted
^C⏎

# pod still has a `kueue.x-k8s.io/managed` finalizer
> kubectl get pods sample-leader-7lpxm -o yaml|yq .metadata
annotations:
  kueue.x-k8s.io/pod-group-total-count: "2"
  kueue.x-k8s.io/role-hash: b514ac0b
creationTimestamp: "2025-07-23T05:31:38Z"
deletionGracePeriodSeconds: 0
deletionTimestamp: "2025-07-23T05:32:33Z"
finalizers:
  - kueue.x-k8s.io/managed
generateName: sample-leader-
generation: 2
labels:
  kueue.x-k8s.io/managed: "true"
  kueue.x-k8s.io/pod-group-name: sample-group
  kueue.x-k8s.io/queue-name: user-queue
name: sample-leader-7lpxm
namespace: default
resourceVersion: "219612"
uid: 07a4cc66-6710-434d-856c-24c1ca3559d2

# workload still exists
> kubectl get workloads sample-group
NAME           QUEUE        RESERVED IN   ADMITTED   FINISHED   AGE
sample-group   user-queue                                       107s

> kubectl get workloads sample-group -o yaml|yq .metadata.ownerReferences
- apiVersion: v1
  kind: Pod
  name: sample-leader-7lpxm
  uid: 07a4cc66-6710-434d-856c-24c1ca3559d2
- apiVersion: v1
  kind: Pod
  name: sample-worker-rkxch
  uid: 28601aa3-8b7f-4c32-8406-d6ba75ef30c4
```

</details>

**Anything else we need to know?**:

I’m wondering if we can propagate pod owner references to the workload to improve cleanup when parent resources are deleted? ( I may be missing something, but if the finalizer is only there to prevent accidental deletion, wouldn't it be better not to attach it for more reliable deletion? )

**Environment**:
- Kubernetes version (use `kubectl version`): 

```
> kubectl version
Client Version: v1.33.3
Kustomize Version: v5.6.0
Server Version: v1.33.1
```

- Kueue version (use `git describe --tags --dirty --always`):

```
> kubectl get deploy kueue-controller-manager -n kueue-system -o=jsonpath='{.spec.template.spec.containers[0].image}'
registry.k8s.io/kueue/kueue:v0.12.4
```

- Cloud provider or hardware configuration: kind
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-23T16:50:50Z

I think that this is expected behavior: https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#termination
If you want to handle the deletion and failure more granularly, we would recommend using the Workload level API, such as Job, JobSet.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-23T17:17:05Z

Thanks for reporting this!

I wasn’t able to reproduce the issue. The `kueue.x-k8s.io/managed` finalizer on Pod objects should be removed by Kueue regardless of the Pod’s state, whether it’s `Running` or still `Pending`/`SchedulingGated`. Once the finalizer is cleared, the Pod should be garbage collected as expected.

Could you double-check that the Kueue controller manager is running and healthy? If it’s not, that might explain why the finalizer isn't getting removed.

For reference, repro data:
```
⋊>  cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  labels:
    kueue.x-k8s.io/queue-name: demo
spec:
  containers:
    - name: pause
      image: registry.k8s.io/pause:3.6

⋊>  kubectl get pod
No resources found in demo namespace.

⋊> kubectl apply -f pod.yaml
pod/test-pod created

⋊> kubectl get pod,workload
NAME           READY   STATUS    RESTARTS   AGE
pod/test-pod   1/1     Running   0          6s

NAME                                         QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/pod-test-pod-2e9bb   demo    demo          True                  6s

⋊> kubectl delete -f pod.yaml
pod "test-pod" deleted

⋊> kubectl get pod,workload
No resources found in demo namespace.

⋊> kubectl get pod -n kueue-system kueue-controller-manager-b9b79464c-5glx5 -o yaml | yq .spec.containers[].image
registry.k8s.io/kueue/kueue:v0.12.4

```

### Comment by [@Ladicle](https://github.com/Ladicle) — 2025-07-23T23:35:32Z

Thank you for your reply. I overlooked `kueue.x-k8s.io/retriable-in-group`. I can confirm that even when evicted simultaneously, a new workload was created and worked without any problems. This resolved most cases.
As for custom resources that require additional care, I will consider integrating them into the existing framework.

@ichekrygin Thank you for covering the single-pod case! This only occurred when a pod-group label is assigned.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-24T03:16:23Z

Thank you for checking that.
/remove-kind bug
/kind support
