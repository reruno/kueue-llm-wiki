# Issue #7255: MultiKueue: eliminate the dispatcherName from the workload webhook

**Summary**: MultiKueue: eliminate the dispatcherName from the workload webhook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7255

**Last updated**: 2025-10-20T16:06:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-14T07:07:39Z
- **Updated**: 2025-10-20T16:06:42Z
- **Closed**: 2025-10-20T16:06:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Delete this hack `dispatcherName != configapi.MultiKueueDispatcherModeAllAtOnce` from : https://github.com/kubernetes-sigs/kueue/blob/af0d80ee04210a537fc25dda7a8e23445dbb2763/pkg/webhooks/workload_webhook.go#L375C64-L385

It was added in the interim step of the development when the "AllAtOnce" dispatcher was not setting NominatedClusterNames. Later we decided to set NominatedClusterNames also for this dispatcher: https://github.com/kubernetes-sigs/kueue/blob/af0d80ee04210a537fc25dda7a8e23445dbb2763/pkg/controller/admissionchecks/multikueue/workload.go#L484

**Why is this needed**:

To cleanup the code from unnecessary complexity.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T07:07:46Z

cc @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-15T12:06:23Z

/assign
