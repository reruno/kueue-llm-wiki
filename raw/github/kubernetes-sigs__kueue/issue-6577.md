# Issue #6577: Fairsharing bug that prevents CQs from reclaiming guarantees

**Summary**: Fairsharing bug that prevents CQs from reclaiming guarantees

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6577

**Last updated**: 2025-08-19T21:59:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-13T23:54:02Z
- **Updated**: 2025-08-19T21:59:28Z
- **Closed**: 2025-08-19T21:59:28Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**: 
We noticed an increase in guarantee violations when fairsharing is turned on where CQs are unable to reclaim their guarantees when preemption is required despite having guarantees.

There were a lot of logs that said...
- `Workload requires preemption, but there are no candidate workloads allowed for preemption` 
- `couldn't assign flavors to pod set foo: insufficient unused quota for nvidia.com/gpu in flavor bar, 5 more needed`. 
  - This cluster also only has 1 flavor.

**What you expected to happen**:
Cqs need to be able to reclaim guarantees. 

**How to reproduce it (as minimally and precisely as possible)**:
We detect this in production and don't know how to repro. But it occurs multiple times in production. 

**Anything else we need to know?**:
Here is a theory:

We do hit these logs: `logV.Info("Simulating fair preemption", "candidates", workload.References(candidates), "resourcesRequiringPreemption", preemptionCtx.frsNeedPreemption.UnsortedList(), "preemptingWorkload", klog.KObj(preemptionCtx.preemptor.Obj))`

* `candidates` is heavily populated within our logs (meaning at some point it had a lot of preemption candidates)

Tracing the code, here is our theory:
1. `fairPreemptions(...)`
2. `logV.Info("Simulating fair preemption", "candidates", workload.References(candidates), ...)`
    1. we do see a lot of candidates here in the logs but later down return no preemption candidates
3. This means `fits` within `fits, targets, retryCandidates := runFirstFsStrategy(preemptionCtx, candidates, strategies[0])` is probably false. Why?

It could be this...
1. `workloadFits()` checks...
```
if v > preemptionCtx.preemptorCQ.Available(fr) {
    return false
} 
// v is resources preemptor workload needs for flavor
// "Available returns the current capacity available, before preempting any workloads"
```
2. `Available` → `available` → `LocalAvailable`
3. `LocalAvailable` returns `guaranteedQuota() - Usage[fr]`

The issue is probably here:
```
func (r resourceNode) guaranteedQuota(fr resources.FlavorResource) int64 {
    if lendingLimit := r.Quotas[fr].LendingLimit; lendingLimit != nil {
        return max(0, r.SubtreeQuota[fr]-*lendingLimit)
    }
    return 0
}
```
1. `guaranteedQuota` isn’t actually returning you guaranteed quota. Its basing the calculation off lendingLimit... which... we do not set. 
2. `LendingLimit == nil` → `return 0`

SO. Back to this:
1. 
```
if v > preemptionCtx.preemptorCQ.Available(fr) {
        return false
}
 ```
2. v > 0 → return false
3. ❌ fails fit check

---
⭐️ Other supporting evidence: This could explain this! https://github.com/kubernetes-sigs/kueue/issues/6219
`Reclamation disappeared as a preemption reason after turning on fairshare`

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): 0.12.2

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-14T01:17:08Z

The other question may be... why doesn't classical preemption have this issue?
Maybe its around the difference in timing of when you add/remove usage for the workloads in relation to fit checks?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:55:46Z

@amy Could you share the ClusterQueue manifests? Especially, I would like to know preemption parameters.
Additionally, did you try to upgrade Kueue version to v0.12.3? The newer v0.12 patch version fixed flavor assignment accuracy bugs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T06:56:04Z

cc @gabesaba @mimowo

### Comment by [@mpaliwal3](https://github.com/mpaliwal3) — 2025-08-14T07:35:02Z

