# MultiKueue Orchestrated Preemption

**Summary**: When a high-priority workload is dispatched to multiple worker clusters in a MultiKueue setup, all of them may simultaneously attempt to preempt lower-priority workloads. This KEP introduces preemption gates to serialize those preemption attempts, letting only one worker cluster preempt at a time.

**Sources**: `raw/kueue/keps/8303-multikueue-orchestrated-preemption/README.md`, `raw/kueue/keps/8303-multikueue-orchestrated-preemption/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gate `MultiKueueOrchestratedPreemption`, disabled by default. (source: keps/8303-multikueue-orchestrated-preemption/kep.yaml)

## The problem

In a [[multikueue]] setup, a workload's replicas are dispatched to multiple worker clusters simultaneously. If the workload needs to preempt lower-priority workloads to gain quota, every worker cluster independently decides to preempt — even though the workload will only run on one cluster. All the preempted workloads on the other clusters were needlessly disrupted. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Solution: preemption gates

A new `spec.preemptionGates` field on the [[workload]] object lets the MultiKueue controller mark a replica as "gated" — it can schedule normally but will not execute preemptions until the manager removes the gate.

```yaml
spec:
  preemptionGates:
  - name: kueue.x-k8s.io/multikueue
```

The gate has a `position` (in `status.preemptionGates`): `Closed` = cannot preempt; `Open` = may preempt. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Orchestration flow

1. The MultiKueue controller adds the `kueue.x-k8s.io/multikueue` preemption gate to all replicated workloads.
2. When a worker cluster scheduler tries to preempt but the gate is `Closed`, it sets the `BlockedOnPreemptionGates` condition on the workload replica and does not proceed.
3. The manager-level preemption orchestration controller watches for this condition:
   - If no gate was opened in the last `SingleClusterPreemptionTimeout` (5 min default), it opens the gate for the replica that signaled first (lowest `LastTransitionTime`).
   - After opening a gate, it waits `SingleClusterPreemptionTimeout` before ungating another replica.
4. The ungated worker cluster proceeds with preemption. The workload is admitted on that cluster.
5. The other replicas remain gated and are eventually cleaned up when the workload is placed.

(source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Timeout mechanism

If the ungated preemption fails (worker crashes, pod never starts), the 5-minute `SingleClusterPreemptionTimeout` eventually elapses, and the orchestrator opens the gate for the next waiting replica. This prevents a single failing preemption from blocking all others. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Interaction with FlavorFungibility

The preemption gate does not affect flavor assignment. The scheduler picks a flavor normally; the gate only blocks the preemption step. With `whenCanPreempt: TryNextFlavor`, if another flavor has free quota, the scheduler admits without preempting — the gate is never triggered. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Interaction with queueing strategy

- `BestEffortFIFO`: gated workloads are marked inadmissible; newer/lower-priority workloads can leapfrog them until the gate opens.
- `StrictFIFO`: gated workloads block the entire ClusterQueue queue.

(source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Related pages

- [[multikueue]]
- [[preemption]]
- [[workload]]
- [[queueing-strategy]]
- [[feature-gates]]
- [[admission]]
