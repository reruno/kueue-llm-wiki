# Integration: AppWrapper

**Summary**: AppWrapper (a Project CodeFlare CRD) wraps one or more component objects — Jobs, Deployments, custom CRDs — into a single gated unit. Kueue's AppWrapper integration is the escape hatch for running Kueue-aware gating against job types that don't have a dedicated Kueue integration yet.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16972.md, pr-16973.md

**Last updated**: 2026-10-21

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

## AppWrapper version pin

Kueue v0.18.0 ships against **AppWrapper v1.2.1** ([[pr-10898]]). v1.2.1 is a dependency-only patch over v1.2.0: bumps `go.opentelemetry.io/otel/sdk` to 1.43.0, `google.golang.org/grpc` to 1.79.3, and the Go toolchain to 1.26. No behavior change in the integration itself.

## Queue-name changes are validated on update

These webhooks did not re-run create-time validation on update, so a suspended job could switch `kueue.x-k8s.io/queue-name` to a valid label value that is not a valid LocalQueue name (for example `Bad_Queue`). The job reconciler then failed on every retry. Since #16221 a changed, non-empty value is validated (backports pr-16972 / release-0.20 and pr-16973 / release-0.19; not yet released at the snapshot; fixed in v0.20.2 and v0.19.9 per CHANGELOG at kueue@3bbb8cce4, released after this snapshot). See [[job-framework-interface#Queue-name format is validated on update]] (source: pr-16973.md).

## Related pages

- [[integrations]] — integration mechanics.
- [[multikueue]] — AppWrapper adapter for MultiKueue.
- [[job-framework-interface]]
