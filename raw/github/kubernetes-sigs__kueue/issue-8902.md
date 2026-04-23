# Issue #8902: Flavor-Aware Fair Sharing for Heterogeneous Resources (Weighted flavours)

**Summary**: Flavor-Aware Fair Sharing for Heterogeneous Resources (Weighted flavours)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8902

**Last updated**: 2026-02-16T17:51:58Z

---

## Metadata

- **State**: open
- **Author**: [@monabil08](https://github.com/monabil08)
- **Created**: 2026-01-30T10:32:43Z
- **Updated**: 2026-02-16T17:51:58Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Flavor-aware Fair Sharing calculation that accounts for the different values/costs of resource flavors when computing Dominant Resource Share (DRS).

Currently, Fair Sharing aggregates resource usage across all flavors (e.g., all nvidia.com/gpu regardless of whether they're T4 or A100). This treats heterogeneous resources as equivalent, leading to unfair preemption decisions.

One solution: Add optional cost weights to ResourceFlavor spec to represent relative resource value:
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: a100-gpu
spec:
  nodeLabels:
    accelerator: nvidia-tesla-a100
  cost:  # New field (optional)
    nvidia.com/gpu: 8.0  # 8x more valuable than baseline
```

When calculating DRS, borrowing would be weighted by cost:
`weighted_borrowing = (borrowed_t4 × 1.0) + (borrowed_a100 × 8.0)`

**Why is this needed**:
Organizations with heterogeneous GPU clusters (H100, A100, T4), different CPU generations (performance tiers) face unfair resource allocation:

Example:
Team A: borrows 20 T4 GPUs (cheap, low-power)
Team B: borrows 20 A100 GPUs (expensive, high-power)
Current Fair Sharing sees both teams are equal, while team B is using a lot more resources cost wise, so they should be more preemptable

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@monabil08](https://github.com/monabil08) — 2026-01-30T10:33:10Z

This is based on my understanding of how things are working today, which might be wrong 🙏

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-01T21:01:14Z

WDYT of this?

seems like a useful feature.

cc @gabesaba @mimowo @tenzen-y @mwielgus

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-02T09:17:01Z

Yes, I could see this being useful. Is this the same proposal as https://github.com/kubernetes-sigs/kueue/issues/4857? If yes, we can deduplicate and keep just one of the issues open.

### Comment by [@monabil08](https://github.com/monabil08) — 2026-02-02T11:47:54Z

@gabesaba I think https://github.com/kubernetes-sigs/kueue/issues/4857 is more about different resource groups as in CPU v GPU giving them a better weight instead of depending on the max aggregation. What I am proposing is more on the flavour side of things in the same resource type. For GPU for example T4 is much cheaper than A100 so it would have less impact on the weight value.

### Comment by [@monabil08](https://github.com/monabil08) — 2026-02-05T11:39:24Z

@kannon92 what would be the next steps if I wanted to contribute and have this feature in, should I get some approval from the community somehow maybe through a KEP, or some other form?

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-02-16T17:51:57Z

@gabesaba I've raised [a KEP](https://github.com/kubernetes-sigs/kueue/pull/9251). Can you review when you can please?
