# Kueue Wiki — Index

**Summary**: Table of contents for the Kueue knowledge base. Each entry is one link and a one-line blurb.

**Sources**: `raw/github/kubernetes-sigs__kueue/` (scraped issues and PRs from `kubernetes-sigs/kueue`, through 2026-04).

**Last updated**: 2026-04-23

---

## Start here

- [[kueue-overview]] — What Kueue is, who uses it, and the class of problems it solves.
- [[architecture]] — Controllers, scheduler, webhooks, manager, and how they fit together.
- [[feature-gates]] — Feature gate lifecycle and how features graduate from alpha → beta → GA.

## Core API objects

- [[cluster-queue]] — Cluster-scoped quota pool; flavors, resource groups, cohort membership, preemption policy.
- [[local-queue]] — Namespace-scoped handle that binds Workloads to a ClusterQueue.
- [[cohort]] — Group of ClusterQueues that can borrow/lend unused quota; supports hierarchy.
- [[resource-flavor]] — Label/toleration descriptor that differentiates otherwise-equivalent resources (GPU models, spot vs on-demand).
- [[workload]] — Kueue's internal representation of a gated job; the unit that gets admitted, preempted, and counted against quota.

## Admission and scheduling

- [[admission]] — The admission flow: QuotaReservation, AdmissionChecks, and `.spec.suspend` toggling.
- [[admission-check]] — Pluggable gates after quota reservation (ProvisioningRequest, MultiKueue dispatch, custom checks).
- [[provisioning-request]] — Canonical capacity-gating check; creates a Cluster Autoscaler `ProvisioningRequest` per Workload and passes once nodes are provisioned.
- [[queueing-strategy]] — StrictFIFO vs BestEffortFIFO and priority-within-queue behavior.
- [[preemption]] — Within-ClusterQueue, reclaim-within-cohort, and preemption-while-borrowing.
- [[fair-sharing]] — DRF-style sharing of unused quota across a cohort.
- [[borrowing-and-lending]] — Borrowing limits, lending limits, and how cohorts redistribute idle capacity.
- [[workload-priority]] — PriorityClass vs WorkloadPriorityClass, priority-sorting within cohort.
- [[gang-scheduling]] — All-or-nothing admission via WaitForPodsReady and scheduler ordering.
- [[elastic-jobs]] — Dynamic scale-up/scale-down of admitted jobs via WorkloadSlices.

## Advanced scheduling

- [[topology-aware-scheduling]] — Pack pods within a topology domain (rack/block/zone) to reduce cross-node latency.
- [[multikueue]] — Dispatch Workloads across multiple worker clusters from a manager cluster.

## Integrations

- [[integrations]] — Overview of supported job APIs and what "integration" means.
- [[integration-batchjob]] — `batch/v1` Job.
- [[integration-jobset]] — JobSet (the recommended multi-template gang-scheduled primitive).
- [[integration-kubeflow]] — PyTorchJob, TFJob, MPIJob, MXJob, PaddleJob, JAXJob, XGBoostJob.
- [[integration-rayjob]] — RayJob and RayCluster.
- [[integration-leaderworkerset]] — LeaderWorkerSet (LWS).
- [[integration-appwrapper]] — AppWrapper (Project CodeFlare).
- [[integration-argo-workflow]] — Argo Workflows.
- [[integration-plain-pod]] — Plain Pods and PodGroups.

## Operator tooling

- [[kueuectl]] — The `kubectl-kueue` CLI.
- [[visibility-api]] — Pending-workload visibility (per-queue and per-cohort).
- [[metrics]] — Prometheus metrics surface.
- [[dashboard]] — KueueViz web UI.
- [[webhooks]] — Validating and mutating admission webhooks.
- [[importer]] — The `kueue-importer` tool for onboarding existing workloads.

## Lifecycle and performance

- [[release-process]] — Branching, versioning, Kubernetes version support.
- [[performance-and-scale]] — Scalability benchmarks and known bottlenecks.

## Developer workflow

- [[testing]] — Landing page: test pyramid, prerequisites, make targets, CI job map, focus strategies, flake debugging.
- [[testing-integration]] — `envtest`-based integration suites; main/baseline/extended/multikueue variants; writing and labeling tests.
- [[testing-e2e]] — Kind-based e2e; `E2E_MODE=dev` loop; full MultiKueue invocation; per-suite matrix.
- [[testing-performance]] — Scheduler perf benchmarks and TAS perf variant.
