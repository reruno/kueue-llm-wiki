# Issue #6493: AFS: document the new policy on picking preemption targets

**Summary**: AFS: document the new policy on picking preemption targets

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6493

**Last updated**: 2026-02-03T09:21:24Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-07T07:57:57Z
- **Updated**: 2026-02-03T09:21:24Z
- **Closed**: —
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 5

## Description

We should document the new policy of ordering preemption targets as implemented in https://github.com/kubernetes-sigs/kueue/pull/5632.

This is motivated by the discussion https://github.com/kubernetes-sigs/kueue/discussions/5609, as it is currently not clear to the users what has priority when picking targets: usages vs priority.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T07:58:12Z

cc @PBundyra @kimminw00

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T08:30:03Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:31:40Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-03T09:16:42Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T09:21:22Z

/remove-lifecycle stale
