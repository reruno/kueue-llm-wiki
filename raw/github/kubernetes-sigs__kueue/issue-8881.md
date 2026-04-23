# Issue #8881: TAS: Hierarchical Resource Flavor Support

**Summary**: TAS: Hierarchical Resource Flavor Support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8881

**Last updated**: 2026-02-12T12:18:47Z

---

## Metadata

- **State**: open
- **Author**: [@Ladicle](https://github.com/Ladicle)
- **Created**: 2026-01-30T02:41:13Z
- **Updated**: 2026-02-12T12:18:47Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I’d like to have a way to structure ResourceFlavors in a hierarchy, similar to how Cohorts organize ClusterQueues. This would enable more efficient, layered quota management.

**Why is this needed**:

Managing quotas with a flat ResourceFlavor structure is challenging in environments with diverse hardware, especially various GPU types. These are our use cases:

- Global pools (CPU/Memory): Enable setting a global quota for resources like CPU and Memory that applies across the entire cluster, regardless of the specific node type (flavor) used.
- Hierarchical GPU Management: Enable setting quotas hierarchically in environments with mixed GPU types. For example, setting quotas based on GPU model families (e.g., GPU-C Total) and further subdividing them based on specific specs (e.g., GPU-C-16GB vs. GPU-C-32GB).

<img width="1368" height="697" alt="Image" src="https://github.com/user-attachments/assets/28bcf318-82ba-4728-ae43-c9843c375d68" />

Without a hierarchy, admins have to set quotas for leaf flavors, which leads to them being tightly restricted. This makes it harder to distribute resources as efficiently as we’d like.

**Why existing solutions are insufficient**:

Using multiple ResourceGroups (as discussed in https://github.com/kubernetes-sigs/kueue/issues/5877#issuecomment-3080005818) works for orthogonal resources like hardware vs. licenses. However, it doesn’t currently support TAS.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T08:25:03Z

@Ladicle would it be possible to model the quotas using the virtual "credits" approach by ResourceTransformations: https://kueue.sigs.k8s.io/docs/tasks/manage/share_quotas_across_flavors/

Currently we are working on fixing this for TAS; https://github.com/kubernetes-sigs/kueue/issues/8860

Surely this is not the most convenient solution, but I'm asking to explore the space of possible short and long term solutions. 

It would be great to present this proposal at wg-batch: https://github.com/kubernetes/community/tree/master/wg-batch

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-02-12T12:18:47Z

@mimowo Thanks for the pointer to the credits approach! For global resources like mem/cpu, the credits approach makes sense for limiting shared resources. I plan to try it once TAS support for #8860 is released.

However, regarding hierarchical GPU management, I feel that the credits approach alone might be challenging for our specific use cases. We manage a wide variety of accelerators (including custom in-house chips), so mapping them all to credits could be quite complex.
I'll try to write up a document exploring the "Hierarchical Resource Flavor Support" solution as a potential long-term approach.
