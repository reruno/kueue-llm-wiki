# Issue #5243: TAS: Resource Fragmentation Causing Admitted/Unschedulable Workload Despite Hostname Level Tag

**Summary**: TAS: Resource Fragmentation Causing Admitted/Unschedulable Workload Despite Hostname Level Tag

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5243

**Last updated**: 2025-12-01T11:32:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@saad-essential](https://github.com/saad-essential)
- **Created**: 2025-05-13T22:14:11Z
- **Updated**: 2025-12-01T11:32:29Z
- **Closed**: 2025-12-01T11:32:29Z
- **Labels**: `kind/bug`
- **Assignees**: [@mykysha](https://github.com/mykysha), [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: At a high level, despite having `podset-preferred-topology` at `kubernetes.io/hostname` for my PodSet's, I was able to have a high-priority full-node Workload admitted when it is impossible for it to be scheduled on any node. 

Specifically:
1. Our cluster has 4 nodes, each with 8 GPU's. Our resourceFlavor tracks GPU resources, and has a topology defined below.
2. I scheduled 6 high-priority Workload's on each Node, where each Workload needs 1 GPU.
3. I also scheduled 8 low-priority Workload's. Because each of our 4 nodes had 2 GPU's free after Step 2, these Workload's were evenly divided across the nodes (2 low-priority Workload's on each of the 4 nodes)
4. I then scheduled 1 high-priority Workload that needs 8 GPU's. I soon saw the 8 pods running low-priority Workloads get Terminated. The high-priority Workload was then admitted, and I see a pod needing 8 GPU's stuck in Pending state.. Because the 8 freed GPU's from pre-emption were distributed across multiple nodes, the high-priority pod can not be scheduled.
5. I then scheduled 1 high-priority Workload that needs 1 GPU. This Workload cannot get admitted, even though technically my farm has 8 GPU's completely idle. The high-priority Workload scheduled in Step 4 is blocking everything below.

**What you expected to happen**:
I expected the Workload scheduled in Step 4 to not be admitted into the queue since I thought Topology Aware Scheduling takes into account the hosts that the pods are getting evicted from.

**How to reproduce it (as minimally and precisely as possible)**:
Repeat Steps 1-5 mentioned above.



**Anything else we need to know?**:
Below are some of my k8s YAML's, let me know if you need more. 

_Topology YAML_
```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "amd-topology"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
```

_ResourceFlavor YAML_
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: infra-test
spec:
  nodeLabels:
    kueue-pool: infra-test
    amd.com/gpu: mi300x
    amd.com/gpu-count: "8"
    amd.com/gpu-memory: "192Gi"
  topologyName: amd-topology
```

**Environment**:
- Kubernetes version (use `kubectl version`):
```
> kubectl version
Client Version: v1.31.6-dispatcher
Kustomize Version: v5.4.2
Server Version: v1.31.5+rke2r1
```
- Kueue version (use `git describe --tags --dirty --always`):
```
> kubectl describe pod kueue-controller-manager-7fc9b7b4d4-2kkt5 -n kueue-system | grep registry.k8s.io/kueue/kueue
    Image:         registry.k8s.io/kueue/kueue:v0.10.0
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T12:45:38Z

@IrvingMg @vladikkuzn @mykysha @mszadkow ptal if you have cycles
cc @PBundyra

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-15T13:49:43Z

Hi @saad-essential, can you try using `podset-required-topology`
https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#user-facing-apis

### Comment by [@saad-essential](https://github.com/saad-essential) — 2025-05-15T14:58:07Z

Hi @gabesaba, yes I tested using `podset-required-topology` and I get the exact same result:
```
annotations:
                kueue.x-k8s.io/podset-required-topology: "kubernetes.io/hostname"
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:22:59Z

We introduced the `TASProfileLeastFreeCapacity` in v0.11. So, could you try the same TAS annotations in Kueue v0.11?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T15:24:28Z

Also, could you share the logs using V(3) logging (probably grepped by the workload in question)?

### Comment by [@mykysha](https://github.com/mykysha) — 2025-05-20T08:37:29Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-21T08:43:11Z

@saad-essential Can you try the latest version of Kueue and see if the error persists?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-21T08:48:21Z

@saad-essential please also share, if possible, the yamls we could use to repro the issue (CQ, RF, Topology, Jobs). Ofc strip any  sensitive info.

### Comment by [@amy](https://github.com/amy) — 2025-07-30T16:31:50Z

Hello! @gabesaba mentioned my integration test was similar to this issue: https://github.com/kubernetes-sigs/kueue/pull/6214

Floating it up in case y'all would like to use it to either repro or close this issue.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-02T08:44:56Z

/assign
