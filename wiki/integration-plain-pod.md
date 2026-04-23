# Integration: plain Pods and PodGroups

**Summary**: The plain-Pod integration lets Kueue govern Pods that aren't owned by a supported higher-level controller. Kueue attaches a scheduling gate at Pod admission-webhook time, creates a Workload, and removes the gate once the Workload is admitted. Groups of related Pods can be treated as a gang using the `kueue.x-k8s.io/pod-group-name` label — a "PodGroup."

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Scheduling gates, not suspend

Plain Pods don't have `.spec.suspend`. Instead, the integration's mutating webhook stamps a scheduling gate onto each Pod at creation time. The Pod is visible to `kube-scheduler` but remains Pending because the gate blocks scheduling. On Workload admission, Kueue removes the gate and `kube-scheduler` proceeds.

This is the same mechanism [[elastic-jobs]] use; bug classes overlap.

## Lifecycle hazards

The gate-based model has sharper edges than suspend-based integrations:

- **Finalizer leaks.** "Failure to remove finalizer for pod / podgroup workload type" (source: issue-6919.md) — Pods stuck undeletable.
- **Stuck terminating.** "Plain Pod remains in Terminating state after deleting" (source: issue-1339.md).
- **Inability to delete before completion.** "Plain Pods cannot delete before completion" (source: issue-6149.md).
- **Admission-check interactions.** "Plain Pod gets deleted once admitted via ProvisioningRequest (DWS)" (source: issue-2213.md) — DWS's reservation model conflicted with the Pod's lifecycle.
- **Externally-removed gates.** "Kueue will say a workload is admitted if its scheduling gates are removed" (source: issue-9482.md) — a third party stripping gates confuses the accounting.
- **WaitForPodsReady.** "Unexplained behavior with plain pods + waitForPodsReady" (source: issue-1648.md) — gang semantics over plain Pods differ from Jobs.

## PodGroups

A PodGroup is a set of Pods sharing `kueue.x-k8s.io/pod-group-name: <name>`. Kueue treats the group as a single Workload — all Pods in the group must be co-admitted and co-evicted. This is how gang scheduling works for plain-Pod workloads.

## Known-owner plain Pods

Some workflows (including custom controllers) create plain Pods with owner references to their own CRDs. "Add Support for Plain Pods with Known OwnerReferences" (source: issue-4106.md) covers the case where Kueue should treat those Pods as a PodGroup but respect the owner's lifecycle.

## MultiKueue

"Support MultiKueue for Plain Pod Integration" (source: issue-2341.md) and PodGroup-specific MultiKueue (source: issue-4719.md — Support PodGroups for MultiKueue, including e2e testing & docs) extended the mechanism cross-cluster, but with caveats because mirroring gated Pods cross-cluster is non-trivial.

## When to disable

Enabling the plain-Pod integration mutates every Pod in the cluster that matches certain namespaces. "Allow usage of plain Pod owned by integrations that are disabled" (source: issue-2481.md) is the control for letting specific owner kinds through without Kueue gating.

## Related pages

- [[integrations]] — integration mechanics.
- [[elastic-jobs]] — same scheduling-gate mechanism.
- [[gang-scheduling]] — PodGroups are the gang primitive.
- [[webhooks]] — the mutating webhook stamps the gate.
- [[multikueue]] — MultiKueue with plain Pods.
