# Dynamic Resource Allocation (DRA)

**Summary**: Kueue's beta integration (`KueueDRAIntegration`, on by default since v0.18) with Kubernetes Dynamic Resource Allocation (DRA) enables quota management, borrowing, and preemption for workloads that request devices via ResourceClaimTemplates or extended resources backed by DRA DeviceClasses.

**Sources**: `raw/kueue/keps/2941-DRA/README.md`, `raw/kueue/keps/2941-DRA/kep.yaml`, `raw/kueue/pkg/dra/claims.go`, `raw/kueue/pkg/dra/extended_resources.go`, `raw/github/kubernetes-sigs__kueue/pr-14951.md`, `issue-14964.md`, pr-14200, pr-14367, pr-15577, pr-15888, pr-15961, pr-15983, pr-16081, pr-16098, pr-16169, pr-16317, issue-14393, issue-15769, pr-13642, pr-16469, issue-13599, issue-14035, pr-16625, pr-16652, pr-17141, pr-17434, pr-14562, pr-17208, pr-17211, issue-14535, pr-17093, pr-17294, pr-17445, pr-17447, pr-17314, pr-17368, pr-17424, pr-17443, pr-17444, issue-17422, issue-14372; `raw/kueue/pkg/cache/queue/manager.go`, `raw/kueue/pkg/controller/core/workload_controller.go`, `raw/kueue/pkg/features/kube_features.go`, `raw/kueue/pkg/cache/scheduler/dra/`, `raw/kueue/pkg/cache/scheduler/tas_dra.go`

**Last updated**: 2026-10-28

---

> **Stage (updated 2026-09-29): the banner below is historical.** In main (v0.20 development) `KueueDRAIntegration` is **Beta, on by default** (since v0.18) and `KueueDRAIntegrationExtendedResource` is Beta/on since v0.19 (Alpha/off in v0.18); see *Feature-gate stages* below (source: kube_features.go). Original text: **Stage: Alpha** — Feature gates `KueueDRAIntegration` (was `DynamicResourceAllocation`) and `KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`), both disabled by default. Not production-ready; API may change before beta. The gates were **renamed in v0.18** to avoid colliding with the upstream Kubernetes `DynamicResourceAllocation` gate; the old names are deprecated + `LockToDefault` and a migration helper maps old→new. See [[feature-gates]].

## What is DRA?

Dynamic Resource Allocation (DRA) is Kubernetes' evolution of the extended-resource model for managing devices such as GPUs, FPGAs, and network cards. Instead of opaque integer counts (`nvidia.com/gpu: 1`), DRA uses structured `ResourceClaim` and `ResourceClaimTemplate` objects that let drivers express richer allocation semantics — partitioning, time-slicing, sharing across pods — that the old extended-resource model could not represent.

(source: keps/2941-DRA/README.md)

## Two integration paths

Kueue's DRA support (KEP-2941, beta since v0.18) handles two distinct request styles:

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

**Implicit name `deviceclass.resource.kubernetes.io/<class>`** (source: pr-17141.md; backport pr-17434/0.20; not in the v0.20.2 CHANGELOG at kueue@3bbb8cce4; no 0.19 backport). Every DeviceClass can also be requested by this implicit extended resource name, whether or not it sets `spec.extendedResourceName`, and KEP-2941 says Kueue supports both. But the workload controller's DeviceClass handler registered only `spec.extendedResourceName` in the DRA-backed resource cache (`dra.ExtendedResourceCache`). A Pod requesting the implicit name was therefore treated as an ordinary extended resource: it never reached `ResolveDeviceClass` (which already handled the name), was not charged to the `deviceClassMappings` logical resource, and could stay pending. Now the handler adds and removes `resourcev1.ResourceDeviceClassPrefix + dc.Name` on DeviceClass create and delete, and requeues pending Workloads that request either name. Update leaves the implicit name alone, because a DeviceClass name cannot change. Because every DeviceClass now writes to the cache, `ExtendedResourceCache.Add`/`Remove` are no-ops on a nil cache, which means DRA extended resources are not configured, the same as `NeedsDRAReconcile` already assumed (source: workload_controller.go, extended_resource_cache.go).

