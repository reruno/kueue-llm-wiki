# ResourceFlavor

**Summary**: A ResourceFlavor is a cluster-scoped label-and-toleration descriptor that distinguishes otherwise-equivalent resources — `a100` vs `h100` GPUs, `spot` vs `on-demand` CPU, `zone-a` vs `zone-b` memory. Flavors attach to [[cluster-queue]] quota slots so that a Workload asking for "10 GPUs of flavor h100" is counted against the right pool and its Pods are directed to the right nodes.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## What a flavor carries

A `ResourceFlavor` object has:

- `nodeLabels` — map of labels that Kueue injects as `nodeSelector` on admitted Pods, so `kube-scheduler` lands them on matching nodes (source: issue-425.md — this is intentional injection, not a naming accident).
- `nodeTaints` — reverse of the label mapping; informational.
- `tolerations` — Pod tolerations that Kueue mutates onto admitted Pods so they can run on tainted nodes. The tolerations also need to flow into any PodTemplate attached to a ProvisioningRequest ([[admission-check]]) so that autoscaled nodes match (source: issue-2572.md).
- `topology` (with TAS) — a reference to a [[topology-aware-scheduling]] Topology object. Only flavors that reference a Topology participate in topology-aware placement.

## Flavors inside ClusterQueue

ClusterQueue `spec.resourceGroups[].flavors[]` references flavors by name and assigns nominal quota per resource per flavor. A single resource group covers one set of resources that must be allocated from a single flavor (e.g. CPU+memory+GPU all from `h100-on-demand`). A Workload cannot split its request across flavors within a resource group.

## Fungibility

If a Workload's first-choice flavor is full, Kueue can try the next flavor in the ClusterQueue's list. The `flavorFungibility` policy on the CQ controls whether Kueue borrows from the cohort first, preempts within the current flavor first, or falls through to the next flavor first. Edge cases around preemption interacting with flavor fallback are common (source: issue-1344.md, source: issue-2560.md).

## Deletion safety

A ResourceFlavor cannot be deleted while any ClusterQueue still references it — Kueue puts a finalizer on the RF (source: issue-249.md, source: issue-283.md). This prevents silently breaking a CQ's quota definition.

## Tolerations in integrations

ResourceFlavor tolerations have to reach the Pods the underlying integration creates. For PyTorchJob this was a bug in early versions (source: issue-1407.md — nodeLabels from ResourceFlavor not added as node selectors to Kubeflow PyTorchJobs). The general pattern: the integration's mutating step must merge flavor labels/tolerations into the Pod template before the Pods become visible to `kube-scheduler`.

## Related pages

- [[cluster-queue]] — where flavors are assigned quota.
- [[admission]] — when flavor labels and tolerations get injected.
- [[topology-aware-scheduling]] — flavors that reference a Topology.
