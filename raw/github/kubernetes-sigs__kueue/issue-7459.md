# Issue #7459: Promote Admission Fair Sharing to beta

**Summary**: Promote Admission Fair Sharing to beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7459

**Last updated**: 2025-12-01T15:09:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-10-30T16:21:07Z
- **Updated**: 2025-12-01T15:09:46Z
- **Closed**: 2025-12-01T15:09:45Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 10

## Description

Admission Fair Sharing is alpha in 0.12.

Looking at the graduation criteria in the KEP I don't see anything outstanding for this to go beta.

Is there any reason why we can't turn this feature gate on?

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-30T16:28:53Z

I don't have strong objections.
The only concern is LocalQueue EntryPenalty, which was introduced in v0.13.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-30T16:32:05Z

cc @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T16:35:32Z

I don't have objections too. Especially if you have some interests among your users it will be great to broaden the adoption.

This is a complex KEP so there is some risk, but:
1. we already have some adoption and the users are not reporting bugs (so far)
2. we had a number of bugs / flakes, but it seems we have eliminated them all, thanks for @IrvingMg and @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T16:36:20Z

cc @mwysokin @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-30T16:40:06Z

/kind feature

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-30T17:44:29Z

Sounds good.

I opened up https://github.com/kubernetes-sigs/kueue/pull/7463.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:31:20Z

Actually, it seems AFS has a bug (or at least confusing behavior) discovered by a flaky test: https://github.com/kubernetes-sigs/kueue/issues/7693

I'm not sure this should be a blocker or not, because it happens rarely, and also the impact is not catastrophic, but the entry penalties don't seem to always work.

Ideally we just fix it, but I don't know how much work there is. cc the feature owners: @PBundyra @IrvingMg 

/reopen 
Let me reopen to re-consider the decision for graduation.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T09:31:26Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7459#issuecomment-3540786649):

>Actually, it seems AFS has a bug (or at least confusing behavior) discovered by a flaky test: https://github.com/kubernetes-sigs/kueue/issues/7693
>
>I'm not sure this should be a blocker or not, because it happens rarely, and also the impact is not catastrophic, but the entry penalties don't seem to always work.
>
>Ideally we just fix it, but I don't know how much work there is. cc the feature owners: @PBundyra @IrvingMg 
>
>/reopen 
>Let me reopen to re-consider the decision for graduation.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-01T15:09:40Z

/close 

As AFS has been promoted to Beta in [Kueue v0.15](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0) and the issues in #7693 have already been addressed by #7780.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T15:09:46Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7459#issuecomment-3597077797):

>/close 
>
>As AFS has been promoted to Beta in [Kueue v0.15](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.15.0) and the issues in #7693 have already been addressed by #7780.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
