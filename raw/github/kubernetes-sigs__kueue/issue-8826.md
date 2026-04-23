# Issue #8826: Support for running hero workloads

**Summary**: Support for running hero workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8826

**Last updated**: 2026-01-30T13:26:51Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T15:22:41Z
- **Updated**: 2026-01-30T13:26:51Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Dedicated API, likely a dedicated Hero/Uber ClusterQueue type/mode, for running "hero" workloads. 

There is no one definition of a hero workload, but they have common characteristics: they often take >50% of the cluster capacity and run for a prolonged time (weeks), and are "super high priority". Such workloads are often used for AI training, and basically impact the cluster for the entire organization within the period.

**Why is this needed**:

There is currently no go-to setup for running "hero" workloads. 

For example, getting suddenly >50% of cluster quota is hard, because even if the workload has "super high priority", then it still cannot preempt from CQs which are below nominal quota.

Different users make different approaches which have their pros / cons, and eventually come up with something that "works", but it is re-discovering the wheel. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:23:29Z

/assign @mwielgus 
who I think is currently cooking some design
cc @tenzen-y @gabesaba  @sohankunkerkar @kannon92  @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T16:32:54Z

Note that it might be considered an alternative design for: https://github.com/kubernetes-sigs/kueue/pull/6141 (at least with strong overlap for use-cases). I tentatively think this approach per CQ is more aligned with the principles of Kueue, but let's re-evaluate both designs when posted.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T18:03:20Z

> Note that it might be considered an alternative design for: [#6141](https://github.com/kubernetes-sigs/kueue/pull/6141) (at least with strong overlap for use-cases). I tentatively think this approach per CQ is more aligned with the principles of Kueue, but let's re-evaluate both designs when posted.

As I checked ~#6141~ #8654, this doesn't cover the ~#6141~ #8654 use case. It seems that they want to relax quotas in a specific tenants managed by a single large shared ClusterQueue.

So, I think this request could be considered another one, and totally agree with the described story in this issue.

[EDIT] I left the above comment assuming #8654. I think that this could replace #6141, surely. Let's see which (#6141 vs this) can cover the almost stories.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-29T02:02:04Z

Alternative approach (very-very rough draft): #8869
