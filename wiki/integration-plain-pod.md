# Integration: plain Pods and PodGroups

**Summary**: The plain-Pod integration lets Kueue govern Pods that aren't owned by a supported higher-level controller. Kueue attaches a scheduling gate at Pod admission-webhook time, creates a Workload, and removes the gate once the Workload is admitted. Groups of related Pods can be treated as a gang using the `kueue.x-k8s.io/pod-group-name` label — a "PodGroup."

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-13014.md, pr-13945.md, pr-17123.md, pr-17124.md, pr-16358.md, pr-16365.md, pr-16385.md, pr-17077.md, pr-17087.md, issue-16517.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-21

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

**No opt-out exists at the snapshot.** The Pod integration skips any Pod whose owner chain contains an object of another enabled Kueue integration, for example TrainJob → JobSet → Job → Pod. [[issue-16517]] asked for an explicit opt-in such as `kueue.x-k8s.io/manage-as-standalone-pod: "true"`. The use case was a MultiKueue setup where plain Pods are the cross-cluster boundary and the worker cluster has no TrainJob/KubeRay CRDs. The issue was closed without an implementation, and no such annotation exists in the code (source: issue-16517.md, raw/kueue/pkg/controller/jobs/pod/).

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

### How the fix got there: merge, revert, re-land

The fix landed twice on `main`. Knowing why the first attempt was reverted explains why the shipped predicate has two conditions.

