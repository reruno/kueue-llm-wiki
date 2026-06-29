# Issue #9090: Add logs and metrics around API conversion webhooks

**Summary**: Add logs and metrics around API conversion webhooks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9090

**Last updated**: 2026-06-11T09:44:20Z

---

## Metadata

- **State**: open
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2026-02-10T12:00:25Z
- **Updated**: 2026-06-11T09:44:20Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Add metrics and logs in conversion webhooks.

**Why is this needed**:

At this moment there is no visibility into how much conversions are going on, leading to issues with troubleshooting Kueue on large clusters. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T13:03:46Z

It might be that controller-runtime is already logging the received conversion webhook requests, just on a deep logging level. Maybe it also has some metrics which we could surface / document better instead of adding new. I'm not sure, but worth investigating what is already in controller-runtime wrt conversion webhooks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T08:36:22Z

If we want to fully handle conversion loggings, we need to stop relying on auto-generation. Fully scratch conversion webhook could control everything, but implementation and maintaining costs will be huge...

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-12T08:55:37Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-11T09:44:17Z

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
