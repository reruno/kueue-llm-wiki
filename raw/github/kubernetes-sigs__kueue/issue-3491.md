# Issue #3491: Use ResourceFlavorReference instead of string consistently

**Summary**: Use ResourceFlavorReference instead of string consistently

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3491

**Last updated**: 2024-11-25T08:14:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-08T12:03:51Z
- **Updated**: 2024-11-25T08:14:57Z
- **Closed**: 2024-11-25T08:14:57Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 7

## Description

/kind cleanup

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

To use ResourceFlavorReference consistently, and only cast to string when absolutly needed

**Why is this needed**:

For example here: 
- flavor is casted ResourceFlavorReference -> string [here](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/controller/core/resourceflavor_controller.go#L242C22-L242C46)
- then down in the invocation stack it is casted back from string to ResourceFlavorReference: [here](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/cache/clusterqueue.go#L604C13-L604C36)

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-09T14:12:19Z

/good-first-issue
/help wanted

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-09T14:12:20Z

@kannon92: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3491):

>/good-first-issue
>/help wanted


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@shubhamch71](https://github.com/shubhamch71) — 2024-11-09T16:06:58Z

Hi @mimowo I understand the goal is to consistently use ResourceFlavorReference type instead of string throughout the codebase, particularly in ClusterQueuesUsingFlavor() and related methods, only casting to string when absolutely necessary (like in NamespacedName). Could you help clarify the specific scenarios where casting to string would still be necessary apart from NamespacedName ? Also anything you can suggest to get started with this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-12T10:00:31Z

> the goal is to consistently use ResourceFlavorReference type instead of string throughout the codebase

yes

>  Could you help clarify the specific scenarios where casting to string would still be necessary apart from NamespacedName ?

AFAIK only when passing to NamespacedName, but I might be missing some place, it is part of the task to figure out all such places.

>  Also anything you can suggest to get started with this issue?

I think you are on the right track.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-11-19T14:29:02Z

/assign 

@shubhamch71 I've assigned this one to myself because it's still free and you didn't add any update in some time. However, if you already started with it please let me know.

### Comment by [@shubhamch71](https://github.com/shubhamch71) — 2024-11-20T07:21:54Z

@kaisoz Thanks for picking this up! I apologize for the delay on my end—I’ve been caught up with work and won’t be able to make further progress on it. Feel free to go ahead and take it forward.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-11-21T14:45:51Z

@shubhamch71 No worries! I'll work on it, thanks for the response 😊
