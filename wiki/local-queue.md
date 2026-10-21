# LocalQueue

**Summary**: A LocalQueue (LQ) is a namespaced resource that points to exactly one [[cluster-queue]]. Tenants reference LocalQueues from their jobs via the `kueue.x-k8s.io/queue-name` label; the LQ is what enforces namespace-to-ClusterQueue binding.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-13481.md, pr-13433.md, pr-13621.md, pr-12786.md

**Last updated**: 2026-10-21

---

## Why LocalQueue exists separately

ClusterQueues are cluster-scoped and platform-owned. Jobs, however, live in namespaces that tenants own. LocalQueue is the bridge: a platform admin creates a CQ, then creates one or more LQs in tenant namespaces pointing to that CQ. Tenants never need to know the CQ name — they reference their LQ.

This also means a single CQ can be reached from many namespaces (one LQ per namespace), which is how shared quota across multiple teams is expressed.

## Defaulting and the `kueue.x-k8s.io/queue-name` label

Jobs opt into Kueue by carrying `kueue.x-k8s.io/queue-name: <local-queue-name>`. If the label is absent, integration controllers ignore the job — it runs normally, outside any Kueue gating. This opt-in design is intentional: non-participating jobs on the cluster keep working.

KEP-2936 ([[feature-gates]] `LocalQueueDefaulting`) added a per-namespace default LocalQueue so that jobs without the label can still be gated ([[pr-3652]], [[issue-9633]]). When enabled and a LocalQueue named `default` exists in the namespace, jobs without the label get admitted through it.

## Status: summary of the CQ

Recent versions added per-LQ status fields that mirror the CQ (pending/admitted counts, usage, fair-share weight) so tenants can query their own LQ without needing RBAC on the cluster-scoped CQ ([[pr-10145]]). Before this, observability was limited for non-admins.

## Visibility

Pending-workload visibility is per-LQ (and per-[[cohort]]) and served by the [[visibility-api]] aggregated-API extension.

## Typical use pattern

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: team-ml
  name: team-ml-gpu
spec:
  clusterQueue: shared-gpu-pool
```

Then:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  namespace: team-ml
  labels:
    kueue.x-k8s.io/queue-name: team-ml-gpu
# ...
```

## Moving a LocalQueue to another ClusterQueue

Retargeting a LocalQueue's `spec.clusterQueue` used to leave the **previous** ClusterQueue counting the moved Workloads as pending. The inflight cleanup now happens inside `Manager.RequeueWorkload`, before `info.Update` clears the source ClusterQueue, which fixes both the retarget path and the `requeueAndUpdate` path ([[pr-13885]]). See [[scheduler-internals#Popped heads must survive a snapshot failure]].

## LocalQueue identity is `namespace/name`

LocalQueue names are namespace-scoped, so `spec.queueName` alone is **not** an identity. Comparing Workloads by `spec.queueName` made `team-a/default` and `team-b/default` indistinguishable and broke admission fair-sharing preemption ordering; the comparison must use the namespace-qualified key (`utilqueue.KeyFromWorkload`) — [[pr-14547]], see [[admission-fair-sharing#LocalQueue identity is namespace-qualified]].

## `fairSharing.weight` on a LocalQueue (Admission Fair Sharing)

With [[admission-fair-sharing]], pending Workloads in a ClusterQueue are ordered by LocalQueue usage divided by `spec.fairSharing.weight` (default 1). Validation accepts `0`; since pr-13481 (v0.20.0, backported to 0.19/0.18) a weight `<= 0` gives usage `+Inf`, so the LocalQueue is served **last**. Before, an idle zero-weight LocalQueue computed `0/0 = NaN`, which sorted first. Weights are read from a per-ClusterQueue cache in the queue manager (`lqWeights`, default `1.0` for an unknown LocalQueue), not from the API at sort time ([[fair-sharing#LocalQueue weight lookup: one cached path for heap and snapshot (AFS ordering)]]).

Other AFS accounting fixes that show up in LocalQueue `status.fairSharing` (`admissionFairSharingStatus.consumedResources`): sub-milli CPU/GPU contributions are no longer truncated to 0 (pr-13621), and Workloads admitted via AdmissionChecks no longer keep their entry penalty forever (pr-12786). Both can change observed ordering after an upgrade ([[admission-fair-sharing#Sub-milli usage is no longer truncated (pr-13621)]]).

## Related pages

- [[cluster-queue]] — the quota pool the LQ points to.
- [[workload]] — what gets created when an LQ-bound job is submitted.
- [[feature-gates]] — `LocalQueueDefaulting` lifecycle.
- [[visibility-api]] — how tenants query pending workloads.
- [[admission-fair-sharing]] — LocalQueue usage-based ordering.
