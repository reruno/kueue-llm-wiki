# Release process

**Summary**: Kueue cuts minor releases on a regular cadence; recent minors are v0.14, v0.15, v0.16, v0.17, v0.18. Patch releases pick fixes into release branches. Release artifacts include container images, a signed manifest bundle, and Helm charts; SLSA attestations are generated for releases.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Branching

Each minor version has a `release-0.X` branch. `main` is the trunk for the next minor. Patch releases go out from the release branch.

Representative release tracking issues:

- v0.4.1 ([[issue-1056]]), v0.4.2 ([[issue-1200]]).
- v0.5.0 ([[issue-1256]]), v0.5.1 ([[issue-1368]]), v0.5.2 ([[issue-1539]]).
- v0.15.8 ([[issue-10054]]), v0.16.5 ([[issue-10053]]), v0.16.6 ([[issue-10476]]), v0.17.1 ([[issue-10477]]).
- v0.18 plan ([[issue-10261]] — "☂️ Release 0.18 plan" umbrella issue).

## Release automation

- **Cherry-pick automation** lifts fixes from main to release branches; "Cherry-picker should copy release notes" ([[issue-1715]]) addressed the release-note-propagation gap.
- **Promotion PR automation** was hardened to always rebase onto latest main ([[issue-10535]] — ensure the promotion PR is created on top of the latest main branch).
- **SLSA attestations** are generated for release artifacts ([[issue-1466]]).
- **Signing** — release artifacts are signed; an early gap was "Release artifacts are not signed" ([[issue-1477]]).
- **OLM listing** — images are packaged for OperatorHub ([[issue-1101]]).
- **Helm chart sync** — webhook configs auto-sync to helm ([[issue-1461]]).

## Kubernetes version support

Kueue supports a rolling window of Kubernetes minor versions (typically the current and previous two). `manager` tests run against multiple kind versions. Kubernetes 1.30 changed scheduling-gate behavior and Kueue had to track ([[issue-2029]]).

## Dependency management

Kueue depends on `cluster-autoscaler/apis` for the ProvisioningRequest types; historically these were sometimes pinned to unreleased commits ([[issue-1194]], [[issue-1896]] — use a released cluster-autoscaler/apis module). Similar for KubeRay ([[issue-1634]]).

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
