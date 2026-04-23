# Issue #7852: Kueue-populator: re-use Kueue configuration to restrict the namespaces

**Summary**: Kueue-populator: re-use Kueue configuration to restrict the namespaces

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7852

**Last updated**: 2026-04-20T08:06:20Z

---

## Metadata

- **State**: open
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2025-11-24T14:18:50Z
- **Updated**: 2026-04-20T08:06:20Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like the `kueue-populator` to use the configuration used by Kueue for `managedJobsNamespaceSelector` instead of defining its own. This would allow the populator to respect the same namespace restrictions as the main Kueue manager without requiring duplicate configuration.

**Why is this needed**:

- Consistency: Ensures that both kueue-populator and the main Kueue controller target the exact same set of namespaces.
- Simplicity

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Code changes to make populator read Kueue config
- [ ] Update `kueue-populator` helm chart values.yaml
- [ ] Docs update (if applicable)

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-11-24T14:19:04Z

https://github.com/kubernetes-sigs/kueue/pull/7814#discussion_r2555792803

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:57:34Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:53Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T08:06:18Z

/remove-lifecycle rotten
