# ResourceFlavor

**Summary**: A ResourceFlavor is a cluster-scoped label-and-toleration descriptor that distinguishes otherwise-equivalent resources — `a100` vs `h100` GPUs, `spot` vs `on-demand` CPU, `zone-a` vs `zone-b` memory. Flavors attach to [[cluster-queue]] quota slots so that a Workload asking for "10 GPUs of flavor h100" is counted against the right pool and its Pods are directed to the right nodes.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-13616.md, pr-13956.md, pr-16766.md, pr-16466.md, pr-16658.md, pr-13622.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-28

---

## What a flavor carries

A `ResourceFlavor` object has:

- `nodeLabels` — map of labels that Kueue injects as `nodeSelector` on admitted Pods, so `kube-scheduler` lands them on matching nodes ([[issue-425]] — this is intentional injection, not a naming accident).
- `nodeTaints` — taints the flavor's nodes carry; a PodSet must tolerate them (NoSchedule/NoExecute) to be assigned this flavor, unless the flavor's own `tolerations` cover them.
- `tolerations` — Pod tolerations that Kueue mutates onto admitted Pods so they can run on tainted nodes. The tolerations also need to flow into any PodTemplate attached to a ProvisioningRequest ([[admission-check]]) so that autoscaled nodes match ([[issue-2572]]).
- `topologyName` (with TAS) — a reference to a [[topology-aware-scheduling]] Topology object. Only flavors that reference a Topology participate in topology-aware placement.

## Flavors inside ClusterQueue

ClusterQueue `spec.resourceGroups[].flavors[]` references flavors by name and assigns nominal quota per resource per flavor. A single resource group covers one set of resources that must be allocated from a single flavor (e.g. CPU+memory+GPU all from `h100-on-demand`). A Workload cannot split its request across flavors within a resource group.

## Fungibility

If a Workload's first-choice flavor is full, Kueue can try the next flavor in the ClusterQueue's list. The `flavorFungibility` policy on the CQ controls whether Kueue borrows from the cohort first, preempts within the current flavor first, or falls through to the next flavor first. Edge cases around preemption interacting with flavor fallback are common ([[issue-1344]], [[issue-2560]]).

Recent fixes to flavor selection (details on [[scheduler-internals#FlavorAssigner]]):

- A flavor whose preemption simulation finds **no candidates** now always ranks below a flavor that fits or can preempt, before `flavorFungibility.preference` is applied; previously `PreemptionOverBorrowing` could pick it over a fitting flavor at a deeper borrowing level and leave the Workload pending (pr-13616, v0.20.0).
- The search **remembers which flavors it already tried** across scheduling cycles (`FlavorScanState`, gate `FlavorFungibilityPreserveScanProgress`, Beta/on in v0.20), so a Workload that fits quota on flavor A but cannot be placed there (typically TAS) moves on to flavor B instead of retrying A forever (pr-13956); since pr-16766 the progress is a set of tried flavors, which fixed `TryNextFlavor` skipping or looping when all flavors borrow or a later flavor fits nominal.
- Zero-count PodSets always restart their capacity probe at the first flavor, so an admission retry cannot hand an elastic Job a flavor without capacity for its future pods (pr-16466).
- Non-adjacent PodSet group members are matched by name, not position, during scan resume (pr-16658).

## Updating a flavor in place (v0.20.0)

- **TAS flavors (`spec.topologyName` set)**: `spec.tolerations` became mutable (pr-13622, part of #3733). The TAS ResourceFlavor controller updates the cached flavor *in place* before retrying inadmissible Workloads, so topology usage and per-Workload usage stay accounted across additions and removals. pr-13622 kept `nodeLabels` and `topologyName` immutable; a later v0.20.0 change (#13738) also allowed `spec.nodeLabels` updates: admitted Workloads keep their reservation and topology assignment, pending Workloads are requeued against the new node set, and usage on overlapping flavors is counted once. `topologyName` stays immutable (source: pr-13622.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).
- **Non-TAS flavors**: editing `nodeTaints` (#13670) or `tolerations`/`nodeLabels` (#13734) now retries Workloads that the previous spec left inadmissible, instead of waiting for an unrelated event (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

## Deletion safety

A ResourceFlavor cannot be deleted while any ClusterQueue still references it — Kueue puts a finalizer on the RF ([[issue-249]], [[issue-283]]). This prevents silently breaking a CQ's quota definition.

## Tolerations in integrations

ResourceFlavor tolerations have to reach the Pods the underlying integration creates. For PyTorchJob this was a bug in early versions ([[issue-1407]] — nodeLabels from ResourceFlavor not added as node selectors to Kubeflow PyTorchJobs). The general pattern: the integration's mutating step must merge flavor labels/tolerations into the Pod template before the Pods become visible to `kube-scheduler`.

### Toleration dedup and the default `Operator` (v0.18)

When admitting a workload, `PodSetInfo.Merge` (`pkg/podset/podset.go`) appends the flavor's tolerations to the Pod template, **deduplicating** against the workload's existing tolerations. The dedup originally compared `corev1.Toleration` values with Go `==`, which treats `Operator: ""` and `Operator: "Equal"` as different — but the Kubernetes API **defaults an empty toleration `Operator` to `Equal`**, so the two forms are semantically identical. A flavor toleration written one way and a Pod toleration written the other both slipped past dedup and **both got appended**, injecting a duplicate ([[pr-11147]]).

The downstream symptom is nasty: on the next Pod/Job update, if a mutating webhook collapses the duplicate between Kueue's read and write, `validateOnlyAddedTolerations` rejects the update (`existing toleration can not be modified except its tolerationSeconds`) and the Pod is stuck `scheduleGated`. The fix adds a `tolerationsEqual` helper that normalizes an empty `Operator` to `Equal` before comparing.

## Related pages

- [[cluster-queue]] — where flavors are assigned quota.
- [[admission]] — when flavor labels and tolerations get injected.
- [[topology-aware-scheduling]] — flavors that reference a Topology.
- [[scheduler-internals]] — flavor assignment and scan progress.
