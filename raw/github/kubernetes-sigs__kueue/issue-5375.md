# Issue #5375: Kueue TAS fails to schedule a workload in LeastFreeCapacity mode if there is a domain that cannot fit that workload.

**Summary**: Kueue TAS fails to schedule a workload in LeastFreeCapacity mode if there is a domain that cannot fit that workload.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5375

**Last updated**: 2025-07-28T09:46:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-05-27T12:48:28Z
- **Updated**: 2025-07-28T09:46:51Z
- **Closed**: 2025-07-28T09:46:51Z
- **Labels**: `kind/bug`
- **Assignees**: [@mwysokin](https://github.com/mwysokin), [@PBundyra](https://github.com/PBundyra)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Kueue TAS scheduling in LeastFreeCapacity mode is failing to schedule workload if the domain with the lowest capacity does not fit it, even if there are domains that could fit that workload.

For example if there are two domains with capacity of 1 pod and 2 pods. User wants to run a workload that requires 2 pods. Kueue will fail to schedule that workload.

**What you expected to happen**:
TAS algorithm should find a domain that can fit the workload and has the lowest free capacity (if it exists).

In our example of two domains with capacity of 1 pod and 2 pods and workload with 2 pods we should expect Kueue to schedule that workload on a second domain with capacity of 2 (which has the lowest free capacity among all domains that can fit the workload).

**How to reproduce it (as minimally and precisely as possible)**:
@PBundyra wrote a UT that should pass, but it is failing:
```go
"host required; single Pod fits in the largest host; LeastFreeCapacityFit": {
  nodes: defaultNodes,
  topologyRequest: &kueue.PodSetTopologyRequest{
    Required: ptr.To(corev1.LabelHostname),
  },
  levels: defaultThreeLevels,
  requests: resources.Requests{
    corev1.ResourceCPU: 1000,
  },
  count: 2,
  wantAssignment: &kueue.TopologyAssignment{
    Levels: defaultOneLevel,
    Domains: []kueue.TopologyDomainAssignment{
      {
        Count: 2,
        Values: []string{
          "x6",
        },
      },
    },
  },
  enableFeatureGates: []featuregate.Feature{features.TASProfileLeastFreeCapacity},
},
```

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

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-05-28T20:30:19Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-30T09:39:12Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T09:46:46Z

/close 
This is fixed by https://github.com/kubernetes-sigs/kueue/pull/5803

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-28T09:46:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5375#issuecomment-3126425449):

>/close 
>This is fixed by https://github.com/kubernetes-sigs/kueue/pull/5803


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
