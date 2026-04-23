# Integration: AppWrapper

**Summary**: AppWrapper (a Project CodeFlare CRD) wraps one or more component objects — Jobs, Deployments, custom CRDs — into a single gated unit. Kueue's AppWrapper integration is the escape hatch for running Kueue-aware gating against job types that don't have a dedicated Kueue integration yet.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## What it's for

If you want to run an arbitrary workload through Kueue but the underlying CRD doesn't have a first-class Kueue integration (e.g. a bespoke training CRD), wrap it in an AppWrapper. AppWrapper itself is Kueue-aware, so the outer object gets suspended and scheduled; when admitted, the inner components are instantiated.

"Document using AppWrappers to manage unsupported types with Kueue" ([[issue-3975]]) is the explicit marker that this is the intended escape hatch.

## Lifecycle

- AppWrapper suspended until Kueue admits.
- On admission, AppWrapper materializes its components.
- On Workload eviction, components are torn down.

## MultiKueue

"Implement multi-kueue adapter for appwrapper integration" ([[issue-3989]]) — the AppWrapper-specific adapter for dispatching wrapped workloads to worker clusters. Associated flaky E2E tests show the maturity progression ([[issue-4376]], [[issue-4378]], [[issue-4477]], [[issue-8970]], [[issue-9608]]).

## TAS

AppWrapper + TAS ([[issue-4495]] — Flaky test: TopologyAwareScheduling for AppWrapper when Creating an AppWrapper Should place pods) is supported but shares topology assignment through the inner components.

## Value validation quirk

"workload.codeflare.dev/appwrapper unsupported value" ([[issue-4215]]) — label-value validation specifics that the integration needed to accept.

## Integration list inclusion

"Add AppWrapper to the lists of integrations consistently" ([[issue-4024]]) — a meta-issue ensuring the integration appears in every documented integration list.

## Related pages

- [[integrations]] — integration mechanics.
- [[multikueue]] — AppWrapper adapter for MultiKueue.
