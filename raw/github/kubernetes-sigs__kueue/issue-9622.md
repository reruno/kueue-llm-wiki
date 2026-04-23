# Issue #9622: MultiKueue Manager Workload admits but does not get "Admitted" condition when additional Admission Checks still "Pending"

**Summary**: MultiKueue Manager Workload admits but does not get "Admitted" condition when additional Admission Checks still "Pending"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9622

**Last updated**: 2026-04-10T15:08:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Created**: 2026-03-02T09:22:36Z
- **Updated**: 2026-04-10T15:08:23Z
- **Closed**: 2026-04-10T15:08:23Z
- **Labels**: `kind/bug`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
If a user of MultiKueue defines additional admission checks beyond the MultiKueue admission check on the Manager Cluster queue, these checks will not be taken into account when dispatching the Remote Workloads to Workers.
As long as the additional check does not enter the "Rejected" or "Retry" state, workloads will continue to be dispatched. Eventually a remote may become Admitted and begin executing the Remote Workload. If the additional check is not "Ready" by then, the process will continue, but the Manager Workload will not be marked as "Admitted". This can proceed to the eventual success of the Remote Workload, leading to the Manager Workload reaching the Finished state without ever getting the "Admitted" condition.

**What you expected to happen**:
The workload should enter the "Admitted" state when a Remote is "Admitted". This could be achieved, for example, by:
* ensuring dispatch may not happen until all admission checks on the Manager Workload (other than the MK AC) are ready,
* propagating the Manager ACs to the Remotes, setting their state to "Ready" there once they become "Ready" on the Manager Workload.

**How to reproduce it (as minimally and precisely as possible)**:
Test verifying this behavior can be found at https://github.com/kubernetes-sigs/kueue/pull/9573

**Anything else we need to know?**:
---

**Environment**:
- Kubernetes version (use `kubectl version`):
```
Client Version: v1.34.4-dispatcher
Kustomize Version: v5.7.1
```
- Kueue version (use `git describe --tags --dirty --always`): `v0.16.0-devel-632-gb08267fe0`

## Discussion

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-02T09:24:52Z

From #7254 

> Regarding the very possibility of defining an admission check separate form the MultiKueue admission check on a manager cluster queue - even if we ensure the MK AC is always present on the workload, the current logic does not support a correct handling of such checks:
> 
> * Such a check would not affect the dispatch of a workload itself unless it enters the Rejected or Retry state. In fact, the check could remain in the Pending state, keeping the workload on the manager from being admitted (condition admitted), but the quota would be reserved and remotes would be created as usual. This could even lead to the workload finishing without being officially admitted at all. This behavior is not ideal and inconsistent with what an AC is meant to be doing: instead of keeping the workload from admission until Ready, it keeps it from admission only after it is Rejected (or Retrying after rejection).
> * Even though the workload can end up finished despite such a check never leaving the Pending state, the check could enter the Rejected or Retry state, leading to the workloads eviction and removal of all of the remote workloads.
> 
> We could resolve this in one of two ways:
> 
> * by ether adding the support for such custom checks to be used by MK or
> * by adding an additional restriction to MK CQs - when the MK AC is defined it has to be the only AC on a cluster queue.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-03T10:00:57Z

/area multikueue

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-03-06T14:10:42Z

I think option 1
> ensuring dispatch may not happen until all admission checks on the Manager Workload (other than the MK AC) are ready,

is better, because:

- the decision is done in one place (on the manager cluster), semantically it's also concise - manager `dispatches`, therefor `admits`
- we don't replicate Acs to remote clusters, which we would have to cleanup afterwards

while option 2 brings risks like:
- ACs may reference manager-only context (namespaces, policies, credentials, external controllers) that don’t exist on workers
-  If AC becomes Ready/Rejected on the manager, we need to propagate the state to all workers

wdyt @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T14:37:30Z

Yes, (1.) is simpler. If we need some configuration in the future, then we will add knobs. For now this is much better.

### Comment by [@alison-lim](https://github.com/alison-lim) — 2026-04-09T05:47:45Z

When will this bug be fixed? I am experiencing the same issue. Please fix it quickly.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-09T05:53:19Z

cc @mszadkow @kshalot
