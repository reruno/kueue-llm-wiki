# Issue #5439: TAS: Two-level JobSet scheduling

**Summary**: TAS: Two-level JobSet scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5439

**Last updated**: 2025-07-08T20:14:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-06-02T10:31:51Z
- **Updated**: 2025-07-08T20:14:19Z
- **Closed**: 2025-06-12T13:42:58Z
- **Labels**: `kind/feature`
- **Assignees**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A possibility to define topology for each Job in ReplicatedJob to co-locate the whole ReplicatedJob in one domain and each Job in that ReplicatedJob in lower-level domain within that domain.

In more generic terms - an API to define required sub PodSet topology and allow for two-level scheduling for the whole PodSet and lower-level topology domain for each chunk within that PodSet.

An example is a JobSet in which user can define topology for all Jobs resulting from a single ReplicatedJob. We want to allow user to define topology for each such Job and possibly co-locate all such Jobs in higher-level topology.

**Why is this needed**:
Currently Topology-Aware Scheduling considers the whole PodSet as a single unit for which Kueue looks for a matching domain. For JobSet PodSet covers all pods resulting from the whole ReplicatedJob. However, there are use-cases in which user would like to co-locate each Job in a lower-level domains and co-locate all those Jobs in higher-level domain.

Additionally, user would like to define a topology only for each Job without any expectations for a topology of the whole ReplicatedJob.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T10:50:54Z

/retitle TAS: Two-level JobSet scheduling

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-02T14:26:07Z

TAS KEP update to reflect two-level scheduling and podset chunk topology: https://github.com/kubernetes-sigs/kueue/pull/5449

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-06-16T15:55:13Z

One quick question: can this solve the https://github.com/kubernetes-sigs/kueue/pull/3941? E.g. co-locate the master and worker jobs in pytorchjob.
Thanks!

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-06-16T15:58:36Z

I'll read the KEP in detail later.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-06-17T07:44:07Z

This focused on podSet chunks, not between multi-podsets.

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-17T07:47:34Z

I will be looking into cross-podsets scheduling in few following weeks. I'll do it mostly for LeaderWorkerSet though, but I think the underlying mechanism will be universal, so probably it'll be easy to add pytorchjob support afterwards.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-06-17T07:50:47Z

Thanks @lchrzaszcz for your response, I think leaderworkerset pytorchjob are just two different workload types, the mechanism should be universal to them all I believe. Glad to jump into the discussion.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T20:14:16Z

/assign @lchrzaszcz