1. **[[pr-13014]]** (merged 2026-08-05) guarded only the **adoption** path. Inside `FindMatchingWorkloads`, a Workload found by group name without the `is-group-workload` marker was refused. Kueue emitted a `WorkloadNameConflict` Warning, returned an unretryable error, and kept the foreign Workload out of the to-delete set. The gate was described as `RefuseForeignPodGroupWorkloadAdoption` and merged as `PodIntegrationValidateGroupOwner` (source: pr-13014.md, pr-13945.md).
2. **[[pr-13945]]** reverted it two days later. The **finalization** path still resolved by name alone: `(*Pod).ListChildWorkloads` → `JobReconciler.getWorkloads` → `finalizeWorkloads` → `workload.FinalizeOrphanedWorkload`. That path could still strip the finalizer from a victim Workload and finish it. The release-0.18 cherry-pick (#13882) was closed. The gate had never been released, so removing it withdrew nothing (source: pr-13945.md).
3. **[[pr-13960]]** re-landed a fix that covers both paths (described above). At the snapshot, `PodIntegrationValidateGroupOwner` is **Beta and on by default**, with its versioned spec at 0.18 (source: raw/kueue/pkg/features/kube_features.go). It shipped in **v0.20.0, v0.19.2 and v0.18.6** (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md).

A second attack, forging the role hash, was split out of #13014 into #13382. See [[integration-plain-pod#Role-hash forgery: requests are verified before ungating]].

## Finalizer removal on eviction (serving pod groups)

`Stop()` used to call `Finalize()` unconditionally only for `StopReasonWorkloadDeleted`. For every other stop reason — a `waitForPodsReady.recoveryTimeout` eviction, a `spec.active` toggle, scheduler preemption — removal of the `kueue.x-k8s.io/managed` finalizer was left to a later `FindMatchingWorkloads` pass, which had two independent gaps for **serving** groups ([[issue-13830]], fixed by [[pr-14632]]; cherry-picks [[pr-14793]], [[pr-14795]]):

- `isPodRunnableOrSucceeded` counted a Pod as still "active" as long as it kept its `NodeName`, even after it had actually terminated and was stuck mid-deletion. A correctly-gated **replacement** Pod for the same role could then be picked as "excess" and deleted instead of the stuck one, driving the owning controller (e.g. a Deployment) into a create/delete thrash loop.
- `finalizeablePodsCount` only cleared an inactive Pod's finalizer once a replacement already existed for its role. For a StatefulSet-owned Pod the API server refuses to create a replacement with the same ordinal name while the old object still exists in etcd — and it exists precisely because of the finalizer only this formula could remove. **Circular deadlock**, previously resolvable only by manually stripping the finalizer.

`Stop()` now removes the finalizer as soon as an evicted Pod has actually terminated. Both changes are gated on `isServing()`: **batch (non-serving) groups keep the old behaviour on purpose**, because a Pod that finishes mid-eviction must stay listed so the group can still be declared finished (`Pods succeeded: N/N`) once every member has concluded.

## `role-hash` determines the PodSet name

`getRoleHash` returns the `kueue.x-k8s.io/role-hash` annotation verbatim when the client already set it, and that value becomes the PodSet name. Two consequences:

- It fed the scheduling-equivalence hash, so a client stamping a unique role hash per Workload got one equivalence class per Workload — fixed by excluding the PodSet name from the hash (see [[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]], [[pr-14784]]).
- Because the client controls it, it used to control **PodSet order** as well, which changed flavor assignment and the representative mode ([[issue-14802]]). **Correction (2026-10-21)**: this page listed issue-14802 as open. It was fixed by #14809, described in the next section (source: pr-16358.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).
- It is the PodSet a Pod is **charged against**. Kueue now checks a Pod against that PodSet before ungating it. See the role-hash forgery section below.

## PodSet order comes from scheduling shape, not role-hash (`PodGroupSchedulingShapeOrdering`)

#14809 (fixes [[issue-14802]]) sorts a pod group's PodSets by a hash derived from their scheduling shape instead of by the client-supplied role-hash name. The sort key at the snapshot is: shape hash, then PodSet `count`, then PodSet name (source: raw/kueue/pkg/controller/jobs/pod/pod_controller.go). The count tie-breaker has its own unit coverage (pr-16385, backport pr-16975). When a Workload already has a PodSet order (`referenceOrder`), reconciliation keeps that order, so existing Workloads are not reshuffled.

- Gate `PodGroupSchedulingShapeOrdering`: **Beta, on by default in v0.20.0**. The backports are **Alpha and off by default**: v0.19.7 ([[pr-16358]]) and v0.18.11 ([[pr-16365]]) (source: pr-16358.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md).
- Effect: flavor assignment for a pod group is deterministic whatever role-hash values clients choose.

## Role-hash forgery: requests are verified before ungating

**This was the second pod-group quota bypass.** `getRoleHash` trusts a client-supplied `kueue.x-k8s.io/role-hash`. A tenant could copy a cheap role's hash onto an oversized Pod and run it under that role's reservation, within the role's count. #13382 (merged 2026-10-12) closes this (source: pr-17124.md, raw/kueue/pkg/controller/jobs/pod/pod_controller.go).

**Design: check once, where quota starts being used.** The annotation is treated as a PodSet *name*, not a credential. The webhook does not rewrite it, and the Workload is built exactly as before. The check runs only in `Pod.Run()`, the single place where the `kueue.x-k8s.io/admission` gate is removed (through `prepare()`). Replacement Pods that join an admitted group also pass through `startJob` → `Run`, so they are checked too.

- `validatePodsBeforeUngating` takes each **still-gated** Pod and looks up the PodSet its role hash names. It compares the Pod's requests with that PodSet's **effective** spec, the same view quota is charged against. The effective spec comes from `workload.ResolveAdjustmentInputs` + `workload.EffectivePodSpecs`, which apply LimitRange defaults, default requests from limits, and add RuntimeClass overhead. The comparison covers **requests only** (`resources.NewRequestsFromPodSpec`). Full template equivalence was rejected because drift in image, env or tolerations would block ungating without affecting quota.
- A Pod that exceeds its PodSet stays **gated** and gets a Warning event `PodExceedsRoleRequests` ("Pod %q requests more %s than podset %q reserves"). The rest of the group is ungated as usual. This is not an error: the Workload stays admitted and running peers are left alone, so a Pod that anyone can create in the namespace cannot fail someone else's group. The cost: the group cannot become `PodsReady` until the oversized Pod is replaced by one that fits. With [[wait-for-pods-ready]], the Workload is evicted and requeued, up to the requeue limit.
- A role hash that names no PodSet returns the permanent `podset.ErrInvalidPodsetInfo`. This check moved into the pre-pass; its behaviour did not change.
- Adjustment inputs are resolved only when the gate is on **and** the group has a gated Pod.
- Not covered: Pods that never carried Kueue's gate, for example Pods in an excluded namespace, Pods whose gate another plugin stripped, or Pods created while the webhook was down.
- Gate **`PodIntegrationVerifyRoleRequests`**: **Beta, on by default** on `main`, versioned 0.21. The backports to release-0.20 ([[pr-17123]]) and release-0.19 ([[pr-17124]]) ship it **Alpha and off by default**. The 0.19 backport uses `workload.AdjustResources` on a copy, because `EffectivePodSpecs` does not exist on that branch. None of these appears in a tagged release at the snapshot (through v0.20.1 / v0.19.8). The backports were fixed in v0.20.2 and v0.19.9 per CHANGELOG at kueue@3bbb8cce4, released after this snapshot (source: pr-17123.md, pr-17124.md, raw/kueue/pkg/features/kube_features.go).
- **Action required** (release note): if a trusted controller sets `role-hash` itself, for example to a stable per-group value so replacement Pods keep matching immutable PodSet names, check that its Pods never request more than the PodSet built from the group's first Pod of that role. Larger Pods now stay gated (source: pr-17124.md).

Validation of owner-reference UIDs in `FindAncestorJobManagedByKueue`, raised in the same review, was moved to a separate PR (#13802) and is not part of this check.

## All-terminating groups are finalized, not re-adopted

Production incident: a pod stuck `Terminating` (kubelet-stuck teardown) whose Workload the platform had deleted regained a Workload on the next controller restart. The rebuild used the admission-mutated spec (TAS `kubernetes.io/hostname` pin), was permanently `NoFit`, and as an inadmissible head consumed ~78% of scheduling cycles of its ClusterQueue for ~16 h.

`Pod.Load` now treats a group whose **every member is terminating**, once **no (child) Workload remains**, like a terminating job: it returns `ShouldFinalize`, so the framework removes the pods' remaining Kueue finalizers instead of creating a Workload. Design points (source: pr-15154.md):

- The gate keys on "no Workload remains", not on pod finalizers: finalizer removal tied to Workload deletion (`Stop` with `StopReasonWorkloadDeleted`) only runs while the Workload is observable mid-deletion.
- While a child Workload exists nothing changes, so eviction/quota-release bookkeeping is still observed. With `PodIntegrationValidateGroupOwner`, a same-named foreign-owned Workload is not mistaken for "no Workload".
- It runs before pod-set composition, so it also covers fast-admission groups; the `ErrWorkloadCompose` warning event is no longer emitted for all-terminating groups.
- The removal of the reconcile-request key rewrite (`key.Name = p.pod.Name`) is an independent, ungated fix.
- The finalization is behind the Alpha, default-off gate **`FinalizeTerminatingPodGroups`** (registered for v0.20); gate off returns the legacy `Load` result and re-creates a Workload (source: pr-15628.md; backports pr-15554.md, pr-15555.md, pr-15665.md, pr-15666.md). Open question: whether finalization should also require the `pod-group-total-count` to be met.

## `PodsReady` counts Succeeded pods as ready

The kubelet sets `PodReady=False` once a pod completes, so a pod group reported `PodsReady=False` as soon as any member finished; with `waitForPodsReady.recoveryTimeout` the Workload entered `WaitForRecovery` and was evicted, deleting pods that were still running. A `Succeeded` pod now counts as ready (matching batch/Job, which counts `Status.Succeeded`). Serving pod groups still require all pods to be ready. Behind **`PodIntegrationCountSucceededPodsAsReady`** (Beta, on by default; disable to restore the old behaviour) (source: pr-15734.md; backports pr-15910.md, pr-15912.md).

## Deployments: `job-uid` label

A Deployment yields one Workload per Pod, each labelled `kueue.x-k8s.io/job-uid` with its own Pod UID, so nothing tied a Deployment's Workloads together and topology spreading had to use `workloadLabelSelectors`. Behind **`DeploymentJobUIDLabel`** (Beta, on by default) the Pod integration resolves the owning Deployment while building the Workload (via `FindAncestorJobManagedByKueue`; the ReplicaSet hop is metadata-only) and labels it with the **Deployment UID**, like StatefulSet and LeaderWorkerSet. Details (source: pr-15641.md; backports pr-16004.md, pr-16005.md):

- A Pod not managed through a Deployment keeps its own UID; a failed owner read is returned for retry, no fallback.
- Existing Workloads keep the label they were created with (never re-synced).
- Adds a Deployment informer (the integration previously registered a noop reconciler); reads are cache-backed.
- `kueuectl list workload --for deployment/foo` matched nothing before; with the gate it returns that Deployment's Workloads (see [[kueuectl]]).

## Failure recovery: no duplicate conditions

With `FailureRecoveryPolicy` on, retries of forceful termination of a Pod stuck in termination added a duplicate `KueueFailureRecovery` Pod condition and a duplicate `KueueForcefullyDeleted` warning event on every reconcile. The condition is now set once and the event emitted only when the condition changes; deletion is still retried (source: pr-16033.md; backport pr-16113.md, pr-16133.md).

## Empty PodGroups of StatefulSet / LeaderWorkerSet

When the last member Pod of a StatefulSet/LWS-backed PodGroup is gone, `Pod.Load()` reports an empty composable job (`jobFound=false`) and finalization ran before the normal eviction branch, so a Workload evicted by `PodsReadyTimeout` kept its admission and quota, or was finished as an orphan while the owner was still live. The empty-PodGroup path now reads the owner through the `IntegrationManager` and checks UID and deletion state; for an unfinished Workload with a live, Kueue-managed non-Pod owner it retains the Workload and finalizer and completes eviction via the same admission-clearing helper as the normal inactive-job path (which re-checks eviction and quota-reservation state inside the status patch). Deleted, terminating or UID-mismatched owners still let the Workload be finished (source: pr-14578.md; backports pr-16127.md, pr-16128.md). Separate, still open at writing: scale-to-zero of a StatefulSet with active Pods can release quota prematurely ([[issue-16043]]). The deletion-grace double count ([[issue-16075]]) is now fixed; see the next section.

## PodGroup activity at the Pod deletion deadline

`Pod.IsActive()` decides whether a group still holds quota. Only `Running` Pods count. A Running Pod with a `deletionTimestamp` used to stay active until `deletionTimestamp + deletionGracePeriodSeconds`. But for graceful deletion the API server already sets `deletionTimestamp` to the *end* of the grace period, so a Pod stuck Running past its deadline (for example on a lost node) kept the group's quota for one extra grace period (#16076, fixes [[issue-16075]]; source: pr-17087.md).

Rules at the snapshot (source: raw/kueue/pkg/controller/jobs/pod/pod_controller.go):

- A Running, terminating Pod **with** a recorded `deletionGracePeriodSeconds` is inactive once `now` is after `deletionTimestamp`. At exactly the timestamp it still counts as active.
- A terminating Pod **without** a recorded grace period still counts as active, as before.
- With `FastQuotaReleaseInPodIntegration` (Alpha, off) any terminating Pod is inactive at once.
- The new decision applies at the **next reconcile** after the deadline. No reconcile is scheduled at the deadline itself.

Main merged 2026-10-12. Backports: [[pr-17077]] (release-0.20) and [[pr-17087]] (release-0.19). None was in a tagged release at the snapshot. The backports were fixed in v0.20.2 and v0.19.9 per CHANGELOG at kueue@3bbb8cce4, released after this snapshot. **Correction (2026-10-21)**: the "Empty PodGroups" section above listed [[issue-16075]] as open.

## Pod-level requests and quota

`resourcehelpers.PodRequests` let an explicit pod-level request smaller than the aggregate container request replace it, so a directly created Workload could reserve less quota than its containers ask for. A shared `PodRequests` helper (in `pkg/resources`) now keeps effective requests at least the aggregate container requests, then adds Pod overhead; valid specs are unchanged (source: pr-16047.md, issue-14255.md). Open: pod-level CPU defaulting from limits ([[issue-15702]]).

## Webhook-side defaulting of WorkloadPriorityClass

The Pod webhook enforces `managedJobsNamespaceSelector` earlier in admission, so it passes `nil` to `ApplyDefaultWorkloadPriorityClass` (see [[workload-priority#Defaulting respects the namespace selector]]).

## Related pages

- [[integrations]] — integration mechanics.
- [[elastic-jobs]] — same scheduling-gate mechanism.
- [[gang-scheduling]] — PodGroups are the gang primitive.
- [[webhooks]] — the mutating webhook stamps the gate.
- [[multikueue]] — MultiKueue with plain Pods.
- [[security]] — the pod-group adoption bug is the wiki's worked example of a tenant-reachable quota bypass.
- [[integration-statefulset]] — shares the Pod reconciler and the same-name replacement hazard.
- [[wait-for-pods-ready]]
- [[security-code-patterns]]
