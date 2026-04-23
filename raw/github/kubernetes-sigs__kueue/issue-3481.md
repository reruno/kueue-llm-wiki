# Issue #3481: [Bug] [Doc] TAS's document is wrong

**Summary**: [Bug] [Doc] TAS's document is wrong

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3481

**Last updated**: 2024-11-13T07:18:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2024-11-07T12:36:34Z
- **Updated**: 2024-11-13T07:18:49Z
- **Closed**: 2024-11-13T07:18:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
![image](https://github.com/user-attachments/assets/2969b96b-990a-4e0a-b06d-5c355c31355d)


**What you expected to happen**:
I think this should be `cloud.provider.com/topology-block`

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T12:52:38Z

Yeah, this is corrupted :) , but it should not be `cloud.provider.com/topology-block`.

The role of the nodeLabel is to restrict TAS nodes to a dedicated subset of nodes. You may want to do that to for example use TAS only on GPU nodes, or exclude control plane nodes. Or have two disjoint TAS pools.

This may depend on the cloud provider and your use case. For example, on GKE you may want to restrict it to a dedicted node pool for GPU using: `cloud.google.com/gke-nodepool: tas-a100-pool`. Still, this node group may contain many blocks or racks.

Surely we should adjust the docs, by renaming it to, for example: `cloud.provider.com/node-group: tas-node-group` + we can better explain the role of the label in the text.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T12:52:58Z

@KunWuLuan feel free to submit a PR

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-11-08T01:30:36Z

> The role of the nodeLabel is to restrict TAS nodes to a dedicated subset of nodes. You may want to do that to for example use TAS only on GPU nodes, or exclude control plane nodes. Or have two disjoint TAS pools.

Thanks mimowo. Let me understand, if I set `cloud.provider.com/topology-block=tas-node-group` in RF, then the podSet will only be scheduled on node with `cloud.provider.com/topology-block=tas-node-group`, right? 
What if only some of the labels are set on nodes?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T09:40:57Z

> if I set cloud.provider.com/topology-block=tas-node-group in RF, then the podSet will only be scheduled on node with cloud.provider.com/topology-block=tas-node-group, right?

This is not the intention of the `cloud.provider.com/topology-block` label. The `cloud.provider.com/topology-block` is meant to be used in the Topology API to denote the "block" level. 

The label on the ResourceFlavor is meant to constrain the pool of nodes dedicated to TAS. For example, for GKE a good candidate might be `cloud.google.com/gke-nodepool` label, but it will depend on the use case.

What if only some of the labels are set on nodes?

TAS only considers nodes which:
- have the same key and value as in the ResourceFlavor spec.nodeLabels
- have the same key as in Topology, `spec.levels.nodeLabel[*]`

cc @mwysokin
