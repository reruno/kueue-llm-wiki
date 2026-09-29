# Importer

**Summary**: `kueue-importer` is a one-shot tool for onboarding existing workloads into Kueue. Run it against a cluster that has jobs/Pods already running and it creates the corresponding [[workload]]s, wiring them up to the right [[local-queue]]s, so the state is consistent without re-creating jobs.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-29

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

## Mapping rules can match on resource requests

The importer selects Pods by `--namespace` and by queue-mapping rules. Rules matched only on `labels` and `priorityClassName`, so a label covering both GPU and CPU-only Pods could not be split. The rule `match` block now accepts a **`resources`** list: a rule matches when the Pod's total requests contain a **non-zero** amount of **all** listed resources, AND-ed with the `labels`/`priorityClassName` conditions; an absent or empty list matches everything (old mapping files behave as before). Details (source: pr-15573.md; backports pr-15662.md, pr-15663.md):

```yaml
- match:
    labels: {src.lbl: src-val}
    resources: [nvidia.com/gpu]
  toLocalQueue: gpu-queue
- match:
    labels: {src.lbl: src-val}
  skip: true
```

- Rules are evaluated in order, so exclusion uses the existing `skip: true`. Filtered-out Pods count in the `skipped` counter of the check and import summaries.
- Requests are totalled with `resources.NewRequestsFromPodSpec` (init and sidecar containers, pod-level resources and overhead included).
- Only available through `--queuemapping-file`, not the simple `--queuelabel`/`--queuemapping` pair. To match any-of several resources use one rule per resource.
- `Rules.QueueFor` now takes the `*corev1.Pod` so requests are computed once per Pod (`cache.ImportCache.LocalQueue` is the only production caller).

## Other fixes

Flavor assignment in the Pod importer was corrected (backports pr-14579.md, pr-14582.md of #12924), and the importer returns an error when listing Pods fails instead of continuing (source: pr-15596.md, pr-15597.md).

## Related pages

- [[workload]] — what gets created.
- [[local-queue]] — what the importer resolves against.
- [[integrations]] — the types the importer knows how to wrap.
