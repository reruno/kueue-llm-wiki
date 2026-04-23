# Issue #7871: KueuePopulator: offload the root makefile by moving the targets to dedicated makefile

**Summary**: KueuePopulator: offload the root makefile by moving the targets to dedicated makefile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7871

**Last updated**: 2025-12-19T13:24:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-25T08:00:20Z
- **Updated**: 2025-12-19T13:24:33Z
- **Closed**: 2025-12-19T13:24:33Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to move the kueue-populator targets to an included makefile, as we do for Makefile-test.mk

**Why is this needed**:

To offload the landing Makefile, as the project is still experimental.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T08:00:31Z

/assign @j-skiba

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-25T08:00:34Z

@mimowo: GitHub didn't allow me to assign the following users: j-skiba.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7871#issuecomment-3574231528):

>/assign @j-skiba 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-11-25T08:01:51Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:55:18Z

ah I see this is still valid: https://github.com/kubernetes-sigs/kueue/blob/main/Makefile#L435-L449

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:57:06Z

/priority important-soon
@j-skiba let me know if you want to continue, otherwise please unassign
