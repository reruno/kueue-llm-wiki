# Issue #8339: [TAS] Kueue tries to move inadmissible workloads to heap too many times upon a node change

**Summary**: [TAS] Kueue tries to move inadmissible workloads to heap too many times upon a node change

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8339

**Last updated**: 2026-01-09T18:53:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-12-18T16:53:00Z
- **Updated**: 2026-01-09T18:53:58Z
- **Closed**: 2026-01-09T18:53:58Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
There's a mechanism in TAS that moves inadmissible workloads back to heap if there's some change to a node.
Once triggered, workloads in a whole CQ/Cohort hierarchy are put back at the front of the queue: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/queue/manager.go#L625

However in lines: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/tas/resource_flavor.go#L183-L190 we trigger this moving for every active CQ.

 **As a result we put back the workloads in a whole hierarchy N times, where N=number of CQ in a hierarchy.** 

**What you expected to happen**:
I expect that putting back workloads happens only once per change of node

**How to reproduce it (as minimally and precisely as possible)**:
Kueue: latest
Kind cluster manifest: `tas-kind-cluster.yaml` from the `hack/` folder
Manifests of the whole hierarchy:

```
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "cloud.provider.com/topology-block"
  - nodeLabel: "kubernetes.io/hostname"
---
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta2
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    cloud.provider.com/node-group: "tas-group"
  topologyName: "default"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "cq"
spec:
  namespaceSelector: {} # match all.
  cohortName: "root"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cq"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "cq-2"
spec:
  cohortName: "root"
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: Cohort
metadata:
  name: "root"
```

Try to change anything about a node e.g. value of some label and observe that for each `Reconcile TAS Resource Flavor` log there are two `Attempting to move workloads` logs

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:29:33Z

/priority important-soon

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-05T20:54:06Z

/assign
