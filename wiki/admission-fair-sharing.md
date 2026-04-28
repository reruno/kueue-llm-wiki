# Admission Fair Sharing

**Summary**: Admission fair sharing orders workloads at admission time based on each LocalQueue's or ClusterQueue's historical resource consumption, ensuring teams that have used less get priority for new admissions — without requiring preemption.

**Sources**: `raw/kueue/keps/4136-admission-fair-sharing/README.md`, `raw/kueue/keps/4136-admission-fair-sharing/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Beta** — Feature gate `AdmissionFairSharing`. (source: keps/4136-admission-fair-sharing/kep.yaml)

## How this differs from preemption-based fair sharing

[[fair-sharing]] (preemption-based) evicts running workloads from over-consuming queues to give capacity to under-consuming ones. It assumes workloads can be preempted.

Admission fair sharing works only at admission time: it reorders the candidates so that queues that have consumed less get to admit first. Running workloads are never touched. This is appropriate when:
- Workloads cannot be preempted (e.g. stateful jobs, no checkpoint).
- Users share a pool of resources but fairness should not block eventual completion.
- Throughput fairness over time is more important than instantaneous fairness.

(source: keps/4136-admission-fair-sharing/README.md)

## Configuration

Admission fair sharing is configured in the Kueue `Configuration` under the `fairSharing` section and enabled per-ClusterQueue or per-Cohort via an `AdmissionScope`:

```yaml
fairSharing:
  enable: true
  # Admission fair sharing config (AdmissionFairSharing)
  admissionFairSharing:
    usageHalfLifeDecayTime: 24h    # how fast usage decays
    usageSamplingInterval: 5m      # how often usage is recalculated
    resourceWeights:
      "nvidia.com/gpu": "10"       # GPUs count 10× more than CPU
      "cpu": "1"
```

(source: keps/4136-admission-fair-sharing/README.md)

## AdmissionScope

A ClusterQueue or Cohort that is designated as an `AdmissionScope` collects all workloads under it and sorts them by:
1. `ConsumedResources` usage (weighted by `resourceWeights`) — queues using less come first.
2. Priority — higher priority within the same usage tier.
3. Timestamp — FIFO within same priority.

(source: keps/4136-admission-fair-sharing/README.md)

## Usage tracking with decay

`ConsumedResources` is updated periodically using an exponential decay (geometric average):

```
usage_sum = (1 - A) * previous_usage_sum + A * current_usage
A = 1 - 0.5 ^ (samplingInterval / halfLifeDecayTime)
```

A half-life of 24 hours means yesterday's usage counts half as much as today's. This prevents historical overconsumption from permanently penalizing a queue. (source: keps/4136-admission-fair-sharing/README.md)

## Entry penalty

To prevent a tenant from exploiting the sampling delay (submitting thousands of jobs before the next usage update), Kueue adds an **entry penalty** immediately on admission:

```
penalty = A * requested_resource
```

This is equivalent to a job's usage that has been running since the last sampling interval. (source: keps/4136-admission-fair-sharing/README.md)

## Weight configuration on LocalQueue / ClusterQueue

Both `LocalQueue` and `ClusterQueue` can set a `fairSharing.weight` field. A queue with higher weight gets a proportionally larger "fair share" of the shared resources (its usage is normalized by weight when comparing). (source: keps/4136-admission-fair-sharing/README.md)

## Interaction with DRA

DRA logical resource names (from `deviceClassMappings`) participate in admission fair sharing usage tracking via `TotalRequests`, the same way regular resources do. Use the logical name in `resourceWeights` to assign DRA resource weights. (source: keps/4136-admission-fair-sharing/README.md)

## Combination with preemption-based fair sharing

Both mechanisms can be active simultaneously. Admission fair sharing reshuffles workloads at admission; if some workloads still can't fit, preemption-based fair sharing may evict running workloads. They are complementary. (source: keps/4136-admission-fair-sharing/README.md)

## Related pages

- [[fair-sharing]]
- [[cluster-queue]]
- [[local-queue]]
- [[cohort]]
- [[workload-priority]]
- [[admission]]
- [[dra]]
