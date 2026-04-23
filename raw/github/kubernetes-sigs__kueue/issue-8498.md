# Issue #8498: Upgrade kubeadm API version to v1beta4

**Summary**: Upgrade kubeadm API version to v1beta4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8498

**Last updated**: 2026-04-13T06:22:11Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-09T14:55:24Z
- **Updated**: 2026-04-13T06:22:11Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would propose to upgrade our test-usage kubeadm resource API version (`kubeadm.k8s.io/v1beta3`) to `kubeadm.k8s.io/v1beta4`: https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20kubeadm.k8s.io%2Fv1beta3&type=code

**Why is this needed**:

Better dependency management.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-12T13:42:02Z

/assign @mbobrovskyi

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-12T13:57:48Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-13T06:22:00Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-13T06:22:11Z

@mbobrovskyi is still working on this
