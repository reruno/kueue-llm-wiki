# Issue #7164: Auto-manage KAL version and avoid hardcoded golangci-lint version

**Summary**: Auto-manage KAL version and avoid hardcoded golangci-lint version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7164

**Last updated**: 2026-04-15T11:36:52Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-10-03T14:09:32Z
- **Updated**: 2026-04-15T11:36:52Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/7017#discussion_r2390209677, I would like to investigate way in the following 2 aspects for KAL:

1. Manage KAL version by dependabot: https://github.com/kubernetes-sigs/kueue/blob/4c6c8c248ef62de4fe54e841bfa363b7877c6073/hack/kal-linter/.custom-gcl.yaml#L6
2. Avoid hardcoded golangci-lint version for KAL for automated golangci-lint version management: https://github.com/kubernetes-sigs/kueue/blob/4c6c8c248ef62de4fe54e841bfa363b7877c6073/hack/kal-linter/.custom-gcl.yaml#L1

**Why is this needed**:
We should rely on dependabot or an automation mechanism to manage third-party tools so that we can better handle the supply chain.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-03T14:10:36Z

cc @mbobrovskyi @mimowo @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T14:40:28Z

sgtm, thank you for raising

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:47:23Z

/priority important-longterm

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-14T20:57:18Z

cc @JoelSpeed @everettraven 

Is it possible to use something like dependabot to manage this for us?

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2026-01-15T11:05:12Z

If you were to switch to the [plugin style mode](https://github.com/kubernetes-sigs/kube-api-linter?tab=readme-ov-file#golangci-lint-plugin) that K/K uses, then you manage the version of both golangci-lint and KAL from the go.mod, in which case, I suspect dependabot would be perfectly happy to oblige in keeping it up to date

https://github.com/kubernetes/kubernetes/blob/0ba578f91f5de11776152b55bac37491d9848ef3/hack/tools/golangci-lint/go.mod#L7

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T11:36:50Z

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
