# Issue #9940: Support Jobsets with semi-independent jobs

**Summary**: Support Jobsets with semi-independent jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9940

**Last updated**: 2026-03-17T12:23:37Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-03-17T12:23:37Z
- **Updated**: 2026-03-17T12:23:37Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What would you like to be added**:

Support for elastic JobSet workloads in Kueue, where individual replicated jobs within a JobSet can be admitted, scheduled (using TAS), run, and fail independently. 

Specifically, add a mechanism to detect/configure JobSet for independent replicas. Upon detection, Kueue should instantiate discrete Workload objects ( "fragments") for each constituent replicated job replica, and manage them in such a way that:

* Ensures that at least some of the fragments are started if the cluster capacity doesn't allow full admission.
* Hardware failure related to a single job within jobset doesn't cause full jobset rescheduling. 
* Fragments don't preempt each other.
* Kueuectl is aware that fragments come from a single jobset and present them in an easy to understand way.

**Why is this needed**:

With modern accelerators hardware failures are quite common and that is especially painful for large workloads. In order to get the best goodput from the infrastructure, some of the Kueue customers are splitting their large jobs into semi-independent fragments and would like to get the corresponding granularity in admission and error handling. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.
