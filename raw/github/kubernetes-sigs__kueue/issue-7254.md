# Issue #7254: Combination of MultiKueue and a non-MultiKueue AdmissionChecks may return an empty list

**Summary**: Combination of MultiKueue and a non-MultiKueue AdmissionChecks may return an empty list

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7254

**Last updated**: 2026-04-07T15:35:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ganczak-commits](https://github.com/ganczak-commits)
- **Created**: 2025-10-14T05:36:44Z
- **Updated**: 2026-04-07T15:35:34Z
- **Closed**: 2026-04-07T15:35:34Z
- **Labels**: `kind/bug`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Comments**: 7

## Description

One of the MultiKueue constraints is that it always applies to all RFs in a CQ. In theory a Workload submitted to such a CQ doesn't need admission (flavor assignment) because regardless of the flavor it would always use the MultiKueue AdmissionCheck - this is what happens [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go#L1180-L1191) - before we check for admission, if all AdmissionChecks applies to all RFs in a CQ it returns a list of the AdmissionChecks. It works correctly if MultiKueue is the only AdmissionCheck in a CQ, but we suspect it would break if there was combination of MultiKueue and an AdmissionCheck that should be run only on part of the flavors. Then the code would return an empty list of AdmissionChecks, even there should be the MultiKueue one (according to its assumption).

In particular, deleting [the code which should merely be a microoptimization](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go#L1180-L1191) breaks the integration test case `MultiKueue when not all integrations are enabled [It] Should not create a MPIJob workload, when MPIJob adapter is not enabled` ([test run](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6785/pull-kueue-test-integration-multikueue-main/1975539260094156800)).

What's happening is that the admissionCheck [here](https://github.com/kubernetes-sigs/kueue/blob/dc263e01760ce118ee580a4a6816dae6fbba962b/test/integration/multikueue/jobs_test.go#L1442) is `Pending` just as the test expects - but then it changes to `nil` because [this code](https://github.com/kubernetes-sigs/kueue/blob/dc263e01760ce118ee580a4a6816dae6fbba962b/pkg/workload/workload.go#L1196-L1199) is now executed (previously the microoptimization was returning the function a few lines above). The test is failing, because its check happens already after `Pending` has changed into `nil`.

What's worse, even if I comment out [this expectation](https://github.com/kubernetes-sigs/kueue/blob/dc263e01760ce118ee580a4a6816dae6fbba962b/test/integration/multikueue/jobs_test.go#L1441-L1450), the test is failing a [couple lines below](https://github.com/kubernetes-sigs/kueue/blob/dc263e01760ce118ee580a4a6816dae6fbba962b/test/integration/multikueue/jobs_test.go#L1478), as `worker2 wl` is never removed.

When investigating the test run with a debugger, [workload.go:456](https://github.com/kubernetes-sigs/kueue/blob/5a6b10a710386852e5b57ce91896dd47c583cfcf/pkg/controller/admissionchecks/multikueue/workload.go#L456) and then [workload_controller.go:543](https://github.com/kubernetes-sigs/kueue/blob/5a6b10a710386852e5b57ce91896dd47c583cfcf/pkg/controller/core/workload_controller.go#L543) are triggered. Then [`UnsetQuotaReservationWithCondition`](https://github.com/kubernetes-sigs/kueue/blob/dc263e01760ce118ee580a4a6816dae6fbba962b/pkg/controller/jobframework/reconciler.go#L540) happens, and inside it `Status.Admission` is set to `nil`.

The PR should consist of:
1. Create an integration test similar to the one that currently fails (with deletion of the linked part of the code) and add AdmissionCheckStrategy to it, with an AdmissionCheck defined only for a one out of two flavors in the CQ - this should prove that there's indeed a bug. No need to change anything in the production code, let's just add another integration test.
1. When we prove that there's indeed a bug, fix the linked part of the code so that whenever there's a MultiKueue AdmissionCheck it should always be returned, regardless of different AdmissionChecks

## Discussion

### Comment by [@ganczak-commits](https://github.com/ganczak-commits) — 2025-10-15T08:13:52Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:22:38Z

/area multikueue
/priority important-longterm

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-16T10:15:04Z

/assign

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-16T10:15:23Z

/unassign ganczak-commits

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-16T10:25:26Z

Links:
1. denotes AdmissionChecksForWorkload function: https://github.com/kubernetes-sigs/kueue/blob/9fd2597755e55160dc976866b1f2254f37d0c8bf/pkg/workload/workload.go#L1309
2. similar

Remaining links seem to point to correct places in code.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-24T13:37:18Z

Regarding the very possibility of defining an admission check separate form the MultiKueue admission check on a manager cluster queue - even if we ensure the MK AC is always present on the workload, the current logic does not support a correct handling of such checks:
* Such a check would not affect the dispatch of a workload itself unless it enters the Rejected or Retry state. In fact, the check could remain in the Pending state, keeping the workload on the manager from being admitted (condition admitted), but the quota would be reserved and remotes would be created as usual. This could even lead to the workload finishing without being officially admitted at all. This behavior is not ideal and inconsistent with what an AC is meant to be doing: instead of keeping the workload from admission until Ready, it keeps it from admission only after it is Rejected (or Retrying after rejection).
* Even though the workload can end up finished despite such a check never leaving the Pending state, the check could enter the Rejected or Retry state, leading to the workloads eviction and removal of all of the remote workloads.

We could resolve this in one of two ways:
* by ether adding the support for such custom checks to be used by MK or
* by adding an additional restriction to MK CQs - when the MK AC is defined it has to be the only AC on a cluster queue.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-03-02T09:23:29Z

> Regarding the very possibility of defining an admission check separate form the MultiKueue admission check on a manager cluster queue - even if we ensure the MK AC is always present on the workload, the current logic does not support a correct handling of such checks:
> 
> * Such a check would not affect the dispatch of a workload itself unless it enters the Rejected or Retry state. In fact, the check could remain in the Pending state, keeping the workload on the manager from being admitted (condition admitted), but the quota would be reserved and remotes would be created as usual. This could even lead to the workload finishing without being officially admitted at all. This behavior is not ideal and inconsistent with what an AC is meant to be doing: instead of keeping the workload from admission until Ready, it keeps it from admission only after it is Rejected (or Retrying after rejection).
> * Even though the workload can end up finished despite such a check never leaving the Pending state, the check could enter the Rejected or Retry state, leading to the workloads eviction and removal of all of the remote workloads.
> 
> We could resolve this in one of two ways:
> 
> * by ether adding the support for such custom checks to be used by MK or
> * by adding an additional restriction to MK CQs - when the MK AC is defined it has to be the only AC on a cluster queue.

Followup bug created: #9622
