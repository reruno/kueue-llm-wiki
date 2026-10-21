# Workload priority

**Summary**: A [[workload]]'s priority is the integer used by the [[queueing-strategy]] heap and by [[preemption]]. It comes from either a stock `scheduling.k8s.io/PriorityClass` (via the Pod template) or, more commonly for Kueue, a `kueue.x-k8s.io/WorkloadPriorityClass` — the latter decouples "how does this job queue?" from "how does the Pod preempt other Pods on the node?"

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-13775.md, pr-13719.md, pr-16422.md, pr-14411.md, raw/kueue/pkg/controller/jobframework/reconciler.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-21

---

## Two priority classes, two concerns

Kubernetes has `PriorityClass` for Pod-level preemption (node-level). Kueue needed a separate concept because job-queueing priority is a different problem from per-node Pod preemption — they answer different questions and may legitimately differ.

`WorkloadPriorityClass` is Kueue's version: cluster-scoped, same shape (name, integer value), but consumed only by Kueue's scheduling loop. A Job labeled `kueue.x-k8s.io/priority-class: <name>` gets that priority. If no label, the integration controller reads the Pod template's `PriorityClassName` and uses the corresponding stock PriorityClass integer.

`spec.priorityClassSource` on the Workload distinguishes the two ([[issue-7342]] — v1beta2 API change for `priorityClassSource`). Metrics also expose `priority_class_source` ([[issue-7291]]).

## Mutability

`priority` as an int32 is mutable. `priorityClassName` / `priorityClassSource` is *not* mutable on an existing Workload ([[issue-2593]] — user asking why). Design reason: changing the source would require re-reading the class at scheduling time, and Kueue prefers to freeze the derived integer at Workload creation so the queue heap is stable.

In-place updates were added for specific cases: the label-based update path ([[issue-5004]] — Update Workload priority based on update of `kueue.x-k8s.io/priority-class` label) and "mutate priority class while running without disruption" ([[issue-7138]]). Deployment-owned Pods have their own nuance ([[issue-5148]]). MultiKueue adds another wrinkle ([[issue-7429]]).

## Defaulting

