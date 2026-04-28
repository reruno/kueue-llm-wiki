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

## Per-flavor checks

`admissionCheckStrategy` lets an admin apply a check only to specific ResourceFlavors — e.g. run ProvisioningRequest for an autoscaled flavor but not a pre-provisioned one. See [[provisioning-request]] for the canonical use case.

## Related pages

- [[admission]] — the two-phase state machine checks live in.
- [[cluster-queue]] — where checks are declared.
- [[provisioning-request]] — the canonical capacity-gating check.
- [[multikueue]] — the canonical multi-cluster dispatch check.
- [[concurrent-admission]] — **[Alpha]** Variant Workloads can run different checks per flavor in parallel.
