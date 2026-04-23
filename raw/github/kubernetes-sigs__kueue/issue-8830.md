# Issue #8830: Graduate LocalQueue metrics to Beta

**Summary**: Graduate LocalQueue metrics to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8830

**Last updated**: 2026-04-01T09:30:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T16:10:34Z
- **Updated**: 2026-04-01T09:30:12Z
- **Closed**: 2026-04-01T09:30:11Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We would like to move forward with the important feature.

The main blocking point is API to ensure users can deal with the metric cardinality. Adding namespace selector seems reasonable.

**Why is this needed**:

This is important feature which we observe is already in use even though it is still alpha.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mykysha](https://github.com/mykysha) — 2026-01-29T08:46:26Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-18T12:27:20Z

- [x] https://github.com/kubernetes-sigs/kueue/pull/9370
- [ ] https://github.com/kubernetes-sigs/kueue/pull/9943
- [ ] https://github.com/kubernetes-sigs/kueue/pull/9371
- [ ] https://github.com/kubernetes-sigs/kueue/pull/9700

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-01T09:30:04Z

/close
As this is already done, https://github.com/kubernetes-sigs/kueue/pull/9943 is a nice-to-have follow up.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-01T09:30:12Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8830#issuecomment-4168773313):

>/close
>As this is already done, https://github.com/kubernetes-sigs/kueue/pull/9943 is a nice-to-have follow up.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
