# Issue #3887: [Discussion][TAS] Best effort placements for pods in lower tier of topology

**Summary**: [Discussion][TAS] Best effort placements for pods in lower tier of topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3887

**Last updated**: 2025-02-09T22:26:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2024-12-19T08:33:42Z
- **Updated**: 2025-02-09T22:26:20Z
- **Closed**: 2025-01-14T15:34:36Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 20

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We have a rough topology like this: node -> superNode -> RDMA domain -> Zone.

![image](https://github.com/user-attachments/assets/d9526ab6-99e2-4f9e-8bea-25f50fbcc284)

We want to build the topology like:
```
  levels:
  - nodeLabel: "cloud.provider.com/topology-zone"
  - nodeLabel: "cloud.provider.com/topology-rdma-domain"
  - nodeLabel: "cloud.provider.com/topology-supernode"
```

So if we want to deploy a job with 4 replicas, each requests 8 GPUs, we can simply set  the annotation like 
```
kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-supernode"
```

then we'll find a supernode.

However, if we want to deploy a 16 replica job, which means 4 superNodes, we have to set the job annotation like

```
kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-rdma-domain"
```

because obviously a supernode is not fit. Then comes the question, is there any way to make sure the 16 pods are colocated within 4 superNodes, rather than 16 pods in 8 superNodes which means fragmentation.

I haven't tried with TAS yet, just ask this question ahead. And what scheduling instructions will be injected?

Ticketed the issue here just in case others have similar questions.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-19T08:34:50Z

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T09:36:01Z

IIUC the best you can do with the current API is to use `kueue.x-k8s.io/podset-preferred-topology: cloud.provider.com/topology-supernode` instead. If the cluster is empty the Job will land on 4 superNodes.
However, if the cluster already has some Jobs running you may overflow to more superNodes.

Suggestion: you can also have the `kubernetes.io/hostname` level at the bottom, and then even have `kueue.x-k8s.io/podset-preferred-topology: hostname.io/nodename`. The algorithm will find that the Job fits in one RDMA domain and will step down optimizing the number of superNodes and nodes used.

cc @mwysokin @PBundyra

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-19T09:46:44Z

> use kueue.x-k8s.io/podset-preferred-topology: cloud.provider.com/topology-supernode instead. If the cluster is empty the Job will land on 4 superNodes. However, if the cluster already has some Jobs running you may overflow to more superNodes

But they're not guaranteed under the same rdma domain right, if insufficient resource in the rdma domain.

> The algorithm will find that the Job fits in one RDMA domain and will step down optimizing the number of superNodes and nodes used.

Can you elaborate more on this? I remember the algo is searching the topo from bottom to up. I'm still reading the codes now.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T09:52:05Z

> But they're not guaranteed under the same rdma domain right, if insufficient resource in the rdma domain.

Yes, not guaranteed, but on prod system with many Jobs competing for resources I believe using "required" is hard - maybe for a hero Job. Maybe "required" will work better when we start supporting preemptions with TAS, but this is for future.

> Can you elaborate more on this? 

There are two BFS passes :
- bottom up starting from the level indicated by the annotation to find the topology domain which fits the entire workload
- top to bottom starting at the found level down to the last specified level

https://github.com/kubernetes-sigs/kueue/blob/b5e745a11fa6e83324718fb27cb95d6eb608dfb7/pkg/cache/tas_flavor_snapshot.go#L215-L226

EDIT: Also, If you use `kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-rdma-domain"` the algorithm will schedule on domain, you are not guarantteed 4 super nodes are used, but the algorithm will optimize the number of super nodes.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-19T10:52:53Z

> because obviously a supernode is not fit. Then comes the question, is there any way to make sure the 16 pods are colocated within 4 superNodes, rather than 16 pods in 8 superNodes which means fragmentation.

When using `kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-rdma-domain"`:

If sufficient quota exists within a single RDMA domain, the TAS will schedule all pods within that domain. However, this might utilize more than 4 supernodes. If insufficient quota exists, the job will not be scheduled.

When using `kueue.x-k8s.io/podset-preferred-topology: "cloud.provider.com/topology-rdma-domain"`:

If sufficient quota exists within a single RDMA domain, TAS will schedule all pods within that domain. Otherwise, it will distribute the pods across multiple RDMA domains.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-24T11:04:29Z

I checked the code @mimowo referred to, IIUC, when set the policy to `kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-rdma-domain"`, and let's assume that there's no pods in the cluster yet, then we'll make sure we'll fill the supernode domain one by one right? Because we're searching from the lowest ones and domains are sorted in descend. 
https://github.com/kubernetes-sigs/kueue/blob/b5e745a11fa6e83324718fb27cb95d6eb608dfb7/pkg/cache/tas_flavor_snapshot.go#L294-L312

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-25T11:58:05Z

I tested with pytorchjob like this:

```
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-simple
  namespace: tas
  labels:
    kueue.x-k8s.io/queue-name: tas-local-queue
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-required-topology: "topology-key/supernode"
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
                requests:
                  nvidia.com/gpu: 8
          tolerations:
          - key: "kwok.x-k8s.io/node"
            operator: "Exists"
            effect: "NoSchedule"
    Worker:
      replicas: 3
      restartPolicy: OnFailure
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-required-topology: "topology-key/supernode"
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
                requests:
                  nvidia.com/gpu: 8
          tolerations:
          - key: "kwok.x-k8s.io/node"
            operator: "Exists"
            effect: "NoSchedule"
```

And I got unexpected results as the status telling:
```
status:
  admission:
    clusterQueue: tas-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        nvidia.com/gpu: tas-flavor
      name: master
      resourceUsage:
        nvidia.com/gpu: "8"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - kwok-node-10
        levels:
        - kubernetes.io/hostname
    - count: 3
      flavors:
        nvidia.com/gpu: tas-flavor
      name: worker
      resourceUsage:
        nvidia.com/gpu: "24"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - kwok-node-10
        - count: 1
          values:
          - kwok-node-11
        - count: 1
          values:
          - kwok-node-8
        levels:
        - kubernetes.io/hostname
```

The master and the worker located to the same node, kwok-node-10 specifically, I think this is not as expected.

Whats' more, since the topology constraint applies to the whole job, why not set the annotation at the job level rather than the spec level.

cc @mimowo @PBundyra 

Happen xmas day anyway! 🎄

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-26T03:38:09Z

This is how we test: https://github.com/kerthcet/benchmark/tree/main/kueue-tas.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-26T11:46:26Z

> The master and the worker located to the same node, kwok-node-10 specifically, I think this is not as expected.

Seems we didn't update the leaf freeCapacity once former podsets assignedTopology.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-31T14:12:35Z

Thank you for providing detailed explanation @kerthcet and thanks for wishes! 

> The master and the worker located to the same node, kwok-node-10 specifically, I think this is not as expected.

Could you elaborate why is it unexpected please? Does one node have 32GPUs? In the link you have provided you set GPUs capacity to 8 per node, but I imagine this configuration is outdated - please correct me if I'm wrong. In case there are 32GPUs per node, I believe this assignment is as intended

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-31T14:14:50Z

> I checked the code @mimowo referred to, IIUC, when set the policy to `kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/topology-rdma-domain"`, and let's assume that there's no pods in the cluster yet, then we'll make sure we'll fill the supernode domain one by one right?

Yes, the algorithm is greedy and minimizes the number of domains at each level. If there is enough capacity in one supernode, then only one supernode will be used

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-01-03T06:59:54Z

> Could you elaborate why is it unexpected please? Does one node have 32GPUs?

No, it's a super node which has 4 nodes and 4*8=32 GPUs as an unit. These four nodes has better network connecting together, you could take it as a NVL or suprePod.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-01-03T07:02:49Z

Take the status for example:
```
status:
  admission:
    clusterQueue: tas-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        nvidia.com/gpu: tas-flavor
      name: master
      resourceUsage:
        nvidia.com/gpu: "8"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - kwok-node-10
        levels:
        - kubernetes.io/hostname
    - count: 3
      flavors:
        nvidia.com/gpu: tas-flavor
      name: worker
      resourceUsage:
        nvidia.com/gpu: "24"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - kwok-node-10
        - count: 1
          values:
          - kwok-node-11
        - count: 1
          values:
          - kwok-node-8
        levels:
        - kubernetes.io/hostname
```

The master podset assignment will be located to kwok-node-10 and the first assignment of worker will also be located to kwok-node-10, which is not right. 

I'll take a deep look of the code these days.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-01-03T07:41:10Z

@kerthcet Can you run one more scenario where the master section is defined after the worker section? I wonder if this is going to make any change at all.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-01-03T08:00:48Z

Sorry, what do you mean `where the master section is defined after the worker section?`

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-01-03T08:04:26Z

In the PyTorchJob specification:

```
spec:
  pytorchReplicaSpecs:
    Worker:
      ...
    Master:
      ...
```

### Comment by [@kebe7jun](https://github.com/kebe7jun) — 2025-01-03T09:57:28Z

If I understand correctly, are you referring to the role order?
After switching the order, there was still no change (`pytorchReplicaSpecs` is a map and does not have an order)：

```yaml
status:
  admission:
    clusterQueue: tas-cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        nvidia.com/gpu: tas-flavor
      name: master
      resourceUsage:
        nvidia.com/gpu: "8"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - node-0201
        levels:
        - kubernetes.io/hostname
    - count: 15
      flavors:
        nvidia.com/gpu: tas-flavor
      name: worker
      resourceUsage:
        nvidia.com/gpu: "120"
      topologyAssignment:
        domains:
        - count: 1
          values:
          - node-0201
        - count: 1
          values:
          - node-0202
        - count: 1
          values:
          - node-0203
        - count: 1
          values:
          - node-0204
        - count: 1
          values:
          - node-0205
        - count: 1
          values:
          - node-0206
        - count: 1
          values:
          - node-0207
        - count: 1
          values:
          - node-0208
        - count: 1
          values:
          - node-0209
        - count: 1
          values:
          - node-0210
        - count: 1
          values:
          - node-0211
        - count: 1
          values:
          - node-0212
        - count: 1
          values:
          - node-0213
        - count: 1
          values:
          - node-0214
        - count: 1
          values:
          - node-0215
        levels:
        - kubernetes.io/hostname
```

PytorchJob:

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  labels:
    kueue.x-k8s.io/queue-name: tas-local-queue
  name: job-eowu-15
  namespace: tas
spec:
  pytorchReplicaSpecs:
    Worker:
      replicas: 15
      restartPolicy: OnFailure
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-preferred-topology: supernode
            kueue.x-k8s.io/workload: pytorchjob-job-eowu-15-1d286
          labels:
            kueue.x-k8s.io/podset: worker
            kueue.x-k8s.io/tas: "true"
        spec:
          containers:
          - command:
            - python3
            - /opt/pytorch-mnist/mnist.py
            - --epochs=1
            image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
            imagePullPolicy: Always
            name: pytorch
            resources:
              limits:
                nvidia.com/gpu: "8"
          nodeSelector:
            topology-key/zone: zone1
          schedulingGates:
          - name: kueue.x-k8s.io/topology
          tolerations:
          - effect: NoSchedule
            key: kwok.x-k8s.io/node
            operator: Exists
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-preferred-topology: supernode
            kueue.x-k8s.io/workload: pytorchjob-job-eowu-15-1d286
          labels:
            kueue.x-k8s.io/podset: master
            kueue.x-k8s.io/tas: "true"
        spec:
          containers:
          - command:
            - python3
            - /opt/pytorch-mnist/mnist.py
            - --epochs=1
            image: docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-21320b6
            imagePullPolicy: Always
            name: pytorch
            resources:
              limits:
                nvidia.com/gpu: "8"
          nodeSelector:
            topology-key/zone: zone1
          schedulingGates:
          - name: kueue.x-k8s.io/topology
          tolerations:
          - effect: NoSchedule
            key: kwok.x-k8s.io/node
            operator: Exists
```

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-03T13:33:25Z

Thanks for providing such a detailed explanation. We'll look into it

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T08:00:38Z

@kerthcet thank you for reporting the issue, I believe there is a bug indeed - the inflight usage from previously considered PodSets is not taken into account when computing placement for the new PodSet. I will leave more comments at your PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-09T22:26:18Z

/remove-kind feature
/kind bug