## Feature gates

Two Kueue feature gates control DRA support (shown with their post-v0.18 names):

| Gate | Purpose |
|---|---|
| `KueueDRAIntegration` (was `DynamicResourceAllocation`) | Enables ResourceClaimTemplate-based quota accounting; uses `deviceClassMappings` |
| `KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`) | Enables extended-resource path; requires `KueueDRAIntegration` also enabled |

Both are Beta/on on main (`KueueDRAIntegration` since v0.18, `KueueDRAIntegrationExtendedResource` since v0.19). (source: keps/2941-DRA/kep.yaml, raw/kueue/pkg/features/kube_features.go)

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
2. Kueue's job reconciler creates a [[workload]] from the job.
3. The `pkg/dra` package reads the `ResourceClaimSpec`, counts devices per DeviceClass, and maps them to logical resource names.
4. The workload controller passes the logical resource quantities to the queue as preprocessed DRA resources; they are merged into the Workload's in-memory `TotalRequests` (the spec is not changed) (source: raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/workload/workload.go).
5. [[admission]] proceeds against ClusterQueue quota as normal.
6. After admission, the unsuspend toggle lets kube-scheduler create the actual `ResourceClaim` objects.

(source: pkg/dra/claims.go)

## Alpha limitations

- **ResourceClaims not supported** — only `ResourceClaimTemplates`. Pods with direct `ResourceClaim` references result in an inadmissible workload. (source: keps/2941-DRA/README.md)
- **No Topology-Aware Scheduling** — TAS + DRA is a future body of work. (source: keps/2941-DRA/README.md)
- ~~**No CEL selectors**~~ / ~~**No AdminAccess or device constraints**~~ — **Correction (2026-10-21)**: these two bullets are outdated. In the snapshot code (`pkg/dra/claims.go` at kueue@8922c563e), CEL selectors are compiled (`validateCELSelectors`) and checked against devices (`validateCELSelectorsAgainstDevices`). The CHANGELOG dates CEL support to v0.18.0 (#9742) and acceptance of `devices.constraints` / device config to v0.19 (#12451). `adminAccess: true` has been accepted with zero charge since v0.20.0 (pr-13642.md), and `firstAvailable` is supported behind `KueueDRAIntegrationPrioritizedList` (see *Prioritized lists* below). The earlier text cited the same file at an older revision (source: claims.go, CHANGELOG-0.18.md, CHANGELOG-0.19.md, pr-13642.md).
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

Out of scope of this fix: `template.spec.overhead`, which `PodRequests` also adds to the charge. The Workload webhook did not reach it (#13991) until pr-17090, which now rejects negative overhead under `WorkloadValidateResourcesAreNonNegative` (v0.20.2 #17201, v0.19.9 #17202); see [[workload#Negative Pod overhead is rejected (pr-17090, fixes issue-13991)]] (source: pr-17090.md).

## Stale DRA resource names after DeviceClass deletion

A Workload kept its DRA-mapped resource names after the referenced DeviceClass was deleted, so requeue re-evaluated it against resources that no longer existed. Fixed in [[pr-14085]] (original #11927).

Still open: a DeviceClass **change** never reaches a Workload that has already reserved quota ([[issue-14563]]).

## Feature-gate stages (main / v0.20 development)

From `pkg/features/kube_features.go` (source: kube_features.go). Contradiction with the older text on this page (Alpha/off): the code marks the first three as Beta and default-on.

| Gate | Stage / default | Depends on |
|---|---|---|
| `KueueDRAIntegration` | Beta, on (v0.18) | none |
| `KueueDRAIntegrationExtendedResource` | Beta, on (v0.19) | `KueueDRAIntegration` |
| `KueueDRAIntegrationPartitionableDevices` | Beta, on (v0.19) | `KueueDRAIntegration` (counter-based quota, e.g. MIG, via `consumesCounters`) |
| `KueueDRAIntegrationConsumableCapacity` | Alpha, off (v0.19) | `KueueDRAIntegration` (KEP-5075 consumable capacity) |
| `KueueDRARejectWorkloadsWhenDRADisabled` | Beta, on (v0.18) | reject DRA workloads when `KueueDRAIntegration` is off |
| `KueueDRADeviceFeasibility` | Alpha, off (v0.20) | `KueueDRAIntegration`, `TopologyAwareScheduling`, `TASNodeFeasibilityForAllLevels` |
| `KueueDRAIntegrationDeviceTaints` | Alpha, off (v0.20) | `KueueDRADeviceFeasibility` |
| `ReservedResourceNameValidation` | Beta, on (v0.20) | see the reserved `pods` section |
| `KueueDRAIntegrationPrioritizedList` | Alpha, off (v0.20) | `firstAvailable` requests (see *Prioritized lists*); also needs Kubernetes `DRAPrioritizedList` (on by default since 1.34) |

The "No Topology-Aware Scheduling" alpha limitation above is superseded for feasibility: `KueueDRADeviceFeasibility` runs inside the TAS placement path.

## Per-node device feasibility (`KueueDRADeviceFeasibility`)

**Problem.** Quota bounds how many devices a ClusterQueue admits, not where they are. A Workload whose ResourceClaims no single node can satisfy was admitted on quota alone; Kueue ungated the Pods, kube-scheduler found no node, and the Workload sat Pending holding quota ([[pr-15577]], part of [[issue-10548]]).

**Behaviour.** Kueue evaluates device availability per node before admission and treats a node that cannot satisfy the claims as unavailable, so a Workload no node can serve stays queued with quota free. It covers `ResourceClaimTemplate`s and DRA-backed extended resources. Implementation shape (source: `pkg/cache/scheduler/dra/`, `tas_dra.go`):

- `dra.Checker` wraps a `simulator.SchedulerSimulator`: it lets the inner simulator pick feasible nodes, then drops candidates whose devices cannot satisfy the Pod's claims. It allocates with the same structured-allocation engine kube-scheduler uses (`k8s.io/dynamic-resource-allocation/structured`), so both reach the same answer. The allocator is built lazily **once per snapshot** from ResourceClaims/ResourceSlices/DeviceClasses as they stand, so device state cannot shift mid-cycle. Compiled CEL selectors live in a shared `CELCache` that outlives snapshots.
- **Extended-resource delegation** (`DRADelegation`): extended resources a DeviceClass can supply are zeroed out of the domain capacity request and left to the per-node device check (`Undelegated` keeps the original request). A leaf whose Node itself publishes every delegated resource (device plugin) counts them normally (`advertisesAll` / `forLeaf`); domains above the leaf cannot ask a node and keep the delegated request. The leader and workers each have their own delegation.
- **Preemption limitation**: `Checker.PreemptWorkload` frees the victim's Pods but **not the devices its claims hold**, so preemption cannot make a Workload device-feasible; the check errs restrictive rather than over-admit. Releasing devices is Beta work in the KEP.
- Because TAS also uses the simulator to ask "what fits if everything is preempted", the fix in [[pr-15436]] (see [[topology-aware-scheduling]]) was motivated by exactly this case, a device held by a preemption candidate.
- Leader PodSet DRA feasibility is checked when picking a domain (`TASLeaderPodSetFeasibility`, [[pr-15447]]). `TASNodeFeasibilityForAllLevels` makes per-node checks apply to Topologies whose lowest level is not `kubernetes.io/hostname`; without it "a rack of CPU-only nodes passes for a Workload requesting devices".
- TAS reports node exclusions with reasons (per-node exclusion stats) so a rejected Workload's message shows why nodes were dropped.

**Device taints** ([[pr-16081]], gate added in [[pr-16169]], fixes [[issue-15621]], [[issue-16112]]): the check ignored `DeviceTaintRule` taints, so Kueue could admit onto a device kube-scheduler rejects. `applyDeviceTaintRules` overlays matching rule taints onto the ResourceSlices (equivalent to kube-scheduler's `resourceslice/tracker`, but without a second typed-informer cache of every slice). It only applies when the `DeviceTaintRules` API is served (decided once at startup, to avoid a discovery request per list), `KueueDRAIntegrationDeviceTaints` is on **and** Kubernetes' own `DRADeviceTaintRules` gate is on. Claims that tolerate the taint may still use the device. The separate gate mirrors Kubernetes' `DRADeviceTaints` so taints graduate independently of feasibility; it covers taints in ResourceSlices as well as rules, including the rule watch.

**Requeue** ([[pr-16098]], fixes [[issue-15769]]): Workloads rejected by the check are requeued when a ResourceSlice, DeviceClass, ResourceClaim (deallocated or deleted) or DeviceTaintRule change may free devices. The ResourceSlice watch is not limited to drivers named in `deviceClassMappings`, since the check reads every slice. Alongside, the TAS ResourceFlavor reconciler now requeues only ClusterQueues using the flavor ([[pr-16152]]). Perf: a TAS+DRA scheduler-performance config measures the check's per-cycle cost ([[pr-16317]], part of [[issue-14994]]). Its pass/fail thresholds were then set from 10 CI runs (source: pr-16652.md, fixes issue-16352, closes issue-14994).

**PodSets of one Workload now see each other's devices** (source: pr-16625.md; backport pr-16809, shipped v0.20.1; 0.20-only). Usage recorded between PodSets used `SinglePodRequests`, where delegated extended resources are zeroed, so two PodSets could share a node's single device-plugin device, and an elastic scale-up could stay pending. Recording now goes through `TASFlavorSnapshot.RequestsForDomain`, the same rule `forLeaf` uses. Remaining gaps: rack-level usage is not charged per node, and a node counts delegated resources only if it publishes all of them. Details: [[topology-aware-scheduling#DRA-backed extended resources counted between PodSets]].

## AdminAccess requests are not charged

A device request with `exactly.adminAccess: true` gives shared, read-only access to devices that are already allocated, for example to a monitoring agent. Charging quota for it would count the device twice, once for the real owner and once for the monitor. kube-scheduler likewise leaves AdminAccess out of `allocatedDevices`. Since v0.20.0, such requests are accepted and **skipped** in every DRA quota path: `isAdminAccessRequest` in `claims.go`, the capacity path (`capacity.go`) and the counter path (`counters.go`). Other requests in the same claim are counted normally. This is a behaviour change, so it was not cherry-picked (source: pr-13642.md, claims.go).

## Prioritized lists (`firstAvailable`, `KueueDRAIntegrationPrioritizedList`, Alpha)

With the gate off, a request with `firstAvailable` is still refused with `FirstAvailable device selection is not supported`, and the Workload is inadmissible. With the gate on, `chargeForFirstAvailable` charges the request **only when the charge equals whatever alternative kube-scheduler will pick** (source: claims.go; CHANGELOG-0.20.md):

- every alternative must map, through `deviceClassMappings`, to the **same logical resource** (otherwise `every alternative must map to "<r>", this one maps to "<r2>"`);
- every alternative must ask for the **same count** (`every alternative must have count N, this one has M`);
- each alternative must be `ExactCount` with `count > 0` and a mapped `deviceClassName` (`NotFound` otherwise), and its CEL selectors must compile;
- an alternative on a **counter-backed or capacity-backed** mapping is refused (`a counter-backed or capacity-backed DeviceClass is not supported for firstAvailable`), because those paths read only `Exactly` requests and would charge nothing;
- an empty `firstAvailable` list is refused (`must list at least one alternative`).

The request is then charged that count once, on the logical resource. The design issue (issue-13599.md) first proposed a looser **component-wise maximum envelope** over alternatives that map to different resources (e.g. a GPU alternative and a CPU alternative charge both). The shipped Alpha contract is the stricter rule above, from the KEP-2941 update in #13601, which "refuses a charge no active representation can hold exactly rather than saturating it". Treat the envelope text in the issue as historical.

User docs (source: pr-16469.md, docs only; website cherry-pick pr-16523). The Workload does **not** record which alternative a Pod received. Read it from the Pod's generated ResourceClaim: `status.allocation.devices.results[*].request` reads `<request>/<alternative>`, e.g. `gpu/a100`. Mismatched counts and unmapped classes are refused with `DRAResourcesUnresolved`. If **any** alternative's DeviceClass does not exist, the kube-scheduler allocator fails the whole claim even when an earlier alternative could be satisfied, and the Pod stays Pending (`device class ... does not exist`). This was verified on kind during review.

## Extended-resource charge computation

`ResolveExtendedResourceQuota` (`pkg/dra/extended_resources.go`) charges DRA-backed extended resources to a logical `deviceClassMappings` quota key.

- **Aggregate before mapping** ([[pr-14200]]; backports [[pr-14396]], [[pr-14397]]): Pod-level aggregation (max over init containers, sum over regular containers, then max of the two) is non-linear, and it used to run *after* mapping each name to its quota key, so two names mapped to one key collapsed: init `vendor.example/a: 5` plus regular `vendor.example/b: 5` charged `gpu-claims: 5` instead of 10. Now aggregation runs per original name and `charge[key] = sum(PodAggregation(R) for R mapped to key)`. Each name's mapping is resolved once per PodSet (not once per container occurrence), closing a window where a DeviceClass created/deleted between reads gave inconsistent results. The integer-quantity check on extended resources now applies only once a matching DeviceClass is found (a fractional request such as `other.example/d: 1500m` with no DeviceClass is fine on the normal quota path), and still runs per container so two fractional requests cannot sum to a whole one.
- **Negative requests dropped** ([[pr-14367]], fixes #14216): `extendedResourceRequests` skipped only zero quantities; it now skips `Sign() <= 0`, so a negative request cannot cancel a legitimate charge on the same key. Defence in depth: `WorkloadValidateResourcesAreNonNegative` (default since v0.20) already rejects negatives at write time, but the webhook is not run on reconcile, so pre-existing or gate-off objects could reach this path. `NeedsDRAReconcile` still uses `!IsZero()`, so a negative-only request triggers a reconcile that resolves to nothing.
- **Init containers** ([[pr-15983]], fixes [[issue-15937]]): collection/charge helpers were extracted and accounting corrected: restartable (sidecar) init containers *add* to regular-container requests; non-restartable ones use max-based accounting. Backports [[pr-16102]], [[pr-16103]].
- **Preprocessing trigger**: `NeedsDRAReconcile` reads raw container `requests` before `AdjustResources` runs, so an extended resource that appears only via a limit or a LimitRange default skipped DRA preprocessing and reached quota under its raw name ([[issue-14393]], closed; see also [[workload-resource-adjustment]]).
- **Per-event cost of the check** (source: pr-17424.md, fixes issue-17422.md; backports pr-17444/0.20, pr-17443/0.19; not in the v0.20.2 / v0.19.9 CHANGELOG at kueue@3bbb8cce4). Since #15284 the workload controller's `needsDRAReconcile` built a full `workload.Info` (LimitRange and RuntimeClass reads, effective specs, total requests, scheduling hash) on every Workload event when the DRA extended-resource gates were on. It now builds it only when a DeviceClass backs an extended resource, because otherwise `NeedsDRAReconcile` returns false anyway. `effectivePodSpecs` also compares only the fields the adjustments change (`Overhead`, container and Pod `Resources`) instead of deep-comparing whole PodSpecs. No behaviour change; in `make run-performance-scheduler`, `needsDRAReconcile` went from 3.03s to 0.05s of CPU and `Info.Update` from 8.49s to 4.98s.

## CEL feature set used to compile device selectors

Kueue compiles DRA selectors with `dracel.NewCache(..., dracel.Features{})` in `pkg/dra/claims.go` and in Configuration validation (`pkg/config/validation.go`). With `k8s.io/dynamic-resource-allocation` v0.36 that empty feature set narrowed the CEL environment, so a selector the apiserver accepted (e.g. `exists()` or `includes()` over a list attribute) could be refused by Kueue. Since v0.20.0 (Kubernetes 1.37 libraries, #15448) the stored-expressions environment uses the newest `device` type whatever `Features` says, so this no longer applies. Kueue 0.19 still uses v0.36.2 and refuses such selectors, but ResourceSlices only carry list attributes while the apiserver's alpha `DRAListTypeAttributes` gate is on, so no backport is planned (source: issue-14372.md, closed; claims.go).

## Requeue keeps charges only for the same generation

DRA charges cannot be rebuilt from the Workload object: the spec carries `resourceClaims`, not the quota keys they translate to, and only the workload controller resolves them. So `Manager.RequeueWorkload` (`pkg/cache/queue/manager.go`) re-reads the object but keeps the preprocessed `TotalRequests` (`workload.WithPreserveTotalRequests()`). Meanwhile `PushOrUpdate` drops updates for a Workload that is inflight in the scheduler. A DRA Workload whose spec changed while inflight was therefore requeued as the new object paired with the old charges, and its scheduling-equivalence hash was computed from that mix, giving at least one cycle of over- or under-admission (issue-14535.md).

Fix (source: pr-14562.md, fixes issue-14535.md; backports pr-17208 in v0.20.2, pr-17211 in v0.19.9 per the CHANGELOGs): with `KueueDRAIntegration` on, if the requeued object's `metadata.generation` differs from the inflight `Info`'s, `requeueWorkloadLocked` does **not** requeue it. It returns a copy that `RequeueWorkload` sends to the workload controller through `draReconcileChannel` **after** releasing `m.Lock()` (as `AddLocalQueue` does), logging `Sent DRA workload to reconcile channel due to a generation change while inflight` at V(4). The controller recomputes the charges and pushes the Workload again. With the same generation, the charges are kept as before. The gate check matters: with it off, `NeedsDRAReconcile` can still be true through `KueueDRARejectWorkloadsWhenDRADisabled`, but no channel is wired, so a send would block. Limitation: a DeviceClass change moves an extended-resource charge without bumping the generation; that case relies on the reconcile the DeviceClass change triggers. Re-running preprocessing inside requeue was rejected because it needs the client, ResourceSlice cache and DeviceClass mapper while `RequeueWorkload` holds the lock (source: manager.go).

## Requeued condition persistence

When a DRA Workload is marked inadmissible (`Requeued=False`, reason `Inadmissible`) and the cause is later resolved, `handleDRA` used to clear the stale conditions **in memory only**, never calling `PatchAdmissionStatus`, so the Workload stayed excluded ([[issue-13969]]). [[pr-15888]] persists `Requeued=True` with reason `DRAResourcesResolved` (backports [[pr-15959]], [[pr-15960]]). [[pr-15961]] (fixes [[issue-15936]], [[issue-14035]]; folds in #14791) removes the remaining in-memory-only condition mutations: the DRA reconciler preprocesses Workloads before queueing and persists `Requeued` transitions so queue/cache decisions match persisted state, including when a Workload leaves backoff. Invariant: DRA controller state changes must be written through the API, never only to the in-memory copy that is queued. Open: dedicated DRA reasons for `WorkloadQuotaReserved=False` ([[issue-15953]]).

**`Requeued=False` is re-asserted on a repeated failure** (source: pr-17093.md, pr-17294.md, workload_controller.go). The DRA paths set `Requeued=False` only when the `QuotaReserved` update itself changed something (`if updated && SetRequeuedCondition(...)`). So when the same validation error was already recorded, a Workload could keep `Requeued=True` after DRA validation failed again. The `Requeued` change is now evaluated on its own (`changed = updated || requeuedChanged`). pr-17093 also stopped error-logging DRA validation failures on every reconcile. pr-17294 then replaced the Warning/Normal events that pr-17093 had added (never released) with `V(3)` logs `Workload status updated` (reason, message) and `Updated previous inadmissible conditions after successful DRA processing`, written only after the status update succeeds. pr-17093 was backported as pr-17332/0.20 and pr-17410/0.19, neither listed in the v0.20.2 / v0.19.9 CHANGELOG at kueue@3bbb8cce4. Backports of pr-17294: pr-17445/0.20, pr-17447/0.19. To make the 0.19 cherry-pick of pr-17093 possible, the DRA reconciler refactor #13549 (pr-17314) and pr-15961 (pr-17368) were backported to release-0.19 as well, all with release note NONE.

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
