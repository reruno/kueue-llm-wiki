# Issue #2404: Distinguish between Preemption due to reclamation and fair sharing

**Summary**: Distinguish between Preemption due to reclamation and fair sharing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2404

**Last updated**: 2024-07-10T15:28:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-06-12T13:47:55Z
- **Updated**: 2024-07-10T15:28:57Z
- **Closed**: 2024-07-10T15:28:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 5

## Description

**What would you like to be added**:

An additional reason in the Preemption condition to indicate that the preemption was due to fair sharing and not regular reclamation.

The current reason for reclamation or fair sharing is `InCohort`

We could have: `InCohortReclamation` and `InCohortFairSharing`.

**Why is this needed**:

For better visibility

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-06-14T01:25:42Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-06-14T10:15:56Z

@alculquicondor
https://github.com/kubernetes-sigs/kueue/blob/6ecaa877ee65791e6333f147fafcbb7888039a03/pkg/scheduler/scheduler.go#L247-L251

If Assigment is borrowing then the reason should be InCohortFairSharing? Or should the decision be based on `enableFairSharing` of Preemptor?
https://github.com/kubernetes-sigs/kueue/blob/45eee46b1c1264a8a025d0a811de78e99fbc7abb/pkg/scheduler/preemption/preemption.go#L49-L59

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T12:15:52Z

I think the decision is based entirely on the preemptor. If the preemptor fits in the nominal quota of its ClusterQueue, then it's preempting others that are borrowing its quota.
Otherwise, it's past the nominal quota, meaning that it's using resources from the fair share.

Note that whether fair sharing is enabled is global.

/assign @vladikkuzn

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T12:16:14Z

cc @gabesaba

### Comment by [@trasc](https://github.com/trasc) — 2024-06-18T15:05:30Z

> I think the decision is based entirely on the preemptor. If the preemptor fits in the nominal quota of its ClusterQueue, then it's preempting others that are borrowing its quota.
> Otherwise, it's past the nominal quota, meaning that it's using resources from the fair share.

Also, if the preemptor and preemptee are in the same cluster queue we can say it's a simple priority based eviction (no quota is reclaimed from a borrower)
