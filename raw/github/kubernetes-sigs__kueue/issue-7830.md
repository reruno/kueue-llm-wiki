# Issue #7830: Prepare build system to build Alpha APIs in a separate yamls

**Summary**: Prepare build system to build Alpha APIs in a separate yamls

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7830

**Last updated**: 2026-04-18T11:15:56Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T08:23:59Z
- **Updated**: 2026-04-18T11:15:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Prepare the build system so that introduction of the new Alpha APIs is opt-in, and they are in a dedicated yaml.
Also they are installed by helm as opt-in, say installAlphaAPIs=Cohort,Topology etc.

**Why is this needed**:

To prepare for the introduction of the new Alpha APIs as opt-ins.

Making them installed by default caused complications on upgrades, see discussion: https://github.com/kubernetes-sigs/kueue/issues/7743

See also release notes which mention the required installation steps due to that:
https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.0
https://github.com/kubernetes-sigs/kueue/releases/tag/v0.13.0
https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T08:24:26Z

cc @tenzen-y @kannon92 @mbobrovskyi @Charleen-z

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:58:37Z

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
