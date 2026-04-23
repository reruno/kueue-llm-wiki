# Importer

**Summary**: `kueue-importer` is a one-shot tool for onboarding existing workloads into Kueue. Run it against a cluster that has jobs/Pods already running and it creates the corresponding [[workload]]s, wiring them up to the right [[local-queue]]s, so the state is consistent without re-creating jobs.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Why it exists

If you install Kueue on a cluster that already has batch jobs running, the integration controllers will not retroactively create Workloads for jobs that pre-existed. Without a Workload, Kueue can't account for their quota use — so subsequent admissions may over-commit. The importer solves this by reading existing jobs, inferring which LocalQueue they should have belonged to (usually by namespace), and creating matching Workloads in the right state.

## When to use

- **First install** on a populated cluster.
- **Migration** from a pre-Kueue queueing solution (e.g. Volcano, Coscheduling) where you want to hand over admission control without disrupting running jobs.
- **Disaster recovery** if Workload objects were mass-deleted and the underlying jobs still exist.

## Scope

The importer is intentionally non-destructive. It doesn't re-create jobs, doesn't change `.spec.suspend`, doesn't toggle admitted state. It only writes Workload objects that mirror existing jobs. The running jobs appear to Kueue as "admitted" from that point on, contributing to quota usage.

## Caveats

- **Priority inference.** If jobs use stock `PriorityClass`, that carries over. If they use Kueue-specific `WorkloadPriorityClass` labels, the importer picks those up; otherwise priority defaults to 0.
- **Missing LocalQueue.** If a namespace has no LocalQueue, the importer can't decide which CQ owns the workload. Operators need to create LocalQueues first.
- **Integration coverage.** The importer covers batch/v1 Job and a subset of CRDs; uncommon integrations may need manual Workload creation.

## Related pages

- [[workload]] — what gets created.
- [[local-queue]] — what the importer resolves against.
- [[integrations]] — the types the importer knows how to wrap.
