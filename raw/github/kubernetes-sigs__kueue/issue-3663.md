# Issue #3663: TAS: API to support rank-based ordering for custom CRDs

**Summary**: TAS: API to support rank-based ordering for custom CRDs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3663

**Last updated**: 2024-12-03T09:41:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-27T08:53:42Z
- **Updated**: 2024-12-03T09:41:02Z
- **Closed**: 2024-12-03T09:41:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 3

## Description

**What would you like to be added**:

API which allows to use custom PodIndex labels for custom CRD jobs, without the incentive to use labels
reserved for kubernetes in the in-house Jobs.

**Why is this needed**:

* the current PodIndex labels lookup only work for "known" jobs with built-in integrations: [here](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/controller/tas/topology_ungater.go#L425-L442)
* this will not work for in-house Jobs, unless the developers use the labels from other projects (like kubernetes.io/job-completion-index), which creates an unhealthy incentive in the long run
* This is part of the graduation plan for stable:  https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling#stable.

**Completion requirements**:

- [ ] KEP update
- [ ] API change
- [ ] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T08:53:48Z

The proposal is to extend the workload [PodSetTopologyRequest API](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/apis/kueue/v1beta1/workload_types.go#L90C6-L90C27) with the following fields:
```golang
// PodIndexLabel indicates the name of the label indexing the pods. 
// For example, in the context of
// - kubernetes job this is: kubernetes.io/job-completion-index
// - JobSet: kubernetes.io/job-completion-index (inherited from Job)
// - Kubeflow: training.kubeflow.org/replica-index
PodIndexLabel *string

// SubGroupIndexLabel indicates the name of the label indexing the instances of replicated Jobs (groups)
// within a PodSet. For example, in the context of JobSet this is jobset.sigs.k8s.io/job-index.
SubGroupIndexLabel *string

// SubGroupIndexLabel indicates the count of replicated Jobs (groups) within a PodSet.
// For example, in the context of JobSet this value is read from jobset.sigs.k8s.io/replicatedjob-replicas.
SubGroupCount *int32
```

The values could be then set when implementing the `PodSets()` function in the `GenericJob` interface via the
`PodSetTopologyRequest` helper function like [here](https://github.com/kubernetes-sigs/kueue/blob/560e4340b746aa811cec06b7a072a1a3faedc80f/pkg/controller/jobs/job/job_controller.go#L256).

Then, the API could be read from TopologyUngater, instead of the lookups.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T08:54:03Z

cc @PBundyra @tenzen-y @mwielgus @mwysokin

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-02T13:51:11Z

/assign