@tenzen-y  Here is a snippet from the impacted CQ. We are running v0.12.2 right now. We only have one resource flavor in this cluster.

```
spec:
  cohort: cohort-ufbw46fk3tkd
  fairSharing:
    weight: "100"
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      maxPriorityThreshold: 80000
      policy: Never
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  resourceGroups:
```

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-14T08:06:29Z

> guaranteedQuota isn’t actually returning you guaranteed quota. Its basing the calculation off lendingLimit... which... we do not set.

This is a poorly named method. It is referring to the quota that will never be lent out, while the rest is bubbled up to the parent (see `accumulateFromChild`). It doesn't refer to the nominal quota which the CQ is guaranteed to reclaim (assuming proper policy, etc).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T08:06:54Z

> [@tenzen-y](https://github.com/tenzen-y) Here is a snippet from the impacted CQ. We are running v0.12.2 right now. We only have one resource flavor in this cluster.
> 
> ```
> spec:
>   cohort: cohort-ufbw46fk3tkd
>   fairSharing:
>     weight: "100"
>   flavorFungibility:
>     whenCanBorrow: TryNextFlavor
>     whenCanPreempt: TryNextFlavor
>   namespaceSelector: {}
>   preemption:
>     borrowWithinCohort:
>       maxPriorityThreshold: 80000
>       policy: Never
>     reclaimWithinCohort: Any
>     withinClusterQueue: LowerPriority
>   queueingStrategy: BestEffortFIFO
>   resourceGroups:
> ```

Thank you for sharing that. Could you share fairSharing.weight value range across all ClusterQueues (e.g, 1-100, 100-1000)?
I want to check if this clusterqueue dws is not rounded down into 0.

### Comment by [@amy](https://github.com/amy) — 2025-08-14T11:16:03Z

Its weighted fairshare on the CQ itself was around 33. But the DRS in logs for this workload during tournament is 0 indicating reclamation.

### Comment by [@amy](https://github.com/amy) — 2025-08-14T16:34:48Z

Updating the thread on other potential theories to follow along with/debug:
Issues with `nextTarget`. Maybe there's something wrong with the pruning logic where its somehow causing a CQ to be discarded prematurely.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-14T18:03:51Z

> Updating the thread on other potential theories to follow along with/debug: Issues with `nextTarget`. Maybe there's something wrong with the pruning logic where its somehow causing a CQ to be discarded prematurely.

+1 to scrutinizing both this as well as `workloadFits`, which you mentioned earlier. Also worth looking at `findCandidates` Linking to them all here:

1) [nextTarget](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/pkg/scheduler/preemption/fairsharing/ordering.go#L127-L133)
2) [workloadFitsForFairSharing](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/pkg/scheduler/preemption/preemption.go#L494-L498)
3) [findCandidates](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/pkg/scheduler/preemption/preemption.go#L417-L420)

Since the scheduling CQ is within nominal quota and the first strategy is [LessThanOrEqualToFinalShare](https://github.com/kubernetes-sigs/kueue/blob/b5234c619aa542cbaf48dc324a8b06a2856ec826/pkg/scheduler/preemption/fairsharing/strategy.go#L35-L38), I expect [strategy](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/pkg/scheduler/preemption/preemption.go#L329) to always return true.

## Mitigation if any other user experiences similar issue:
For the CQ failing to schedule, set lending limit to 0. This will immediately put the rest of the Cohort in debt. As other workloads in Cohort finish up/are preempted (paying back the debt), this capacity would return to this CQ. This shouldn't result in overadmission: see [this testcase](https://github.com/kubernetes-sigs/kueue/blob/b5234c619aa542cbaf48dc324a8b06a2856ec826/pkg/cache/resource_test.go#L117-L153)

### Comment by [@amy](https://github.com/amy) — 2025-08-15T23:28:06Z

I've augmented our Kueue image *temporarily* with these logs: https://github.com/kubernetes-sigs/kueue/pull/6593
Please take a look and let me know if I missed any areas that need logging coverage. Feel free to directly make a PR against https://github.com/amy/kueue/tree/v0.12.2-kueueteam with suggestions 🙏

We're hoping to catch the guarantee violation again in action & use these augmented logs to narrow down the code areas.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-08-18T19:23:00Z

I'm not entirely sure but is it possible that the [DRS calculation](https://github.com/kubernetes-sigs/kueue/blob/7aae396d525f000e907adfb521f34801fc3e2032/pkg/cache/fair_sharing.go#L49-L86) could be wrong in some cases?

In this line:
`ratio := b * 1000 / lr`
the ratio can be 0 (due to rounding) if some CQ is only borrowing 1 unit of quota and `lr > 1000` (`lr` is the total amount of resource in the cohort and `b` is the amount borrowed by the CQ). This means that in such a large cohort any CQ can borrow 1 GPU and get `DRS = 0`.

Now, when iterating over the candidates we [prune CQs with DRS = 0](https://github.com/kubernetes-sigs/kueue/blob/7aae396d525f000e907adfb521f34801fc3e2032/pkg/scheduler/preemption/fairsharing/ordering.go#L144) so (perhaps) this is why some valid candidates are not considered for preemption. 

If we can't find sufficiently many candidates for preemption that would allow to fit the workload we get `fits = false`.

I'm going to try to reproduce this scenario in a test and check my hypothesis.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-18T20:39:53Z

> I'm not entirely sure but is it possible that the [DRS calculation](https://github.com/kubernetes-sigs/kueue/blob/7aae396d525f000e907adfb521f34801fc3e2032/pkg/cache/fair_sharing.go#L49-L86) could be wrong in some cases?
> 
> In this line: `ratio := b * 1000 / lr` the ratio can be 0 (due to rounding) if some CQ is only borrowing 1 unit of quota and `lr > 1000` (`lr` is the total amount of resource in the cohort and `b` is the amount borrowed by the CQ). This means that in such a large cohort any CQ can borrow 1 GPU and get `DRS = 0`.
> 
> Now, when iterating over the candidates we [prune CQs with DRS = 0](https://github.com/kubernetes-sigs/kueue/blob/7aae396d525f000e907adfb521f34801fc3e2032/pkg/scheduler/preemption/fairsharing/ordering.go#L144) so (perhaps) this is why some valid candidates are not considered for preemption.
> 
> If we can't find sufficiently many candidates for preemption that would allow to fit the workload we get `fits = false`.
> 
> I'm going to try to reproduce this scenario in a test and check my hypothesis.

That's a good point. 
I think that weird fair sharing could be caused by (1 the unbalanced borrowing usage between resources (e.g., borrowing a lot of CPUs, but GPUs are accommodated within the nominal quota), OR (2 there is a CQ that has a large lendable resource (e.g., global-default) and others have a small lendable resource.

In the case of (1, the CPU dws is respected than the GPU dws, then the cq will be disadvantaged across the cohort based on CPU borrowing usage.
In the case of (2, the non-global-default cq dws could be rounded down to 0 (as @pajakd mentioned) due to subtree lendable resource (including global-default cq) being large, then the non-global-default cq dws could be pruned.

NOTE: When Kueue calculates the lendable resources, it does not consider the current usage. So, in the large cluster, the lendable resources could be technically large numbers due to the large nominal quota across all cq and cohort.
The proper borrowing limit could mitigate this large number of lendable resource since the borrowing limit is considered when Kueue calculates lendable resources.

### Comment by [@amy](https://github.com/amy) — 2025-08-18T20:57:25Z

I've added this logging into fairsharing.go. Will use this logging image in production tomorrow:
```
			ratio := b * 1000 / lr

			// Log when ratio is 0 due to rounding (b < lr/1000)
			if ratio == 0 && b > 0 {
				logger.Info("DRS ratio calculation resulted in 0 due to rounding",
					"resource", rName,
					"borrowed", b,
					"lendable", lr,
					"threshold", lr/1000,
					"actualRatio", 1000.0*float64(b)/float64(lr))
			}
```

and 

```
dws := drs * 1000 / node.fairWeight().MilliValue()
	if dws == 0 && drs > 0 {
		logger.Info("DWS ratio calculation resulted in 0 due to rounding",
			"drs", drs,
			"fairsharingWeight", node.fairWeight().MilliValue(),
			"actualRatio", 1000.0*float64(drs)/float64(node.fairWeight().MilliValue()))
	}
```

For this latter log, even if your CQ is borrowing a lot of GPUs, if it has a high CQ weight, it can still result in a scenario where you're rounding down to `DRS=0`

### Comment by [@pajakd](https://github.com/pajakd) — 2025-08-19T08:10:11Z

> if it has a high CQ weight, it can still result in a scenario where you're rounding down to `DRS=0`

Yes, large weights aggravate the rounding problem and this is the main reason of the problem. With weights it can happen that even a large amount of quota cannot be reclaimed.

I would expect this test to pass (can be added to `integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go`). But instead when I run it, the reclamation does not happen and I can observe familiar log lines `Workload requires preemption, but there are no candidate workloads allowed for preemption`.

```	
ginkgo.When("Preemption is enabled in fairsharing and there are large values of weight and quota", func() {
		var (
			cqA *kueue.ClusterQueue
			cqB *kueue.ClusterQueue
		)
		ginkgo.BeforeEach(func() {
			cqA = createQueue(testing.MakeClusterQueue("a").
				Cohort("all").FairWeight(resource.MustParse("300")).
				ResourceGroup(
					*testing.MakeFlavorQuotas("default").Resource(corev1.ResourceCPU, "600").Obj(),
				).Preemption(kueue.ClusterQueuePreemption{
				ReclaimWithinCohort: kueue.PreemptionPolicyAny,
				WithinClusterQueue:  kueue.PreemptionPolicyLowerPriority,
			}).Obj())

			cqB = createQueue(testing.MakeClusterQueue("b").
				Cohort("all").FairWeight(resource.MustParse("300")).
				ResourceGroup(
					*testing.MakeFlavorQuotas("default").Resource(corev1.ResourceCPU, "600").Obj(),
				).Preemption(kueue.ClusterQueuePreemption{
				ReclaimWithinCohort: kueue.PreemptionPolicyAny,
				WithinClusterQueue:  kueue.PreemptionPolicyLowerPriority,
			}).Obj())
		})

		ginkgo.It("Queue can reclaim its nominal quota", framework.SlowSpec, func() {
			ginkgo.By("Adding so many workloads in cqA that it borrows some quota from cqB")
			for range 10 {
				createWorkload("a", "100")
			}
			util.ExpectReservingActiveWorkloadsMetric(cqA, 10)
			ginkgo.By("Creating newer workload in cqB that needs only nominal quota")
			createWorkload("b", "500")
			ginkgo.By("Evict the some workloads in cqA and reclaim the nominal quota in cqB")
			util.FinishEvictionOfWorkloadsInCQ(ctx, k8sClient, cqA, 3)
			util.ExpectReservingActiveWorkloadsMetric(cqA, 7)
			util.ExpectReservingActiveWorkloadsMetric(cqB, 1)
		})
	})
```

EDIT: Changing the weights to resource.MustParse("1") makes the test pass.

### Comment by [@amy](https://github.com/amy) — 2025-08-19T12:04:53Z

@pajakd nice work! And based off offline preliminary evidence. Theory seems promising. (We did find some incorrect DRS=0 values in tournament logs for candidate CRs that were clearly borrowing at the time. Need to wait for recurrence of bug to find how often this happens.)

Will update the thread if we catch the logs above during recurrence in prod.
