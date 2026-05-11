# Concurrent Admission

**Summary**: An alpha feature that lets a Workload simultaneously pursue admission on multiple ResourceFlavors in parallel, enabling flavor migration and racing long-running AdmissionChecks across different accelerator types.

**Sources**: `raw/kueue/keps/8691-concurrent-admission/README.md`, `raw/kueue/keps/8691-concurrent-admission/kep.yaml`

**Last updated**: 2026-05-08

---

> **Stage: Alpha** — Feature gate `ConcurrentAdmission`, disabled by default. (source: keps/8691-concurrent-admission/kep.yaml)

## Problem

Kueue's current admission model evaluates one [[resource-flavor]] at a time. A workload picks a flavor and pursues it until admitted. This prevents two useful scenarios:

1. **Flavor migration**: a workload starts on `spot` but should upgrade to `reservation` when it becomes available, without being manually re-queued.
2. **Racing AdmissionChecks**: a workload could try `nvidia-a100` and `nvidia-h100` simultaneously and take whichever checks pass first.

(source: keps/8691-concurrent-admission/README.md)

## Core concepts

### Parent and Variant Workloads

Concurrent Admission introduces two new Workload roles:

- **Parent Workload**: the original Workload. It is excluded from Kueue's scheduling loop; it acts only as an owner and status aggregator.
- **Variant Workload**: a clone of the parent with specific `AdmissionConstraints` restricting it to a subset of ResourceFlavors. Variants are scheduled independently by Kueue's regular scheduling loop.

A Parent has a 1:N relationship with its Variants. Each Variant is a distinct Kubernetes object in etcd. (source: keps/8691-concurrent-admission/README.md)

### Variant controller

A new `VariantController` manages the lifecycle of Variants:
- **Creation**: creates Variant Workloads from the Parent according to the ClusterQueue's `concurrentAdmission` spec.
- **Aggregation**: collects Variant statuses and rolls them up to the Parent.
- **Policy enforcement**: ensures only one Variant is admitted at a time. If a preferred Variant becomes available (higher flavor), the currently admitted Variant is evicted.
- **Eviction**: when the admitted Variant needs to be evicted (to migrate), the controller triggers eviction and re-queues the parent flow.

(source: keps/8691-concurrent-admission/README.md)

## ClusterQueue API extension

The [[cluster-queue]] spec gains a `concurrentAdmission` field that describes which flavor subsets Variants should target:

```yaml
spec:
  concurrentAdmission:
    variants:
    - flavors: [reservation]          # most preferred
    - flavors: [on-demand]            # fallback
    - flavors: [spot]                 # least preferred
```

(source: keps/8691-concurrent-admission/README.md)

## Workload API extension

Variants carry `spec.admissionConstraints` that restrict which flavors they may use. The constraints also define upgrade/migration policies:

```yaml
spec:
  admissionConstraints:
    allowedFlavors: [on-demand]
    # upgrade policies (when to migrate to a more preferred variant)
```

Only one Variant per Parent may be admitted at a time. The Variant controller enforces this. (source: keps/8691-concurrent-admission/README.md)

## Key use cases

**Story 1 — Flavor upgrade**: A workload starts on `spot`. When `reservation` quota becomes available, the `reservation` Variant can be admitted, the `spot` Variant is evicted, and the job migrates.

**Story 2 — Racing admission checks**: Two Variants target different GPU types. Each runs its [[provisioning-request]] or custom [[admission-check]] independently. The Variant whose check passes first wins; the other is deactivated.

**Story 3 — Delay fallback**: Configure a timeout before falling back to a less preferred flavor, giving the preferred flavor a chance to free up.

(source: keps/8691-concurrent-admission/README.md)

## Constraints

- Only works with job types that can tolerate pod recreation (migration involves pod deletion and restart).
- **`StrictFIFO` queueing strategy is rejected at the webhook layer** when ConcurrentAdmission is enabled on a CQ — the [[cluster-queue]] validation webhook now returns an error if both are configured ([[pr-11022]]; per the KEP, ConcurrentAdmission cannot be combined with StrictFIFO because Variants migrating in and out of admission would violate strict ordering).
- Increases API object count in etcd (one Variant per flavor subset per pending workload).

(source: keps/8691-concurrent-admission/README.md)

## Implementation details (v0.18 hardening)

### Variant scheduling-equivalence hash

Kueue's scheduler skips re-evaluating Workloads whose **scheduling hash** matches one already determined inadmissible in the same cycle (the SchedulingEquivalenceHashing optimization). Variants of the same Parent share PodSets and most spec fields, so without an extra disambiguator they would all hash to the same value and only the first Variant's NoFit decision would matter — a pessimistic same-flavor result on Variant A would suppress Variant B even though B targets a different ResourceFlavor.

[[pr-10910]] adds the `kueue.x-k8s.io/allowed-resource-flavor` annotation (`WorkloadAllowedResourceFlavorAnnotation`) into the scheduling-hash computation, so each Variant gets its own bucket and is evaluated independently.

### Indexer for parent → Variant lookup

[[pr-10921]] swaps the ConcurrentAdmission controller's manual scan over Workloads for the existing `OwnerReferenceUID` indexer, so finding all Variants of a given Parent is an O(1) hash lookup. Closes [[issue-10904]].

### Skipping less-favorable Variants while a more-favorable one is running

Without this guard, the scheduler can admit a less-favorable Variant (e.g. `spot`) while a more-favorable Variant (e.g. `reservation`) is already running — typically because the more-favorable Variant's evaluation took longer in the same cycle. [[pr-10917]] makes the scheduler skip admission of a less-favorable Variant when **any** more-favorable Variant of the same Parent is already running; the ConcurrentAdmission controller subsequently deactivates the skipped Variant. Fixes [[issue-10913]].

### Events on Variant lifecycle

The ConcurrentAdmission controller now emits Kubernetes Events on Variant **creation, activation, and deactivation** ([[pr-10951]]), making the migration lifecycle visible via `kubectl describe` and metrics.

### Comma-separated annotation parsing cleanup

[[pr-10957]] consolidates the parsing of comma-separated annotation values used by the controller (e.g. for the allowed-flavor list).

### Preemption.Target wrapping removed

[[pr-10954]] removes a redundant `preemption.Target` wrapping around `workload.Info` in the ConcurrentAdmission scheduler path; no behaviour change but cleaner internal types.

## Related pages

- [[admission]]
- [[resource-flavor]]
- [[cluster-queue]]
- [[workload]]
- [[admission-check]]
- [[provisioning-request]]
- [[elastic-jobs]]
- [[feature-gates]]
