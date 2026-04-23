# Issue #1145: Allow AdmissionChecks controllers to set additional annotations, labels, node selectors and taints on workload pods.

**Summary**: Allow AdmissionChecks controllers to set additional annotations, labels, node selectors and taints on workload pods.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1145

**Last updated**: 2023-10-24T06:46:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2023-09-21T15:10:04Z
- **Updated**: 2023-10-24T06:46:29Z
- **Closed**: 2023-10-24T06:46:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@trasc](https://github.com/trasc)
- **Comments**: 7

## Description

**What would you like to be added**:

An additional field(s) in `Workload` and integration framework changes to allow setting additional
annotations, labels, node selector and taints on pods that belong to a particular `Workload`.

**Why is this needed**:

Some admission checks may want to narrow down the nodes on which the workload pods should be run. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-10-02T06:01:53Z

/assign 
for API change

### Comment by [@mimowo](https://github.com/mimowo) — 2023-10-02T12:29:55Z

/assign
For propagating and restoring the labels, annotations & tolerations

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-06T12:57:57Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-06T12:58:01Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1145#issuecomment-1750637539):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-10-24T06:44:28Z

@tenzen-y I think this should be closed

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-24T06:46:25Z

> @tenzen-y I think this should be closed

It makes sense.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-24T06:46:29Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1145#issuecomment-1776622429):

>> @tenzen-y I think this should be closed
>
>It makes sense.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
