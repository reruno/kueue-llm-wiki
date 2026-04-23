# Issue #2207: Add condition WaitingForReplacementPods for pod groups integration

**Summary**: Add condition WaitingForReplacementPods for pod groups integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2207

**Last updated**: 2024-05-24T18:43:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-15T20:08:37Z
- **Updated**: 2024-05-24T18:43:11Z
- **Closed**: 2024-05-24T18:43:11Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A condition `WaitingForReplacementPods` that is True when Kueue doesn't observe all the Pods declared for the group.

If Kueue was the one to delete Pods (due to preemption, waitForPodsReady, etc), then this should be included in the reason.
This can be achieved if Kueue adds the condition right before deleting Pods. 

This condition can be independent of whether the Workload is admitted or not.

**Why is this needed**:

For visibility and for pod controllers to easily detect whether they need to replace pods.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T20:08:45Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-16T07:08:41Z

/assign
