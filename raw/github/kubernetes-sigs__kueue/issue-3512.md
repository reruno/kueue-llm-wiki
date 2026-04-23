# Issue #3512: Discard concatenating reasons when setting Workload's condition

**Summary**: Discard concatenating reasons when setting Workload's condition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3512

**Last updated**: 2024-11-21T12:10:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-12T11:09:23Z
- **Updated**: 2024-11-21T12:10:36Z
- **Closed**: 2024-11-21T12:10:33Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
[Concatenating reasons when setting Workload's condition](https://github.com/kubernetes-sigs/kueue/blob/52d10c7713c399904ac228b3ac7d4836443cac8c/pkg/controller/core/workload_controller.go#L192)

**Why is this needed**:
I believe we should always set only one reason per condition

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-13T08:05:09Z

Can you provide an example of the current reason, and the one you would expect?

> I believe we should always set only one reason per condition

I think this is what is happening as we have only one DeactivationTarget condition, so the reason is taken from it.

Maybe it would be good enough to concatenate using "DueTo"? For example "WorkloadInactiveDueToAdmissionChecks", or ideally "DeactivatedDueToAdmissionCheckRejected" (but it means renaming more, like "WorkloadInactive -> Deactivated).

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-13T10:13:59Z

>> Can you provide an example of the current reason, and the one you would expect?

I've provided logic that does such concatenation. The case could be as following:

1. Workload has an AdmissionCheck 
2. AdmissionCheck is Rejected
3. Workload is Evicted due to a rejected AdmissionCheck
4. DeactivationTarget is set for Workload
5. In the logic above Condition's reasons are concatenated and currently it's `InactiveWorkloadAdmissionCheck`
6. Message in the Workload's Condition is `The workload is deactivated due to Admission check(s): foo, were rejected`

I believe the message in the Workload's Condition is sufficient for users and we don't need to concatenate reasons as they should be easy to parse programmatically. 

The behavior I described above is also reflected in [integration tests for provisioning controller](https://github.com/kubernetes-sigs/kueue/blob/00a05fcf481bd13b6c779ddfc7059890c7282517/test/integration/controller/admissionchecks/provisioning/provisioning_test.go#L438)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-13T10:20:42Z

I see, I get the point now. I think it makes sense, but it seems this was the explicit suggestion to concatenate during the previous review when adding: https://github.com/kubernetes-sigs/kueue/pull/2409/files#r1653510593, and there is some merit for making it parsable my machines. Still, `InactiveWorkloadAdmissionCheck` does not read well.
So, maybe saying `InactiveWorkloadDueToAdmissionCheck` is good enough? We do something similar here: https://github.com/kubernetes-sigs/kueue/blob/00a05fcf481bd13b6c779ddfc7059890c7282517/pkg/controller/jobframework/reconciler.go#L864.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-21T12:10:28Z

/close 
while working on https://github.com/kubernetes-sigs/kueue/pull/3593 we decided to keep the concatenation, but use "DueTo" for better reasability.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-21T12:10:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3512#issuecomment-2490968842):

>/close 
>while working on https://github.com/kubernetes-sigs/kueue/pull/3593 we decided to keep the concatenation, but use "DueTo" for better reasability.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
