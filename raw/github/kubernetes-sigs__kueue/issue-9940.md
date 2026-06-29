# Issue #9940: Support Jobsets with semi-independent jobs

**Summary**: Support Jobsets with semi-independent jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9940

**Last updated**: 2026-06-15T12:55:24Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-03-17T12:23:37Z
- **Updated**: 2026-06-15T12:55:24Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 1

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

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-15T12:55:21Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
