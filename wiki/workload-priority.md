# Workload priority

**Summary**: A [[workload]]'s priority is the integer used by the [[queueing-strategy]] heap and by [[preemption]]. It comes from either a stock `scheduling.k8s.io/PriorityClass` (via the Pod template) or, more commonly for Kueue, a `kueue.x-k8s.io/WorkloadPriorityClass` — the latter decouples "how does this job queue?" from "how does the Pod preempt other Pods on the node?"

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Two priority classes, two concerns

Kubernetes has `PriorityClass` for Pod-level preemption (node-level). Kueue needed a separate concept because job-queueing priority is a different problem from per-node Pod preemption — they answer different questions and may legitimately differ.

`WorkloadPriorityClass` is Kueue's version: cluster-scoped, same shape (name, integer value), but consumed only by Kueue's scheduling loop. A Job labeled `kueue.x-k8s.io/priority-class: <name>` gets that priority. If no label, the integration controller reads the Pod template's `PriorityClassName` and uses the corresponding stock PriorityClass integer.

`spec.priorityClassSource` on the Workload distinguishes the two ([[issue-7342]] — v1beta2 API change for `priorityClassSource`). Metrics also expose `priority_class_source` ([[issue-7291]]).

## Mutability

`priority` as an int32 is mutable. `priorityClassName` / `priorityClassSource` is *not* mutable on an existing Workload ([[issue-2593]] — user asking why). Design reason: changing the source would require re-reading the class at scheduling time, and Kueue prefers to freeze the derived integer at Workload creation so the queue heap is stable.

In-place updates were added for specific cases: the label-based update path ([[issue-5004]] — Update Workload priority based on update of `kueue.x-k8s.io/priority-class` label) and "mutate priority class while running without disruption" ([[issue-7138]]). Deployment-owned Pods have their own nuance ([[issue-5148]]). MultiKueue adds another wrinkle ([[issue-7429]]).

## Defaulting

Without any priority annotation and without a `priorityClassName` on the Pod template, the Workload gets priority `0`. A missing `WorkloadPriorityClass` raises an event ([[issue-3439]]) rather than silently failing.

## Observability

`kueue_admitted_workloads_total{priority_class=...,priority_class_source=...}` and similar labels are on most relevant metrics ([[issue-5989]], [[issue-7291]]). See [[metrics]].

## Related pages

- [[workload]] — where priority is stored.
- [[queueing-strategy]] — how priority affects queue order.
- [[preemption]] — priority determines candidates.
- [[preemption-cost]] — **[Alpha]** dynamic priority adjustment via the `priority-boost` annotation.
