# Dynamic Resource Allocation (DRA)

**Summary**: Kueue's alpha integration with Kubernetes Dynamic Resource Allocation (DRA) enables quota management, borrowing, and preemption for workloads that request devices via ResourceClaimTemplates or extended resources backed by DRA DeviceClasses.

**Sources**: `raw/kueue/keps/2941-DRA/README.md`, `raw/kueue/keps/2941-DRA/kep.yaml`, `raw/kueue/pkg/dra/claims.go`, `raw/kueue/pkg/dra/extended_resources.go`, `raw/github/kubernetes-sigs__kueue/pr-14951.md`, `issue-14964.md`

**Last updated**: 2026-09-01

---

> **Stage: Alpha** — Feature gates `KueueDRAIntegration` (was `DynamicResourceAllocation`) and `KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`), both disabled by default. Not production-ready; API may change before beta. The gates were **renamed in v0.18** to avoid colliding with the upstream Kubernetes `DynamicResourceAllocation` gate; the old names are deprecated + `LockToDefault` and a migration helper maps old→new. See [[feature-gates]].

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

Two Kueue feature gates control DRA support (shown with their post-v0.18 names):

| Gate | Purpose |
|---|---|
| `KueueDRAIntegration` (was `DynamicResourceAllocation`) | Enables ResourceClaimTemplate-based quota accounting; uses `deviceClassMappings` |
| `KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`) | Enables extended-resource path; requires `KueueDRAIntegration` also enabled |

Both are alpha. (source: keps/2941-DRA/kep.yaml)

## Startup safety: DeviceClass index is conditional

The manager registers a field index over `DeviceClass` objects for DRA accounting. If the cluster does not expose the DRA **v1** APIs, that index registration would fail and crash `kueue-controller-manager` at startup. [[pr-11405]] makes the registration conditional — the DeviceClass index is **skipped** (disabled) when the DRA v1 API is unavailable, so the manager starts cleanly on clusters without DRA (release note: "DRA: Disable the DeviceClass indexing when DRA v1 APIs are not available"). The cherry-pick to release-0.17 was deliberately skipped due to conflicts (DRA is alpha on 0.17). **Invariant**: DRA-dependent indexers/controllers must be wired conditionally on API discovery.

## Scheduling-equivalence hash and DRA

DRA preprocessing rewrites a device-class resource (e.g. `example.com/gpu`) into its `deviceClassMappings`-mapped logical resource (e.g. `gpu`) in the Workload's `TotalRequests` **without** mutating the pod spec. Because the `SchedulingEquivalenceHashing` optimization originally hashed only the PodSet *spec* shape, two DRA Workloads with different effective device requests could hash identically and wrongly share an equivalence-cache result. [[pr-11399]] folds each PodSet's effective `TotalRequests.Requests` into `computeSchedulingHash`. See [[scheduler-internals]] / [[feature-gates]].

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

### Qualified-name validation: more than one slash is now rejected

`validateQualifiedName` (`pkg/config/validation.go`) — a port of upstream Kubernetes' DRA resource validation, and today reached only from `DeviceClassMapping.Sources[].Capacity.Name` — switched on the number of `/`-separated parts and handled **only** `len(parts) == 1` and `len(parts) == 2`. A name with two or more slashes (`a/b/c`) matched neither case, so `allErrs` stayed empty and the value was **silently accepted**, producing a mapping that could never match any device. [[pr-14951]] (fixes [[issue-14846]], cherry-picked to release-0.19 as [[pr-14953]]) adds a `default:` case emitting `field.Invalid`. **Correction to an earlier reading in this wiki**: [[issue-14846]] was previously logged as closed-not-a-bug on the assumption the `IsLabelKey` refactor already covered it; the merged fix and its release note ("Fixed config validation silently accepting capacity names with more than one slash, which produced a mapping that never matched any device") show the gap was real.

Note the ratcheting argument that made failing fast acceptable here: this field lives in Kueue's own `Configuration` file, re-validated from scratch on every controller-manager start, not in a persisted CRD — so there are no existing non-compliant stored objects to grandfather in. Contrast [[feature-gates]]' `ReservedResourceNameValidation`, where the same *kind* of tightening did need an escape hatch because config-validation failure calls `os.Exit`. The equivalent gap in `k8s.io/apimachinery`'s declarative-validation helper (`resourcesQualifiedName` in `strfmt.go`) was deliberately left to be fixed upstream.

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

