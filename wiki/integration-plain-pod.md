# Integration: plain Pods and PodGroups

**Summary**: The plain-Pod integration lets Kueue govern Pods that aren't owned by a supported higher-level controller. Kueue attaches a scheduling gate at Pod admission-webhook time, creates a Workload, and removes the gate once the Workload is admitted. Groups of related Pods can be treated as a gang using the `kueue.x-k8s.io/pod-group-name` label — a "PodGroup."

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

---

## Scheduling gates, not suspend

Plain Pods don't have `.spec.suspend`. Instead, the integration's mutating webhook stamps a scheduling gate onto each Pod at creation time. The Pod is visible to `kube-scheduler` but remains Pending because the gate blocks scheduling. On Workload admission, Kueue removes the gate and `kube-scheduler` proceeds.

This is the same mechanism [[elastic-jobs]] use; bug classes overlap.

## Lifecycle hazards

The gate-based model has sharper edges than suspend-based integrations:

- **Finalizer leaks.** "Failure to remove finalizer for pod / podgroup workload type" ([[issue-6919]]) — Pods stuck undeletable.
- **Stuck terminating.** "Plain Pod remains in Terminating state after deleting" ([[issue-1339]]).
- **Inability to delete before completion.** "Plain Pods cannot delete before completion" ([[issue-6149]]).
- **Admission-check interactions.** "Plain Pod gets deleted once admitted via ProvisioningRequest (DWS)" ([[issue-2213]]) — DWS's reservation model conflicted with the Pod's lifecycle.
- **Externally-removed gates.** "Kueue will say a workload is admitted if its scheduling gates are removed" ([[issue-9482]]) — a third party stripping gates confuses the accounting.
- **WaitForPodsReady.** "Unexplained behavior with plain pods + waitForPodsReady" ([[issue-1648]]) — gang semantics over plain Pods differ from Jobs.

## PodGroups

A PodGroup is a set of Pods sharing `kueue.x-k8s.io/pod-group-name: <name>`. Kueue treats the group as a single Workload — all Pods in the group must be co-admitted and co-evicted. This is how gang scheduling works for plain-Pod workloads.

## Known-owner plain Pods

Some workflows (including custom controllers) create plain Pods with owner references to their own CRDs. "Add Support for Plain Pods with Known OwnerReferences" ([[issue-4106]]) covers the case where Kueue should treat those Pods as a PodGroup but respect the owner's lifecycle.

## MultiKueue

"Support MultiKueue for Plain Pod Integration" ([[issue-2341]]) and PodGroup-specific MultiKueue ([[issue-4719]] — Support PodGroups for MultiKueue, including e2e testing & docs) extended the mechanism cross-cluster, but with caveats because mirroring gated Pods cross-cluster is non-trivial.

## When to disable

Enabling the plain-Pod integration mutates every Pod in the cluster that matches certain namespaces. "Allow usage of plain Pod owned by integrations that are disabled" ([[issue-2481]]) is the control for letting specific owner kinds through without Kueue gating.

## PodGroup Workload adoption is guarded by `is-group-workload`

