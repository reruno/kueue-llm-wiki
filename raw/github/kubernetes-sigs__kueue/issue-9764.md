# Issue #9764: Systematic approaches for faster debugging and categorization of flakes

**Summary**: Systematic approaches for faster debugging and categorization of flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9764

**Last updated**: 2026-06-22T05:53:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T16:06:04Z
- **Updated**: 2026-06-22T05:53:37Z
- **Closed**: 2026-06-22T05:53:37Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Some approaches worth exploging:
- record historical cases and analyze them, see https://github.com/Sebastianhayashi/kueue-ci-reliability-retro mentioned in https://github.com/kubernetes-sigs/kueue/pull/9570#issuecomment-4018766624
- agent skill for fetching and analyzing failure logs I was recently playing with: https://github.com/mimowo/kueue/blob/agent-skill/agents/stills/flake-debugger/SKILL.md

**Why is this needed**:

Flakes take us signifficant amount of time to debug / diagonoze and fix. Some automation or even collection of data points will be useful to share the knowledge.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T16:06:25Z

cc @mbobrovskyi @sohankunkerkar @PBundyra @tenzen-y @gabesaba

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-07T16:06:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-06-22T05:53:37Z

/close
As we already have the debugger skill: https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental/skills/kueue-flake-debugger
