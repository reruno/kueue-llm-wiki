# Issue #634: Avoid unnecessary casting for reconcillers

**Summary**: Avoid unnecessary casting for reconcillers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/634

**Last updated**: 2023-06-16T14:30:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-03-15T14:07:52Z
- **Updated**: 2023-06-16T14:30:22Z
- **Closed**: 2023-06-16T14:30:22Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

There are potentially unnecessary castings in the MPI/Job reconcillers: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_controller.go#L304-L307. 

This was contested in the PR discussions: https://github.com/kubernetes-sigs/kueue/pull/627#discussion_r1135777564.
The use of generics along with https://github.com/kubernetes-sigs/kueue/pull/627#discussion_r1134513118.

However, despite an attempt I couldn't make it work, so it was deferred for later.

**Why is this needed**:

The library code should be as easy to use as possible.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-03-15T14:08:51Z

cc @alculquicondor @mwielgus

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-06-13T14:30:03Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-13T14:30:48Z

/remove-lifecycle stale
