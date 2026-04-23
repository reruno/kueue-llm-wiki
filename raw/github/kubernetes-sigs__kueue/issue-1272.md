# Issue #1272: Add support for RayCluster

**Summary**: Add support for RayCluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1272

**Last updated**: 2024-01-26T18:50:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@andrewsykim](https://github.com/andrewsykim)
- **Created**: 2023-10-26T17:15:53Z
- **Updated**: 2024-01-26T18:50:41Z
- **Closed**: 2024-01-26T18:50:41Z
- **Labels**: `kind/feature`
- **Assignees**: [@andrewsykim](https://github.com/andrewsykim)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support RayCluster as a queue-able workload in Kueue (much like RayJob).

**Why is this needed**:

Currently Kueue supports RayJob which works great when managing ray jobs that run on ephemeral ray clusters. However, there are many use-cases and existing workloads that depend on long-lived RayClusters. Being able to account for these RayClusters with Kueue would greatly improve integration of Kueue with Ray.

**Completion requirements**:

This probably needs a KEP, but very roughly the requirements would be:
* Kueue should only account for ray worker nodes in ClusterQueue quotas (we may account for head nodes later)
* Scaling of worker nodes should be blocked on quota reservations
* Evicting or pre-empting RayClusters involves scaling worker groups to 0

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-10-26T17:16:50Z

@alculquicondor initial thoughts on this? I can try to put together a KEP if this idea doesn't sound crazy :)

### Comment by [@trasc](https://github.com/trasc) — 2023-10-27T07:03:31Z

Hi, in my opinion an easy way to do this is to have Ray create "Kueueble" pods for the workers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T13:17:53Z

It sounds reasonable to me to add support for RayCluster.
The additional thing to take into consideration is to make sure RayJobs are not doubly queued once RayCluster is also queueable.

cc @kerthcet as one of the primary users of Ray+Kueue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-27T17:39:30Z

+1

I think that supporting long-living resources would be worth it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T08:08:46Z

Make sense to me, several points here:
- RayCluster is somehow similar to RayJob because RayJob reuses `rayClusterSpec`, so the code should be reuse.
- RayCluster doesn't support `suspend` semantics, so it behaves as long-lived resources, right? Then we can't guarantee the resource utilization if the cluster is empty of jobs.

> make sure RayJobs are not doubly queued once RayCluster is also queueable.

I think we can tell this via the `clusterSelector` field.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-11-10T16:33:36Z

/assign

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-12-13T18:11:48Z

Do we still want a KEP for this? I think with the new suspend API (https://github.com/ray-project/kuberay/issues/1667), the implementation should be very straight forward.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T18:26:25Z

Historically, we haven't written KEPs for integrations.

FWIIW, the implementation should be quite similar to that of Job, whereas the implementation for RayJob will change a little to be more similar to Job. Note that if a user is queuing a RayJob, its RayCluster shouldn't be doubly queued.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-12-13T18:39:26Z

FYI @vicentefb who is working on the feature now