**This was an exploitable quota-bypass.** [[pr-13960]] (re-landing #13014 plus the gap it missed; cherry-picks [[pr-14617]], [[pr-14630]]) closes it.

**The bug.** A Pod carrying `kueue.x-k8s.io/pod-group-name: <victim-workload-name>` could make Kueue finish an *unrelated* Workload:

1. `(*Pod).Load` returns `shouldFinalize = !p.isFound`, which is true whenever a reconcile of `{Name: <groupName>, Namespace: "group/<ns>"}` finds **zero** Pods with that group name. `key` is left as `{groupName, ns}`.
2. `JobReconciler.ReconcileGenericJob` calls `r.finalize` **before** the namespace-selector check, before `FindAncestorJobManagedByKueue`, before the queue-name check, and before `ensureOneWorkload`. `(*Pod).Skip` does not help — its first branch requires `p.isFound`.
3. `finalizeWorkloads` → `getWorkloads` → `ListChildWorkloads`, which resolved the Workload **by name alone**.
4. `FinalizeOrphanedWorkload` then marks the victim's Workload `Finished` with reason `OwnerNotFound` and strips the `kueue.x-k8s.io/resource-in-use` finalizer.

It never *deletes* the victim — the damage is Finish + de-finalize. The victim's quota is released from the cache while its real Pods keep running, and the victim's own Job reconciler then sees `IsFinished`, emits `FinishedWorkload`, and drops the Job finalizer, so the Job runs completely untracked. `controllerutil.HasControllerReference(wl)` makes it *worse* for a real victim: a Workload owned by a `batch/Job` has a controller reference, so `canFinish` is true and it gets Finished; a genuine pod-group Workload only has non-controller owner references and merely loses its finalizer.

**Reachability.** A *managed* attacker Pod cannot get there (it carries `podconstants.PodFinalizer`, so deleting it leaves it `Terminating`, `p.isFound` stays true, and the group wedges on `errNotPodGroupWorkload`). The reachable variants are Pods that never received the finalizer:

- a Pod with **no queue name**, with `manageJobsWithoutQueueName=false` and no default LocalQueue — the webhook adds no gate, no finalizer and no managed label, yet the Pod still carries the group-name label and `podEventHandler.Delete` enqueues `{groupName, "group/<ns>"}` unconditionally. **Creating and deleting one throwaway Pod is enough** — no queue, no quota reservation, no admission required;
- Pods with `SuspendedByParentAnnotation` (`suspendByParent` gates the Pod but deliberately skips `AddFinalizer`);
- namespace/pod-selector-excluded Pods, and Pods created while the webhook was down.

**The fix.** `ListChildWorkloads` refuses a Workload that **lacks the `kueue.x-k8s.io/is-group-workload` marker *and* carries a controller reference**. `NewGroupWorkload` always stamps the marker, and a pod group only ever adds *non-controller* owner references, so a controller reference means the Workload belongs to someone else.

Two design points worth remembering:

- It returns an **empty list**, not an error and not an event. `ListChildWorkloads` has exactly one caller chain (`getWorkloads` → `finalizeWorkloads`), so no caller can be driven into creating a duplicate Workload; an error would propagate through `finalize` and requeue the doomed request forever while short-circuiting `finalizeJob`; and an event is impossible because `p.pod` is the zero Pod when no Pods exist. The user-visible `WorkloadNameConflict` warning still fires on the `FindMatchingWorkloads` path, where a real Pod exists.
- The predicate needs **both** conditions. Checking only the marker would regress user-supplied **prebuilt pod-group Workloads**: the prebuilt branch bypasses `FindMatchingWorkloads`, and `isOrphanedWorkload` returns false while owner refs exist, so `finalizeWorkloads` is the only thing that removes their `resource-in-use` finalizer — they would leak it forever.

See [[security-code-patterns]]: a client-supplied string used as a cross-object primary key is the pattern.

## Finalizer removal on eviction (serving pod groups)

`Stop()` used to call `Finalize()` unconditionally only for `StopReasonWorkloadDeleted`. For every other stop reason — a `waitForPodsReady.recoveryTimeout` eviction, a `spec.active` toggle, scheduler preemption — removal of the `kueue.x-k8s.io/managed` finalizer was left to a later `FindMatchingWorkloads` pass, which had two independent gaps for **serving** groups ([[issue-13830]], fixed by [[pr-14632]]; cherry-picks [[pr-14793]], [[pr-14795]]):

- `isPodRunnableOrSucceeded` counted a Pod as still "active" as long as it kept its `NodeName`, even after it had actually terminated and was stuck mid-deletion. A correctly-gated **replacement** Pod for the same role could then be picked as "excess" and deleted instead of the stuck one, driving the owning controller (e.g. a Deployment) into a create/delete thrash loop.
- `finalizeablePodsCount` only cleared an inactive Pod's finalizer once a replacement already existed for its role. For a StatefulSet-owned Pod the API server refuses to create a replacement with the same ordinal name while the old object still exists in etcd — and it exists precisely because of the finalizer only this formula could remove. **Circular deadlock**, previously resolvable only by manually stripping the finalizer.

`Stop()` now removes the finalizer as soon as an evicted Pod has actually terminated. Both changes are gated on `isServing()`: **batch (non-serving) groups keep the old behaviour on purpose**, because a Pod that finishes mid-eviction must stay listed so the group can still be declared finished (`Pods succeeded: N/N`) once every member has concluded.

## `role-hash` determines the PodSet name

`getRoleHash` returns the `kueue.x-k8s.io/role-hash` annotation verbatim when the client already set it, and that value becomes the PodSet name. Two consequences:

- It fed the scheduling-equivalence hash, so a client stamping a unique role hash per Workload got one equivalence class per Workload — fixed by excluding the PodSet name from the hash (see [[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]], [[pr-14784]]).
- Because the client controls it, it also controls **PodSet order**, which changes flavor assignment and the representative mode ([[issue-14802]], open).

## Related pages

- [[integrations]] — integration mechanics.
- [[elastic-jobs]] — same scheduling-gate mechanism.
- [[gang-scheduling]] — PodGroups are the gang primitive.
- [[webhooks]] — the mutating webhook stamps the gate.
- [[multikueue]] — MultiKueue with plain Pods.
- [[security]] — the pod-group adoption bug is the wiki's worked example of a tenant-reachable quota bypass.
- [[integration-statefulset]] — shares the Pod reconciler and the same-name replacement hazard.
