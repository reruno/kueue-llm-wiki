# Issue #706: Set up resource flavor to clusterqueue

**Summary**: Set up resource flavor to clusterqueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/706

**Last updated**: 2023-04-20T22:27:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@blackironj](https://github.com/blackironj)
- **Created**: 2023-04-19T06:13:41Z
- **Updated**: 2023-04-20T22:27:48Z
- **Closed**: 2023-04-20T22:27:48Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 2

## Description

I have a question about setting up resource flavor to cluster queue.
If multiple nodes have the same node label, I'm wondering if the flavor quota should be the sum of the resources on the node or if it's an amount per node.


**For example)**
Three nodes on k8s cluster
|       | gpu-type        | how many | 
|-------|-----------------|----------|
| nodeA | nvidia-rtx-3090 | 8        |
| nodeB | nvidia-rtx-3090 | 8        |
| nodeC | nvidia-a100     | 4        |

- clsuterqueue.yaml
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "nvidia-rtx-3090"
spec:
  nodeLabels:
    gpu-type: "nvidia-rtx-3090"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "nvidia-a100"
spec:
  nodeLabels:
    gpu-type: "nvidia-a100"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cluster-total
spec:
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: "nvidia-rtx-3090"
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: # 8? 16? 
        - name: "nvidia-100"
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 4
```
In this case, What value should I put to assign all GPUs of nodeA, B to the clusterqueue? 
Or Should I make another flavor? (nvidia-rtx-3090-1, nvidia-rtx-3090-2)

Thank you!

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-20T09:11:01Z

@blackironj 
Hi! I think in your case, you should set nominalQuota to 16 for flavor nvidia-rtx-3090.
nominalQuota should be the sum of resources.

### Comment by [@blackironj](https://github.com/blackironj) — 2023-04-20T22:27:04Z

> @blackironj 
> 
> Hi! I think in your case, you should set nominalQuota to 16 for flavor nvidia-rtx-3090.
> 
> nominalQuota should be the sum of resources.

Thank you for replying!
