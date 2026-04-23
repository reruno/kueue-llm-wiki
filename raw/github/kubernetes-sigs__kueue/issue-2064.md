# Issue #2064: Cleanup creation of conditions

**Summary**: Cleanup creation of conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2064

**Last updated**: 2024-04-26T07:56:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-25T08:23:22Z
- **Updated**: 2024-04-26T07:56:25Z
- **Closed**: 2024-04-26T07:56:25Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We should apply `api.TruncateConditionMessage` consistently to ensure the messages are not too long, for example [here](https://github.com/kubernetes-sigs/kueue/blob/9ea94ac20f4a4b5546ab899c60f3627b23bd0a74/pkg/workload/workload.go#L446C26-L446C33) we might be missing the protection.

Also, we don't need to set `LastTransitionTime` to `now`, since this is set in the `SetStatusCondition` function.

**Why is this needed**:

Make sure that users don't hit an issue with too long messages. Also, code consistency.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-25T08:23:30Z

/assign @kaisoz
