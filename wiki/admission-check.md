# AdmissionCheck

**Summary**: An AdmissionCheck is a pluggable gate that runs after QuotaReservation and before the Workload is `Admitted`. Checks can gate on capacity (ProvisioningRequest / cluster-autoscaler), dispatch ([[multikueue]]), or any custom condition. A [[cluster-queue]] lists the checks it requires; each must pass for the Workload to proceed.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Shape

`AdmissionCheck` is a cluster-scoped CRD identifying a controller that will supply Ready status per Workload. Key fields:

- `spec.controllerName` — the unique name the owning controller filters on.
- `spec.parameters` — a ref to a controller-specific config object (e.g. `ProvisioningRequestConfig`).

A [[cluster-queue]]'s `spec.admissionChecks` or `spec.admissionCheckStrategy` references AdmissionChecks by name. The strategy variant lets checks apply only to specific ResourceFlavors, so a CQ can gate an `h100` flavor on a ProvisioningRequest while leaving `cpu-on-demand` ungated.

## Built-in check types

- **ProvisioningRequest** — the canonical check. Kueue creates a `ProvisioningRequest` object (Cluster Autoscaler API); the autoscaler provisions nodes; when `Provisioned=True` is reported, the check passes. Used to gate admission on node availability, e.g. GPU-class nodes that need to spin up. Tolerations from the [[resource-flavor]] must flow into the PR's PodTemplate (source: issue-2572.md). DWS (Dynamic Workload Scheduler) mode adds support for GPU reservations with deletion semantics (source: issue-2213.md — plain Pod deletion edge case).
- **MultiKueue** — the check that dispatches a Workload to a worker cluster. See [[multikueue]].

## Check results and retry

Each check writes to `status.admissionChecks[].state` as one of:

- `Pending` — not yet evaluated.
- `Ready` — check passed. If all checks are Ready, Workload is `Admitted`.
- `Retry` — check cannot pass right now; evict the Workload and requeue. Was motivated by "ProvisioningRequest can fail; try again in a different flavor" (source: issue-10660.md — interaction of Retry with PodsReadyTimeout is tricky). Retry with `AdmissionCheckRetry` feature gate governs behavior when retrying across flavors (source: issue-10618.md).
- `Rejected` — terminal. Workload is deactivated.

## Check-applied updates

A check can populate `Workload.spec.podSetUpdates` with extra labels, annotations, tolerations, or node selectors that must be merged into the job's PodTemplate at unsuspend time. This is how ProvisioningRequest injects node-affinity to the specific provisioned capacity block, and how MultiKueue labels worker-cluster workloads.

## Per-flavor checks

`admissionCheckStrategy` lets an admin say: "only run the ProvisioningRequest check when this Workload is assigned to flavor X." This is critical when a CQ mixes on-demand (pre-provisioned) and autoscaled flavors — only the autoscaled flavor should gate on a PR.

## Related pages

- [[admission]] — the two-phase state machine checks live in.
- [[cluster-queue]] — where checks are declared.
- [[multikueue]] — the canonical multi-cluster dispatch check.
