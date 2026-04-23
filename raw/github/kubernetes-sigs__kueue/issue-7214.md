# Issue #7214: Switch default TAS placement algorithm (BestFit -> Mixed)

**Summary**: Switch default TAS placement algorithm (BestFit -> Mixed)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7214

**Last updated**: 2025-11-04T09:22:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-10-09T07:40:55Z
- **Updated**: 2025-11-04T09:22:16Z
- **Closed**: 2025-11-04T09:22:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@iomarsayed](https://github.com/iomarsayed)
- **Comments**: 3

## Description

**What would you like to be added**:

Not really "added" - it's about changing the default TAS placement algorithm from BestFit to Mixed. \
This has been agreed on in #4570 . \
I'm opening this separately because #4570 is originally about sth else.

**Why is this needed**:

The old default, as we understand, does not match users' needs very well.

**Completion requirements**:

This enhancement requires the following artifacts:

- [X] Design doc (just a small KEP update)
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T14:07:49Z

/reopen
Implementations have not been done, yet.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-10T14:07:54Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7214#issuecomment-3390350489):

>/reopen
>Implementations have not been done, yet.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-23T08:10:29Z

/assign
