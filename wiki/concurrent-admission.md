# Concurrent Admission

**Summary**: An alpha feature that lets a Workload simultaneously pursue admission on multiple ResourceFlavors in parallel, enabling flavor migration and racing long-running AdmissionChecks across different accelerator types.

**Sources**: `raw/kueue/keps/8691-concurrent-admission/README.md`, `raw/kueue/keps/8691-concurrent-admission/kep.yaml`

**Last updated**: 2026-04-28

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
- `StrictFIFO` queueing strategy behavior with Concurrent Admission is undefined (non-goal for alpha).
- Increases API object count in etcd (one Variant per flavor subset per pending workload).

(source: keps/8691-concurrent-admission/README.md)

## Related pages

- [[admission]]
- [[resource-flavor]]
- [[cluster-queue]]
- [[workload]]
- [[admission-check]]
- [[provisioning-request]]
- [[elastic-jobs]]
- [[feature-gates]]
