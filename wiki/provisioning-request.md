# ProvisioningRequest

**Summary**: ProvisioningRequest is the canonical [[admission-check]] that gates admission on node availability. Kueue creates a `ProvisioningRequest` (Cluster Autoscaler API) per Workload; when the autoscaler reports `Provisioned=True`, the check passes and the Workload can be admitted. It is how Kueue interoperates with cluster autoscalers to acquire GPU-class (or otherwise scarce) capacity just-in-time instead of forcing those nodes to sit idle.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Controller and API object

Kueue ships a ProvisioningRequest admission-check controller. When a [[cluster-queue]] declares an [[admission-check]] of controller name `kueue.x-k8s.io/provisioning-request`, the controller creates a `ProvisioningRequest` object (from the `autoscaling.x-k8s.io` API group provided by cluster-autoscaler) for each Workload that reaches that check ([[issue-2213]] — illustrates the generated PR shape). The object references a `PodTemplate` built from the Workload's PodSet(s) and names a `provisioningClassName` (e.g. `queued-provisioning.gke.io` for GKE DWS).

The check reads the PR's status and reflects it back into the Workload's `status.admissionChecks[]` entry: `Ready` once `Provisioned=True`, `Retry` on transient failures.

## ProvisioningRequestConfig

`ProvisioningRequestConfig` (a Kueue CRD) is pointed to by the AdmissionCheck's `spec.parameters`. It carries the `provisioningClassName` and the set of `managedResources` the PR should be created for ([[issue-2260]]):

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ProvisioningRequestConfig
metadata:
  name: dws-config
spec:
  provisioningClassName: queued-provisioning.gke.io
  managedResources:
  - nvidia.com/gpu
```

`managedResources` narrows which resources trigger a PR — e.g. for an MPIJob, this avoids creating a PR for the non-GPU launcher replica while still requesting capacity for the GPU workers ([[issue-2260]]).

## Per-flavor gating via `admissionCheckStrategy`

A CQ that mixes pre-provisioned and autoscaled flavors should only gate admission on a PR for the autoscaled flavor. `admissionCheckStrategy` on the [[cluster-queue]] expresses this: it lets an admin say "only run the ProvisioningRequest check when this Workload is assigned to flavor X." Without this, on-demand flavors would incur a pointless autoscaler round-trip.

## Tolerations and nodeSelectors flow-through

Tolerations and nodeSelectors declared on a [[resource-flavor]] must flow into the PR's `PodTemplate`. Otherwise the autoscaler provisions nodes that the resulting Pods cannot schedule onto, and the Job fails ([[issue-2572]]).

More broadly, a check can populate `Workload.spec.podSetUpdates` with labels, annotations, tolerations, or node selectors that are merged into the Job's PodTemplate at unsuspend time; ProvisioningRequest uses this mechanism to inject node-affinity pointing at the specific provisioned capacity block.

## DWS (Dynamic Workload Scheduler) mode

DWS is a GKE mode (`provisioningClassName: queued-provisioning.gke.io`) that reserves GPU capacity ahead of execution. It interacts with Kueue in subtle ways:

- **Plain Pod deletion edge case** — after the PR is provisioned and Kueue ungates the Pod with the provisioning-specific node selectors/annotations, equivalence checks treated the mutated Pod as "no matching Workload" and deleted it ([[issue-2213]]). The fix was to ignore tolerations and nodeSelector changes in the equivalence check once the Workload is admitted.
- **MPIJob launcher vs workers** — DWS only needs capacity for the GPU worker replicas, not the launcher; `managedResources` in ProvisioningRequestConfig is how this is expressed ([[issue-2260]]).

See [[integration-plain-pod]] and [[integration-kubeflow]] for integration-specific notes.

## Interaction with Retry

If the PR cannot be provisioned, the check sets state `Retry`, which evicts and requeues the Workload so it can try a different flavor or wait. The interaction of `Retry` with `PodsReadyTimeout` is delicate — an admitted workload with `Retry` may not be evicted promptly, leaving it admitted longer than intended ([[issue-10660]]). See the `Retry` state on [[admission-check]].

## Related pages

- [[admission-check]] — the general admission-check framework this check plugs into.
- [[cluster-queue]] — declares the check and (via `admissionCheckStrategy`) per-flavor gating.
- [[resource-flavor]] — source of tolerations/nodeSelectors that must flow into the PR.
- [[integration-plain-pod]] — DWS deletion edge case.
- [[integration-kubeflow]] — MPIJob launcher/workers and ProvisioningRequestConfig.
- [[feature-gates]] — `AdmissionCheckRetry` and related gates.
