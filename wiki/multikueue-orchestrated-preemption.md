# MultiKueue Orchestrated Preemption

**Summary**: When a high-priority workload is dispatched to multiple worker clusters in a MultiKueue setup, all of them may simultaneously attempt to preempt lower-priority workloads. This KEP introduces preemption gates to serialize those preemption attempts, letting only one worker cluster preempt at a time.

**Sources**: `raw/kueue/keps/8303-multikueue-orchestrated-preemption/README.md`, `raw/kueue/keps/8303-multikueue-orchestrated-preemption/kep.yaml`, pr-16235.md, issue-13966.md, raw/kueue/pkg/controller/admissionchecks/multikueue/workload.go, pr-17157.md, pr-17468.md, pr-17469.md, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/apis/kueue/v1beta2/workload_types.go

**Last updated**: 2026-10-21

---

> **Stage: Beta since v0.20 (enabled by default)** — Feature gate `MultiKueueOrchestratedPreemption`; Alpha (off) in v0.17 through v0.19. Graduated by pr-16235 (tracked in issue-13966.md; a concrete Configuration API for the timeout is planned under issue-9852 and is not merged). (source: raw/kueue/pkg/features/kube_features.go, pr-16235.md)

## The problem

In a [[multikueue]] setup, a workload's replicas are dispatched to multiple worker clusters simultaneously. If the workload needs to preempt lower-priority workloads to gain quota, every worker cluster independently decides to preempt — even though the workload will only run on one cluster. All the preempted workloads on the other clusters were needlessly disrupted. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Solution: preemption gates

A new `spec.preemptionGates` field on the [[workload]] object lets the MultiKueue controller mark a replica as "gated" — it can schedule normally but will not execute preemptions until the manager removes the gate.

```yaml
spec:
  preemptionGates:
  - name: kueue.x-k8s.io/multikueue
```

The gate has a `position` (in `status.preemptionGates[]`, entries `name`, `position`, `lastTransitionTime`): `Closed` = cannot preempt; `Open` = may preempt. **A gate listed in `spec.preemptionGates` with no state in status is closed.** (source: keps/8303-multikueue-orchestrated-preemption/README.md, raw/kueue/apis/kueue/v1beta2/workload_types.go)

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

The timeout is a hard-coded constant, `singleClusterPreemptionTimeout = 5 * time.Minute`, in `pkg/controller/admissionchecks/multikueue/workload.go` (the ConcurrentAdmission controller has its own identical `preemptionTimeout = 5m` for Variants; see [[concurrent-admission]]). Neither is configurable yet.


If the ungated preemption fails (worker crashes, pod never starts), the 5-minute `SingleClusterPreemptionTimeout` eventually elapses, and the orchestrator opens the gate for the next waiting replica. This prevents a single failing preemption from blocking all others. (source: keps/8303-multikueue-orchestrated-preemption/README.md)

## Gate states are written only when a gate opens (pr-17157)

**Regression.** After the gate went Beta/on in v0.20 (pr-16235), every Workload that MultiKueue replicates carries the `kueue.x-k8s.io/multikueue` gate. The worker's Workload controller (`syncPreemptionGateStates`) wrote a `Closed` state for it into `status.preemptionGates`; the scheduler's admission apply, built from its queued copy without that state and sent with the same `kueue-admission` field manager, removed it again; the Workload controller re-added it. That was two extra status writes per replicated Workload, plus the watch events and reconciles they cause; the periodic MultiKueue perf job dropped from about 46 to about 33 workloads/s (source: pr-17157.md).

**Now.** `syncPreemptionGateStates` only **removes** states of gates that are no longer in `spec.preemptionGates`; it never adds a `Closed` state. States are still written when a gate is opened, and eviction still resets existing states to `Closed`. All readers already treat a missing state as closed: the scheduler (`HasClosedPreemptionGate`), MultiKueue orchestration (`workloadToOpenPreemptionGate`) and [[concurrent-admission]] (`HasOpenPreemptionGate`, `latestOpenGateTime`). User-visible effect: `status.preemptionGates` no longer lists `Closed` entries for gates that were never opened. Local benchmark (1,000 Workloads, 3 workers): 99 to 100 workloads/s with the fix versus 86 to 94 on main, matching the gate-disabled run; worker status applies fell from about 3,000 to 1,000 (source: pr-17157.md, raw/kueue/pkg/controller/core/workload_controller.go).

Release note: "MultiKueue: Fixed a regression where `MultiKueueOrchestratedPreemption`, enabled by default since v0.20, added two status writes for every Workload replicated to a worker cluster, reducing MultiKueue admission throughput. `status.preemptionGates` no longer lists a `Closed` state for gates that have not been previously opened; such gates are considered closed by default." Main merged 2026-10-20; backports pr-17468 (0.20) and pr-17469 (0.19, where the gate is still Alpha/off) merged the same day, after v0.20.2 / v0.19.9 (source: pr-17157.md, pr-17468.md, pr-17469.md).

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