Without any priority annotation and without a `priorityClassName` on the Pod template, the Workload gets priority `0`. A label that names a missing `WorkloadPriorityClass` now produces a Warning event on the job ([[issue-3439]], shipped in v0.20.0; see [[workload-priority#Missing WorkloadPriorityClass: Warning event]]). A Workload stored with a nil `spec.priority`, such as a prebuilt Workload created when no default class existed, is read everywhere through `priority.Priority`, which resolves nil to `constants.DefaultPriority`. The visibility pending-workloads endpoints dereferenced the pointer directly; one such pending Workload made them panic and return 500 for every caller. Fixed in #14411 (source: pr-14411.md).

## Observability

`kueue_admitted_workloads_total{priority_class=...,priority_class_source=...}` and similar labels are on most relevant metrics ([[issue-5989]], [[issue-7291]]). See [[metrics]].

## Transitions the API server refuses while quota is reserved

Once a Workload holds a quota reservation, CEL on the Workload CRD makes `priorityClassRef` effectively immutable — no add, no remove, no group/kind change, and no name change for a Pod `PriorityClass`. Kueue skips those writes instead of retrying them forever ([[pr-14565]], fixes [[issue-14482]]); see [[workload#`priorityClassRef` is frozen once quota is reserved]]. The skip is logged at **`V(4)`** — it was `V(2)`, but a reserved Workload can sit in the mismatch state for the entire life of its reservation, so the line repeated on every reconcile at the default verbosity ([[pr-14922]], fixes [[issue-14921]]).

One case in the original report was already covered: #13780's `!HasNoPriority(wl) && !IsWorkloadPriorityClass(wl)` skip means a Workload already on a Pod `PriorityClass` never reaches the write.

## The WorkloadPriorityClass sweep is bounded and cancellable

`WorkloadPriorityClassReconciler.Reconcile` listed every Workload referencing the changed class and wrote them in a plain `for` loop — one `client.Update` at a time, never reading `ctx`, and accumulating one error per failure via `errors.Join`. Since `WorkloadPriorityClassDefaulting` became beta-default in v0.20, a **single** class (the default one) can cover every Workload in the cluster that does not set its own, so the set one reconcile walks is no longer bounded by opt-in.

[[pr-14737]] (fixes [[issue-13982]]) switches the sweep to `pkg/util/parallelize.Until` — the same helper the LeaderWorkerSet reconciler, the Pod controller, the elastic-job ungater and the TAS topology ungater already use. It bounds concurrency to **at most 8 workers**, checks `ctx.Done()` before each item so a cancelled reconcile stops promptly, and returns a **single** error rather than one per item. Backported to **release-0.19** ([[pr-14945]]) and **release-0.18** ([[pr-14944]]), both merged 2026-08-31.

The shape before the fix also explains the failure signature: the `List` is unpaginated (one reconcile holds the whole membership in memory), and because `ctx` was never read, cancelling the manager mid-sweep let the loop run to the end — every remaining `Update` failed locally and was appended, so the returned `errors.Join` carried one entry per un-swept Workload (source: issue-13982.md).

### The sweep does not filter terminal Workloads

`WorkloadPriorityClassKey` indexes **every** Workload referencing the class, including finished ones, so an installation that retains terminal Workloads (see [[workload-garbage-collection]]) walks and writes them too, even though the value written can no longer affect anything — a finished Workload has already been deleted from the scheduler cache on the workload controller's `StatusFinished` branch. The priority path is the only Workload-keyed writer that does **not** ask `workloadfinish.IsFinished`; the concurrent-admission controller, the MultiKueue workload group, the provisioning controller, the incremental dispatcher, the Pod and StatefulSet reconcilers, the elastic-job ungater and both the TAS indexer and node controller all do (source: issue-13982.md comment).

### Worker-cluster classes must not re-price MultiKueue remote Workloads

The same sweep is a [[multikueue]] hazard. The manager cluster resolves `priorityClassRef` locally and copies both the ref and the resolved `spec.priority` to the worker, tagging the remote Workload with `kueue.x-k8s.io/multikueue-origin` — so the **manager owns that priority**. If the worker cluster defines a `WorkloadPriorityClass` with the *same name but a different value* (e.g. `high = 100` on the manager, `high = 999` on the worker) and that class is created, recreated or modified, the worker's sweep rewrites the remote Workload's priority to its own value, because it does not distinguish locally owned Workloads from remote ones. **Correction (2026-10-21)**: this was described as an open bug with a fix in review. [[pr-14963]] merged and shipped in **v0.20.0**: the WorkloadPriorityClass controller now skips MultiKueue remote Workloads during priority synchronization (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

Known related bug, still open: restarting the controller can overwrite `.spec.priority` with the WorkloadPriorityClass's priority ([[issue-14698]]).

## `WorkloadPriorityClassDefaulting` is Beta (v0.20)

[[pr-13719]] (fixes #13689) graduated the gate from Alpha (since 0.18) to **Beta, on by default in v0.20**. When a WorkloadPriorityClass named `default` exists, jobs that set no class get `kueue.x-k8s.io/priority-class: default`. The **job-webhook** defaulting approach is kept for Beta, the same as `LocalQueueDefaulting`. Moving defaulting to the Workload level is left for later, if problems show up. That item was moved to the KEP's GA criteria at the reviewer's request. In 0.18/0.19 the gate is still off unless enabled (source: pr-13719.md, raw/kueue/pkg/features/kube_features.go). This is why the sweep below can now touch every Workload in the cluster.

## Missing WorkloadPriorityClass: Warning event

A job whose `kueue.x-k8s.io/priority-class` names a class that does not exist cannot get a Workload: the reconcile fails, the job stays suspended, and nothing is queued. The only trace used to be a manager log line. [[pr-13775]] (fixes [[issue-3439]]; v0.20.0) reports it on the job object:

```
Warning  WorkloadPriorityClassNotFound  WorkloadPriorityClass "low" not found
```

- `ExtractPriority` records the event (reason `WorkloadPriorityClassNotFound`) at the point where the label-driven lookup returns NotFound. The error is still returned, so the reconcile still fails and no Workload is created. One call site covers Workload creation, Workload update and a changed priority label. A Forbidden on the same lookup, or a missing `scheduling.k8s.io` PriorityClass named in the Pod template, does **not** emit this event (source: pr-13775.md, raw/kueue/pkg/controller/jobframework/reconciler.go).
- Paths that never resolve the label emit nothing: a prebuilt Workload; a StatefulSet whose Workload already exists (#13827, where a label change is ignored); a Workload whose priority came from a Pod `PriorityClass` (deliberate, #13781); and a Workload that reserved quota without a `priorityClassRef`.
- LeaderWorkerSet resolves the class per component, so it emits one event per component (folded into one event with a count) until #13820 lands.
- **Recovery is the reconcile retry.** The controller watches the job and its Workload, not `WorkloadPriorityClass`. Creating the missing class later does not enqueue the job; it is picked up at the next backoff step (#13779 tracks adding a watch).
- The lookup reads through the informer cache. A job created immediately after its class can briefly see NotFound and emit a spurious warning before the retry succeeds. Maintainers accepted this rather than adding a live API read (source: pr-13775.md).

## Defaulting respects the namespace selector

With `WorkloadPriorityClassDefaulting` (on by default since v0.20), the defaulting webhook adds `kueue.x-k8s.io/priority-class: default` when a WorkloadPriorityClass named `default` exists. It used to do so even in namespaces excluded by `managedJobsNamespaceSelector`, although `ManagedJobsNamespaceSelectorAlwaysRespected` has been GA since 0.19 and the LocalQueue path was already fixed (pr-13375). Unlike the LocalQueue case this did not hang workloads (the label suspends nothing), but Kueue mutated objects in namespaces it was told to ignore, and the label would take effect if the namespace was later opted in (source: pr-15851.md; backports pr-15998.md, pr-15999.md).

`ApplyDefaultWorkloadPriorityClass` now checks the object's namespace against the selector before setting the label:

- The namespace check runs after the existing eligibility checks, so objects that would return early cost no extra Namespace `Get`; with no selector configured no Namespace read happens.
- Every Job webhook passes the configured selector; the Pod webhook passes `nil` because it enforced the selector earlier.
- A Namespace read error is returned from the admission webhook (as `ApplyDefaultLocalQueue` does). `DefaultWorkloadPriorityClassExist` still logs at V(2) and continues if the default class is missing; the read of the default class happens before the Namespace read, so tests use a separate sentinel error per lookup (source: pr-15997.md; release-0.18 backport pr-16422.md, test-only).

Open bug: for Deployment, StatefulSet and LeaderWorkerSet the defaulting also runs on **update**, so Ready objects that predate the `default` class become un-updatable ([[issue-16333]]; expected behaviour: default only on create).

## Related pages

- [[workload]] — where priority is stored.
- [[queueing-strategy]] — how priority affects queue order.
- [[preemption]] — priority determines candidates.
- [[preemption-cost]] — **[Alpha]** dynamic priority adjustment via the `priority-boost` annotation.
- [[integration-statefulset]]
- [[integration-leaderworkerset]]
- [[job-framework-interface]]
