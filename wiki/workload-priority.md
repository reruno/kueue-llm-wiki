# Workload priority

**Summary**: A [[workload]]'s priority is the integer used by the [[queueing-strategy]] heap and by [[preemption]]. It comes from either a stock `scheduling.k8s.io/PriorityClass` (via the Pod template) or, more commonly for Kueue, a `kueue.x-k8s.io/WorkloadPriorityClass` — the latter decouples "how does this job queue?" from "how does the Pod preempt other Pods on the node?"

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

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

## Transitions the API server refuses while quota is reserved

Once a Workload holds a quota reservation, CEL on the Workload CRD makes `priorityClassRef` effectively immutable — no add, no remove, no group/kind change, and no name change for a Pod `PriorityClass`. Kueue skips those writes instead of retrying them forever ([[pr-14565]], fixes [[issue-14482]]); see [[workload#`priorityClassRef` is frozen once quota is reserved]]. The skip is logged at **`V(4)`** — it was `V(2)`, but a reserved Workload can sit in the mismatch state for the entire life of its reservation, so the line repeated on every reconcile at the default verbosity ([[pr-14922]], fixes [[issue-14921]]).

One case in the original report was already covered: #13780's `!HasNoPriority(wl) && !IsWorkloadPriorityClass(wl)` skip means a Workload already on a Pod `PriorityClass` never reaches the write.

## The WorkloadPriorityClass sweep is bounded and cancellable

`WorkloadPriorityClassReconciler.Reconcile` listed every Workload referencing the changed class and wrote them in a plain `for` loop — one `client.Update` at a time, never reading `ctx`, and accumulating one error per failure via `errors.Join`. Since `WorkloadPriorityClassDefaulting` became beta-default in v0.20, a **single** class (the default one) can cover every Workload in the cluster that does not set its own, so the set one reconcile walks is no longer bounded by opt-in.

[[pr-14737]] (fixes #13982) switches the sweep to `pkg/util/parallelize.Until` — the same helper the LeaderWorkerSet reconciler, the Pod controller, the elastic-job ungater and the TAS topology ungater already use. It bounds concurrency to **at most 8 workers**, checks `ctx.Done()` before each item so a cancelled reconcile stops promptly, and returns a **single** error rather than one per item.

Known related bug, still open: restarting the controller can overwrite `.spec.priority` with the WorkloadPriorityClass's priority ([[issue-14698]]).

## Related pages

- [[workload]] — where priority is stored.
- [[queueing-strategy]] — how priority affects queue order.
- [[preemption]] — priority determines candidates.
- [[preemption-cost]] — **[Alpha]** dynamic priority adjustment via the `priority-boost` annotation.
