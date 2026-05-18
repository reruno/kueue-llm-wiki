# Security — Denial of Service

**Summary**: DoS vulnerability patterns drawn from 83 DoS-class CVEs in `raw/cve/`. The highest-relevance category for Kueue because the scheduler, webhooks, and reconcilers all process untrusted CR input on a hot path.

**Sources**: `raw/cve/` — 83 entries with `Category: Denial of Service`, including representative cases `CVE-2019-11253.md` (Kubernetes API server YAML/JSON CPU exhaustion), `CVE-2020-8552.md` (API server resource exhaustion via valid requests), `CVE-2020-8569.md` (CSI snapshot-controller nil-pointer crash loop), `CVE-2020-8557.md` (kubelet `/etc/hosts` disk exhaustion), `CVE-2022-39272.md` (Flux `.spec.interval` halts kind-wide reconciliation), `CVE-2022-31016.md` (Argo CD).

**Last updated**: 2026-05-18

---

## Why this matters for Kueue

DoS is the most realistic class of attack against Kueue today because:

1. **Every tenant can create Workloads.** The unit of input is user-controlled.
2. **Scheduler hot path.** [[scheduler-internals|The 6-phase scheduling cycle]] runs on a single goroutine snapshot per cycle — a crash, panic, or wedge stops scheduling for every queue, not just the offender's.
3. **Webhook in the API-server admission path.** A panic or slow webhook with `failurePolicy: Fail` (the recommended setting; see [[webhooks]]) stops *all* CRUD on the resources it gates.
4. **Reconciler crash loops.** The Flux CVE-2022-39272 pattern — invalid `.spec.interval` halts the entire reconciler — applies to any field Kueue parses without validation in webhook *before* the controller dereferences it.

## Patterns to flag in review

The five core patterns appear in every DoS CVE file in `raw/cve/`:

1. **Unbounded loops iterating over user-supplied input.** Examples in Kueue: iterating `workload.Spec.PodSets[*].Count` (cap is required), iterating ResourceFlavor selectors, walking [[cohort|cohort]] hierarchy without depth cap.
2. **Missing context timeouts (`context.WithTimeout`) on API calls.** Every outbound call from a controller — list, patch, SAR, ProvisioningRequest creation — must inherit a deadline. A blocked call wedges the workqueue worker.
3. **Large allocations proportional to untrusted user input.** Pre-allocating a slice of length `len(spec.X)` where `spec.X` is user-controlled is the canonical anti-pattern. CVE-2019-11253 is the textbook case: nested YAML caused `O(n²)` memory.
4. **Missing `LimitRanger` / `ResourceQuota` enforcement before admit.** Kueue's [[cluster-queue|ClusterQueue]] and [[borrowing-and-lending|borrowing limits]] are a partial substitute — but only for accounted resources. Anything outside the resource list (PV count, secret count, CR object count) is unbounded.
5. **Workloads admitted without CPU/memory limits set.** Kueue admits based on requests, not limits. A workload with requests << limits passes [[admission]] but can consume node capacity beyond quota intent. Document this in [[manage-jobs-selectively]] guidance.

## Specific anti-patterns by CWE

### CWE-400 / CWE-770 — Uncontrolled resource consumption

The dominant pattern (15 + 10 CVEs respectively). In Kueue, the highest-risk locations are:

- **Snapshot construction** in [[cache-architecture|the scheduler cache]] — a tenant who registers many ResourceFlavors or PodSets inflates per-cycle work.
- **Workqueue depth.** No bound on pending Workloads. A tenant who creates 1M Workloads in a namespace they own forces the workqueue past memory limits. The cluster-admin mitigation is `ResourceQuota{count/workloads.kueue.x-k8s.io: N}`; Kueue itself does not enforce this.
- **Webhook payload size.** Default `webhook` admission body is 3 MiB; large CRs can still inflate handler memory. Stream-parse or reject early.

### CWE-476 — Nil-pointer dereference

10 of the 83 DoS CVEs. Pattern: a reconciler dereferences a field that's optional in the schema but assumed present. CVE-2020-8569 (snapshot-controller) is the canonical case — the controller crashed on a `VolumeSnapshot` referencing a non-existent PVC and entered a crash loop because the same object kept being reprocessed.

**In Kueue**, the equivalents are:

- Dereferencing `workload.Status.Admission` before the workload is admitted.
- Dereferencing `cq.Spec.Cohort` when cohort is unset.
- Dereferencing `rf.Spec.NodeLabels` when the ResourceFlavor uses default labels only.

Every such deref must be either schema-guaranteed (CRD `+required`) or guarded.

### CWE-1284 — Improper validation of specified quantity

The Flux CVE-2022-39272 pattern. A reconciler parses `.spec.interval` as a `time.Duration`; if invalid, the parse error propagates and the reconciler keeps re-enqueueing the object. The whole kind stops being processed because the workqueue head can't progress.

**Mitigation in Kueue**: validation belongs in [[webhooks|the validating webhook]], not the reconciler. If a field's parse can fail, reject at admission so a malformed object never reaches the controller. Where validation depends on cluster state (cross-object refs), the controller must record the error in `.status` and ack-without-retry rather than re-enqueue indefinitely.

### CWE-776 — XML entity expansion ("billion laughs")

Listed under CVE-2019-11253. Kueue doesn't parse XML, but the equivalent is **nested YAML/JSON depth**. The Kubernetes API server caps this; webhooks receive already-decoded objects. Still: any *re-parsing* of an embedded YAML string (e.g. a template field) must use the same depth-limited decoder.

## Mitigation pattern in CVE corpus

The mitigation text is shared verbatim across the DoS CVEs:

> Enforce `ResourceQuota` and `LimitRange` objects in every tenant namespace. Add `context.WithTimeout` to all controller-to-API-server calls. Use Kueue's own admission and borrowing limits to cap resource consumption per ClusterQueue. Implement rate limiting on webhook endpoints.

For Kueue-internal mitigations, see the [[security-best-practices|best-practices checklist]].

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[scheduler-internals]]
- [[webhooks]]
- [[cluster-queue]]
- [[borrowing-and-lending]]
- [[performance-and-scale]]
