# Issue #8016: **[Enhancement] Enable elastic autoscaling for RayJob (similar to RayCluster/JobSet)**

**Summary**: **[Enhancement] Enable elastic autoscaling for RayJob (similar to RayCluster/JobSet)**

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8016

**Last updated**: 2026-01-21T10:08:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@jianzhihao](https://github.com/jianzhihao)
- **Created**: 2025-12-01T09:44:19Z
- **Updated**: 2026-01-21T10:08:32Z
- **Closed**: 2026-01-21T10:08:31Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

Kueue already supports elastic autoscaling for RayCluster and JobSet via the `ElasticJobsViaWorkloadSlices` feature gate. RayJob, however, is still required to keep `enableInTreeAutoscaling: false`, which prevents the Ray autoscaler from dynamically adding/removing workers. As a result, users who want **queue-aware elastic scaling** must drop back to RayCluster and manage the cluster lifecycle manually.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:45:11Z

tentatively
/priority important-longterm
cc @yaroslava-serdiuk  @hiboyang

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-12-19T19:13:03Z

@jianzhihao RayJob works with `enableInTreeAutoscaling: true` now in latest releases ([v0.15.2](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.2), [v0.14.7](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.7)).

There is [long term work](https://github.com/kubernetes-sigs/kueue/issues/8201) to disable RayJob integration and make Kueue only handle RayCluster (same way as Kueue handling RayService).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T10:08:25Z

/close 
as this is done already in https://github.com/kubernetes-sigs/kueue/pull/8284

For the long term plan we will rather go with the Workload at the RayJob level, due to the MultiKueue support: https://github.com/kubernetes-sigs/kueue/issues/8712

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-21T10:08:32Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8016#issuecomment-3777239627):

>/close 
>as this is done already in https://github.com/kubernetes-sigs/kueue/pull/8284
>
>For the long term plan we will rather go with the Workload at the RayJob level, due to the MultiKueue support: https://github.com/kubernetes-sigs/kueue/issues/8712


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
