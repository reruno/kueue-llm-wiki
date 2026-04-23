# Issue #7421: Add an agents file to Kueue to better enable AI assistants

**Summary**: Add an agents file to Kueue to better enable AI assistants

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7421

**Last updated**: 2026-04-18T12:16:57Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-10-28T18:07:00Z
- **Updated**: 2026-04-18T12:16:57Z
- **Closed**: —
- **Labels**: `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

Following https://github.com/kubernetes/kubernetes/pull/133386,

It would be nice to have an Agents file that can aide in common Kueue development practices.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-28T19:21:58Z

I added https://github.com/kubernetes-sigs/kueue/pull/7422

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-29T06:29:06Z

I have no objections, but I would like to wait for https://github.com/kubernetes/kubernetes/pull/133386 completion.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-29T18:01:22Z

> I have no objections, but I would like to wait for [kubernetes/kubernetes#133386](https://github.com/kubernetes/kubernetes/pull/133386) completion.

Why should we wait for kubernetes PR to merge?

It sounds like the author has left it to go stale.

- https://github.com/kubernetes-sigs/cluster-api-provider-azure/pull/5899

I also am adding an agents file to JobSet.

https://github.com/kubernetes-sigs/cluster-api-provider-azure/pull/5899#issuecomment-3405930946

They at least highlight a few other repos in kubernetes that merged the agents directory. I don't think we need to wait for k/k PR to merge if we want this change.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:42:19Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:22Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:54Z

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
