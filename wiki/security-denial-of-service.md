# Security — Denial of Service

**Summary**: DoS vulnerability patterns drawn from 100 DoS-class CVEs in `raw/cve/`. The highest-relevance category for Kueue because the scheduler, webhooks, and reconcilers all process untrusted CR input on a hot path.

**Sources**: `raw/cve/` — 100 entries with `Category: Denial of Service`, including representative cases `CVE-2019-11253.md` (Kubernetes API server YAML/JSON CPU exhaustion), `CVE-2020-8552.md` (API server resource exhaustion via valid requests), `CVE-2020-8569.md` (CSI snapshot-controller nil-pointer crash loop), `CVE-2020-8557.md` (kubelet `/etc/hosts` disk exhaustion), `CVE-2022-39272.md` (Flux `.spec.interval` halts kind-wide reconciliation), `CVE-2022-31016.md` (Argo CD); 2026-09 additions `CVE-2026-53716.md`, `CVE-2026-53717.md`, `CVE-2026-53719.md`, `CVE-2026-54247.md`, `CVE-2026-61794.md`; 2026-10 additions `CVE-2026-95838.md`, `CVE-2026-107446.md`.

**Last updated**: 2026-10-21

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

10 of the 94 DoS CVEs. Pattern: a reconciler dereferences a field that's optional in the schema but assumed present. CVE-2020-8569 (snapshot-controller) is the canonical case — the controller crashed on a `VolumeSnapshot` referencing a non-existent PVC and entered a crash loop because the same object kept being reprocessed.

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

## Admin-writable regex compiled with `MustCompile`

`CVE-2026-65834` (Capsule, CWE-20/248): `CapsuleConfiguration.Spec.NodeMetadata.ForbiddenLabels.Regex` was not validated by the configuration admission webhook, so a malformed pattern was stored and later reached `regexp.MustCompile` inside the **node admission webhook**, crashing it on every Node create, update or patch. One bad config string took out a cluster-wide admission path.

Kueue equivalents to check: any pattern or selector that arrives from the Configuration file or from a CR and is compiled or parsed inside a webhook handler — `managedJobsNamespaceSelector`, `integrations.podOptions.namespaceSelector`, label selectors on ResourceFlavor node matching. Validate at the point the value is **accepted**, not at the point it is used, and never `MustCompile` a value that crossed a trust boundary. Also relevant to [[webhooks]]: a panic in a webhook handler is a cluster-wide DoS, not a single-request failure.

## 2026-09 additions: size and lifetime bounds on tenant-supplied artifacts

Most new DoS entries are **operators fetching or parsing something a tenant points them at**, with the size trusted from the artifact itself. None is a Kueue CVE.

| CVE | Product / versions | CWE, CVSS | Mechanism | Kueue rule |
| --- | --- | --- | --- | --- |
| CVE-2026-53716 | Envoy Gateway < 1.7.4 / 1.8.1 | CWE-789, 6.5 | `io.ReadAll` on a `gzip.Reader` with no cap on decompressed output; the 256 MiB limit applies only to compressed input (source: CVE-2026-53716.md) | wrap decompressors in `io.LimitReader` **after** decompression |
| CVE-2026-53717 | Envoy Gateway, same | CWE-789, 6.5 | tar-header `h.Size` used to allocate before the entry name or size is validated; a small PAX/GNU header claims terabytes (source: CVE-2026-53717.md) | never `make([]byte, hdr.Size)`; validate against a cap first |
| CVE-2026-50125 | MKP (MCP server for Kubernetes) < 0.4.1 | CWE-400, 7.5 | unauthenticated `get_resource` tool with unbounded `limitBytes`/`tailLines`, log stream copied into an in-memory buffer (source: CVE-2026-50125.md) | cap every user-controlled numeric that sizes a read |
| CVE-2026-54247 | Skipper < 0.26.22 | CWE-770, 4.3 | `io.ReadAll(r.Body)` in the admission handler with no limit (source: CVE-2026-54247.md) | wrap webhook bodies in `http.MaxBytesReader` (see [[webhooks]]) |
| CVE-2026-53493 | containerd < 1.7.36 / 2.0.13 / 2.2.9 / 2.3.6 / 2.4.1 | CWE-400/770/834 | crafted OCI index graph forces high CPU and memory during `PullImage` (source: CVE-2026-53493.md) | bound graph depth and node count of any recursive structure |
| CVE-2026-53495 | containerd < 1.7.35 / 2.0.12 / 2.2.8 / 2.3.5 | CWE-400 | CRI `ExecSync` drain goroutine has no timeout and ignores context cancellation when a background child holds stdio pipes (source: CVE-2026-53495.md) | every blocking drain or copy needs a deadline and must select on `ctx.Done()` |
| CVE-2026-53715 | Envoy Gateway | CWE-362, 5.3 | plain map read in `ServeHTTP` while `Get` writes it during policy translation; concurrent map access aborts the process (source: CVE-2026-53715.md) | shared caches touched by an HTTP handler and a reconciler need a mutex or `sync.Map` |
| CVE-2026-44778, CVE-2026-53941 | Inspektor Gadget 0.27/0.28 - 0.53.1 | CWE-20 / CWE-770, no CVSS | privileged process trusts sizes in ELF `.note.stapsdt` and `ld.so.cache` from an unprivileged container: `DescSize` and `EntryCount` unchecked, length arithmetic overflow (source: CVE-2026-44778.md, CVE-2026-53941.md) | validate length fields from untrusted binary formats before allocation or loops |

