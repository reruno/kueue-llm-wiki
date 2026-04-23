# Issue #6868: TAS does not respect node taints

**Summary**: TAS does not respect node taints

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6868

**Last updated**: 2025-09-18T16:14:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@jessicaxiejw](https://github.com/jessicaxiejw)
- **Created**: 2025-09-16T20:56:18Z
- **Updated**: 2025-09-18T16:14:14Z
- **Closed**: 2025-09-18T16:14:14Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When a node has a taint with NoSchedule as the effect, the TAS scheduler will consider the node usable and count it towards the total number of nodes that can be scheduled. Neither the pods nor the resource flavor has tolerations for the taints.

**What you expected to happen**:

When the node has a taint with NoSchedule and neither pods nor the flavor has tolerations, I expect TAS to not assign pods to the node.

**How to reproduce it (as minimally and precisely as possible)**:

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: jessica-cluster-queue
spec:
  cohort: training
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: Preempt
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups: []
  stopPolicy: None
  namespaceSelector: {}
  resourceGroups:
  - coveredResources:
    - memory
    - cpu
    - nvidia.com/gpu
    flavors:
    - name: jessica-gpu
      resources:
        - name: memory
          nominalQuota: "42000Gi"
        - name: cpu
          nominalQuota: "3136"
        - name: nvidia.com/gpu
          nominalQuota: "224"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: jessica-queue
  namespace: default
spec:
  clusterQueue: jessica-cluster-queue
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: nvlink-domain
spec:
  levels:
  - nodeLabel: "mydomain.com/jessica-nvlink-domain" 
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: jessica-gpu
spec:
  topologyName: nvlink-domain
  nodeLabels:
    node.kubernetes.io/instance-type: gpu # your own instance type
```

Label 2 nodes with `mydomain.com/jessica-nvlink-domain=a` and 1 node with `mydomain.com/jessica-nvlink-domain=b`.  Taint one of the 2 pods from the `mydomain.com/jessica-nvlink-domain=a` with `mydomain.com/do-no-schedule=true:NoSchedule`

Then creating a jobset for it
```
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: simple-jobset
  labels:
    kueue.x-k8s.io/queue-name: jessica-queue
spec:
  replicas: 2
  template:
    spec:
      template:
        metadata:
          annotations:
            kueue.x-k8s.io/podset-preferred-topology: mydomain.com/jessica-nvlink-domain
        spec:
          containers:
            - name: busybox
              image: busybox
              command: ["sleep", "60"]
              resources:
                requests:
                  nvidia.com/gpu: 8
          restartPolicy: Never
```

You should see the nodeSelector on both pods set to `mydomain.com/jessica-nvlink-domain=a` instead of one in group a and one in group b. One of the pods will be stuck on Pending.

**Anything else we need to know?**:

I changed the log level to `--zap-log-level=3` and didn't see `excluding node with untolerated taint` in the log.

**Environment**:
- Kubernetes version (use `kubectl version`):
   ```
   Client Version: v1.32.0
   Server Version: v1.29.1
  ```
- Kueue version (use `git describe --tags --dirty --always`): v0.13.4
- Cloud provider or hardware configuration: Oracle
- OS (e.g: `cat /etc/os-release`): MacOS
- Kernel (e.g. `uname -a`): Darwin arm64
- Install tools: N/A
- Others: N/A

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T08:03:18Z

Oh, Kueue respects taints, but only provided the lowest topology level is kubernetes.io/hostname, see this test case: https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/tas/tas_test.go#L1876-L1929

For sure we should mention that in the limitations of TAS on our webpage: https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#limitations.

Let me know if this would work for you, and if you would like to update the website.

### Comment by [@jessicaxiejw](https://github.com/jessicaxiejw) — 2025-09-17T13:46:25Z

@mimowo I couldn't get the lowest topology level `kubernetes.io/hostname` to work. It finally dawned on me this morning that I have to add the tolerance to the ResourceFlavor. We have a webhook that injects the toleration to the pod based on the nodeSelector. Since the injection happens on the pod level but the actual object the workload corresponds to is a jobset, the workload doesn't have the right toleration on the podset level.

For those who have the same issue when using `kubernetes.io/hostname`, change your resource flavour to add the toleration
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: jessica-gpu
spec:
  topologyName: nvlink-domain
  nodeLabels:
    node.kubernetes.io/instance-type: gpu # your own instance type
  tolerations:
    - key: "nvidia.com/gpu"  # have to have this, otherwise TAS think the nodes aren't tolerable
      operator: "Equal"
      value: "present"
      effect: "NoSchedule"
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: nvlink-domain
spec:
  levels:
  - nodeLabel: "mydomain.com/jessica-nvlink-domain" 
  - nodeLabel: "kubernetes.io/hostname"
```

After this change, the toleration is respected.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:00:27Z

Awesome, happy to hear. I would be very happy to welcome a PR with documentation update with such an example. It could be a subsection like "Example for using GPUs", or something like this.

### Comment by [@jessicaxiejw](https://github.com/jessicaxiejw) — 2025-09-17T14:19:50Z

@mimowo Before we document this as a limitation, how come kueue only respects node tolerations when the lowest level is `kubernetes.io/hostname`? It looks like it was introduced in https://github.com/kubernetes-sigs/kueue/pull/3678 and I cannot find the reason.

Wouldn't it work if we change
```golang
		if s.isLowestLevelNode() {
			leafDomain.nodeTaints = slices.Clone(node.Spec.Taints)
			leafDomain.nodeLabels = node.GetLabels()
		}
```
to
```golang
			leafDomain.nodeTaints = slices.Clone(node.Spec.Taints)
			leafDomain.nodeLabels = node.GetLabels()
```

Is it a hack to get around the issue of finding the bottom-most leaf nodes? I am not familiar with kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:36:54Z

The thing is that if you don't specify the hostname as the lowest level, the the lowest level domain (like a rack) may contain multiple nodes. The nodes may contain a mixed set of taints, so Kueue wouldn't know if the scheduling decisions are correct or not. Say if it assumed that every node in the domain does not have a taint, but one Node contains a taint, then the Pod scheduled on the Node would remain Pending.

Maybe it is solvable with a "virtual" layer inside Kueue for the "hostname", that would only be constructed in-memory, but it is a complication to main.

### Comment by [@jessicaxiejw](https://github.com/jessicaxiejw) — 2025-09-18T13:34:17Z

@mimowo Let me know what you think: https://github.com/kubernetes-sigs/kueue/pull/6912/files

I also fixed some grammar issues.
