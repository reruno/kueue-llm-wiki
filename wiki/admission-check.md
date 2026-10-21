# AdmissionCheck

**Summary**: An AdmissionCheck is a pluggable gate that runs after QuotaReservation and before the Workload is `Admitted`. Checks can gate on capacity (ProvisioningRequest / cluster-autoscaler), dispatch ([[multikueue]]), or any custom condition. A [[cluster-queue]] lists the checks it requires; each must pass for the Workload to proceed.

**Sources**: `raw/github/kubernetes-sigs__kueue/` (this update: pr-16514.md), `raw/kueue/pkg/controller/elasticjobs/elastic_job_ungater.go`.

**Last updated**: 2026-10-21

---

## Shape

`AdmissionCheck` is a cluster-scoped CRD identifying a controller that will supply Ready status per Workload. Key fields:

- `spec.controllerName` — the unique name the owning controller filters on.
- `spec.parameters` — a ref to a controller-specific config object (e.g. `ProvisioningRequestConfig`).

A [[cluster-queue]]'s `spec.admissionChecks` or `spec.admissionCheckStrategy` references AdmissionChecks by name. The strategy variant lets checks apply only to specific ResourceFlavors, so a CQ can gate an `h100` flavor on a ProvisioningRequest while leaving `cpu-on-demand` ungated.

## Built-in check types

- **ProvisioningRequest** — the canonical check. Kueue creates a `ProvisioningRequest` (Cluster Autoscaler API); when `Provisioned=True`, the check passes. Used to gate admission on node availability (e.g. GPU-class nodes). See [[provisioning-request]] for the controller, `ProvisioningRequestConfig`, DWS mode, and tolerations flow-through.
- **MultiKueue** — the check that dispatches a Workload to a worker cluster. See [[multikueue]].

## Check results and retry

Each check writes to `status.admissionChecks[].state` as one of:

- `Pending` — not yet evaluated.
- `Ready` — check passed. If all checks are Ready, Workload is `Admitted`.
- `Retry` — check cannot pass right now; evict the Workload and requeue. Was motivated by "ProvisioningRequest can fail; try again in a different flavor" ([[issue-10660]] — interaction of Retry with PodsReadyTimeout is tricky). Improving the surfaced reason for Retry was tracked in [[issue-10618]].
- `Rejected` — terminal. Workload is deactivated.

## Check-applied updates

A check can populate `Workload.spec.podSetUpdates` with extra labels, annotations, tolerations, or node selectors that must be merged into the job's PodTemplate at unsuspend time. This is how ProvisioningRequest injects node-affinity to the specific provisioned capacity block, and how MultiKueue labels worker-cluster workloads.

**Correction (2026-10-21)**: the updates live in the Workload **status**, at `status.admissionChecks[].podSetUpdates[]` (each entry is keyed by PodSet `name`), not in `spec`. Code reads them from `wl.Status.AdmissionChecks[*].PodSetUpdates` (source: elastic_job_ungater.go; [[topology-aware-scheduling]] NodeHotSwap section). Other consumers besides the unsuspend-time template merge:

- **Elastic Pods created before the template was stamped** get the updates directly from the elastic ungater. Since v0.20.1, *every* annotation and node-selector entry of the matching `PodSetUpdates` is copied, and conflicting values across checks are an error (source: pr-16514.md). See [[elastic-jobs]] and [[provisioning-request]].
- TAS NodeHotSwap and the WAS simulator merge `PodSetUpdates` tolerations and node selectors into the effective PodSpec they evaluate (see [[topology-aware-scheduling]]).

## Per-flavor checks

`admissionCheckStrategy` lets an admin apply a check only to specific ResourceFlavors — e.g. run ProvisioningRequest for an autoscaled flavor but not a pre-provisioned one. See [[provisioning-request]] for the canonical use case.

## A `Rejected` check during an in-flight eviction

`reconcileCheckBasedEviction` bailed out on `IsEvicted` **before** either of its branches, so an AdmissionCheck flipped to `Rejected` while an eviction was already in flight was silently dropped: no `DeactivationTarget`, no event, and the Workload kept `Admitted=True` sitting next to a `Rejected` check.

[[pr-14309]] (fixes #10807; cherry-pick [[pr-14871]]) moves the `IsEvicted` guard **below** the `Rejected` branch so it only protects the `Retry` path:

| Case | Workload state | Before | After |
|---|---|---|---|
| `Rejected` check, evicted | evicting | ignored — nothing written | deactivated + event |
| `Rejected` check, not evicted | — | deactivated + event | unchanged |
| `Retry` check, evicted | evicting | skipped | unchanged — still skipped |

The guard is *moved* rather than deleted because a `Retry` must not evict a Workload that is already being evicted. Rejection is terminal, and `SetDeactivationTarget` writes a condition whose consumer flips `spec.Active=false` independently of `Evicted`; `apimeta.SetStatusCondition` makes repeat reconciles a no-op, so no extra API requests. Easiest to hit under [[multikueue]] — a worker-side eviction flips the MultiKueue check to `Retry`, which evicts the manager Workload and resets every check to `Pending` — but the handling is not MultiKueue-specific.

Follow-up [[pr-14874]] fixed the matching reactivation path for derived `DeactivatedDueTo<Cause>` reasons; see [[workload#Reactivation matches deactivation reasons by prefix]].

## `observedGeneration` on the `Active` condition

An AdmissionCheck reconciler that skips the status write when status/reason/message are unchanged leaves `observedGeneration` stale after a parameter change that happens to preserve the health result. Fixed for the MultiKueue check in [[pr-14838]]; see [[multikueue#AdmissionCheck `observedGeneration` is refreshed on config change]].

## Related pages

- [[admission]] — the two-phase state machine checks live in.
- [[cluster-queue]] — where checks are declared.
- [[provisioning-request]] — the canonical capacity-gating check.
- [[multikueue]] — the canonical multi-cluster dispatch check.
- [[concurrent-admission]] — **[Alpha]** Variant Workloads can run different checks per flavor in parallel.
