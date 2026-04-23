# Issue #1648: Unexplained behavior with plain pods + waitForPodsReady

**Summary**: Unexplained behavior with plain pods + waitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1648

**Last updated**: 2024-02-02T19:46:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@shrinandj](https://github.com/shrinandj)
- **Created**: 2024-01-26T06:53:20Z
- **Updated**: 2024-02-02T19:46:06Z
- **Closed**: 2024-02-02T19:46:06Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
A plain pod managed by Kueue was not being able to be deleted. Kueue places a finalizer on the pod and that cause the pod deletion to hang.

**What you expected to happen**:
It should be possible delete/terminate pod even when they are managed by kueue.

**How to reproduce it (as minimally and precisely as possible)**:
- Create a pod in a namespace managed by kueue. Ensure that the pods localqueue label:
```
  labels:
    kueue.x-k8s.io/queue-name: localqueue
```
- Ensure that the pod is in running state
- Delete the pod


**Environment**:
- Kubernetes version (use `kubectl version`): v1.28.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-rc.1
- Cloud provider or hardware configuration: AWS
- OS (e.g: `cat /etc/os-release`): NA
- Kernel (e.g. `uname -a`): NA
- Install tools: NA
- Others: NA

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T10:13:10Z

I don't think this is specific to `waitForPodsReady`, same happens for priority-based preemption, or manual deletion of pods.

Further, this is "by design". The reason the pod is not deleted (it remains the Terminating state) is that it has a finalizer added by Kueue to keep it around. However, it should have a terminal phase (Failed or Succeeded, depending on the exit code), so it would not occupy any node resources, potentially small etcd size to keep the object on API server. 

Kueue uses the pod to indicate that the associated workload object is still in use (the workload has an owner reference to the Pod). If you really want to delete the pod, then remove the finalizer, but then you risk the workload being deleted by the garbage-collector.

I think questions like this warrant a documentation page about pod groups.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T10:13:21Z

/cc @tenzen-y @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T10:24:35Z

> I don't think this is specific to `waitForPodsReady`, same happens for priority-based preemption, or manual deletion of pods.
> 
> Further, this is "by design". The reason the pod is not deleted (it remains the Terminating state) is that it has a finalizer added by Kueue to keep it around. However, it should have a terminal phase (Failed or Succeeded, depending on the exit code), so it would not occupy any node resources, potentially small etcd size to keep the object on API server.
> 
> Kueue uses the pod to indicate that the associated workload object is still in use (the workload has an owner reference to the Pod). If you really want to delete the pod, then remove the finalizer, but then you risk the workload being deleted by the garbage-collector.

Yes, this is an intended behavior. We would suggest not manually deleting the pods. It means that the starting and termination of pods should be fully managed by kueue.

> > I think questions like this warrant a documentation page about pod groups.

I agree with you.

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-01-26T15:39:18Z

> Yes, this is an intended behavior. We would suggest not manually deleting the pods. It means that the starting and termination of pods should be fully managed by kueue.

This part is a bit tricky, right? As a user, I started the pods (in this case simply using kubectl). There is an expectation that I should be able to delete the pods as well. Running a `kubectl get pod <pod-name>` was basically stuck because of the finalizer.

The kueue controller on noticing a pod delete should delete any other dependent resources it has created and eventually remove the finalizer so that the pod deletion can proceed as expected.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T16:17:47Z

When you submit a single plain pod (no pod-group label), the user intention is indeed obvious. In this case, we allow the Pod to be cleaned up.

When there is a pod group, it's not obvious. The pods in the group might be retriable. And if you can retry, you wouldn't want to lose your place in the queue (you would lose it if we delete the Pod and the corresponding Workload). It's not easy to discern the user intention from preemption if all pods are deleted, as they have the same API footprint.

Hence, if you don't want to retry, we expect the user to give us extra evidence. Either by removing the Workload object or putting an annotation in the Pod. https://github.com/kubernetes-sigs/kueue/tree/main/keps/976-plain-pods#retrying-failed-pods

Unfortunately, that's as far as we can get with plain pods. We highly recommend Jobs or CRDs for more intuitive experience.

### Comment by [@shrinandj](https://github.com/shrinandj) — 2024-02-02T19:46:06Z

Good to know about the annotation. 

I'll close this for now.
