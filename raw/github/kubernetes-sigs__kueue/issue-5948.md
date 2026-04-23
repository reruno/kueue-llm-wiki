# Issue #5948: Refactor `util` packages by renaming them to fix `revive.var-naming` exclusion

**Summary**: Refactor `util` packages by renaming them to fix `revive.var-naming` exclusion

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5948

**Last updated**: 2026-03-20T21:36:10Z

---

## Metadata

- **State**: open
- **Author**: [@alexandear](https://github.com/alexandear)
- **Created**: 2025-07-11T14:28:51Z
- **Updated**: 2026-03-20T21:36:10Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Remove the following `golangci-lint` exclusion (added in #5914):

```yaml
linters:
    exclusions:
      - linters:
          - revive
        path: 'util/*'
        text: 'var-naming: avoid meaningless package names'

```

and refactor the affected `util` packages by renaming them to more descriptive and meaningful names.

**Why is this needed**:

This exclusion suppresses valid `revive` warnings about vague package names like `util`. Such names make code harder to navigate and understand. Addressing this will improve clarity, promote better package boundaries, and align with best practices enforced by the `revive.var-naming` rule.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-09T15:08:25Z

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

### Comment by [@alexandear](https://github.com/alexandear) — 2025-10-09T17:28:14Z

/remove-lifecycle stale

### Comment by [@wmcnamee-coreweave](https://github.com/wmcnamee-coreweave) — 2025-12-20T01:42:28Z

Can you provide some better names for the functions in util, that wouldn't also conflict with the standard library and cause a different kind of confusion?

### Comment by [@alexandear](https://github.com/alexandear) — 2025-12-20T20:51:48Z

@wmcnamee-coreweave Please take a look at PR #8377, where I showed an example of renaming the `util` package and splitting it into three separate packages.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-20T21:08:19Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-20T21:36:06Z

/remove-lifecycle stale
