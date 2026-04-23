# Issue #426: Document how Kueue works with cluster-autoscaler

**Summary**: Document how Kueue works with cluster-autoscaler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/426

**Last updated**: 2025-08-03T17:55:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-11-16T19:40:44Z
- **Updated**: 2025-08-03T17:55:16Z
- **Closed**: 2025-08-03T17:55:15Z
- **Labels**: `help wanted`, `kind/cleanup`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be cleaned**:

We claim that Kueue can be used alongside CA, but we don't explain how. Perhaps a version of theory of operation in bit.ly/kueue-apis could help.

/kind documentation

**Why is this needed**:

We got a [question in slack](https://kubernetes.slack.com/archives/C032ZE66A2X/p1668590719134009) about this, where the user story was:

> I guess my suggestion/story would be, I would like a jobs node pool in my cluster to be auto scalable with min: 0 nodes and max: (my budget limit, or a sane guardrail). And as my node pool hits its max nodes, have the jobs queue up for placement.

Which is exactly what kueue is meant to do.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-16T19:40:53Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-16T19:40:54Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/426):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-11-24T02:50:31Z

Not only cluster-autoscaler, I think we can also mention the relationship with other components, especially kube-scheduler, we have users had this confusion, see https://kubernetes.slack.com/archives/C032ZE66A2X/p1669212423358399?thread_ts=1669137423.710669&cid=C032ZE66A2X

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:55:10Z

@mimowo @tenzen-y I think we can close this issue. We have documentation on ProvisionRequests so I think this is sufficient.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-03T17:55:16Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/426#issuecomment-3148601390):

>@mimowo @tenzen-y I think we can close this issue. We have documentation on ProvisionRequests so I think this is sufficient.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
