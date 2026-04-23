# Issue #8081: Investigation: check scheduler performance when there are many workloads

**Summary**: Investigation: check scheduler performance when there are many workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8081

**Last updated**: 2025-12-05T14:05:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-04T16:56:39Z
- **Updated**: 2025-12-05T14:05:59Z
- **Closed**: 2025-12-05T14:05:58Z
- **Labels**: _none_
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

I'm not sure if we have an issue or not, but I would like to verify if scheduler would send multiple Workload update requests or not in case the cluster is busy. Consider the scenario;

1. the cluster has 100 gpu, all are busy
2. we consider workload-X but it is inadmissible, so we put it into inadmissibleWorklaods (we update the workload with the reason [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L798-L807)
3. some workload ends, so we requeue all workloads 
4. the workload-X is reconsidered, but still cannot fit
Question: do we send another request to update the Workload-X, or we just skip the update? IIUC the code even if we skip then we still send the [event](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L808)

The ask comes to better understand if we could improve performance on large scale deployments where we have 10k workloads, and constant inflow of new workloads, so "requeue" is called almost all the time, and workloads are constantly re-evaluated.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-04T16:56:48Z

cc @mbobrovskyi @PBundyra @mwielgus

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T11:20:41Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T14:05:53Z

/close 
as we have more generic https://github.com/kubernetes-sigs/kueue/issues/8095

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-05T14:05:59Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8081#issuecomment-3617064259):

>/close 
>as we have more generic https://github.com/kubernetes-sigs/kueue/issues/8095


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
