# Issue #9694: Skip identical workloads in CQ processing

**Summary**: Skip identical workloads in CQ processing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9694

**Last updated**: 2026-03-06T20:28:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-03-05T16:09:28Z
- **Updated**: 2026-03-06T20:28:20Z
- **Closed**: 2026-03-06T20:28:20Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 8

## Description

**What would you like to be added**:

A Hash based blacklist of already processed scheduling constraints. 

I imagine that this could work in the following way:

* Every incoming workload will generate a strict, deterministic hash based on its exact resource requests, node selectors, affinity rules, tolerations, and any other fields that impact scheduling.
* During a CQ evaluation iteration, if a workload is deemed inadmissible, its hash is immediately added to an in-memory, volatile blacklist hash set.
* As the queue is processed, the scheduler checks the hash of each subsequent workload; if it matches a blacklisted hash, the workload is bypassed without undergoing a full evaluation.
* The blacklist hash set is cleared and rebuilt whenever the inadmissible workloads are "added back" to CQ for reevaluation.

**Why is this needed**:

In best effort FIFO CQ with high churn and mixed workloads (like combination of CPU and GPU), Kueue has problems in reaching deep enough into the CQ before reevaluation is triggered. As the result, some workloads may not get admitted while there is enough capacity for them in the cluster. 

The number of different scheduling requirements (pod count, pod requirements, node selector) is usually significantly smaller than the number of workloads. Not doing unnecessary evaluations by skipping the already processed requirements will allow to reach much deeper into Best Effort FIFO CQs and improve cluster utilization.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T16:22:28Z

/assign @sohankunkerkar 
who is already looking into this

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T17:44:29Z

At the implementation level:
- we already have a function to generate the "RoleHash" for Pods. I believe we could use a similar approach here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/pod/pod.go#L125-L137
- since the hash generation might be heavy we could store it in the Workload.Info structure on Update().

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T18:58:15Z

/priority important-soon

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-05T19:15:24Z

Thanks for the write-up on this. The hash-blacklist approach is promising, but a few implementation constraints need to be explicit:
1. Only class-equivalent inadmissible workloads: only workloads that went through full assignment evaluation and definitively cannot fit any node should be hash-blacklisted. Early-exit failures (namespace selector, LimitRange, admission check state) are specific to that workload or namespace and must not populate the blacklist.

2. Cross-cycle vs in-Pop(): Hash learning is cross-cycle (because one head per CQ is nominated per cycle), while hash application may still skip multiple already-blacklisted entries inside a single Pop() call.

3. Sticky/preemption semantics: It must be preserved. In BestEffortFIFO with AFS ordering, a non-sticky workload can be popped ahead of sticky; blacklist checks must never cause sticky workloads to be skipped.

The rest of the design, like computing the hash, keeping it volatile, and clearing it on requeue, looks solid.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T19:21:57Z

> Cross-cycle vs in-Pop(): Hash learning is cross-cycle (because one head per CQ is nominated per cycle), while hash application may still skip multiple already-blacklisted entries inside a single Pop() call.

I was thinking a bit different: whenever we Pop a workload and call Requeue as Inadmissible, then we also put to inadmissible all workloads which belong to the same equivalence class (have the same hash). This will allow to avoid even wasting cycles to Pop them. I think this is important, because in case of TAS even Pop and building the snapshot is costly (often mode than actual looking for placement even).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T19:24:08Z

> Only class-equivalent inadmissible workloads: only workloads that went through full assignment evaluation and definitively cannot fit any node should be hash-blacklisted. Early-exit failures (namespace selector, LimitRange, admission check state) are specific to that workload or namespace and must not populate the blacklist.

I was thinking we would "backlist" hashes, not workloads specifically. So we have a set of "inadmissible hashes" and put into the "inadmissible list" all workloads which have a hash in this set. This moving could be done on Requeue of one of the representive of the class.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T19:25:09Z

> Sticky/preemption semantics: It must be preserved. In BestEffortFIFO with AFS ordering, a non-sticky workload can be popped ahead of sticky; blacklist checks must never cause sticky workloads to be skipped.

Yes. If we have a sticky workload, then it was admissible already. It stays admissible until the preemptions are over.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-05T20:58:38Z

That makes sense. The bulk-move on requeue avoids wasting cycles entirely, including the snapshot cost. On the sticky point, confirmed from the code: NoFit is only returned when capacity is exceeded or CQ policy blocks preemption while borrowing, both priority-independent. `noPreemptionCandidates` maps to Preempt not NoFit, so a sticky workload's hash never enters the inadmissible set.
