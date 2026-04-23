# Issue #2491: Add a metric that tracks the number of preemptions issued by a ClusterQueue

**Summary**: Add a metric that tracks the number of preemptions issued by a ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2491

**Last updated**: 2024-07-18T14:16:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-06-27T14:31:31Z
- **Updated**: 2024-07-18T14:16:55Z
- **Closed**: 2024-07-18T14:16:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

**What would you like to be added**:

A metric that counts how many preemptions a ClusterQueue has issued, broken down by whether it was internal to the ClusterQueue, it was a reclamation, fair sharing or priority threshold.

This is somewhat the opposite direction of `evicted_workloads_total`, but focused on Preemption.

**Why is this needed**:

Improve observability.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-27T14:31:38Z

/assign @vladikkuzn

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-02T15:19:22Z

To clarify, this counter should increment for every workload that is preempted.

### Comment by [@trasc](https://github.com/trasc) — 2024-07-03T05:59:33Z

In this case we can just extend 

https://github.com/kubernetes-sigs/kueue/blob/1d849aa016c8d3672adb3afcddedc23527f00429/pkg/metrics/metrics.go#L137-L149

and add an additional label for the preemption scope.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T11:50:02Z

Yes, indeed, that would be useful.

But this counter is from the point-of-view of the preemptee CQ.

The request is from the point-of-view of the preemptor CQ.

### Comment by [@trasc](https://github.com/trasc) — 2024-07-03T12:29:31Z

...  that is a bit different , so count the preemptees but group but group by the preemptor's CQ name. We could ad yet another metric label "preemptor_cluster_queue" but we can end up creating too many metric data-points.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T14:17:50Z

Preemption is one of the few actions that involves two entities.
We could also have one metric that has both clusterqueues as labels, but that could cause explosion of cardinality.
Having one for each side sounds like a reasonable compromise.
