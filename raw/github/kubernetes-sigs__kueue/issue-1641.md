# Issue #1641: Pod Groups: when a workload representing group of pods is readmitted then pods are not created

**Summary**: Pod Groups: when a workload representing group of pods is readmitted then pods are not created

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1641

**Last updated**: 2024-01-26T14:32:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-01-25T10:42:53Z
- **Updated**: 2024-01-26T14:32:37Z
- **Closed**: 2024-01-25T13:54:29Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

When a workload representing a group of pods is evicted, for example due to exceeding the timeout, and re-admitted, then the pods are not created. 

**What you expected to happen**:

Create replacement pods for the newly re-admitted workload.

Note that this is a different scenario than creating replacement pods for a running workload.

**How to reproduce it (as minimally and precisely as possible)**:

Install Kueue with "pod" integration enabled.

Also, enable `waitForReadyPods`, with `timeout: 1m`.

Create a cluster with the close to infinite quota:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-inf"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 10000
      - name: "memory"
        nominalQuota: 1000000Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue-inf"
spec:
  clusterQueue: "cluster-queue-inf"
```

Then, schedule the group of pods as follows:
```
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-pod-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue-inf
    kueue.x-k8s.io/pod-group-name: "group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  terminationGracePeriodSeconds: 1
  containers:
  - name: dummy-job
    image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
    args: ["60s"]
    resources:
      requests:
        cpu: "1000"
        memory: "1Gi"
      limits:
        cpu: "1000"
        memory: "1Gi"
  restartPolicy: Never
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-pod-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue-inf
    kueue.x-k8s.io/pod-group-name: "group"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "2"
spec:
  terminationGracePeriodSeconds: 1
  containers:
  - name: dummy-job
    image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
    args: ["60s"]
    resources:
      requests:
        cpu: "1000"
        memory: "1Gi"
      limits:
        cpu: "1000"
        memory: "1Gi"
  restartPolicy: Never
```

The pods are pending (because we request 1000CPU (tune the value in case you have more :) ). 
Issue: after 1min the two pods are terminated, and the workload is preempted. 

**Issue:** the re-admitted workload does not create replacement pods.

Note that the similar case happens when the workload is re-admitted if it was preempted due to priority-based eviction.

**Anything else we need to know?**:

This is the example status of the `Terminating` pods:

```
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: null
      message: '0/2 nodes are available: 1 Insufficient cpu, 1 node(s) had untolerated
        taint {node-role.kubernetes.io/control-plane: }. preemption: 0/2 nodes are
        available: 1 No preemption victims found for incoming pod, 1 Preemption is
        not helpful for scheduling..'
      reason: Unschedulable
      status: "False"
      type: PodScheduled
    - lastProbeTime: null
      lastTransitionTime: "2024-01-25T10:29:03Z"
      message: Exceeded the PodsReady timeout default/group
      reason: StoppedByKueue
      status: "True"
      type: TerminationTarget
    phase: Failed
    qosClass: Guaranteed
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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T10:43:08Z

/cc @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T10:54:40Z

IIUC, this is not a bug. This is intended behavior since the external job dispatcher should be responsible for recreating pods.

Also, kueue doesn't implement pod retry policies:

> Support for advanced Pod retry policies
> 
> Kueue shouldn't re-implement core functionalities that are already available in the Job API.

https://github.com/kubernetes-sigs/kueue/tree/main/keps/976-plain-pods#non-goals

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T11:59:39Z

I see, I'm ok to close the Issue if this is indeed the intention, just thought it is worth discussing. the non-goals section does not clarify IMO the behavior on re-admission.

The way I understand "Kueue shouldn't re-implement core functionalities that are already available in the Job API."  is that the dispatcher is responsible for creating replacements of failed pods *while the job is running*. When a job is re-admitted I don't see why we treat pod creation differently than on the first admisison.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T12:12:05Z

However, if this is the intended behavior, maybe a note in docs / KEP specifically about re-admission would be useful?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T13:20:06Z

> When a job is re-admitted I don't see why we treat pod creation differently than on the first admission.

Sorry, I'm not sure what you wanted to say. You mean that the kueue should mutate the schedulingGate to the evicted pods, right? If so, it isn't possible since we can not add schedulingGates to pods after pods are scheduled to nodes.

> However, if this is the intended behavior, maybe a note in docs / KEP specifically about re-admission would be useful?

SGTM. We have a similar description in the Drawbacks section. However, a note in docs / KEP non-goal is also nice to have.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T13:38:18Z

> You mean that the kueue should mutate the schedulingGate to the evicted pods, right?

No, I meant that kueue should recreate the pods when workload is re-admitted (after being preempted / timedout). It was surprising to me that the pods are created on the first admission, but not re-admission.

However, when I think this more about it it sort of makes sense. Pod creation after re-admission is still re-creation. 
So, I would like to extend the non-goals note "Support for advanced Pod retry policies

Kueue shouldn't re-implement core functionalities that are already available in the Job API. In particular, it does not recreate failed pods while the workload is running, which also means no pods are created on workload re-admission.". WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T13:47:49Z

I see. Thank you for the clarifications.

> No, I meant that kueue should recreate the pods when workload is re-admitted (after being preempted / timedout). It was surprising to me that the pods are created on the first admission, but not re-admission.

IIUC, In the first admission, the kueue doesn't create any pods.
Let me describe the steps until the plain pod starts:

1. The external job dispatcher creates pods
2. The kueue webhook injects schedulingGate to the pods before the pod is started and the kueue creates the workload object matched the pod.
3. The kueue removes injected schedulingGate from the pod once the workload is admitted
4. The pod starts

Does it make sense?

Sure, I agree with extending the non-goals note.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T13:54:26Z

> IIUC, In the first admission, the kueue doesn't create any pods.

Right! I sort of missed that, because on the initial run (admission) they are always there :) 

/close

EDIT: I will add a small PR to extend the note as a follow up

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-25T13:54:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1641#issuecomment-1910265375):

>> IIUC, In the first admission, the kueue doesn't create any pods.
>
>Right! I sort of missed that, because on the initial run they are always there :) 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T12:05:24Z

> EDIT: I will add a small PR to extend the note as a follow up

Or preferably we can just make sure it is mentioned in the user-facing docs. Here is another issue about "working as intended behavior": https://github.com/kubernetes-sigs/kueue/issues/1648. WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T14:32:36Z

> > EDIT: I will add a small PR to extend the note as a follow up
> 
> Or preferably we can just make sure it is mentioned in the user-facing docs. Here is another issue about "working as intended behavior": #1648. WDYT?

Documentation SGTM.
