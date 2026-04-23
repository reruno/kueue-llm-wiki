# Issue #6184: FlavorFungability: replace FlavorFungibilityImplicitPreferenceDefault feature gate with API

**Summary**: FlavorFungability: replace FlavorFungibilityImplicitPreferenceDefault feature gate with API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6184

**Last updated**: 2025-11-14T16:02:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-25T13:06:31Z
- **Updated**: 2025-11-14T16:02:42Z
- **Closed**: 2025-11-14T16:02:41Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 4

## Description

**What would you like to be added**:

An API which will allow to users to determine flavor preference in case the set of identified candidate flavors has either Borrowing, Preemption, and potentially BorrowAndPreempt flavors.

consider 
```yaml
whenCanBorrow: TryNextFlavor
whenCanPreempt: TryNextFlavor
```
may return multiple flavors like: (Borrow, Fit), (BorrowAndPreempt), (Preempt).

Current algorithm, without the feature gate returns Borrow.

However, this is problematic to some users, because borrowing workloads are likely preemption targets by reclaiming workloads, just a couple minutes later. So, some users prefer to proactively preemption rather than borrow to be preempted soon after. This is common pattern when FairSharing is enabled, but not only then.


**Why is this needed**:

The feature gate cannot be graduated to GA, because it changes the behavior which can be breaking to some users. So, we need to provide API which supports both preferring Borrowing, or Preemption.

Some API ideas were discussed in the KEP PR, but it was too close to release to choose wisely: https://github.com/kubernetes-sigs/kueue/pull/6133

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T13:07:08Z

cc @tenzen-y @pajakd @gabesaba

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-17T19:17:36Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-14T16:02:36Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-14T16:02:41Z

@vladikkuzn: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6184#issuecomment-3533453139):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
