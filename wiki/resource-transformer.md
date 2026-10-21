# Resource Transformer

**Summary**: Resource transformers let cluster admins define global rules that rewrite a workload's resource requests into different quota units before Kueue applies admission and quota calculations — without touching the actual Pod resource requests seen by kube-scheduler.

**Sources**: `raw/kueue/keps/2937-resource-transformer/README.md`, `raw/kueue/keps/2937-resource-transformer/kep.yaml`, pr-15926.md, pr-15974.md, pr-15954.md, pr-16041.md, issue-14204.md, issue-15979.md, issue-14007.md, pr-12961.md, pr-12962.md, raw/kueue/pkg/workload/workload.go

**Last updated**: 2026-10-21

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
- Since v0.20-era fixes (pr-15954, pr-16041), transformations run **before** `excludeResourcePrefixes`; see the next section. (Earlier text of KEP-2937 says exclusions run first; that is no longer the implementation.)
- Workload resource requests are not retroactively updated if transformations change after admission.

(source: keps/2937-resource-transformer/README.md)

## Comparison with DRA

Both mechanisms allow Kueue's quota view to differ from pod requests, but:
- Resource transformer: pod uses ordinary extended resources; Kueue rewrites them mathematically.
- [[dra]]: pod uses `ResourceClaimTemplates`; Kueue maps `DeviceClasses` to logical names via `deviceClassMappings`.

They can coexist — a cluster might use resource transformers for legacy MIG resources while adopting DRA for new workloads.

## Order of operations: transformations first, exclusions on what is retained

`totalRequestsFromPodSets` (`pkg/workload/workload.go`) builds a PodSet's effective requests in this order (source: raw/kueue/pkg/workload/workload.go, pr-15954.md, pr-16041.md, issue-14204.md):

1. `resources.PodRequests(podSpec)` gives the raw (LimitRange/RuntimeClass-adjusted) requests.
2. `applyResourceTransformations(specRequests, specRequests, transforms)` returns two lists: **retained** (inputs not transformed, plus inputs of `Retain` strategy) and **generated** (outputs). `multiplyBy` looks up the multiplier in the *full* raw request list, so an excluded resource still works as a multiplier.
3. `dropExcludedResources(retained, excludeResourcePrefixes)` filters **only the retained** list. Generated outputs are never dropped by an exclusion.
4. DRA logical resources are merged into `generated` (see [[dra]]); `effectiveRequests = retained + generated` (summed per name), floored at zero, then multiplied by the PodSet count.

Why this order (both bugs let a tenant bypass ClusterQueue quota):

- **Excluded multiplier** (pr-15954; the bug report is issue-14007.md, closed once pr-15954 and pr-16041 landed): with `excludeResourcePrefixes: [acme.io/vgpu-count]` and `input: acme.io/cores-per-vgpu, multiplyBy: acme.io/vgpu-count`, exclusions used to run first, so `multiplyBy` could not find `vgpu-count` and 2 vGPUs x 20 cores were accounted as 20 cores instead of 40. Excluded resources stay out of direct CQ accounting but remain available to transformations.
- **Excluded input** (pr-16041, backports pr-16053/0.19, pr-16054/0.18): with `excludeResourcePrefixes: [acme.io/]` and `input: acme.io/vgpu-count`, the input was removed before it could generate `quota.acme.io/total-vgpu-cores`, so usage recorded 0. Now the input is transformed first and only then excluded.
- **No validation error for the overlap.** pr-15926 tried to reject configurations where a transformation `input` matches an exclude prefix (KEP-2937 graduation criterion; issue-14204.md). It was **reverted before release (pr-15974)** because such configurations can be sensible (an input that is `Replace`d, so the exclusion just keeps the raw resource out of quota) and because the docs themselves show `excludeResourcePrefixes: ["example.com"]` next to a transformation on `example.com/gpu-type1`; rejecting it would turn a running cluster into one that fails to start (config errors call `os.Exit(1)`). Validation rules for transformations are to be defined separately (issue-15979.md, open). If a KEP text still says "raise a config error", treat it as not implemented.
- **Negative output factors** are how an "allowance" is written: outputs from different inputs are summed so they can cancel each other, but the per-resource generated total is clamped to zero and can never reduce an ordinary request under the same name or the DRA charge merged afterwards.

## Milli-valued inputs are not rounded before multiplication

A milli-valued input quantity used to be rounded **before** the output factor was applied, so `300m` CPU times `1000` gave `3000` instead of `300`. The multiplication now keeps the milli precision (main #12953; backports pr-12961.md to release-0.18 and pr-12962.md to release-0.17, shipped v0.18.3 and v0.17.7 per CHANGELOG-0.17/0.18.md). Watch for this when an output factor scales a fractional CPU or memory request.

## `multiplyBy: pods` cannot resolve

issue-14007.md raised a second trigger for the silent multiplier-of-one fallback: `multiplyBy: pods`. `pods` is not a container resource, so it is not in the list transformations run over; flavor assignment writes it from the PodSet count much later. A PodSet of four asking `1024` was charged `1024` per Pod instead of `4096`. Naming `pods` in `multiplyBy` is now refused outright (next section). Any other `multiplyBy` name the workload does not request still multiplies by one silently. That case is visible in configuration rather than hidden by an exclusion (source: issue-14007.md).

## `pods` is refused in every transformation position

A transformation may not name `pods` in `input`, `multiplyBy`, or as an `outputs` key. An `outputs: {pods: ...}` entry collides with Kueue's own Pod-count accounting and is silently overwritten by flavor assignment; `input` and `multiplyBy` are operands and cannot denote it at all, because transformations run *before* the Pod-count request is synthesized. Refused behind the `ReservedResourceNameValidation` gate (Beta/on from v0.20, Alpha/off on the 0.18 and 0.19 branches). Renaming an `outputs` key also requires updating the matching [[cluster-queue]] resource name. Full analysis in [[dra#The reserved `pods` resource name]] ([[pr-13989]], [[pr-14756]], [[pr-14758]], [[pr-14778]]).

## Related pages

- [[cluster-queue]]
- [[workload]]
- [[resource-flavor]]
- [[admission]]
- [[dra]]
- [[feature-gates]]
