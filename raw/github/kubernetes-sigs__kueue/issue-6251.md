# Issue #6251: TAS: documentation for 2-level scheduling: JobSet and LWS

**Summary**: TAS: documentation for 2-level scheduling: JobSet and LWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6251

**Last updated**: 2025-12-08T11:04:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T13:30:30Z
- **Updated**: 2025-12-08T11:04:54Z
- **Closed**: 2025-12-08T11:04:53Z
- **Labels**: `lifecycle/stale`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 5

## Description

/kind documentation

Describe the API for using 2-level scheduling in JobSet (PodSet + PodSetSlice) and LWS (PodSetGroup + PodSet).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:30:41Z

cc @tenzen-y @lchrzaszcz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T08:06:55Z

cc @mwysokin

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-07T08:48:31Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T11:04:48Z

/close 
Replaced by https://github.com/kubernetes-sigs/kueue/issues/8039 and https://github.com/kubernetes-sigs/kueue/issues/8038

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-08T11:04:54Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6251#issuecomment-3626356325):

>/close 
>Replaced by https://github.com/kubernetes-sigs/kueue/issues/8039 and https://github.com/kubernetes-sigs/kueue/issues/8038


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
