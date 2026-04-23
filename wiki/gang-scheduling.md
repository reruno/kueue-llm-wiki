# Gang scheduling

**Summary**: "Gang scheduling" in Kueue means: if a [[workload]] can't get *all* its Pods running within a deadline, tear it down and requeue — rather than leave it partially running and holding quota. The mechanism is `WaitForPodsReady`, an opt-in config gate per ClusterQueue (and globally in the Kueue configuration).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## The problem

All-or-nothing workloads (distributed training, MPI) only make progress once every replica is running. Without gang semantics, `kube-scheduler` may admit a partial set — say 60 of 64 Pods are Pending because 4 nodes worth of GPU capacity is stuck elsewhere. The job holds quota but does no useful work, and other jobs wait.

## WaitForPodsReady

When enabled, after a Workload is admitted (see [[admission]]) Kueue watches the job's Pod readiness. If not every Pod reaches `Ready` within `waitForPodsReady.timeout`, the Workload is **evicted**: Pods deleted, quota released, Workload requeued (per `requeuingStrategy`).

Key configuration fields (global and/or per-CQ):

- `timeout` — deadline for PodsReady.
- `requeuingStrategy.timestamp` — re-queue by creation time or eviction time.
- `requeuingStrategy.backoffBaseSeconds` — exponential backoff base. Default consistency with timeout was debated (source: issue-2215.md).
- `requeuingStrategy.backoffMaxSeconds` — cap on retry backoff (source: issue-2216.md — limit the retry period length).
- `requeuingStrategy.backoffLimit` — after N evictions, deactivate the Workload (source: issue-2174.md — reactivated workload could be immediately re-deactivated).

## When gang eviction fires

The scheduler emits an `Evicted` condition with a PodsReady-specific reason; an event is recorded (though the absence of events was itself a bug — source: issue-2012.md). `status.conditions.Requeued` tracks re-entry into the queue (source: issue-2291.md).

"WaitForPodsReady will requeue after `timeout` if a *replacement* Pod can't schedule" — useful for handling a crashed Pod that can't be rescheduled (source: issue-2732.md).

## Integrations supported

Not every integration supports WaitForPodsReady out of the box. "Adding waitForPodsReady capability for all the jobs kueue supports" tracks the gap (source: issue-2594.md). PyTorchJob-specific gang scheduling on AWS EKS was a recurring ask (source: issue-2796.md, source: issue-2508.md).

For multi-template jobs (JobSet, RayJob), gang means "all PodSets' replicas must reach Ready" — one PodSet finishing its startup doesn't excuse another that's slower.

## Interaction with AdmissionChecks

`waitForPodsReady` timer should probably pause while an [[admission-check]] is still pending — otherwise the timer can expire before the Pods are even unsuspended. This was tracked as "Extend waitForPodsReady config to account for AdmissionChecks" (source: issue-3231.md) and is material for ProvisioningRequest flows where check duration can be large.

## Interaction with TAS

[[topology-aware-scheduling]] adds a twist: if an admitted Workload has `UnhealthyNodes` and needs re-admission but the AdmissionCheck `Retry` path is active, the workload might not get re-evicted as expected (source: issue-10660.md — TAS: admitted workload with UnhealthyNodes is not evicted due to AdmissionCheck Retry or PodsReadyTimeout).

## Related pages

- [[workload]] — the object being evicted.
- [[admission]] — the admission state machine.
- [[admission-check]] — AdmissionChecks and their interaction with the PodsReady timer.
- [[elastic-jobs]] — dynamic Pod-count changes on admitted Workloads.
