# Preemption Cost (Priority Boost)

**Summary**: External controllers can set the `kueue.x-k8s.io/priority-boost` annotation on a Workload to dynamically adjust its effective scheduling priority, influencing both admission ordering and preemption candidate selection within a ClusterQueue.

**Sources**: `raw/kueue/keps/7990-preemption-cost/README.md`, `raw/kueue/keps/7990-preemption-cost/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gate `WorkloadPriorityBoost`, disabled by default. (source: keps/7990-preemption-cost/kep.yaml)

## Motivation

Kueue's preemption decisions are based on static priority classes, fair-share weights, and recency. They have no mechanism to incorporate runtime signals like:
- A workload has been preempted many times and is starving.
- A workload is mid-epoch (expensive to interrupt vs. one that is still initializing).
- A workload holds a checkpoint and can restart cheaply.

(source: keps/7990-preemption-cost/README.md)

## The annotation

```yaml
metadata:
  annotations:
    kueue.x-k8s.io/priority-boost: "150"   # signed integer; negative values lower priority
```

The annotation is set on the **Workload** object by an external controller — not on the job. This prevents batch users from self-serving priority increases. (source: keps/7990-preemption-cost/README.md)

## Effective priority

```
effectivePriority = workload.priority + priorityBoost
```

Kueue uses `effectivePriority` everywhere it currently uses `workload.priority` within a [[cluster-queue]], including:
- Scheduling order (higher effective priority → scheduled first).
- Preemption candidate selection (`LowerPriority`, `LowerOrNewerEqualPriority` policies use effective priority).

The boost **can cross priority class boundaries**. A `low` (100) workload with boost `150` has effective priority 250, placing it between `mid` (200) and `high` (300). (source: keps/7990-preemption-cost/README.md)

## Validation

Invalid or non-integer values cause the Workload create/update to be rejected by the webhook. (source: keps/7990-preemption-cost/README.md)

## RBAC

Only trusted external controllers should have `patch` access to `workloads.kueue.x-k8s.io`. Batch users who submit jobs do not get RBAC to patch Workloads in typical deployments. (source: keps/7990-preemption-cost/README.md)

## Reference controller pattern

The KEP ships with a reference external controller that computes boost using a bounded heuristic:

- Starts at 0.
- Increments the boost after every N preemptions (threshold-based to avoid flapping).
- Can factor in job phase (initializing vs. running) or checkpoint status.

Platform teams replace this with organization-specific logic. (source: keps/7990-preemption-cost/README.md)

## Risk: preemption flapping

If two workloads repeatedly preempt each other (A preempts B → B's boost increases → B preempts A → …), the cluster oscillates. Kueue does not impose anti-flapping policies internally; this is the external controller's responsibility. The reference controller uses threshold-based increments to limit oscillation. (source: keps/7990-preemption-cost/README.md)

## Interaction with fair sharing

Priority boost affects scheduling order and preemption eligibility but does **not** affect DRS (Dominant Resource Share) calculations used by [[fair-sharing]]. Fair sharing operates on actual resource usage, not priority. (source: keps/7990-preemption-cost/README.md)

## Related pages

- [[workload-priority]]
- [[preemption]]
- [[fair-sharing]]
- [[cluster-queue]]
- [[workload]]
- [[feature-gates]]
