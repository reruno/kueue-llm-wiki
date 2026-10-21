# ProvisioningRequest

**Summary**: ProvisioningRequest is the canonical [[admission-check]] that gates admission on node availability. Kueue creates a `ProvisioningRequest` (Cluster Autoscaler API) per Workload; when the autoscaler reports `Provisioned=True`, the check passes and the Workload can be admitted. It is how Kueue interoperates with cluster autoscalers to acquire GPU-class (or otherwise scarce) capacity just-in-time instead of forcing those nodes to sit idle.

**Sources**: `raw/github/kubernetes-sigs__kueue/` (cited inline; this update: pr-16514.md, pr-16543.md), `raw/kueue/pkg/controller/elasticjobs/elastic_job_ungater.go`.

**Last updated**: 2026-10-21

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

More broadly, a check can populate `status.admissionChecks[].podSetUpdates` (correction 2026-10-21: earlier text said `Workload.spec.podSetUpdates`; the field is on `AdmissionCheckState` in the status, source: apis/kueue/v1beta2/workload_types.go) with labels, annotations, tolerations, or node selectors that are merged into the Job's PodTemplate at unsuspend time; ProvisioningRequest uses this mechanism to inject node-affinity pointing at the specific provisioned capacity block.

## DWS (Dynamic Workload Scheduler) mode

DWS is a GKE mode (`provisioningClassName: queued-provisioning.gke.io`) that reserves GPU capacity ahead of execution. It interacts with Kueue in subtle ways:

- **Plain Pod deletion edge case** — after the PR is provisioned and Kueue ungates the Pod with the provisioning-specific node selectors/annotations, equivalence checks treated the mutated Pod as "no matching Workload" and deleted it ([[issue-2213]]). The fix was to ignore tolerations and nodeSelector changes in the equivalence check once the Workload is admitted.
- **MPIJob launcher vs workers** — DWS only needs capacity for the GPU worker replicas, not the launcher; `managedResources` in ProvisioningRequestConfig is how this is expressed ([[issue-2260]]).

See [[integration-plain-pod]] and [[integration-kubeflow]] for integration-specific notes.

## Interaction with Retry

If the PR cannot be provisioned, the check sets state `Retry`, which evicts and requeues the Workload so it can try a different flavor or wait. The interaction of `Retry` with `PodsReadyTimeout` is delicate — an admitted workload with `Retry` may not be evicted promptly, leaving it admitted longer than intended ([[issue-10660]]). See the `Retry` state on [[admission-check]].

## PodTemplate contents are enforced by Kueue

The controller computes a deterministic PodTemplate name (`ppt-<workload>-<check>-<attempt>-<podset>`) in the tenant's namespace. It used to reference an already existing PodTemplate at that name **verbatim** in the generated `ProvisioningRequest`, so a user able to write PodTemplates could pre-create one with unrelated resource requests and decouple what Cluster Autoscaler provisions from what Kueue quota-checked. Now the controller is the sole authority on contents (source: pr-13015.md; backports pr-16070.md, pr-16072.md):

- `createPodTemplate` is split into a pure `buildPodTemplate` (deep-copies the PodSet template because `podset.Merge` mutates in place).
- On reconcile: **create** when absent; **skip** when equivalent to the Kueue-derived contents (shared `equality.ComparePodTemplate`, same strategy as Job to Workload); **replace** (delete then create) when a pre-existing object differs. Replace rather than Retry avoids blocking re-admission after preemption when attempt 1 collides with a leftover template from a prior flavor. A recreate racing the still-finalizing delete returns the error and controller-runtime retries with backoff; no admission-check Retry is involved.
- Ownership/label checks are deliberately not the trust boundary, because a tenant who can write PodTemplates can forge them.
- Gated by `EnforceProvisioningPodTemplateContents` (renamed from `RetryProvisioningDueInconsistentPodTemplate` before release). Out of scope: ProvisioningRequest name squatting and post-creation tampering.

## Name truncation and the attempt suffix

`ProvisioningRequestName` hashed the full name including the attempt number while `getAttemptRegex` hashed only the workload+check prefix, so a long name produced two hashes. `matchesWorkloadAndCheck` missed the object, `deleteUnusedProvisioningRequests` deleted it and `syncOwnedProvisionRequest` recreated it in an endless loop. The stable prefix is now truncated first (reserving room for an int32 attempt) and the attempt appended afterwards, keeping the final name within 253 characters; short names like `wl-check-1` are unchanged. Objects named under the old scheme will not match after upgrade (they were already looping) (source: pr-14916.md, backports pr-15466.md, pr-15467.md).

## Elastic jobs

Elastic Jobs with a ProvisioningRequest check rely on per-pod (not per-template) lifetime of the `consume-provisioning-request` / `provisioning-class-name` identity annotations, so GKE's node-selector injection for `queued-provisioning.gke.io` stays scoped to the current request across scale-ups; this is currently implicit in `podset.go` and `elastic_job_ungater.go` ([[issue-14615]], documentation request; source: issue-14615.md).

**Both annotations travel together** (source: pr-16514.md; backport pr-16543, shipped v0.20.1; gate `ElasticJobsViaWorkloadSlicesForProvisioningRequests`, Alpha). Pods created before the job template was stamped, such as those of the first ProvisioningRequest-backed slice in a chain, used to be ungated with `consume-provisioning-request` but **without** `provisioning-class-name`. GKE's provisioning-request mutator warns (`"autoscaling.x-k8s.io/provisioning-class-name" annotation should be populated`) and then applies queued-provisioning semantics anyway. It injects the node selector `autoscaling.gke.io/provisioning-request=<id>`, which is immutable, plus the `cloud.google.com/gke-queued` toleration. With `best-effort-atomic-scale-up.autoscaling.x-k8s.io` and existing capacity (`Provisioned=True`, reason `CapacityIsFound`), no node carries that label. The cluster autoscaler also ignores consume-annotated Pods for normal scale-up, so the Pod stays Unschedulable forever while Kueue reports the Workload admitted. When the class annotation is present, the mutator is class-aware and leaves atomic and check-capacity Pods alone. The elastic ungater's `admissionUpdateForPodSet` now copies **all** `PodSetUpdates` annotations (and node selectors) for the PodSet onto each gated Pod. Only the consume annotation is checked as the Pod's immutable identity. See [[elastic-jobs]].

## Related pages

- [[admission-check]] — the general admission-check framework this check plugs into.
- [[cluster-queue]] — declares the check and (via `admissionCheckStrategy`) per-flavor gating.
- [[resource-flavor]] — source of tolerations/nodeSelectors that must flow into the PR.
- [[integration-plain-pod]] — DWS deletion edge case.
- [[integration-kubeflow]] — MPIJob launcher/workers and ProvisioningRequestConfig.
- [[elastic-jobs]] — ProvisioningRequest-backed workload slices.
- [[feature-gates]] — `AdmissionCheckRetry` and related gates.
