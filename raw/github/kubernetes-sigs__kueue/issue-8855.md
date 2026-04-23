# Issue #8855: ☂️ Review the state of feature gates and drop those no longer needed for 0.17

**Summary**: ☂️ Review the state of feature gates and drop those no longer needed for 0.17

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8855

**Last updated**: 2026-03-05T13:57:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-28T12:59:30Z
- **Updated**: 2026-03-05T13:57:40Z
- **Closed**: 2026-03-05T13:57:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 22

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We have quite a few feature gates which accumulated over time, some could already be graduated or dropped.

Probably (let's see if there is a veto)
- drop TASProfileLeastFreeCapacity
- GA LendingLimit
- GA PrioritySortingWithinCohort
- GA SanitizePodSets 
- GA PropagateBatchJobLabelsToWorkload 
- drop MultiKueueAllowInsecureKubeconfigs (or at least mark as deprecated clearly)

Let me know if you see other candidates for 0.17 or 0.18

**Why is this needed**:

To keep the code as simple as possible, but no more. so let me know if you are using some of the feature gates, then we can defer the graduation / drop in time.

## Discussion

### Comment by [@mykysha](https://github.com/mykysha) — 2026-01-28T13:07:27Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T13:11:02Z

cc @kannon92 @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T13:12:09Z

cc @amy

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T13:12:27Z

cc @tenzen-y @gabesaba

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-28T14:03:14Z

For our operator we don't allow people to set feature gates because we realized that eventually they would be removed.

I have no issues with removing any of these features gates.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T16:49:37Z

@mimowo what about promoting `MultiKueueBatchJobWithManagedBy` to GA? The JobManagedBy K8s feature has already enabled by default in all Kueue supporting K8s versions (v1.32 - v1.35).

https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#:~:text=1.31-,JobManagedBy,%E2%80%93,-JobPodReplacementPolicy

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T13:27:48Z

+1, I think we are ready, cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-12T21:08:39Z

- [x] drop TASProfileLeastFreeCapacity: https://github.com/kubernetes-sigs/kueue/pull/9298
- [x] GA LendingLimit: https://github.com/kubernetes-sigs/kueue/pull/9258
- [x] GA SanitizePodSets: https://github.com/kubernetes-sigs/kueue/pull/9260
- [x] GA PropagateBatchJobLabelsToWorkload
- [x] GA MultiKueueBatchJobWithManagedBy
- [x] GA HierarchicalCohorts: https://github.com/kubernetes-sigs/kueue/pull/9618
- [x] GA LocalQueueDefaulting: https://github.com/kubernetes-sigs/kueue/pull/9299
- [x] GA ObjectRetentionPolicies: https://github.com/kubernetes-sigs/kueue/pull/9300

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T11:20:00Z

@mimowo @gabesaba I'd like to propose HierarchicalCohorts, LocalQueueDefaulting, and ObjectRetentionPolicies GA graduations as well.
Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T11:40:13Z

sgtm, I see no concerns about graduating these features as well

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-16T13:52:32Z

> [@mimowo](https://github.com/mimowo) [@gabesaba](https://github.com/gabesaba) I'd like to propose HierarchicalCohorts, LocalQueueDefaulting, and ObjectRetentionPolicies GA graduations as well. Any thoughts?

Let's do that as dedicated issues for each feature.

I'd like to leave this issue as dropping feature gates or deprecations.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-16T13:53:07Z

Based on https://github.com/kubernetes-sigs/kueue/issues/9289, I think we will not drop MultiKueueAllowInsecureKubeconfigs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T14:02:10Z

> > [@mimowo](https://github.com/mimowo) [@gabesaba](https://github.com/gabesaba) I'd like to propose HierarchicalCohorts, LocalQueueDefaulting, and ObjectRetentionPolicies GA graduations as well. Any thoughts?
> 
> Let's do that as dedicated issues for each feature.
> 
> I'd like to leave this issue as dropping feature gates or deprecations.

This is an umbrella issue for 0.17 and 0.18. So, if anyone take each graduation, they can open a dedicated issue.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-16T16:29:04Z

> Based on [#9289](https://github.com/kubernetes-sigs/kueue/issues/9289), I think we will not drop MultiKueueAllowInsecureKubeconfigs.

On second thought the main ask is to mark the feature gate as deprecated. https://github.com/kubernetes-sigs/kueue/pull/9297

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T16:36:30Z

> On second thought the main ask is to mark the feature gate as deprecated. https://github.com/kubernetes-sigs/kueue/pull/9297

Yes, let's start here as we don't fully know if this is needed for dev envs or not https://github.com/kubernetes-sigs/kueue/issues/9289. We don't need to rush, deprecating for now is enough, and we will drop when we can have the dev setup working without it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T16:47:40Z

> > Based on [#9289](https://github.com/kubernetes-sigs/kueue/issues/9289), I think we will not drop MultiKueueAllowInsecureKubeconfigs.
> 
> On second thought the main ask is to mark the feature gate as deprecated. https://github.com/kubernetes-sigs/kueue/pull/9297

+1 on deprecation as starting point.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-04T11:56:29Z

@kannon92 can I assign this issue to you?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-04T18:14:27Z

Once https://github.com/kubernetes-sigs/kueue/pull/9618 merges, we should be good to close this one out.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-05T06:08:14Z

/unassign @mykysha

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-05T06:08:36Z

/assign @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-05T13:57:33Z

Thank you @PannagaRao for finishing this off.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-05T13:57:40Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8855#issuecomment-4005243839):

>Thank you @PannagaRao for finishing this off.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
