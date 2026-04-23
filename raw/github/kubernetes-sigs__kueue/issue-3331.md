# Issue #3331: Use DeactivationTarget to improve message when deactivating due to Rejected AdmissionChecks

**Summary**: Use DeactivationTarget to improve message when deactivating due to Rejected AdmissionChecks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3331

**Last updated**: 2024-11-12T14:30:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-28T07:57:56Z
- **Updated**: 2024-11-12T14:30:50Z
- **Closed**: 2024-11-12T14:30:49Z
- **Labels**: `kind/feature`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 7

## Description

**What would you like to be added**:

When deactivating due to rejected admission checks we just active=false: https://github.com/kubernetes-sigs/kueue/blob/3d278a9ada0cd7e994bd17201d23e314ffefc0f0/pkg/controller/core/workload_controller.go#L370-L379
Then, the generic message for the `Evicted` condition is set [here](https://github.com/kubernetes-sigs/kueue/blob/3d278a9ada0cd7e994bd17201d23e314ffefc0f0/pkg/controller/core/workload_controller.go#L189).

The message can be improved when DeactivationTarget is used, see [here](https://github.com/kubernetes-sigs/kueue/blob/3d278a9ada0cd7e994bd17201d23e314ffefc0f0/pkg/controller/core/workload_controller.go#L194).

The message candidate: `The workload is deactivated due to rejected AdmissionChecks(s): check1, check2.`

**Why is this needed**:

To inform the end user about the reason of deactivation.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-28T07:58:27Z

cc @PBundyra @tenzen-y @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-28T08:03:47Z

I was supposed to improve this mechanism in https://github.com/kubernetes-sigs/kueue/issues/1353.
So, I guess that @PBundyra is implementing this improvement now.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T06:47:39Z

I see @KPostOffice is already working on this under https://github.com/kubernetes-sigs/kueue/pull/3350/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T06:48:15Z

/assign @KPostOffice

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T06:48:18Z

@mimowo: GitHub didn't allow me to assign the following users: KPostOffice.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3331#issuecomment-2456369676):

>/assign @KPostOffice


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T06:49:20Z

@KPostOffice you should be able to assign yourself

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-05T15:26:11Z

/assign
