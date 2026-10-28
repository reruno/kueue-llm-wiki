# Admission

**Summary**: "Admission" is Kueue's term for releasing a [[workload]] to run. It's a two-phase process: first the scheduler reserves quota (`QuotaReserved`), then any configured [[admission-check]]s must return `Ready`, after which the Workload is `Admitted` and the integration controller unsuspends the underlying job.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15371.md, pr-16627.md, pr-17010.md, pr-12786.md, pr-16479.md, pr-16630.md, pr-17041.md, pr-16728.md, pr-17147.md

**Last updated**: 2026-10-28

---

## The two phases

1. **QuotaReservation.** Kueue's scheduler picks a pending Workload from a ClusterQueue's queue (per [[queueing-strategy]]), checks that enough quota is available (nominal + borrowed per [[borrowing-and-lending]]), assigns a [[resource-flavor]] per PodSet, and writes `status.admission`. The condition `QuotaReserved=True` is set. At this point quota is consumed but the job is still suspended.
2. **AdmissionChecks.** If the ClusterQueue declares `spec.admissionChecksStrategy.admissionChecks`, each check observes the Workload and writes a per-check status entry. A check can **Pass** (Workload progresses), **Retry** (Workload is re-evaluated), or **Reject** (terminal; Workload is evicted and deactivated).
3. **Admitted.** Once all checks are `Ready`, the Workload's `Admitted=True` condition is set and the integration controller flips `.spec.suspend: false` on the underlying job (or removes scheduling gates for Pod-level integrations).

If there are no AdmissionChecks, phase 2 is a no-op and `Admitted=True` is set immediately after QuotaReserved.

## State machine

```
created → QuotaReserved → Admitted → (Finished | Evicted)
                           ↑           ↓
                     (checks pass)  (requeue with backoff)
```

Evicted Workloads can be requeued; too many evictions → deactivation ([[issue-2174]]). Deactivated Workloads stay in the API but are ignored by the scheduler until `spec.active` is flipped.

## What the scheduler actually does per cycle

Per scheduling cycle, for each ClusterQueue:

1. Read the head of the CQ's pending queue per [[queueing-strategy]].
2. Compute the assignment: for each PodSet, find the first flavor in each resource group that has enough nominal quota, or can borrow enough from the [[cohort]], or from which a [[preemption]] can free enough capacity.
3. If the assignment works without preemption, admit. The fit check uses exact request totals even past `int64` (pr-16479), so an oversized Workload can no longer slip under a quota it exceeds.
4. If not, gather preemption candidates, mark them `Evicted`, and wait for them to release quota on the next cycle.
5. If still not, either defer to the next cycle (BestEffortFIFO, may attempt another CQ) or block the queue head (StrictFIFO).

The scheduler is single-threaded per binary; this is where scale work focuses. TAS multiplies the per-cycle cost ([[issue-10037]]).

