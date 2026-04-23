# Issue #27: Use klog.KObj or klog.KRef for every log that involves a Queue or Capacity

**Summary**: Use klog.KObj or klog.KRef for every log that involves a Queue or Capacity

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/27

**Last updated**: 2022-10-31T13:30:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-18T17:29:19Z
- **Updated**: 2022-10-31T13:30:46Z
- **Closed**: 2022-10-31T13:30:45Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`, `size/S`
- **Assignees**: _none_
- **Comments**: 13

## Description

This should help filter logs by namespace.
Although less important for Capacity (because it's ClusterScoped), I prefer to have everything uniform.

/kind cleanup

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T13:41:52Z

Anything blocking this? if not, pls mark with help wanted

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T14:00:46Z

/good-first-issue
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-13T14:00:47Z

@alculquicondor: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/27):

>/good-first-issue
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ystkfujii](https://github.com/ystkfujii) — 2022-04-13T15:08:52Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T15:18:54Z

/help cancel

### Comment by [@ystkfujii](https://github.com/ystkfujii) — 2022-05-19T01:29:30Z

/unassign

### Comment by [@kanha-gupta](https://github.com/kanha-gupta) — 2022-05-27T18:39:03Z

/assign

### Comment by [@aetherrootr](https://github.com/aetherrootr) — 2022-06-30T12:17:34Z

I want try this issue, please tell me about Capacity.
And I think every code about queue in pkg/queue/
@alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-30T18:51:32Z

Yes, let's do it for Capacity (now ClusterQueue) as well.

### Comment by [@aetherrootr](https://github.com/aetherrootr) — 2022-07-01T12:05:27Z

ok, let me try this issue.
/assign

### Comment by [@utkarsh-singh1](https://github.com/utkarsh-singh1) — 2022-10-30T20:33:37Z

Hi @alculquicondor, I have an interest in this issue, So can I get a small brief about this one, so it can give me a head start.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-31T13:30:41Z

/close

this was already completed

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-31T13:30:46Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/27#issuecomment-1297095552):

>/close
>
>this was already completed


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
