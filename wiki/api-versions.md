# API versions: v1beta1 → v1beta2

**Summary**: Kueue's `kueue.x-k8s.io`, visibility and Configuration APIs moved from `v1beta1` to `v1beta2`. In **v0.20** the `v1beta1` versions stop being **served** (`served: false`) and the v1beta1 conversion support is removed — an action-required upgrade for any client, manifest or GitOps repo still writing v1beta1.

**Sources**: `raw/github/kubernetes-sigs__kueue/pr-14558.md`, `raw/github/kubernetes-sigs__kueue/pr-14720.md`, `raw/github/kubernetes-sigs__kueue/pr-13224.md`, pr-15913.md, pr-16300.md, pr-16168.md, raw/kueue/config/components/crd/alpha/kustomization.yaml.

**Last updated**: 2026-09-29

---

## What changed in v0.20

[[pr-14558]] (part of #13957) sets `served: false` on the **v1beta1** types and resources across CRDs, the runtime schemes, the visibility API, test infrastructure, upgrade workflows, configuration references and documentation. The net diff is `+42 / −9114` across 58 files — it is a removal, not a migration shim.

Concretely:

- **Deprecated `v1beta1` API versions are no longer served.** The API server rejects reads and writes at that version.
- **Deprecated `v1beta1` configuration options and the v1beta1 conversion support are removed.** There is no in-cluster conversion path left to lean on.
- All examples and docs (English and Chinese) reference `v1beta2`.

Individual API changes still land in *both* versions while v1beta1 exists — e.g. `scheduling.quotaReleaseStrategy` ([[pr-13224]]) and the `PodSet.minCount >= 0` relaxation ([[pr-14720]]) were applied to v1beta1 and v1beta2 — but new fields are increasingly added to `v1beta2` only, deliberately, to nudge migration (the MultiKueue `incrementalDispatcherConfig.stepSize` field is an earlier example).

## Alpha APIs (`kueue.x-k8s.io/v1alpha1`) added in v0.20

Three cluster-scoped, opt-in CRDs live in `v1alpha1`, are built from `config/components/crd/alpha/` (not installed by default) and are shipped in the Helm chart only when `enableAlphaAPIs: true`:

| Kind (short name) | Purpose | Gate |
|---|---|---|
| `PreemptionConfig` (`preempcfg`) | Configurable preemption rules, referenced from a ClusterQueue annotation ([[configurable-preemptions]]) | `ConfigurablePreemptions` |
| `DynamicQuotaOrchestrator` (`dqo`) | Aggregates provider capacity, writes `status.effectiveQuotas` ([[dynamic-quota-orchestration]]) | `DynamicQuotaOrchestration` |
| `CapacityProvider` (`cp`) | Capacity published by an external controller | `DynamicQuotaOrchestration` |

Alpha means field changes without a deprecation window; for example pr-16168 relaxed the CEL on capacity `resources` from 1-64 to at most 64 entries. Editor/viewer ClusterRoles exist for `PreemptionConfig` (pr-15992); every manager-managed resource must have both roles (`hack/testing/rbac/verify.sh`, pr-16240). API linting (KAL) was extended to v1alpha1 and the existing alpha CRDs were fixed to pass (pr-16300, issue-16272.md), so new alpha fields are held to the same API-lint rules as beta ones. `PreemptionConfigNameAnnotation` on the ClusterQueue is a stop-gap that becomes a field when the API graduates.

## Action required before upgrading to v0.20

Existing objects stored at `v1beta1` must be rewritten at `v1beta2` **while the conversion webhook is still available** — that is, on your current version, before the upgrade. The project ships a migration script:

```
https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/hack/migrate-to-v1beta2.sh
```

It triggers a **no-op update** for every existing Kueue object, which forces the API server to pass each one through the conversion webhooks and persist it at the new storage version. Run it and verify cluster stability *before* installing v0.20.

Anything that writes Kueue objects directly also needs updating: Helm values and raw manifests, GitOps repositories, CI fixtures, custom controllers and admission checks, and any client-go/controller-runtime scheme registration that still imports the v1beta1 packages.

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