Two consistency guarantees added in October 2026 (main, then release-0.20 after v0.20.2): the first cycle runs only after the cache-filling event handlers have processed their initial lists, so a freshly elected leader no longer admits against a partial view of ClusterQueues, Cohorts and admitted Workloads (pr-16630); and an admission write that the apiserver committed but the client saw fail no longer drops the Workload from the cache (pr-17041). See [[scheduler-internals#Phase 0: wait for the initial cache sync (pr-16630)]] and [[scheduler-internals#Admission write errors keep a committed admission in the cache (pr-17041)]].

## When a Workload cannot be admitted

Common reasons surfaced in events:

- No flavor has enough quota, no preemption can free it, and borrowing is capped.
- The required ResourceFlavor or Topology doesn't exist / isn't labeled on any node.
- An AdmissionCheck is failing (e.g. ProvisioningRequest still pending).
- The ClusterQueue is `stopPolicy: Hold` (or `HoldAndDrain`, which also evicts admitted Workloads; since pr-16728 that includes Workloads whose LocalQueue is held or deleted, [[cluster-queue#Stop policies]]).
- The ClusterQueue is inactive because its Cohort hierarchy has a cycle (`CohortCycleDetected`, [[cohort#Cycles in the Cohort hierarchy]]).
- Preemption is needed but the Workload's preemption gate is closed: `QuotaReserved=False` reason `PreemptionGated` (was `AdmissionGated` before pr-16627; [[preemption#Preemption-gated Workloads report `PreemptionGated` (pr-16627)]]).
- `workload.ValidateAdmissibility` rejected the candidate — most commonly `resources didn't satisfy LimitRange constraints`, i.e. the effective requests violate a namespace LimitRange `max`/`min`. This rejection leaves the requeue reason at `RequeueReasonGeneric` and, under BestEffortFIFO, used not to recover when the LimitRange was relaxed; LimitRange create/update/delete events now retry the namespace's inadmissible Workloads; see [[workload-resource-adjustment]].

With `UnadmittedWorkloadsObservability` (Beta/on in v0.20) each of these is reported as a distinct `QuotaReserved=False` reason (`WaitingForQuota`, `NoMatchingFlavor`, `ExceedsMaxQuota`, `Misconfigured`, `Suspended`, `AdmissionGated`, ...) rather than `Pending`; see [[unadmitted-workloads-observability]].

Events are attached to the Workload for each of these cases. The `Admitted` event's message reports the real wait time since quota reservation (pr-15829), not `0s`. The [[metrics]] surface also exposes pending counts, admission attempts, and preemption counts.

## Wait after quota reservation

Between `QuotaReserved` and `Admitted` a Workload may wait for AdmissionChecks; Admission Fair Sharing counts that reserved usage by default since v0.20 ([[admission-fair-sharing#Accounting anchor: quota reservation, not admission (v0.20, Beta)]]). On 0.18/0.19 (and v0.20 with the anchor gate off) the AFS entry penalty is settled on the transition into `Admitted`, including `QuotaReserved -> Admitted` since pr-12786. After `Admitted`, the [[wait-for-pods-ready]] timers run.

## When quota is released

**Correction (2026-10-21)**: this section said quota release is governed by the Configuration field `scheduling.quotaReleaseStrategy` ([[pr-13224]], KEP-6143). That field was **reverted by pr-15371** before v0.20 and does not exist at this snapshot; a per-integration replacement (`.integrations.frameworkConfigs[].quotaReleaseStrategy`) is designed but not merged. Quota is therefore released per each integration's existing behaviour (for batch/v1 Jobs, when Pods get a `deletionTimestamp`). On eviction, the job reconciler releases the reservation only after the job has no active Pods; a webhook-rejected `reclaimablePods` decrease used to stop it before that step and leave quota reserved forever (fixed by pr-17147, v0.20.2 / v0.19.9; [[workload#`reclaimablePods` must not block eviction (pr-17147, fixes issue-14811)]]). See [[cluster-queue#Configuration: `scheduling.quotaReleaseStrategy` (removed before v0.20)]] (source: pr-15371.md).

## Admission is not the same as "checks passed"

Two conditions that used to be able to disagree, both now fixed:

- An AdmissionCheck flipping to `Rejected` **while an eviction was in flight** was dropped, leaving `Admitted=True` beside a `Rejected` check ([[pr-14309]]). See [[admission-check#A `Rejected` check during an in-flight eviction]].
- A Workload deactivated with a derived `DeactivatedDueTo<Cause>` reason stayed stuck after reactivation because its `Requeued` condition was never transitioned ([[pr-14874]]). See [[workload#Reactivation matches deactivation reasons by prefix]].

## Related pages

- [[admission-check]] — pluggable gates.
- [[queueing-strategy]] — how the scheduler picks the next candidate.
- [[preemption]] — how admission displaces lower-priority workloads.
- [[workload]] — the object whose conditions track this state machine.
- [[workload-resource-adjustment]] — what requests admission actually evaluates, and where they come from.
