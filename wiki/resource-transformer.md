# Resource Transformer

**Summary**: Resource transformers let cluster admins define global rules that rewrite a workload's resource requests into different quota units before Kueue applies admission and quota calculations — without touching the actual Pod resource requests seen by kube-scheduler.

**Sources**: `raw/kueue/keps/2937-resource-transformer/README.md`, `raw/kueue/keps/2937-resource-transformer/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Stable** — Promoted to GA on 2025-09-08. (source: keps/2937-resource-transformer/kep.yaml)

## Problem

Kueue normally maps a job's resource requests 1:1 into the [[workload]]'s resource requirements. This creates two pain points:

1. A [[cluster-queue]] must list every resource name the job requests in its `coveredResources` — including all MIG variants like `nvidia.com/mig-1g.5gb`, `nvidia.com/mig-2g.10gb`, `nvidia.com/mig-4g.20gb`.
2. There is no way to express quota in abstract units (e.g., "accelerator memory GB" or "team credits") without modifying pod specs.

(source: keps/2937-resource-transformer/README.md)

## Solution

A `ResourceTransformation` list in Kueue's global `Configuration` defines per-resource rules that Kueue applies when computing the workload's effective resource request. The pod spec is never changed — only the quota-accounting view inside the [[workload]] is affected.

## Transformation rules

Each rule specifies:

| Field | Description |
|---|---|
| `input` | The resource name to match (e.g. `nvidia.com/mig-1g.5gb`) |
| `strategy` | `Replace` — remove the input resource; `Retain` — keep it and add outputs |
| `outputs` | Map of output resource name → quantity per unit of input |
| `multiplyBy` | (optional) Another resource name whose quantity multiplies the output |

(source: keps/2937-resource-transformer/README.md)

## Use case 1: MIG GPU slicing (Replace)

NVIDIA MIG mixed-strategy creates many resource names (`nvidia.com/mig-1g.5gb`, `nvidia.com/mig-2g.10gb`, …). Using `Replace`, all variants collapse into a single `example.com/accelerator-memory` quota resource:

```yaml
resources:
  transformations:
  - input: nvidia.com/mig-1g.5gb
    strategy: Replace
    outputs:
      example.com/accelerator-memory: 5Gi
  - input: nvidia.com/mig-2g.10gb
    strategy: Replace
    outputs:
      example.com/accelerator-memory: 10Gi
  - input: nvidia.com/mig-4g.20gb
    strategy: Replace
    outputs:
      example.com/accelerator-memory: 20Gi
```

A job requesting `nvidia.com/mig-1g.5gb: 2` and `nvidia.com/mig-2g.10gb: 1` is charged `20Gi` of `example.com/accelerator-memory`. The ClusterQueue only needs `coveredResources: ["cpu", "memory", "example.com/accelerator-memory"]`. (source: keps/2937-resource-transformer/README.md)

## Use case 2: Budget / credits (Retain)

`Retain` keeps the original resource and adds an extra output. This can express monetary cost as a synthetic quota dimension:

```yaml
resources:
  transformations:
  - input: foo.com/gpu
    strategy: Retain
    outputs:
      example.com/credits: 10
  - input: cpu
    strategy: Retain
    outputs:
      example.com/credits: 1
```

Set `borrowingLimit: 0` and `lendingLimit: 0` on the `credits` resource to enforce it as a hard team budget. (source: keps/2937-resource-transformer/README.md)

## Use case 3: Multiply two resources (multiplyBy)

Compute total GPU memory as the product of GPU count × per-GPU memory:

```yaml
resources:
  transformations:
  - input: nvidia.com/gpumem
    strategy: Retain
    multiplyBy: nvidia.com/gpu
    outputs:
      nvidia.com/total-gpumem: 1
```

(source: keps/2937-resource-transformer/README.md)

## Observability

The transformed resources appear in `workload.status.admission.podSetAssignments[*].resourceUsage` once admitted. For a pending workload, the `QuotaReserved` condition message shows the transformed resource name in the "insufficient quota" message, e.g.:

```
couldn't assign flavors to pod set main: insufficient unused quota for
example.com/accelerator-memory in flavor default-flavor, 20G more needed
```

(source: keps/2937-resource-transformer/README.md)

## Scope and limitations

- Transformations are **global** — applied to all workloads at startup. There is no per-ClusterQueue or per-Workload scoping in the current implementation.
- Changing the transformation list requires a Kueue manager restart.
- `excludeResourcePrefixes` is applied **before** transformations; a resource that matches an exclusion prefix will never reach a matching transformation rule.
- Workload resource requests are not retroactively updated if transformations change after admission.

(source: keps/2937-resource-transformer/README.md)

## Comparison with DRA

Both mechanisms allow Kueue's quota view to differ from pod requests, but:
- Resource transformer: pod uses ordinary extended resources; Kueue rewrites them mathematically.
- [[dra]]: pod uses `ResourceClaimTemplates`; Kueue maps `DeviceClasses` to logical names via `deviceClassMappings`.

They can coexist — a cluster might use resource transformers for legacy MIG resources while adopting DRA for new workloads.

## Related pages

- [[cluster-queue]]
- [[workload]]
- [[resource-flavor]]
- [[admission]]
- [[dra]]
- [[feature-gates]]
