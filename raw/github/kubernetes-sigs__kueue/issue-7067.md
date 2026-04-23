# Issue #7067: Add more details for Fair Sharing preemption in Workload Conditions

**Summary**: Add more details for Fair Sharing preemption in Workload Conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7067

**Last updated**: 2025-11-05T20:32:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-09-29T22:16:24Z
- **Updated**: 2025-11-05T20:32:53Z
- **Closed**: 2025-11-05T20:32:53Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Today, the Preemption condition only adds the following information in case of Fair Sharing:
```
Last Transition Time:  2025-09-29T20:49:34Z
    Message:               Preempted to accommodate a workload (UID: df90xyz9e-qq69-1297-98eb-abcd3e7bcd46, JobUID: UNKNOWN) due to Fair Sharing within the cohort
    Observed Generation:   1
    Reason:                Preempted
    Status:                True
    Type:                  Requeued
```

Here, it is not very clear how we can use the UID or JobUID.
In case of Fair Sharing, especially for Hierarchical Cohorts, it would be beneficial to get more details like:
- Nearest parent within which the fair sharing happened.
- Which workload caused the preemption?

**Why is this needed**:
This could be useful to report why a workload got preempted, was it due to fair sharing within the parent cohort, or fair sharing at a higher level. Also, what workload brought about the preemption.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-29T22:34:06Z

/cc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T07:58:24Z

> Nearest parent within which the fair sharing happened.

Does this indicate that showing the parent node (ClusterQueue / Cohort) for the preemptor Workload's node (ClusterQueue / Cohort)?

> Which workload caused the preemption?

IIUC, `UID` indicates preemptor. So, in the case of the above example, `df90xyz9e-qq69-1297-98eb-abcd3e7bcd46` is preemptor Workload.

### Comment by [@amy](https://github.com/amy) — 2025-09-30T16:08:27Z

@varunsyal we can't float preemptor information outside of UIDs to the condition because that's a violation of kubernetes security guidance. (ie, you could have preemptor names from other namespaces)

We can do something similar to this log line though: https://github.com/kubernetes-sigs/kueue/pull/6873/files

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-10-01T07:30:48Z

> Does this indicate that showing the parent node (ClusterQueue / Cohort) for the preemptor Workload's node (ClusterQueue / Cohort)?

I think what I meant is the Least Common Ancestor (LCA) of the preemptor and preempted workload (or its clusterqueue). My description may not have been very clear before. But the LCA here should be the cohort within which the fair sharing happened causing the preemption.
This will tell us whether the fair sharing which caused preemption happened between the clusterqueues within their parent cohort, or between its parent cohort and its siblings, and so on.

> IIUC, UID indicates preemptor. So, in the case of the above example, df90xyz9e-qq69-1297-98eb-abcd3e7bcd46 is preemptor Workload.

If the UID represents the preemptor workload, then that requirement should be good.

@Amy What's the difference between preemptorJobUID and preemptorUID in the log line update above?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T09:14:08Z

The most detailed information we have currently is under the `Preempted` condition, rather than `Requeued`. The machine readable field is reason, one of the following: https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/kueue/v1beta1/workload_types.go#L650-L664

So, it may look like:
```yaml
type: Preempted
reason: InCohortFairSharing
status: True
message: Preempted to accommodate a workload (UID: df90xyz9e-qq69-1297-98eb-abcd3e7bcd46, JobUID: UNKNOWN) due to Fair Sharing within the cohort
```

Now, there are two directions we could take depending on the aim:
1. improve the message for humans or regex parsers
2. improve for machines with API contract guarantees

For (1.) we can relatively easily add the LCA information to the message (or any other information you would find useful). For example: append: `[LCA UID= <>](message: Preempted to accommodate a workload (UID: df90xyz9e-qq69-1297-98eb-abcd3e7bcd46, JobUID: UNKNOWN) due to Fair Sharing within the cohort); LCA UID: xyz`. However, there is no API compatibility guarantee on the `message` field.

For (2.) we would need to probably have a dedicated field just for informative purposes, but it is tricky, so I would like check if (1.) is enough.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-09T09:17:10Z

When I talked to @mwielgus about this he mentioned possibly using a fully qualified path to be able to properly identify who/what caused the preemption.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T10:30:07Z

I think that can also be relatively easily to include in the preemption message.  It might be trickier if we want to have the fully qualified path for machine readable code, the again it would probably need to be a field. New fields are added by KEPS, so I would love to iterate on this feature first starting just with improving the message.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-27T08:55:17Z

/assign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-28T13:43:19Z

@varunsyal @amy My approach would be to provide fully qualified paths for both preemptor and preemptee. But it'd be good if you could confirm from your side whether it's going to be useful or not.
