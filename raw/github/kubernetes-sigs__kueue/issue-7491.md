# Issue #7491: Dealing with CQ that has RF with and without topology

**Summary**: Dealing with CQ that has RF with and without topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7491

**Last updated**: 2025-11-03T08:37:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GonzaloLuminary](https://github.com/GonzaloLuminary)
- **Created**: 2025-11-01T23:12:21Z
- **Updated**: 2025-11-03T08:37:00Z
- **Closed**: 2025-11-03T06:23:56Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 2

## Description

I have a CQ that can be simplified as

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  queueingStrategy: BestEffortFIFO
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory"]
      flavors:
        - name: "cpu-tas"
          resources:
            - name: "cpu"
              nominalQuota: "64"
            - name: "memory"
              nominalQuota: 512Gi
        - name: "cpu-autoscaling"
          resources:
            - name: "cpu"
              nominalQuota: "64"
            - name: "memory"
              nominalQuota: 512Gi
```

The RC `cpu-tas` has topology and does not autoscale while `cpu-autoscaling` does not have topology and autoscales. The issue is that the only way to schedule a workload that can run in `cpu-tas` is by adding a TAS label (for example `kueue.x-k8s.io/pod-set-unconstrained-topology`). However, if `cpu-tas` does not have capacity, then RF `cpu-autoscaling` will not be available because it does not support TAS. Is there an easy solution to this problem? Do I have to use ProvisioningRequest to handle this situation? Is there any plans to support this scenario in a simpler way (maybe a different annotation)?

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T08:28:00Z

That is a great use-case @GonzaloLuminary. AFAIK currently there is no easy workaround, what you could do is to use a custom class in ProvisioningRequest integration, and always respond true, but it means overhead of creating the AC.

I think we could consider relaxing the "implicit" mode - currently it requires all flavors to use TAS, but this requirement I feel could be relaxed. However, it would require still a change in the TAS KEP and thinking a bit deeper about consequences, probably some prototype. 

cc @mwysokin

### Comment by [@GonzaloLuminary](https://github.com/GonzaloLuminary) — 2025-11-03T08:37:00Z

Thanks @mimowo. For now I have added an admission check to the autoscaling RF and it's working fine. It's a bit unfortunate since the additional admission check increases the scheduling latency by up to 10s in GKE.
