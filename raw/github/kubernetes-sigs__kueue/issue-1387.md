# Issue #1387: Add an event in the Job when the workload is declared Finished

**Summary**: Add an event in the Job when the workload is declared Finished

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1387

**Last updated**: 2024-01-12T05:35:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-11-30T15:51:44Z
- **Updated**: 2024-01-12T05:35:15Z
- **Closed**: 2024-01-12T05:35:15Z
- **Labels**: `kind/feature`
- **Assignees**: [@achernevskii](https://github.com/achernevskii)
- **Comments**: 4

## Description

**What would you like to be added**:

An event for the job (Job, MPIJob, Pods, etc), probably through the generic reconciler, that triggers when Kueue declares the workload Finished.

We can probably do this once here https://github.com/kubernetes-sigs/kueue/blob/8431cbd69a14882f2c465be6c56e006494093be2/pkg/controller/jobframework/reconciler.go#L242

**Why is this needed**:

This is especially important when an AdmissionCheck is Rejected. So that the user can react accordingly, by either:
- deleting the job
- deleting the workload (to essentially trigger a requeue)

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-30T15:52:14Z

/assign @stuton 
cc @nstogner

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-30T16:05:45Z

It will be useful to distinguish between a "regular" finish (when the job ends) versus another kind of failure, in a machine readable way.

For this, it might be useful to move from `record.EventRecorder` to `events.EventRecorder`, which has extra machine-readable fields https://github.com/kubernetes/client-go/blob/84a6fe7e4032ae1b8bc03b5208e771c5f7103549/tools/events/interfaces.go#L29

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-04T15:02:03Z

/assign @achernevskii

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-04T10:14:00Z

/unassign @stuton
