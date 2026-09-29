# Admission Fair Sharing

**Summary**: Admission fair sharing orders workloads at admission time based on each LocalQueue's or ClusterQueue's historical resource consumption, ensuring teams that have used less get priority for new admissions — without requiring preemption.

**Sources**: `raw/kueue/keps/4136-admission-fair-sharing/README.md`, `raw/kueue/keps/4136-admission-fair-sharing/kep.yaml`, pr-15000.md, pr-16034.md, pr-16241.md, issue-15221.md, issue-13602.md

**Last updated**: 2026-09-29

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

To prevent a tenant from exploiting the sampling delay (submitting thousands of jobs before the next usage update), Kueue adds an **entry penalty** immediately (on admission in v0.19 and earlier; on quota reservation by default since v0.20, see below):

```
penalty = A * requested_resource
```

This is equivalent to a job's usage that has been running since the last sampling interval. (source: keps/4136-admission-fair-sharing/README.md)

## Accounting anchor: quota reservation, not admission (v0.20, Beta)

Until v0.19 the entry penalty was charged and the LocalQueue's usage was sampled only once a Workload was **Admitted**. A Workload holding quota while waiting on [[admission-check]]s therefore counted only a tiny entry penalty (about 0.034% of the request in the docs example with a 5m sampling interval and 168h half-life). Gate **`AdmissionFairSharingAnchorAtQuotaReservation`** (Beta, **default on since v0.20**, depends on `AdmissionFairSharing`) moves both sides of the boundary together to "actively holds a quota reservation" (source: pr-15000.md, raw/kueue/pkg/features/kube_features.go):

- **Penalty settlement** happens when `HasActiveQuotaReservation` flips false to true (`reachedAfsAnchor`); reactivating a Workload that still has a reservation crosses the anchor. With the gate off the old admission transition (`Admitted` and active) is used.
- **Sampled usage** used by the decay (`afsAccountedUsage`) is the LocalQueue's `ReservedUsage()` instead of `AdmittedUsage()`, but only for ClusterQueues that actually admit on usage (`ClusterQueueUsesAdmissionFairSharing`); other CQs keep admitted usage. Sampling behind the anchor would let a Workload's cost decay away while it still holds quota.
- Disabling `AdmissionFairSharing` now requires disabling the anchor gate too (dependency validated at startup).
- pr-16034 renamed the internal LocalQueue cache fields/getters for consistency (`totalReserved` to `reservedUsage`, `GetReservedUsage()`/`GetAdmittedUsage()` to `ReservedUsage()`/`AdmittedUsage()`); no behaviour change, backported to 0.19/0.18.

Penalty bookkeeping lives in `AfsUsageLedger` (`pkg/cache/queue/afs`), which stores a **per-Workload** pending-penalty record per LocalQueue. Settlement folds exactly the pushed amount into `consumed` and removes that record in the same write, so a repeated settlement folds nothing and other Workloads' penalties are untouched; a Workload deleted, deactivated without reservation, finished, or moved to another LocalQueue before settling has its penalty dropped (`SubPenalty`). A record missing (for example pushed before a manager restart) folds nothing; restart recovery is out of scope (source: raw/kueue/pkg/controller/core/workload_controller.go).

Known accounting quirks called out in pr-15000.md: (1) every reservation can settle another entry penalty, including retries that are not tenant-driven, and `TryPreferredFlavors` / [[concurrent-admission]] can amplify this when more-preferred Variants obtain further reservations; deduplication per Workload and LocalQueue is not implemented (open: issue-15221.md). (2) A LocalQueue reserving faster than `usageSamplingInterval` can defer its next published usage sample and heap rebuild until the burst pauses.

## Weight configuration on LocalQueue / ClusterQueue

Both `LocalQueue` and `ClusterQueue` can set a `fairSharing.weight` field. A queue with higher weight gets a proportionally larger "fair share" of the shared resources (its usage is normalized by weight when comparing). (source: keps/4136-admission-fair-sharing/README.md)

## Interaction with DRA

DRA logical resource names (from `deviceClassMappings`) participate in admission fair sharing usage tracking via `TotalRequests`, the same way regular resources do. Use the logical name in `resourceWeights` to assign DRA resource weights. (source: keps/4136-admission-fair-sharing/README.md)

## Combination with preemption-based fair sharing

Both mechanisms can be active simultaneously. Admission fair sharing reshuffles workloads at admission; if some workloads still can't fit, preemption-based fair sharing may evict running workloads. They are complementary. (source: keps/4136-admission-fair-sharing/README.md)

## LocalQueue identity is namespace-qualified

Admission fair-sharing preemption orders candidate Workloads from different LocalQueues in the same [[cluster-queue]] by their LocalQueue usage. The identity check compared **only `spec.queueName`** — but LocalQueue names are namespace-scoped, so `team-a/default` and `team-b/default` were treated as the *same* LocalQueue. Their usage comparison was skipped entirely, and a lower-priority or more recently admitted Workload could be picked for preemption even though its LocalQueue had lower usage.

[[pr-14547]] (cherry-picks [[pr-14875]], [[pr-14876]]) compares the full namespace-qualified reference via `utilqueue.KeyFromWorkload`. The regression test uses exactly `team-a/default` vs `team-b/default` and asserts the higher-usage LocalQueue stays first in the candidate order; it fails on the unpatched code.

This is the "namespace confusion" class — see [[security-code-patterns]] and the analogous ecosystem CVE noted in [[security-authn-authz]].

## Weight lookup

The pending heap and the visibility snapshot both read LocalQueue weights from the same cached per-ClusterQueue map (`lqWeights`, default `1.0`); see [[fair-sharing#LocalQueue weight lookup: one cached path for heap and snapshot (AFS ordering)]] (pr-16241).

## Known gap

Scheduling-equivalence hashing does not compose correctly with usage-based admission fair sharing ([[issue-14231]], open).

## Related pages

- [[fair-sharing]]
- [[cluster-queue]]
- [[local-queue]]
- [[cohort]]
- [[workload-priority]]
- [[admission]]
- [[dra]]
