# Issue #2258: Show fair share of a CQ in status and a metric

**Summary**: Show fair share of a CQ in status and a metric

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2258

**Last updated**: 2024-05-27T17:13:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-22T14:58:20Z
- **Updated**: 2024-05-27T17:13:30Z
- **Closed**: 2024-05-27T17:13:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A metric `cluster_queue_weighted_share` and a field in the ClusterQueue status that shows the live calculation of https://github.com/kubernetes-sigs/kueue/blob/a7ca2acc2042b047137a769bfcb1e6b749eba469/pkg/cache/clusterqueue.go#L673

The API could look like:

```yaml
status:
  fairSharing:
    rawShare: 50
    weightedShare: 25
```

Note that the comment in the function needs to be updated. rawShares can be 0 to 1000, but weightedShare can be up to 1M (because the smallest possible value for the weight is 0.001).

**Why is this needed**:

For visibility and debugability

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T14:58:28Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T14:58:33Z

cc @gabesaba

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-23T08:05:06Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-23T12:11:59Z

@alculquicondor Is I correct understood that in the context of 

https://github.com/kubernetes-sigs/kueue/blob/a7ca2acc2042b047137a769bfcb1e6b749eba469/pkg/cache/clusterqueue.go#L719-L722

drs before L720 is rawShare and after that it's the weightedShare?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T15:16:13Z

correct.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T15:16:36Z

That said, I'm not convinced that `rawShare` is the best name for it. I'm open to suggestions.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-23T16:34:40Z

> That said, I'm not convinced that `rawShare` is the best name for it. I'm open to suggestions.

In my opinion, if there is no  plan to change the weight algorithm, one of the two fields can be skipped ,one multiply and one division  (with 1000 and a spec field) should not be that hard to extract the one from the other.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T16:56:55Z

The only value that is actually used in algorithms is `weightedShare`, so that would have to definitely be included.

The other one just increases debuggability, as it directly summarizes what the "usage" of a ClusterQueue is. But we can skip it for now and wait for user feedback if it's needed in the future.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-23T18:08:07Z

@alculquicondor should we add this metric only if `metrics.enableClusterQueueResources` is enabled?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T18:14:06Z

Yes, that sounds like a good call

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T18:14:59Z

Also, if fairSharing is enabled.
