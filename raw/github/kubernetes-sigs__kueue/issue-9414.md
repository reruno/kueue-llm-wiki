# Issue #9414: Add an option to E2E_MODE=dev to skip rebuild (and re-install) of Kueue

**Summary**: Add an option to E2E_MODE=dev to skip rebuild (and re-install) of Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9414

**Last updated**: 2026-03-10T06:57:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-23T09:43:20Z
- **Updated**: 2026-03-10T06:57:10Z
- **Closed**: 2026-03-10T06:57:10Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 4

## Description

**What would you like to be cleaned**:

Add the SKIP_REBUILD=true option which would skip re-building and re-installing of Kueue.

Maybe it could be also called SKIP_REINSTALL actually.

**Why is this needed**:

This will be useful when we are done with code and need to repeat multiple times the tests only. 

This will save time in that case.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T09:43:33Z

cc @IrvingMg

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-05T09:38:42Z

/assign @reruno

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-05T09:38:45Z

@mbobrovskyi: GitHub didn't allow me to assign the following users: reruno.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9414#issuecomment-4003728945):

>/assign @reruno


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@reruno](https://github.com/reruno) — 2026-03-05T09:41:19Z

/assign @reruno
