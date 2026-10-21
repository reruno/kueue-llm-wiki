# API versions: v1beta1 → v1beta2

**Summary**: Kueue's `kueue.x-k8s.io`, visibility and Configuration APIs moved from `v1beta1` to `v1beta2`. In **v0.20** the `v1beta1` versions stop being **served** (`served: false`) and the v1beta1 conversion support is removed — an action-required upgrade for any client, manifest or GitOps repo still writing v1beta1. On **main (v0.21 dev)** the v1beta1 Go packages and CRD versions are deleted entirely (pr-16485), so every stored object must be at v1beta2 and `status.storedVersions` trimmed before that upgrade.

**Sources**: `raw/github/kubernetes-sigs__kueue/pr-14558.md`, `raw/github/kubernetes-sigs__kueue/pr-14720.md`, `raw/github/kubernetes-sigs__kueue/pr-13224.md`, pr-15913.md, pr-16300.md, pr-16168.md, raw/kueue/config/components/crd/alpha/kustomization.yaml, pr-16485.md, issue-13957.md, pr-16489.md, pr-16984.md, issue-16983.md, pr-15371.md, pr-14445.md, pr-14449.md, raw/kueue/hack/migrate-to-v1beta2.sh, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-17159.md, pr-17528.md, issue-17498.md, pr-17121.md, issue-17120.md, pr-16035.md, raw/kueue/apis/config/v1beta2/configuration_types.go

**Last updated**: 2026-10-21

---

## What changed in v0.20

