# Issue #1750: Set observedGeneration in Conditions

**Summary**: Set observedGeneration in Conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1750

**Last updated**: 2024-04-16T06:48:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-16T21:08:32Z
- **Updated**: 2024-04-16T06:48:07Z
- **Closed**: 2024-04-16T06:48:07Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Set the .observedGeneration in conditions based on .metadata.generation, in all Kueue objects.

**Why is this needed**:

From the k8s docs:

```
observedGeneration represents the .metadata.generation that the condition was set based upon.
For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9,
the condition is out of date with respect to the current state of the instance.
```

It could be useful for understanding whether Kueue might still have to do other operations on the object

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-16T21:08:56Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-04-04T15:50:35Z

/assign @vladikkuzn

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-04T15:50:37Z

@trasc: GitHub didn't allow me to assign the following users: vladikkuzn.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1750#issuecomment-2037576110):

>/assign @vladikkuzn


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-04T16:04:16Z

/unassign @trasc

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-08T09:23:59Z

/assign @vladikkuzn
