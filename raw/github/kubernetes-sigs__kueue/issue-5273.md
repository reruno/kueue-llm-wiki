# Issue #5273: Respect PodDisruptionBudget

**Summary**: Respect PodDisruptionBudget

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5273

**Last updated**: 2026-02-18T05:38:37Z

---

## Metadata

- **State**: open
- **Author**: [@Gab-Menezes](https://github.com/Gab-Menezes)
- **Created**: 2025-05-17T03:14:36Z
- **Updated**: 2026-02-18T05:38:37Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**: It would be nice for kueue to strictly respect PDBs, or at least be best effort (like the kube scheduler).

**Why is this needed**: Lets say you are running multiple production workloads with kueue and each has it's own priority. During some periods of high demand, low priority workloads can be completely evicted causing downtime.

So in the case where PDBs are respect (or at least best effort) could lead to kueue choosing other workloads in the same priority level. Leading to less degradation.

This feature could have a two modes:
* Best effort: Tries to find another workload in the same priority class or lower with budget to be evicted, if it can't find another workload the PDB will not be honored.
* Strict: Similar to best effort, but if it can find another workload the PDB will be honored and the preemptor would be gated, until one workload is allowed to be disrupted.

The strict version can be accomplished already with two separate workloads (one with high priority and one with the default priority) for the desired resource. In this case you can guarantee that at least the pods in the high priority are not evicted, but this feels clunky (because for example if you are using deployments now you need 2 deployments for the same thing).

**Completion requirements**:
* Support both modes (best effort, strict)

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@Gab-Menezes](https://github.com/Gab-Menezes) — 2025-05-17T09:02:49Z

Now that I think about it, modeling around PDBs might the hard, maybe having a similar alternative for the workload world would be better, in this case a workload disruption budget (wdb).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-15T09:35:50Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-15T11:17:44Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-15T11:19:20Z

In this release cycle, we probably do not have enough capacity to consider this feature. But, the use case sounds reasonable. We could introduce a similar mechanism as the Pod PriorityClass: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#poddisruptionbudget-is-supported-but-not-guaranteed

OTOH, I don't think that we should introduce `strict` mode to avoid bypassing the capacity and priority by users (due to PDB is namespace scoped resource).

### Comment by [@Gab-Menezes](https://github.com/Gab-Menezes) — 2025-08-20T17:34:40Z

I think the strict mode has a very good and clear use and maybe worth considering.

Let's say you are using kueue as a way to manage production pods, but your cluster is running low in resources and you have a deployment workload A and B, you also use HPA.
Each pod from a deployment is considered a separate workload, you as the manager of the cluster would like to at least have 1 or 2 pods from B at all time to serve traffic.

Imagine the scenario where you have 10 cpus as quota, A and B request 1 cpu each. 
The current state is 6 A pods, 4 B pods. A's HPA decide to scale to 10, now all B pods will die, making the B service unavailable.
If we have the strict mode this would be prevented.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T19:03:58Z

> I think the strict mode has a very good and clear use and maybe worth considering.
> 
> Let's say you are using kueue as a way to manage production pods, but your cluster is running low in resources and you have a deployment workload A and B, you also use HPA. Each pod from a deployment is considered a separate workload, you as the manager of the cluster would like to at least have 1 or 2 pods from B at all time to serve traffic.
> 
> Imagine the scenario where you have 10 cpus as quota, A and B request 1 cpu each. The current state is 6 A pods, 4 B pods. A's HPA decide to scale to 10, now all B pods will die, making the B service unavailable. If we have the strict mode this would be prevented.

That means that application developer bypass the quota management which means other users's workload will be preempted by the apprication with strict mode. We never allow them. Application developer should use proper priority for the Deployment.

Additionally, we have Node failure handling mechanism powered by TAS which could be handled by cluster admins. If they want to keep QuotaReservation on Node disruption, they should rely on the TopologyAwareScheduling Node failure handling (`TASFailedNodeReplacement` and `TASFailedNodeReplacementFailFast` FGs).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-19T19:57:15Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T21:08:19Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-17T21:18:11Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-18T05:38:34Z

/remove-lifecycle stale
