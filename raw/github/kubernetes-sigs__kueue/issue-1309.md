# Issue #1309: When preempt, the released resources cannot meet the scheduling needs

**Summary**: When preempt, the released resources cannot meet the scheduling needs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1309

**Last updated**: 2024-01-09T03:19:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hanlaipeng](https://github.com/hanlaipeng)
- **Created**: 2023-11-06T13:36:08Z
- **Updated**: 2024-01-09T03:19:16Z
- **Closed**: 2024-01-09T03:19:14Z
- **Labels**: `kind/bug`, `triage/needs-information`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I create two clusterqueue and set reclaimWithinCohort = Any,  when preempt, the released resources cannot meet the scheduling needs. 
For example, when i submit one (1 * 2GPUs) task，I want this task to get 2 GPUs on the same machine，however, the resources released after preemption are one machine has 0.5 GPUs and the other has 1.5 GPUs

<img width="259" alt="截屏2023-11-06 21 34 31" src="https://github.com/kubernetes-sigs/kueue/assets/13792422/42a9b9f3-479e-45e3-8616-1c0095093029">

**What you expected to happen**:

I want this task to get 2 GPUs on the same machine,

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 
- Kueue version (use `git describe --tags --dirty --always`): v 0.4.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T03:23:06Z

cc @B1F030 can you help to take a look?

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-07T06:32:25Z

Could you please provide yaml of ResourceFlavor, ClusterQueue, and Job?
/triage needs-information
I guess you need to set an only-a-clusterqueue.
For example, there are two clusterqueues: gpu-a-cq and gpu-b-cq, they are in the same cohort, so that they can share resources with eachother.
When preemption happens, everything goes right. But when you want to create a workload that can only run on gpu-a-cq, you will need to create another clusterqueue, as only-a-cq, that not belongs to any cohort.
If you claim workload to the only-a-queue, this workload will only use gpu-a. Is that what you want?

### Comment by [@hanlaipeng](https://github.com/hanlaipeng) — 2023-11-07T06:43:33Z

> Could you please provide yaml of ResourceFlavor, ClusterQueue, and Job? /triage needs-information I guess you need to set an only-a-clusterqueue. For example, there are two clusterqueues: gpu-a-cq and gpu-b-cq, they are in the same cohort, so that they can share resources with eachother. When preemption happens, everything goes right. But when you want to create a workload that can only run on gpu-a-cq, you will need to create another clusterqueue, as only-a-cq, that not belongs to any cohort. If you claim workload to the only-a-queue, this workload will only use gpu-a. Is that what you want?

gpu-a-cq clusterqueue: : 

spec:
  cohort: gpu-hlp
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: Never
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - nvidia.com/gpu
    flavors:
    - name: gpu-hlp
      resources:
      - borrowingLimit: "0"
        name: cpu
        nominalQuota: "57"
      - borrowingLimit: "0"
        name: memory
        nominalQuota: 209Gi
      - borrowingLimit: "0"
        name: nvidia.com/gpu
        nominalQuota: "8"

gpu-b-cq clusterqueue: :

spec:
  cohort: gpu-hlp
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - nvidia.com/gpu
    flavors:
    - name: gpu-hlp
      resources:
      - borrowingLimit: "57"
        name: cpu
        nominalQuota: "0"
      - borrowingLimit: 209Gi
        name: memory
        nominalQuota: 0
      - borrowingLimit: "8"
        name: nvidia.com/gpu
        nominalQuota: "0"

resourceflavor:

apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  creationTimestamp: "2023-08-30T09:17:46Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  name: gpu-hlp
  resourceVersion: "3121760923"
  selfLink: /apis/kueue.x-k8s.io/v1beta1/resourceflavors/gpu-hlp
  uid: e48e90c9-5fdd-41d6-9f77-11cea43b5125
spec: {}

resource pool has tow 4 GPUS nodes，i submit 2 GPUs * 1 pod job to gpu-a-cq, however the resources released after preemption are one machine has 0.5 GPUs and the other has 1.5 GPUs, can not meet the job scheduling needs

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-07T07:01:01Z

Could you also paste the Job yaml too?

### Comment by [@hanlaipeng](https://github.com/hanlaipeng) — 2023-11-07T07:06:32Z

> Could you also paste the Job yaml too?

ok, just sample pod yaml, resource is:
Resources:
            Limits:
              Cpu:             2
              Memory:          5Gi
              nvidia.com/gpu:  2
            Requests:
              Cpu:     2
              Memory:  5Gi
              nvidia.com/gpu:  2

kueue preemption strategy is to preempt those with lower priorities first, and those with the same priority that have a shorter startup time are preempted first.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-07T07:55:24Z

Since your ResourceFlavor has nil spec, I recommend to use default-flavor.

Would you like to try these yamls below, and see if that problem happens again?

`gpu-a-cq.yaml `
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "gpu-a-cq"
spec:
  namespaceSelector: {} # match all.
  cohort: "gpu-ab"
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 57
        borrowingLimit: 57
      - name: "memory"
        nominalQuota: 209Gi
        borrowingLimit: 209Gi
      - name: "nvidia.com/gpu"
        nominalQuota: 8
        borrowingLimit: 8
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
```
`kubectl create -f gpu-a-cq.yaml`

`gpu-b-cq.yaml`
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "gpu-b-cq"
spec:
  namespaceSelector: {} # match all.
  cohort: "gpu-ab"
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 57
        borrowingLimit: 57
      - name: "memory"
        nominalQuota: 209Gi
        borrowingLimit: 209Gi
      - name: "nvidia.com/gpu"
        nominalQuota: 8
        borrowingLimit: 8
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
```
`kubectl create -f gpu-b-cq.yaml`

`localqueue-a.yaml`
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: gpu-a-queue
spec:
  clusterQueue: gpu-a-cq
```
`kubectl create -f localqueue-a.yaml`

`localqueue-b.yaml`
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: gpu-b-queue
spec:
  clusterQueue: gpu-b-cq
```
`kubectl create -f localqueue-b.yaml`

`sample-job.yaml`
```
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: gpu-a-queue
spec:
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        imagePullPolicy: IfNotPresent
        args: ["60s"]
        resources:
          limits:
            cpu: 2
            memory: "5Gi"
            nvidia.com/gpu: 2
          requests:
            cpu: 2
            memory: "5Gi"
            nvidia.com/gpu: 2
      restartPolicy: Never
```
`kubectl create -f sample-job.yaml`

### Comment by [@hanlaipeng](https://github.com/hanlaipeng) — 2024-01-08T06:37:42Z

i had solved this problem by adding node resource scheduling in our internal environment，can i solve this problem ? gratefully  @kerthcet

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-08T10:18:49Z

Does the node resource scheduling means the nodeResourceFit plugin in kube-scheduler?

### Comment by [@hanlaipeng](https://github.com/hanlaipeng) — 2024-01-08T11:06:44Z

> Does the node resource scheduling means the nodeResourceFit plugin in kube-scheduler?

yes，we can add this plugin to solve the problem of the released resources cannot meet the scheduling needs after preempted

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-09T03:19:10Z

Generally, kueue can not solve this problem as kueue and kube-scheduler are two different components, they can't aware of each other, so let's close this so far. Thanks for your feedbacks.

And `waitForPodsReady` in kueue may help you here as well, the Job will be requeued after a period time of not-ready.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-09T03:19:15Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1309#issuecomment-1882315380):

>Generally, kueue can not solve this problem as kueue and kube-scheduler are two different components, they can't aware of each other, so let's close this so far. Thanks for your feedbacks.
>
>And `waitForPodsReady` in kueue may help you here as well, the Job will be requeued after a period time of not-ready.
>/close 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
