# Issue #3909: Preemption does not meet expectations

**Summary**: Preemption does not meet expectations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3909

**Last updated**: 2025-10-23T15:26:37Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@dafu-wu](https://github.com/dafu-wu)
- **Created**: 2024-12-25T02:42:07Z
- **Updated**: 2025-10-23T15:26:37Z
- **Closed**: 2025-10-23T15:26:36Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 13

## Description


**What happened**:
There is a pytorchjob that occupies three nodes (master 1, worker 2) and 24 GPUs. The workload priority is 1000 and runs normally. Now, a pytorchjob with the same configuration is submitted to the same clusterqueue and the priority is 1000. High-priority tasks cannot Preempt low-priority tasks and report the following error:
```status:
  conditions:
  - lastTransitionTime: "2024-12-25T02:15:59Z"
    message: 'couldn''t assign flavors to pod set master: insufficient unused quota
      for nvidia.com/gpu in flavor multi-node-h100, 8 more needed, insufficient unused
      quota for nvidia.com/gpu in flavor single-node-h100, 8 more needed; couldn''t
      assign flavors to pod set worker: insufficient quota for nvidia.com/gpu in flavor
      multi-node-h100, request > maximum capacity (16 > 8), insufficient quota for
      nvidia.com/gpu in flavor single-node-h100, request > maximum capacity (24 >
      16)'
    observedGeneration: 1
    reason: Pending
    status: "False"
    type: QuotaReserved 
```


But, a pytorchjob（master 1, worker 2， 16GPUs） is submitted to the same clusterqueue and the priority is 1000，it‘s works


**What you expected to happen**:
It is hoped that the high-priority pytorchjob configured the same as the low-priority pytorchjob can normally preempt the low-priority pytorchjob.

**How to reproduce it (as minimally and precisely as possible)**:
- clusterqueue
```---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cluster-queue-asr
spec:
  namespaceSelector: {} 
  cohort: h100-dev
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: Preempt
  preemption:
    borrowWithinCohort:
      maxPriorityThreshold: 100
      policy: LowerPriority
    reclaimWithinCohort: LowerPriority
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - nvidia.com/gpu
    flavors:
    - name: single-node-h100
      resources:
      - name: nvidia.com/gpu
        nominalQuota: "16"
        borrowingLimit: "8"
    - name: multi-node-h100
      resources:
      - name: nvidia.com/gpu
        nominalQuota: "8"
        borrowingLimit: "8"
  stopPolicy: None
---

apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: multi-node-h100
spec:
  nodeLabels:
    mlp: multi-node

---

apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: single-node-h100
spec:
  nodeLabels:
    mlp: single-node
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: asr
spec:
  clusterQueue: cluster-queue-asr```
- pytorch-simple-low-priority
```apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-simple-low-priority
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: asr
    kueue.x-k8s.io/priority-class: low-priority
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
#              If you have gpu, pytorch-mnist-gpu would be helpful. pytorch-mnist-gpu is approximately 22GB
#              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
              imagePullPolicy: Always
              command:
                - "python3"
                - "/opt/pytorch-mnist/mnist.py"
                - "--epochs=100000"
              resources:
                limits:
                  nvidia.com/gpu: 8

    Worker:
      replicas: 2
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
#              If you have gpu, pytorch-mnist-gpu would be helpful. pytorch-mnist-gpu is approximately 22GB
#              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
              imagePullPolicy: Always
              command:
                - "python3"
                - "/opt/pytorch-mnist/mnist.py"
                - "--epochs=100000"
              resources:
                limits:
                  nvidia.com/gpu: 8
```
- pytorch-simple-high-priority
```apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-simple-high-priority
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: asr
    kueue.x-k8s.io/priority-class: high-priority
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
#              If you have gpu, pytorch-mnist-gpu would be helpful. pytorch-mnist-gpu is approximately 22GB
#              image: docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
              imagePullPolicy: Always
              command:
                - "python3"
                - "/opt/pytorch-mnist/mnist.py"
                - "--epochs=1"
              resources:
                limits:
                  nvidia.com/gpu: 8

   ```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.29.5
- Kueue version (use `git describe --tags --dirty --always`):0.10.0
- OS (e.g: `cat /etc/os-release`):  Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): Linux scl-c26-r3-svr05 5.15.0-117-generic

## Discussion

### Comment by [@dafu-wu](https://github.com/dafu-wu) — 2024-12-25T08:36:38Z

Whether low priority workloads should be considered in maxCapacity？

`maxCapacity := a.cq.PotentialAvailable(fr)`

https://github.com/kubernetes-sigs/kueue/blame/95bc3b28da49862186f5e38924e1507ce4b7c703/pkg/scheduler/flavorassigner/flavorassigner.go#L608C22-L608C40

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-01-03T15:46:59Z

Can you share the [WorkloadPriorityClass](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/) CRs associated with `high-priority` and `low-priority`?

### Comment by [@dafu-wu](https://github.com/dafu-wu) — 2025-01-11T01:21:26Z

@KPostOffice 

```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: low-priority
value: 100
description: "low priority"

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: high-priority
value: 1000
description: "high priority"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-13T07:51:09Z

cc @gabesaba as closely related to scheduling

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-13T15:40:54Z

Hi @dafu-wu, is there any capacity provided by the Cohort? Based on the messages, it looks like, though there is a borrowing limit configured and Cohort configured, there is no capacity in the Cohort which to borrow.

**What I think is happening:**
When the high-priority workload with 24 GPUs is submitted, the master's pod-set is assigned to flavor `single-node-h100`, which has 16 GPUs. Then, when we try to assign flavor to the worker's pod-set, the 8 GPUs (master) + 16 (worker) is greater than the 16 GPUs max available in the `single-node-h100` flavor (the message 24>16 we are seeing). And the worker won't fit in the `multi-node-h100` flavor (16 > 8 message we are seeing)

Apparently, the initial workload is able to assign the Master's podset to `multi-node-h100`, and assign the worker's podset to `single-node-h100`. But we fail to do this for the high-priority workload.

### Comment by [@dafu-wu](https://github.com/dafu-wu) — 2025-01-25T00:21:06Z

@gabesaba Yes, but why high-priority can't preempt the low-priority pytorchjob?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-02-25T13:48:45Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-26T14:01:56Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-26T14:17:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-24T14:21:00Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-23T15:00:51Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T15:26:30Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T15:26:37Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3909#issuecomment-3437635737):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
