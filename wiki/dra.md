# Dynamic Resource Allocation (DRA)

**Summary**: Kueue's alpha integration with Kubernetes Dynamic Resource Allocation (DRA) enables quota management, borrowing, and preemption for workloads that request devices via ResourceClaimTemplates or extended resources backed by DRA DeviceClasses.

**Sources**: `raw/kueue/keps/2941-DRA/README.md`, `raw/kueue/keps/2941-DRA/kep.yaml`, `raw/kueue/pkg/dra/claims.go`, `raw/kueue/pkg/dra/extended_resources.go`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gates `DynamicResourceAllocation` and `DRAExtendedResources`, both disabled by default. Not production-ready; API may change before beta.

## What is DRA?

Dynamic Resource Allocation (DRA) is Kubernetes' evolution of the extended-resource model for managing devices such as GPUs, FPGAs, and network cards. Instead of opaque integer counts (`nvidia.com/gpu: 1`), DRA uses structured `ResourceClaim` and `ResourceClaimTemplate` objects that let drivers express richer allocation semantics — partitioning, time-slicing, sharing across pods — that the old extended-resource model could not represent.

(source: keps/2941-DRA/README.md)

## Two integration paths

Kueue's DRA support (KEP-2941, alpha) handles two distinct request styles:

### Path 1 — ResourceClaimTemplates

The pod spec directly references a `ResourceClaimTemplate`, which the kube-scheduler uses to create a `ResourceClaim` per pod. Kueue reads the template, counts devices per `DeviceClass`, maps them to logical resource names via `deviceClassMappings` in the Kueue Configuration, and enforces quota against those logical names. (source: keps/2941-DRA/README.md)

```yaml
# Pod references a ResourceClaimTemplate
resourceClaims:
- name: gpu
  resourceClaimTemplateName: single-gpu
```

### Path 2 — Extended resources backed by DRA

Pods use the familiar `resources.requests: {example.com/gpu: 1}` syntax. When a `DeviceClass` sets `spec.extendedResourceName`, the kube-scheduler automatically creates `ResourceClaims`. Kueue accounts for quota using the extended resource name directly — no `deviceClassMappings` entry is needed, but the Kubernetes `DRAExtendedResource` feature gate (alpha in k8s 1.35) must be enabled. (source: keps/2941-DRA/README.md)

## Feature gates

Two Kueue feature gates control DRA support:

| Gate | Purpose |
|---|---|
| `DynamicResourceAllocation` | Enables ResourceClaimTemplate-based quota accounting; uses `deviceClassMappings` |
| `DRAExtendedResources` | Enables extended-resource path; requires `DynamicResourceAllocation` also enabled |

Both are alpha. (source: keps/2941-DRA/kep.yaml)

## Configuration: deviceClassMappings

Cluster admins map DeviceClass names to logical quota resource names in the Kueue `Configuration` ConfigMap:

```yaml
resources:
  deviceClassMappings:
  - name: whole-gpus
    deviceClassNames:
    - gpu.example.com
  - name: shared-gpus
    deviceClassNames:
    - ts-shard-gpus.example.com
    - sp-shared-gpus.example.com
```

The logical names (`whole-gpus`, `shared-gpus`) are then used as `coveredResources` in a [[cluster-queue]]. Each DeviceClass may appear in at most one mapping entry — duplicate entries are rejected at configuration load time. (source: keps/2941-DRA/README.md)

## Workload processing flow

1. Job is submitted with a `ResourceClaimTemplate` reference.
2. Kueue's webhook creates a [[workload]] from the job.
3. The `pkg/dra` package reads the `ResourceClaimSpec`, counts devices per DeviceClass, and maps them to logical resource names.
4. The logical resource quantities appear in `workload.spec.podSets[*].template.spec` as if they were ordinary requests.
5. [[admission]] proceeds against ClusterQueue quota as normal.
6. After admission, the unsuspend toggle lets kube-scheduler create the actual `ResourceClaim` objects.

(source: pkg/dra/claims.go)

## Alpha limitations

- **ResourceClaims not supported** — only `ResourceClaimTemplates`. Pods with direct `ResourceClaim` references result in an inadmissible workload. (source: keps/2941-DRA/README.md)
- **No Topology-Aware Scheduling** — TAS + DRA is a future body of work. (source: keps/2941-DRA/README.md)
- **No CEL selectors** — `devices.requests[*].exactly.selectors` and `FirstAvailable` are unsupported and produce a validation error. (source: pkg/dra/claims.go)
- **No AdminAccess or device constraints** — `adminAccess: true` and `devices.constraints` are rejected. (source: pkg/dra/claims.go)
- **AllocationMode=All not supported** — worst-case counting for `All` mode is deferred. (source: pkg/dra/claims.go)
- **GPU time-slicing / MPS not supported** in alpha extended-resources path.

## TOCTOU risk for extended resources

Between Kueue admitting a workload and kube-scheduler scheduling it, a DeviceClass may be created or updated, causing the two components to pick different DeviceClasses for the same `extendedResourceName`. Mitigation: enable `waitForPodsReady` so that a scheduling failure surfaces as a timeout and triggers re-queue. (source: keps/2941-DRA/README.md)

## Interaction with admission fair sharing

DRA resources participate in [[admission-fair-sharing]] calculations the same way extended resources do — usage is counted at quota-accounting time when the workload is admitted. (source: keps/2941-DRA/README.md)

## Comparison with resource-transformer

For how DRA differs from [[resource-transformer]] (and when to use each), see the canonical comparison in [[resource-transformer#comparison-with-dra]].

## Related pages

- [[resource-flavor]]
- [[cluster-queue]]
- [[workload]]
- [[admission]]
- [[resource-transformer]]
- [[provisioning-request]]
- [[feature-gates]]
- [[admission-fair-sharing]]
- [[topology-aware-scheduling]]
