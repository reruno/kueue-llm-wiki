# Issue #7215: Add validation to make release process more robust

**Summary**: Add validation to make release process more robust

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7215

**Last updated**: 2026-03-19T12:40:20Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-09T09:02:24Z
- **Updated**: 2026-03-19T12:40:20Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Validation on the format of the GIT_TAG during the release process. In particular to make sure it starts with "v" for the `make artifacts` step, but potentially other steps too.

**Why is this needed**:

To fail early on typos that cause: https://github.com/kubernetes-sigs/kueue/issues/7210

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T09:02:59Z

cc @gabesaba @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:46:38Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:40:16Z

/remove-lifecycle stale
