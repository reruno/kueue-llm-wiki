# Release process

**Summary**: Kueue cuts minor releases on a regular cadence; recent minors are v0.14, v0.15, v0.16, v0.17, v0.18. Patch releases pick fixes into release branches. Release artifacts include container images, a signed manifest bundle, and Helm charts; SLSA attestations are generated for releases.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Branching

Each minor version has a `release-0.X` branch. `main` is the trunk for the next minor. Patch releases go out from the release branch.

Representative release tracking issues:

- v0.4.1 (source: issue-1056.md), v0.4.2 (source: issue-1200.md).
- v0.5.0 (source: issue-1256.md), v0.5.1 (source: issue-1368.md), v0.5.2 (source: issue-1539.md).
- v0.15.8 (source: issue-10054.md), v0.16.5 (source: issue-10053.md), v0.16.6 (source: issue-10476.md), v0.17.1 (source: issue-10477.md).
- v0.18 plan (source: issue-10261.md — "☂️ Release 0.18 plan" umbrella issue).

## Release automation

- **Cherry-pick automation** lifts fixes from main to release branches; "Cherry-picker should copy release notes" (source: issue-1715.md) addressed the release-note-propagation gap.
- **Promotion PR automation** was hardened to always rebase onto latest main (source: issue-10535.md — ensure the promotion PR is created on top of the latest main branch).
- **SLSA attestations** are generated for release artifacts (source: issue-1466.md).
- **Signing** — release artifacts are signed; an early gap was "Release artifacts are not signed" (source: issue-1477.md).
- **OLM listing** — images are packaged for OperatorHub (source: issue-1101.md).
- **Helm chart sync** — webhook configs auto-sync to helm (source: issue-1461.md).

## Kubernetes version support

Kueue supports a rolling window of Kubernetes minor versions (typically the current and previous two). `manager` tests run against multiple kind versions. Kubernetes 1.30 changed scheduling-gate behavior and Kueue had to track (source: issue-2029.md).

## Dependency management

Kueue depends on `cluster-autoscaler/apis` for the ProvisioningRequest types; historically these were sometimes pinned to unreleased commits (source: issue-1194.md, source: issue-1896.md — use a released cluster-autoscaler/apis module). Similar for KubeRay (source: issue-1634.md).

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
