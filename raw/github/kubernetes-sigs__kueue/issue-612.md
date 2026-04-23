# Issue #612: Apply LimitRange validation on workloads.

**Summary**: Apply LimitRange validation on workloads.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/612

**Last updated**: 2023-04-19T12:41:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-03-07T07:58:30Z
- **Updated**: 2023-04-19T12:41:13Z
- **Closed**: 2023-04-19T12:41:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
This is a followup of #541.

The reasons is  to limit the changes done in #600 and reach a decision for: 
1. What should happen if/when the  LimitRange based validation fails. 
  * For batch/jobs the strategy is to record an event and retry the pod creation.


**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

cc: @alculquicondor @mwielgus

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-03-07T08:05:38Z

#613 Contains a partial (work in progress) implementation for this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-07T14:45:33Z

I didn't check the code, but my idea is:
1. Fail in the Workload webhook.
2. Record the failure as an event in the job controller.

### Comment by [@trasc](https://github.com/trasc) — 2023-04-05T12:04:52Z

/assign
