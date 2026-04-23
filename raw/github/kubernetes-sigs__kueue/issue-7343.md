# Issue #7343: DRA cleanup: use structured assert on errors using cmp.Diff

**Summary**: DRA cleanup: use structured assert on errors using cmp.Diff

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7343

**Last updated**: 2026-03-30T14:46:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-22T17:00:46Z
- **Updated**: 2026-03-30T14:46:26Z
- **Closed**: 2026-03-30T14:46:26Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@akbad](https://github.com/akbad)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to assert on validation errors in pkg/dra/claims_test.go using structured approach based on cmp.Diff. Currently there is only bool checked wantErr, in this PR we introduce assert on message: https://github.com/kubernetes-sigs/kueue/pull/7226/. However, the end goal for me is to use cmp.Diff, and probably use `field.Invalid` for the validation errors.

**Why is this needed**:

To produce cleaner diffs when the errors don't much expectations. The use of cmp.Diff also allows to reduce the amount of code to do asserts.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T10:56:55Z

I fully agree with you.

### Comment by [@harche](https://github.com/harche) — 2025-10-24T11:07:56Z

/assign

### Comment by [@harche](https://github.com/harche) — 2025-10-29T17:57:21Z

I will be looking into this issue in the upcoming week.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:49:37Z

/unassign harche
due to long inactivity
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T12:48:22Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:52:04Z

/close
I think https://github.com/kubernetes-sigs/kueue/pull/7226 address the comments

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T12:52:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7343#issuecomment-4089920170):

>/close
>I think https://github.com/kubernetes-sigs/kueue/pull/7226 address the comments


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:53:20Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T12:53:27Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7343#issuecomment-4089926709):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:53:59Z

/unassign @harche

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:54:13Z

/remove-lifecycle stale

### Comment by [@akbad](https://github.com/akbad) — 2026-03-30T11:39:43Z

Hi, I took a look at this issue and seems like the remaining issues to fix are:

1. `extended_resources_test.go` still using `wantErr bool`/`wantErrCount int` instead of the structured `field.ErrorList` + `cmp.Diff` pattern from #7529
2. the lingering `reflect.DeepEqual` in `claims_test.go` that was flagged in the review of #7529 

I'll open a PR resolving both shortly.

### Comment by [@akbad](https://github.com/akbad) — 2026-03-30T11:39:59Z

/assign