**A nil dereference that survives `recover()`.** CVE-2026-53719 (Envoy Gateway, CWE-476, 6.5): `translateSecurityPolicyForRoute` dereferenced an omitted `spec.authorization` for a `SecurityPolicy` targeting a `TCPRoute`. The panic recovery kept the process alive but unwound the runner, and because the object is persistent it re-panicked on every reconcile (source: CVE-2026-53719.md). Rule: a `recover()` in a reconcile wrapper turns a crash loop into a silent stall of the whole runner; the only fix is to validate the optional field, and "poison object" tests should create a minimal CR with every optional field omitted.

**Validating the wrong side of an update.** Three Capsule entries all end in `regexp.MustCompile` panicking an admission path (source: CVE-2026-61794.md, CVE-2026-61795.md; earlier `CVE-2026-65834` above):

- CVE-2026-61794 (CWE-20, 6.8, 0.13.0-0.13.7): the Tenant update check compiled `ForbiddenLabels.Regex` for both labels and annotations, so a malformed `ForbiddenAnnotations.Regex` was never validated.
- CVE-2026-61795 (CWE-697, 6.8): `hostnameRegexHandler.OnUpdate` had `new` and `old` swapped and validated the previous value.

Rule: a validating webhook's `ValidateUpdate(old, new)` must be tested with a valid old and an invalid new value in each field, and copy-pasted validators must be checked for the *field name* they read. Both bugs need admin write access (`PR:H`), so they are availability bugs rather than tenant escalations, but the blast radius was every namespace or Ingress create.

**Access-point ownership in a CSI driver.** CVE-2026-85781 (Amazon EFS CSI Driver < 3.4.1, CWE-283, 8.7): volume deletion did not verify that the access point belonged to the filesystem in a user-created PersistentVolume `volumeHandle`, allowing recursive deletion of directories on an unauthorised filesystem (source: CVE-2026-85781.md). Rule: a destructive action driven by an identifier in a tenant-writable object must resolve and verify ownership of *both* halves of a compound key.

## 2026-10 additions

Only two runtime entries are DoS-shaped, and neither affects Kueue ([[security#2026-10 wave: what the 26 new CVEs add]]):

- **containerd < 1.7.35 / 2.0.12 / 2.2.8 / 2.3.5, CVE-2026-95838** (CWE-400/407): the layer unpack handler re-traversed directories for some opaque-whiteout configurations. A malicious layer burned CPU, delayed container start and cut image-pull concurrency for unrelated deployments (source: CVE-2026-95838.md). This is an algorithmic-complexity bug (CWE-407): each step was bounded, but the *number of repetitions* scaled with attacker input. The Kueue analogue is any per-cycle loop in [[scheduler-internals]] or [[preemption]] that re-walks a cohort tree or the Workload list for each candidate. Reviewers ask for the complexity in the number of Workloads, flavors and cohort depth, not only for bounded inputs.
- **containerd overlaybd <= 1.0.18, CVE-2026-107446** (CWE-190): integer overflow in a length field from an untrusted blob, then an out-of-bounds heap access (source: CVE-2026-107446.md). Same rule as the ELF `DescSize` row above: check length arithmetic for overflow before allocating.

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[scheduler-internals]]
- [[webhooks]]
- [[cluster-queue]]
- [[borrowing-and-lending]]
- [[performance-and-scale]]
