# Issue #4041: Drop the Pod TAS label in favor of an indexed field based on Workload

**Summary**: Drop the Pod TAS label in favor of an indexed field based on Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4041

**Last updated**: 2025-09-25T14:15:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-23T09:40:29Z
- **Updated**: 2025-09-25T14:15:24Z
- **Closed**: 2025-09-25T14:15:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 18

## Description

**What would you like to be added**:

We would drop the use of the Pod TAS label which is used for filtering out the pods managed by TAS: https://github.com/kubernetes-sigs/kueue/blob/fd2519a76bc4d51b3b464d1f27525136a69b080e/apis/kueue/v1alpha1/tas_types.go#L57-L61

This was requested as a cleanup in the comment: https://github.com/kubernetes-sigs/kueue/pull/3271#issuecomment-2426461284

However, if we hit roadblocks, we should revisit the proposal of dropping the label,

**Why is this needed**:

To avoid using labels which duplicate the information which is already present in the workload.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T09:40:40Z

cc @PBundyra @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T09:55:03Z

cc @mbobrovskyi

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-10T13:14:35Z

@mimowo  OK i will look into that , if its breaking changes , will notify else i will implement the indexed field-based.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T13:31:02Z

Awesome!

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-10T14:36:39Z

/assign

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-02-12T15:23:39Z

Switching to an indexed field instead of the TAS label requires careful consideration: Kubernetes field selectors don’t support arbitrary spec fields, so labels enable efficient API lookups via LabelSelector, while indexed fields though fast for controller-level filtering don’t provide the same external query efficiency. For existing Kubernetes resources, labels remain the better choice for dynamic querying. 

This statement is Based on  Tas Readme[[this](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling#integration-support)]

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-13T16:22:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-12T17:15:16Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-12T18:05:48Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-12T18:05:53Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4041#issuecomment-3065925761):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-13T22:04:15Z

/reopen
/remove-lifecycle rotten

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-13T22:04:20Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4041#issuecomment-3067327423):

>/reopen
>/remove-lifecycle rotten


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-22T08:04:02Z

@Horiodino are you still working on it?

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-08-22T15:40:35Z

> [@Horiodino](https://github.com/Horiodino) are you still working on it?

nope

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-08-22T15:41:15Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T10:33:01Z

/assign
I will try to make it happen along with the TAS graduation to Beta

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T14:15:18Z

This has been resolved by https://github.com/kubernetes-sigs/kueue/pull/6828
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-25T14:15:24Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4041#issuecomment-3334377899):

>This has been resolved by https://github.com/kubernetes-sigs/kueue/pull/6828
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
