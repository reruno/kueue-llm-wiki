# Issue #9764: Systematic approaches for faster debugging and categorization of flakes

**Summary**: Systematic approaches for faster debugging and categorization of flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9764

**Last updated**: 2026-03-09T16:06:25Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T16:06:04Z
- **Updated**: 2026-03-09T16:06:25Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

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
