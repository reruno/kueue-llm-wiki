# Issue #9957: featureGates unit tests cleanup

**Summary**: featureGates unit tests cleanup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9957

**Last updated**: 2026-03-26T16:46:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Created**: 2026-03-17T17:55:56Z
- **Updated**: 2026-03-26T16:46:22Z
- **Closed**: 2026-03-26T16:46:22Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ivnovakov](https://github.com/ivnovakov)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Use `featureGates map[featuregate.Feature]bool` as a standard way for enabling/disabling features in unit tests
```go
// ✅ GOOD
featureGates map[featuregate.Feature]bool

// ❌ BAD — separate booleans per gate
enablePriorityBoost           bool
admissionFairSharingEnabled   bool
```

**Why is this needed**:
To have a standard way for enabling/disabling features in unit tests

Ref: https://github.com/kubernetes-sigs/kueue/pull/9120#discussion_r2939419215

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T18:01:54Z

Thank you for the issue, yes let's use the new pattern consistently in the codebase, it is much more flexible

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-18T11:39:17Z

Tentatively assigning to get more familiarity with the tests
/assign @ivnovakov

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-18T11:39:20Z

@vladikkuzn: GitHub didn't allow me to assign the following users: ivnovakov.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9957#issuecomment-4081822200):

>Tentatively assigning to get more familiarity with the tests
>/assign @ivnovakov 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ivnovakov](https://github.com/ivnovakov) — 2026-03-19T09:59:01Z

/assign
