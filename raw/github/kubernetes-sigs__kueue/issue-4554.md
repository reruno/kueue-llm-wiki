# Issue #4554: Cohort Fair Sharing Status and Metrics

**Summary**: Cohort Fair Sharing Status and Metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4554

**Last updated**: 2025-03-17T13:07:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-11T11:06:14Z
- **Updated**: 2025-03-17T13:07:51Z
- **Closed**: 2025-03-17T13:07:51Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What would you like to be added**:
Add [FairSharingStatus](https://github.com/kubernetes-sigs/kueue/blob/e1c027a57d128925b8d1e2944d3cc20bf5edc009/apis/kueue/v1beta1/fairsharing_types.go#L38-L47) to [Cohort](https://github.com/kubernetes-sigs/kueue/blob/e1c027a57d128925b8d1e2944d3cc20bf5edc009/apis/kueue/v1alpha1/cohort_types.go#L70-L73), and expose Cohort weighted share metric. Implementation should be similar to ClusterQueue:

https://github.com/kubernetes-sigs/kueue/blob/e1c027a57d128925b8d1e2944d3cc20bf5edc009/pkg/controller/core/clusterqueue_controller.go#L729-L739

Note that this value will only appear in the Hierarchical case - as the value is only defined Cohorts which have a parent Cohort.

**Why is this needed**:
Related to #3759. This will allow customers to introspect usage of Cohort hierarchies

**Completion requirements**:
- Create CohortStatus
- Add FairSharingStatus to CohortStatus
- Create metric, similar to [ClusterQueueWeightedShare](https://github.com/kubernetes-sigs/kueue/blob/e1c027a57d128925b8d1e2944d3cc20bf5edc009/pkg/metrics/metrics.go#L360-L372)
- Set these values in Cohort reconciler, calculated using [dominantResourceShare](https://github.com/kubernetes-sigs/kueue/blob/567af080c12aee76cde34c116ae7ce8e3d7181f5/pkg/cache/fair_sharing.go#L41-L47)(cache.Cohort, nil)
  - see how CQ does this [here](https://github.com/kubernetes-sigs/kueue/blob/567af080c12aee76cde34c116ae7ce8e3d7181f5/pkg/cache/cache.go#L683-L686)
- Test this logic. Tests must use hierarchical Cohorts, as value is only defined for non-root Cohorts

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update
- [x] Code Change

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-11T11:07:04Z

cc @mbobrovskyi @mimowo

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-11T13:17:48Z

/assign