## The reserved `pods` resource name

`pods` is reserved for Kueue's own Pod-count accounting. The Workload webhook already refused it (`validateResourceList` in `pkg/webhooks/workload_webhook.go` returns `"the key is reserved for internal kueue use"`), but the **operator Configuration** did not: `validateDeviceClassMappings` only checked the mapping name for label-key syntax, length and uniqueness, so a DeviceClass could be mapped to a logical resource named `pods` — and a [[resource-transformer]] could name it too.

**Why it is silently wrong.** `totalRequestsFromPodSets` merges the preprocessed DRA resources into the PodSet's requests without filtering reserved names, and `dropExcludedResources` only removes administrator-configured prefixes. Then flavor assignment overwrites the key:

```go
// pkg/scheduler/flavorassigner/flavorassigner.go, assignFlavors
if a.cq.RGByResource(corev1.ResourcePods) != nil {
    if podSet.Requests != nil {
        podSet.Requests.Set(corev1.ResourcePods, int64(podSet.Count))
    }
    // ...
}
```

`Set` **replaces** rather than adds, in `MapRequests` and `SliceRequests` alike. So on a ClusterQueue that tracks `pods` quota, one Pod claiming eight devices of a mapped class is charged **one**. This is not specific to prioritized lists — the `ExactCount` path charges through the same merge.

[[pr-13989]] (fixes [[issue-13988]]; cherry-picks [[pr-14756]], [[pr-14758]]) refuses the name in the four Configuration positions that reach this accounting path:

| Position | Why |
|---|---|
| `deviceClassMappings[].name` | writes under the reserved key — the collision above |
| `resources.transformations[].outputs` key | same |
| `resources.transformations[].input` | operand — a transformation runs *before* the Pod-count request is synthesized, so it cannot denote it |
| `resources.transformations[].multiplyBy` | same |

Nothing else in the Configuration is touched: `admissionFairSharing.resourceWeights` and friends still accept `pods`, where it correctly means the Pod count.

**Where the refusal lives.** Only the *mapping-name* check moved behind `KueueDRAIntegration`: the mapper is built inside that gate check in `main.go`, so with the gate off nothing reads the name and a mapping carrying it is dormant — and Configuration validation failure is `os.Exit`, so refusing it unconditionally would have crashed an upgrade over something inert. Count limits, name syntax and length, duplicate names, device-class syntax and per-class conflicts stay **unconditional** (a mapping that is malformed while dormant is malformed the day it is switched on), following the shape #12134 already used for `sources`. The three transformation positions are also unconditional, because `main.go` installs transformations with no gate above them.

**Upgrade escape hatch.** Because no released version refused the name (verified absent from `pkg/config/validation.go` in v0.18.6 and v0.19.2), the refusal is gated behind **`ReservedResourceNameValidation`** — Alpha/off on release-0.18 and release-0.19 ([[pr-14773]], [[pr-14774]], fixes [[issue-14763]]), Beta/on from v0.20 ([[pr-14778]]). Registering the name on `main` too is mandatory: `Set`/`SetFromMap` return `unrecognized feature gate` for an unregistered name and `main.go` exits, so an operator who used the branch mitigation would crash-loop one release later. Renaming a mapping name or an `outputs` key also requires updating the matching ClusterQueue resource name.

Out of scope of this fix: `template.spec.overhead`, which `PodRequests` also adds to the charge and which the Workload webhook does not reach (#13991).

## Stale DRA resource names after DeviceClass deletion

A Workload kept its DRA-mapped resource names after the referenced DeviceClass was deleted, so requeue re-evaluated it against resources that no longer existed. Fixed in [[pr-14085]] (original #11927).

Still open: a DeviceClass **change** never reaches a Workload that has already reserved quota ([[issue-14563]]).

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
- [[workload-resource-adjustment]] — DRA detection and DRA processing can run against different (raw vs adjusted) request views.
