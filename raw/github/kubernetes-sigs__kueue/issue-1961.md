# Issue #1961: [metrics] The admission_wait_time_seconds metric is misleading when AdmissionChecks are used

**Summary**: [metrics] The admission_wait_time_seconds metric is misleading when AdmissionChecks are used

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1961

**Last updated**: 2024-04-23T06:48:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-09T12:40:14Z
- **Updated**: 2024-04-23T06:48:57Z
- **Closed**: 2024-04-23T06:48:57Z
- **Labels**: `kind/bug`, `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

/kind bug
/kind feature

**What happened**:

The metric is incremented whenever a workload has QuotaReserved:  https://github.com/kubernetes-sigs/kueue/blob/b9c346a83d965d7849e4e27cf7e06e5ee1ad22df/pkg/scheduler/scheduler.go#L540

However, it may take arbitrarily long to admit the workload, but the metric says "The time between a Workload was created until it was admitted, per 'cluster_queue'".

**What you expected to happen**:

The metric should measure time to admission.

**How to reproduce it (as minimally and precisely as possible)**:

Create a cluster Queue with an admission check. 

**Proposed approach**:

The fix should contain two things:
- "fix" the metrics `admission_wait_time_seconds` so that it measures time to "Admitted" condition since creation time, or last eviction time
- "add" a new metric `quota_reserved_wait_time_seconds` which is measures what the current implementation is measuring

Regarding the  `admission_wait_time_seconds`  metric, the good starting point would be to move incrementing the metric under `IsAdmitted` [here](https://github.com/kubernetes-sigs/kueue/blob/b9c346a83d965d7849e4e27cf7e06e5ee1ad22df/pkg/scheduler/scheduler.go#L537-L539). However, there is another place which needs to be adjusted, around [here](https://github.com/kubernetes-sigs/kueue/blob/b9c346a83d965d7849e4e27cf7e06e5ee1ad22df/pkg/controller/core/workload_controller.go#L179-L182).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T12:49:38Z

/cc @alculquicondor @tenzen-y WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-09T15:29:19Z

This metric was created before admission checks existed :(

We need a better name for it. I would be ok making a "breaking change", given that the metric is essentially broken.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T15:42:22Z

I'm ok changing the name, but keeping the name and fixing seems reasonable either. 

The metric is still correct for installations without admission checks. And the built-in admission checks are still alpha.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T15:43:39Z

Or essentially rename to QuotaReservedWaitTime :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-09T16:03:58Z

Right, so keeping the existing metric, but actually based on admission time.

And add a new metric for quota reserved time.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-10T10:01:41Z

> Right, so keeping the existing metric, but actually based on admission time.
> 
> And add a new metric for quota reserved time.

I prefer to select this approach. Also, I think we should introduce the `QuotaReservedWaitTime` metric and change semantic of existing metrics in the same minor release.

Also, notifying `ACTION REQUIRED` in the release note would be better.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-10T16:44:38Z

I have updated the "Proposed approach" section.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-10T17:01:25Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-11T07:16:48Z

/assign
