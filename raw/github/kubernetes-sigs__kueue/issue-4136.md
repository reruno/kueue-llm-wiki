# Issue #4136: Fair sharing mechanism without preemptions

**Summary**: Fair sharing mechanism without preemptions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4136

**Last updated**: 2025-05-15T17:31:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-02-03T14:24:38Z
- **Updated**: 2025-05-15T17:31:39Z
- **Closed**: 2025-05-15T17:31:37Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What would you like to be added**:

An admission-time mechanism to fair share unused resources without preemptions.

**Why is this needed**:

The current fair sharing approach enforces fair sharing via preemptions. Workloads from CQ that is consuming more shared resources are preempted in favor of workloads that is consuming less. This however has couple of drawbacks:

* Doesn't work in a situation when preemptions are not recommended.
* Doesn't allow stable admission of large (like consuming more than 1/Nth) amount of shared resources. 

A new, complementary mechanism is needed to address these needs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T08:16:18Z

@mwielgus What is this expectation instead of preemption? Do we want to scale out cluster to have fair sharing instead of preemption? Or do we want to restrict Job admission based on the fair share policy even if the cluster has unused resources?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T11:14:49Z

/reopen 
This was closed by the robot, based on the tag in KEP PR, we still need implementation and docs 🙂

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-24T11:14:54Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4136#issuecomment-2827237684):

>/reopen 
>This was closed by the robot, based on the tag in KEP PR, we still need implementation 🙂 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-07T17:51:19Z

Reopening to keep track about the docs update.
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-07T17:51:24Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4136#issuecomment-2859606844):

>Reopening to keep track about the docs update.
>/reopen 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T17:31:31Z

/close
I opened the follow up issue for documentation: https://github.com/kubernetes-sigs/kueue/issues/5262

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-15T17:31:38Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4136#issuecomment-2884574235):

>/close
>I opened the follow up issue for documentation: https://github.com/kubernetes-sigs/kueue/issues/5262


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
