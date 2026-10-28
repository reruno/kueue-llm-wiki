# Admission Fair Sharing

**Summary**: Admission fair sharing orders workloads at admission time based on each LocalQueue's or ClusterQueue's historical resource consumption, ensuring teams that have used less get priority for new admissions — without requiring preemption.

**Sources**: `raw/kueue/keps/4136-admission-fair-sharing/README.md`, `raw/kueue/keps/4136-admission-fair-sharing/kep.yaml`, pr-15000.md, pr-16034.md, pr-16241.md, issue-15221.md, issue-13602.md, pr-12786.md, pr-13844.md, pr-13621.md, pr-13481.md, pr-13433.md, pr-12946.md, raw/kueue/pkg/util/admissionfairsharing/admission_fair_sharing.go, raw/kueue/pkg/util/resource/resource.go

**Last updated**: 2026-10-28

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

Admission fair sharing is configured in the Kueue `Configuration` in the top-level `admissionFairSharing` section (a sibling of `fairSharing`) and enabled per ClusterQueue via `spec.admissionScope`:

```yaml
admissionFairSharing:
  usageHalfLifeTime: 24h         # time after which usage decays by half
  usageSamplingInterval: 5m      # how often consumedResources is updated (default 5m)
  resourceWeights:
    nvidia.com/gpu: 10           # GPUs count 10x more than CPU (default weight 1)
    cpu: 1
```

(source: raw/kueue/apis/config/v1beta2/configuration_types.go, raw/kueue/apis/config/v1beta2/defaults.go; the KEP's draft nested this under `fairSharing` with `usageHalfLifeDecayTime`, keps/4136-admission-fair-sharing/README.md)

## AdmissionScope

A ClusterQueue with `spec.admissionScope` (`admissionMode: UsageBasedAdmissionFairSharing`) collects all workloads under it and sorts them by:
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

## Entry-penalty fixes that also apply to 0.18/0.19 (pre-ledger)

These fixes predate or sit beside the `AfsUsageLedger` above and were backported to the older lines:

- **Leak on the AdmissionCheck path (pr-12786, fixes #12539; backports pr-13795/0.19, pr-13805/0.18; v0.20.0).** After the consumed-resources cache refactor (#7780) settlement ran only in the `Pending -> Admitted` branch of the workload status-transition switch, so Workloads admitted through `Pending -> QuotaReserved -> Admitted` ([[admission-check]]s: ProvisioningRequest, MultiKueue, TAS) kept their penalty forever and their LocalQueue was deprioritized. The settle call is now centralized after the switch, covering every transition into `Admitted`, and `AfsEntryPenalties.Sub` clamps at zero so a settle without a matching in-memory penalty (e.g. after a manager restart) cannot become a permanent usage discount. Rollback paths (`QuotaReserved -> Pending`, deletion while reserved) were left to #12787 (source: pr-12786.md).
- **Push only where it will be settled (pr-13844, fixes #13495; backports pr-13851/0.19, pr-13853/0.18).** The scheduler pushes an entry penalty at assume time only for ClusterQueues with `UsageBasedAdmissionFairSharing` and only for Workloads that do not already hold a reservation (no re-push on a TAS second pass); the same predicate gates the rollback on a failed admission write. See [[scheduler-internals#AFS entry penalties are pushed only where they will be settled (pr-13844)]].
- **Tick race (pr-12946, cherry-pick of #12939 to 0.17).** A sampling tick running concurrently with settlement could persist a skewed `ConsumedResources` in LocalQueue status; the tick computation is clamped and a future `LastUpdate` is handled (source: pr-12946.md).

## Sub-milli usage is no longer truncated (pr-13621)

The decay multiplies usage by `1 - A` and the new sample by `A`, where `A` is tiny for a long half-life (about 0.00034 for 168h with a 5m interval). `resource.MulByFloat` used to round each product to whole milli-units before summing, so a 2 CPU contribution of 0.6875m became 0, the stored value never grew, and **CPU and GPU usage stayed at 0 forever** (memory was unaffected because its milli value is large). `CalculateEntryPenalty` shares the helper and was affected the same way. `MulByFloat` now multiplies in arbitrary-precision decimals (`inf.Dec`) at a fixed 9-decimal scale and panics on a non-finite factor; the code rounds **down** so repeated decay reaches zero instead of settling on a non-zero fixed point (the PR text says half-up; the code is authoritative). A finer scale was rejected because a `Quantity` is `int64`-backed and `16Gi` in nano-units overflows. Expected after upgrade: LocalQueues that silently scored 0 start accumulating real usage, which can change admission order. Fixes #13596; backports pr-13761/0.19, pr-13763/0.18; v0.20.0 (source: pr-13621.md, raw/kueue/pkg/util/resource/resource.go).

## Weight configuration on LocalQueue / ClusterQueue

Both `LocalQueue` and `ClusterQueue` can set a `fairSharing.weight` field. A queue with higher weight gets a proportionally larger "fair share" of the shared resources (its usage is normalized by weight when comparing). (source: keps/4136-admission-fair-sharing/README.md)

**A weight of 0 sorts last (pr-13481, fixes #13479; backports pr-13559/0.19, pr-13564/0.18; v0.20.0).** `CalculateUsage` divides the resource-weighted usage by the LocalQueue weight. Validation accepts `fairSharing.weight: 0`, and an idle zero-weight LocalQueue produced `0/0 = NaN`, which sorts **ahead** of every real value, so it was served first. `CalculateUsage` now returns `+Inf` for any weight `<= 0`, matching `DRS.PreciseWeightedShare` for ClusterQueues (source: pr-13481.md, raw/kueue/pkg/util/admissionfairsharing/admission_fair_sharing.go).

## Interaction with DRA

DRA logical resource names (from `deviceClassMappings`) participate in admission fair sharing usage tracking via `TotalRequests`, the same way regular resources do. Use the logical name in `resourceWeights` to assign DRA resource weights. (source: keps/4136-admission-fair-sharing/README.md)

## Combination with preemption-based fair sharing

Both mechanisms can be active simultaneously. Admission fair sharing reshuffles workloads at admission; if some workloads still can't fit, preemption-based fair sharing may evict running workloads. They are complementary. (source: keps/4136-admission-fair-sharing/README.md)

## LocalQueue identity is namespace-qualified

Admission fair-sharing preemption orders candidate Workloads from different LocalQueues in the same [[cluster-queue]] by their LocalQueue usage. The identity check compared **only `spec.queueName`** — but LocalQueue names are namespace-scoped, so `team-a/default` and `team-b/default` were treated as the *same* LocalQueue. Their usage comparison was skipped entirely, and a lower-priority or more recently admitted Workload could be picked for preemption even though its LocalQueue had lower usage.

[[pr-14547]] (cherry-picks [[pr-14875]], [[pr-14876]]) compares the full namespace-qualified reference via `utilqueue.KeyFromWorkload`. The regression test uses exactly `team-a/default` vs `team-b/default` and asserts the higher-usage LocalQueue stays first in the candidate order; it fails on the unpatched code.

This is the "namespace confusion" class — see [[security-code-patterns]] and the analogous ecosystem CVE noted in [[security-authn-authz]].

## Weight lookup

The pending heap and the visibility snapshot both read LocalQueue weights from the same cached per-ClusterQueue map (`lqWeights`, default `1.0`); see [[fair-sharing#LocalQueue weight lookup: one cached path for heap and snapshot (AFS ordering)]] (pr-16241). Earlier, pr-13433 made the snapshot fall back to base ordering for the whole snapshot on any lookup error (to keep the comparator transitive); pr-16241 made that path obsolete.

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
