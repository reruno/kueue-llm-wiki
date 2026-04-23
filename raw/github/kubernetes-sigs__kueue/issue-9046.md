# Issue #9046: TAS: Support Multi-Layer Topology Constraints

**Summary**: TAS: Support Multi-Layer Topology Constraints

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9046

**Last updated**: 2026-03-06T10:55:44Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@Huang-Wei](https://github.com/Huang-Wei)
- **Created**: 2026-02-07T08:41:54Z
- **Updated**: 2026-03-06T10:55:44Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

## What would you like to be added

Support training workloads with **multi-layer topology constraints** (e.g., GB200/GB300 clusters).

[kubernetes-sigs/kueue#6554 (comment)](https://github.com/kubernetes-sigs/kueue/issues/6554#issuecomment-3179837495) cleanly illustrates the need.
Real-world data center topologies often have multiple physical levels (e.g., data center → building → row/NVLink domain/block → rack → host); to get the best performance, workloads increasingly need to express constraints at more than two of those levels simultaneously.

## Current situation and gap

TAS balanced placement ([#6851](https://github.com/kubernetes-sigs/kueue/pull/6851), v0.15) is a best-effort primitive that balances pod placement on a specified topology. However, in real-world GB200 clusters we need to **guarantee** that a training Job's Pods are co-located into NVLink domain / rack / other topology levels with specific, layered criteria.

Even if we changed semantics of TAS balanced placement to guaranteed, it still lacks the flexibility to express **multi-layer topology constraints**. For example, a 96-replica Job may require:

- all 96 Pods land in the same datacenter
- groups of 48 Pods land within the same virtual zone (so it doesn't end with landing on 3 zones, with each having 32 Pods)
- groups of 16 Pods land within the same rack
- (or even finer granularity)

## Closest existing primitive

The closest mechanism is [KEP-2724: Two-level Topology Aware Scheduling](https://github.com/kubernetes-sigs/kueue/pull/5449) (#5449 / #5596), which introduced the `podset-slice-required-topology` / `podset-slice-size` annotations. Although designed primarily for JobSet, the mechanism is generic enough to support arbitrary PodSet-based workloads.

However, it is limited to exactly **2 constraint tiers**: one for the entire PodSet and one for slices — close to what we need, but not sufficient.

## Proposed change

Extend TAS to support **multi-layer topology constraints** - up to N total constraint levels (1 podset-level + N−1 slice layers). Users specify **additional slice layers** that recursively subdivide slices into smaller groups, each constrained to a finer topology level.

**Example: 4-layer constraints on 96 pods:**

```yaml
# Existing "kueue.x-k8s.io/podset-slice-*" annotations are kept as-is for backward compatibility
annotations:
  # Layer 0 (podset): all 96 pods in the same datacenter
  kueue.x-k8s.io/podset-required-topology: "cloud.provider.com/datacenter"
  # Layer 1 (existing slice): groups of 48 in the same logical zone
  kueue.x-k8s.io/podset-slice-required-topology: "cloud.provider.com/logical-zone"
  kueue.x-k8s.io/podset-slice-size: "48"
  # Layer 2 (new): groups of 16 on the same rack
  kueue.x-k8s.io/podset-slice-required-topology-1: "cloud.provider.com/rack"
  kueue.x-k8s.io/podset-slice-size-1: "16"
  # Layer 3 (new): groups of 2 on the same host (optional: depends on GB200 setup: NVL36 vs. NVL72)
  # kueue.x-k8s.io/podset-slice-required-topology-2: "kubernetes.io/hostname"
  # kueue.x-k8s.io/podset-slice-size-2: "2"
```

Result: 96 pods → 2 logical zones → 6 racks of 16. So it ends up w/ `{3 racks, 3 racks}` which is a symmetric distribution instead of `{4 racks, 2 racks}`.

There are other variants of needing multiple layers, but not restricted to the following:

- As time goes, the cluster gets fragmented, and w/o (or we cannot) active de-fragmentation, we need more layers to achieve optimal performance upon cluster's fragmentation
- For an XL training Job, it may need 1000+ replicas and would need more layers to support it
- ...

> [!IMPORTANT]
> The concrete number of `N` can be discussed. We may start with a conservative cap of **2 additional layers** (3 slice layers total).

```diff
diff --git a/apis/kueue/v1beta2/workload_types.go b/apis/kueue/v1beta2/workload_types.go
index ce630751e..79a0d56b8 100644
--- a/apis/kueue/v1beta2/workload_types.go
+++ b/apis/kueue/v1beta2/workload_types.go
@@ -223,6 +223,33 @@ type PodSetTopologyRequest struct {
 	//
 	// +optional
 	PodSetSliceSize *int32 `json:"podSetSliceSize,omitempty"`
+
+	// additionalSliceLayers defines additional layers of recursive slice
+	// subdivision beyond the first slice layer (podSetSliceRequiredTopology /
+	// podSetSliceSize). Each layer further subdivides the parent layer's
+	// groups into smaller groups constrained to a finer topology domain.
+	// At most 2 additional layers are supported (for a total of 3 slice layers).
+	//
+	// +optional
+	// +listType=atomic
+	// +kubebuilder:validation:MaxItems=2
+	AdditionalSliceLayers []SliceLayer `json:"additionalSliceLayers,omitempty"`
+}
+
+// SliceLayer defines a single additional slice subdivision layer.
+type SliceLayer struct {
+	// topology indicates the topology level required for this slice layer.
+	//
+	// +required
+	// +kubebuilder:validation:MinLength=1
+	// +kubebuilder:validation:MaxLength=63
+	Topology string `json:"topology"`
+
+	// size indicates the number of pods in each group at this slice layer.
+	//
+	// +required
+	// +kubebuilder:validation:Minimum=1
+	Size int32 `json:"size"`
 }

 type Admission struct {
```

## Why is this needed

### 1. Real data center topologies are deeper than 2 levels

Modern GPU clusters have hierarchies like **data center → building -> virtual zone -> NVLink Doamin/block/row → rack →  → host**. AI/ML training workloads need different communication granularities at each level: all-reduce within a host, ring-reduce within a rack, hierarchical all-reduce across racks within a block. Being limited to 2 constraint tiers means users can only optimize for 2 of these boundaries, leaving performance on the table.

### 2. Natural extension of existing design

The slice mechanism already supports recursive subdivision conceptually - a slice is just a fixed-size group constrained to a topology domain. Multi-layer slicing is "slices within slices," following the same pattern. The existing TAS algorithm's 2-phase traversal (greedy above slice level, parent-constrained at/below) generalizes naturally to N phases.

### 3. Avoids workarounds

Without this, users must work around the limitation by:

- Manually splitting workloads into smaller Jobs and coordinating placement externally
- Using multiple JobSets with separate topology constraints, losing the "all in one topology" guarantee
- Relying on the Kubernetes scheduler's topology spread constraints, which lack TAS's capacity-aware admission

## Completion requirements

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-02-07T08:44:42Z

cc @mimowo @tenzen-y @mbobrovskyi PTAL when you get a chance.

(internally we implemented this in a forked Kueue repo, and more than happy to contribute back)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T08:30:09Z

Hi @Huang-Wei this looks very interesting! 

+1, certainly I can imagine this is a great addition.  The extended API looks reasonable too. The cap of 2/3 additional layers sgtm.

To move forward it would be great to see the KEP update, potentially with the prototype implementation already.

cc @tenzen-y, @gabesaba, @mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T16:07:39Z

I think it would also make a great topic for the [wg-batch community](https://github.com/kubernetes/community/tree/master/wg-batch) meeting, so please consider presenting.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-02-11T19:14:39Z

> I think it would also make a great topic for the [wg-batch community](https://github.com/kubernetes/community/tree/master/wg-batch) meeting, so please consider presenting.

Yup, that's exactly what I'm planning to do - i've signed up in the 2/12 meeting's agenda, and will present the idea as well as a live demo.

After the meeting, if we can get to a consensus, I will update the existing TAS KEP, _probably_ introduce a new featuregate.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T10:55:38Z

/reopen 
To track the remaining effort:
- make sure NodeHotSwap is supported
- documentation

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-06T10:55:44Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9046#issuecomment-4011034904):

>/reopen 
>To track the remaining effort:
>- make sure NodeHotSwap is supported
>- documentation


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