[[pr-14558]] (part of #13957) sets `served: false` on the **v1beta1** types and resources across CRDs, the runtime schemes, the visibility API, test infrastructure, upgrade workflows, configuration references and documentation. The net diff is `+42 / −9114` across 58 files — it is a removal, not a migration shim.

Concretely:

- **Deprecated `v1beta1` API versions are no longer served.** The API server rejects reads and writes at that version.
- **Deprecated `v1beta1` configuration options and the v1beta1 conversion support are removed.** There is no in-cluster conversion path left to lean on.
- All examples and docs (English and Chinese) reference `v1beta2`.

Individual API changes still landed in *both* versions while v1beta1 existed — e.g. the `PodSet.minCount >= 0` relaxation ([[pr-14720]]) and the `maximumExecutionTimeSeconds` CEL message fix (pr-14449) were applied to v1beta1 and v1beta2. **Correction (2026-10-21)**: `scheduling.quotaReleaseStrategy` ([[pr-13224]]), previously cited here as such an example, was **reverted before v0.20 code freeze** by pr-15371 and never shipped in a release; KEP-10076 moved the design to a per-integration `integrations.frameworkConfigs[].quotaReleaseStrategy`, which is not in the Configuration API at the kueue@8922c563e snapshot (source: pr-15371.md, raw/kueue/apis/config/v1beta2/configuration_types.go) — but new fields are increasingly added to `v1beta2` only, deliberately, to nudge migration (the MultiKueue `incrementalDispatcherConfig.stepSize` field is an earlier example).

## Alpha APIs (`kueue.x-k8s.io/v1alpha1`) added in v0.20

Three cluster-scoped, opt-in CRDs live in `v1alpha1`, are built from `config/components/crd/alpha/` (not installed by default) and are shipped in the Helm chart only when `enableAlphaAPIs: true`:

| Kind (short name) | Purpose | Gate |
|---|---|---|
| `PreemptionConfig` (`preempcfg`) | Configurable preemption rules, referenced from a ClusterQueue annotation ([[configurable-preemptions]]) | `ConfigurablePreemptions` |
| `DynamicQuotaOrchestrator` (`dqo`) | Aggregates provider capacity, writes `status.effectiveQuotas` ([[dynamic-quota-orchestration]]) | `DynamicQuotaOrchestration` |
| `CapacityProvider` (`cp`) | Capacity published by an external controller | `DynamicQuotaOrchestration` |

Alpha means field changes without a deprecation window; for example pr-16168 relaxed the CEL on capacity `resources` from 1-64 to at most 64 entries. Editor/viewer ClusterRoles exist for `PreemptionConfig` (pr-15992); every manager-managed resource must have both roles (`hack/testing/rbac/verify.sh`, pr-16240). API linting (KAL) was extended to v1alpha1 and the existing alpha CRDs were fixed to pass (pr-16300, issue-16272.md), so new alpha fields are held to the same API-lint rules as beta ones. `PreemptionConfigNameAnnotation` on the ClusterQueue is a stop-gap that becomes a field when the API graduates.

**API reference.** Since pr-17528 (fixes issue-17498, merged 2026-10-21 to main and the `website` branch as pr-17539) the generated reference covers the alpha group at `/docs/reference/kueue.v1alpha1/` (`kueue.v1alpha1.md`, entry `kueue` in `hack/genref/config.yaml`, genref v0.28.0). Contributor impact: a PR that changes `apis/kueue/v1alpha1` must regenerate this page, and `make verify` flags a stale one (source: pr-17528.md).

## Action required before upgrading to v0.20

Existing objects stored at `v1beta1` must be rewritten at `v1beta2` **while the conversion webhook is still available** — that is, on your current version, before the upgrade. The project ships a migration script:

```
https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh
```

It triggers a **no-op update** for every existing Kueue object, which forces the API server to pass each one through the conversion webhooks and persist it at the new storage version. Run it and verify cluster stability *before* installing v0.20.

Anything that writes Kueue objects directly also needs updating: Helm values and raw manifests, GitOps repositories, CI fixtures, custom controllers and admission checks, and any client-go/controller-runtime scheme registration that still imports the v1beta1 packages.

## v1beta1 removed entirely on main (pr-16485, v0.21 dev)

Plan from issue-13957: `served: false` in 0.20 ([[pr-14558]]), delete in 0.21. pr-16485 (merged 2026-10-02, `+1 / −52669`, 218 files) deletes `apis/kueue/v1beta1`, `apis/config/v1beta1`, `apis/visibility/v1beta1`, their generated client-go code and the v1beta1 entries of every CRD under `config/components/crd/bases` and the Helm chart. At the snapshot the tree has only `apis/kueue/{v1alpha1,v1beta2}`, `apis/config/v1beta2` and `apis/visibility/v1beta2` (source: pr-16485.md, raw/kueue `git ls-tree`). Release note: "API: Kueue no longer provides the kueue.x-k8s.io/v1beta1 APIs."

**Upgrade gotcha (issue-13957):** a cluster that ever stored v1beta1 still lists `v1beta1` in each CRD's `status.storedVersions`, and the API server refuses a CRD update that removes a version still listed there. So before upgrading to a release without v1beta1 you must (1) rewrite every object at v1beta2 (the script below) and (2) trim `storedVersions` to `["v1beta2"]` — do this while on 0.20, where v1beta1 is still declared but unserved.

Docs: pr-16489 switched every documentation example to `config.kueue.x-k8s.io/v1beta2` (also cherry-picked to the `website` and `release-0.20` branches) and dropped the obsolete `e2e_v1beta1` test label.

## The migration script (`hack/migrate-to-v1beta2.sh`)

The script patches every Kueue object so the API server re-encodes it at the CRD's storage version. Two patch types: `annotate` (default; writes `kueue.x-k8s.io/storage-version=<target>`) and `apiVersion` (no marker; patches everything on every run). Other flags: `--dry-run[=client|server]`, `--namespace-regex`, `--kubectl-get-api-version` (default `v1beta1`; listing at the version most objects are stored at avoids a conversion-webhook call per object, which can time out etcd lists on large clusters), `--downgrade` (needs Kueue v0.15.x) (source: raw/kueue/hack/migrate-to-v1beta2.sh).

pr-16984 (fixes issue-16983, merged 2026-10-09, main) made it usable on large or busy clusters:

| Change | Why |
|---|---|
| **Skips objects already annotated** with the target version (read in the same LIST); `--reannotate` forces a full pass | reruns used to re-patch everything |
| **Batches** up to `--batch-size` names (default 100) per `kubectl annotate`/`patch` call; calls stay sequential | each kubectl process cost about 1 s (start, discovery, exec-credential auth) vs about 50 ms per request |
| **Keeps going** on per-object errors; counts migrated / gone (`NotFound`, deleted after the list, not a failure) / failed; derives and prints failed names (batched webhook denials do not name the object); exits non-zero at the end | the first failure used to stop the kind or namespace, e.g. a ClusterQueue whose existing spec fails the validating webhook on *any* update (`lendingLimit ... must be less than or equal to the nominalQuota`) blocked every rerun |
| **Checks the CRD storage version first** and skips a kind with an error if it is not the target | annotating would otherwise mark unmigrated objects as migrated, and skip-on-rerun would hide them |

**`--resources=LIST`** (pr-17159, main, follow-up to pr-16984): migrate only the listed kinds, given as the plural names the script knows (`cohorts`, `localqueues`, `clusterqueues`, ..., `workloads`). Selected kinds run in the script's usual order whatever the list order, and a repeated name runs once. An empty list, an empty item (`a,,b`), an unknown name, or `--resources` without `=LIST` (which other unknown-flag handling would have ignored, migrating everything) fails during flag parsing with exit 1 before any kubectl call. Unselected kinds make **no** kubectl call, so a wrong storage version on their CRDs does not fail the run. Motivation: on a cluster with about 24K Workloads and 1K other objects, the Workloads pass dominates, and Workloads are often already stored at v1beta2 because every write re-encodes them. The help text warns to check unselected kinds before removing `v1beta1` from `storedVersions` (source: pr-17159.md).

New RBAC need: `get` on `customresourcedefinitions`; without it every kind is skipped with an error. Measured: a server-side dry run over about 5k objects took 8m53s, with 1,829 ClusterQueues patched in about 20 kubectl calls (source: pr-16984.md, issue-16983.md). Practical consequence: objects whose current spec no longer passes validation cannot be migrated by any no-op update; fix them first.

## Config v1beta2 default worth knowing

`clientConnection` defaults to QPS 1000 / Burst 1000 in config v1beta2 (`apis/config/v1beta2/defaults.go`; #15206, v0.20.0) (source: CHANGELOG-0.20.md). See [[performance-and-scale]].

`metrics.accessControlMode` (`Delegated` | `None`) is a new v1beta2 field on main, settable only with the Alpha `MetricsAccessControl` gate (pr-16035). See [[metrics]].

## Annotation reference completeness

`site/data/labels_and_annotations.yaml` (rendered at `/docs/reference/labels_and_annotations/`) was missing two in-tree annotations: `kueue.x-k8s.io/podset-topology-spreading` (TAS topology spreading, see [[topology-aware-scheduling]]) and `kueue.x-k8s.io/workload-allowed-resource-flavors` (Concurrent Admission, see [[concurrent-admission]]). pr-17121 (fixes issue-17120; backports pr-17393, pr-17399, website pr-17508) adds them, sorted by key (source: pr-17121.md).

## Validation messages that name the wrong thing

Two small fixes that matter when you read webhook/CEL errors (backported to 0.20/0.19 as pr-16943/pr-16942):

- `admissionFairSharing.usageSamplingInterval` errors carried the value of `usageHalfLifeTime`, and a negative `resourceWeights` entry reported the whole map; both now report the value at the field path they name (`pkg/config/validation.go`) (source: pr-14445.md).
- The Workload CEL rule on `spec.maximumExecutionTimeSeconds` keys on `Admitted=True` but its message said "while workload quota reserved"; the message is now "maximumExecutionTimeSeconds is immutable while the workload is admitted" — a `QuotaReserved` but not yet `Admitted` Workload may still change it (source: pr-14449.md). See [[workload-max-execution-time]].


## Versioning policy that governs this

The project's rule is that **deprecation and removal happen on version-promotion boundaries, not in place**: a field added in `v1beta2` stays in `v1beta2` until the API graduates, and only then can it be dropped. See [[reviewer-pbundyra]] and [[code-quality]].

## Known cross-version gotcha

CEL validation rules are attached per version, and a rule written for `v1beta1` can fail against a `v1beta2`-stored object — the reported case was `v1beta1 CEL validation fails on v1beta2-stored workloads: no such key: priorityClassSource` ([[issue-10593]]). This class of failure disappears once v1beta1 is unserved, but it is the reason a mixed-version window is worth keeping short. See [[webhooks]].

## Related pages

- [[release-process]] — which release carries the change.
- [[webhooks]] — conversion and CEL validation.
- [[workload]], [[cluster-queue]], [[local-queue]] — the objects being converted.
- [[code-quality]] — the API-versioning bar reviewers enforce.
- [[reviewer-pbundyra]] — the reviewer who owns API-versioning rules.
- [[visibility-api]] — now served only at `v1beta2`.
- [[admission-fair-sharing]] — the AFS config fields whose validation messages were fixed.
