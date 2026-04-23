# Issue #3476: Promote kueue apis to V1

**Summary**: Promote kueue apis to V1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3476

**Last updated**: 2026-04-15T11:40:58Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-11-06T14:47:25Z
- **Updated**: 2026-04-15T11:40:58Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Promote the core Kueue APIs to V1.
**Why is this needed**:
We would need to use Kueue in more of our products. Many customers would like a stable API to build on top of.

We would like to start the discussion for what it would take to promote the v1beta1(2) APIs to v1 and stablize the API.
**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-06T14:49:18Z

https://github.com/kubernetes-sigs/kueue/issues/3192#issuecomment-2394506049

Some context is above.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-06T14:50:23Z

It is not clear to me if https://github.com/kubernetes-sigs/kueue/issues/768 must be satisfied before we promote to V1 or not.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T14:54:51Z

Actually, we use in Kueue both alpha and beta.

I'm wondering if we could migrate to v1 only a subset of API which we consider already stable (like Workload, LQ, CQ and so on), while keeping the other still in alpha or beta (like Topology or MultiKueue, or other new features).

This would give us more flexibility and serial that we promote APIs which aren't battle tested yet. In any case new features to Kueue will start in Alpha.
 
WDYT @kannon92 @tenzen-y ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T14:56:08Z

> It is not clear to me if https://github.com/kubernetes-sigs/kueue/issues/768 must be satisfied before we promote to V1 or not.

This is wishlist for v1beta2, so yes, this should happen before  v1

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-06T15:01:55Z

> This would give us more flexibility and serial that we promote APIs which aren't battle tested yet. In any case new features to Kueue will start in Alpha.

I don't think we need features to start in alpha API fields. Unless we are introducing a new API field entirely. One can always add a new field to v1 or v1beta API.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-06T15:02:47Z

> This is whitelist for v1beta2, so yes, this should happen before v1

My concern is not there isn't really a hard and fast rule on this one so I worry that it will stay as a wishlist with this API in beta while we add more items to it.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T15:10:47Z

When I was talking about new features I was thinking that the API objects, like recently introduced Topology or Cohort, should go via Alpha API. For extending existing objects, sure we have no choice than extend them.

As for the wishlist, I'm with you, I would like to promote the APIs, but the list is long and so think it will be safer and with less friction if we move via interim step of v1beta2 than directly to v1.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T16:45:07Z

As I commented in https://github.com/kubernetes-sigs/kueue/issues/3192#issuecomment-2396510965, I would like to wait any API graduation (even v1beta2) for the graduation of the TAS and HirarchyCohort since both are still alpha stage and potentially plan API change.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-07T17:45:56Z

> I'm wondering if we could migrate to v1 only a subset of API which we consider already stable (like Workload, LQ, CQ and so on), while keeping the other still in alpha or beta (like Topology or MultiKueue, or other new features).

@tenzen-y is there room to do something like this?

I would really like to see some kind of stabilization of the API for at least the core resources.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T18:09:03Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-05T18:11:27Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-06T18:20:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T18:22:21Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T19:07:35Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-04T19:19:08Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T20:03:06Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-19T17:27:15Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:28:57Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T11:18:35Z

I would like to consider that before v1: https://github.com/kubernetes-sigs/kueue/issues/8607 which relates to https://github.com/kubernetes-sigs/kueue/issues/7035

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T11:36:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-15T11:40:56Z

/remove-lifecycle stale
