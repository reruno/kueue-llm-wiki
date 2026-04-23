# Issue #6659: Graduate LendingLimit to GA

**Summary**: Graduate LendingLimit to GA

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6659

**Last updated**: 2026-03-25T06:46:56Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-08-24T16:10:27Z
- **Updated**: 2026-03-25T06:46:56Z
- **Closed**: —
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 8

## Description

LendingLimit feature gate has been beta since 0.9. Is there any reason not to graduate this to GA?

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T09:02:21Z

The blocker is FlavorFungibility. Before graduate LendingLimit to GA , we should define the FlavorFungibility specificaton then move to GA.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-26T18:32:37Z

> The blocker is FlavorFungibility. Before graduate LendingLimit to GA , we should define the FlavorFungibility specificaton then move to GA.

Is there an issue for that?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T06:38:05Z

> The blocker is FlavorFungibility. Before graduate LendingLimit to GA , we should define the FlavorFungibility specificaton then move to GA.

Can you elaborate why FlavorFungability graduation would block graduation of LendingLimit? I don't recall blockers / discussions on that.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-27T19:28:55Z

> > The blocker is FlavorFungibility. Before graduate LendingLimit to GA , we should define the FlavorFungibility specificaton then move to GA.
> 
> Can you elaborate why FlavorFungability graduation would block graduation of LendingLimit? I don't recall blockers / discussions on that.

@tenzen-y any ideas here?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-25T01:46:16Z

So for 0.16, can we promote this feature to GA?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-23T02:27:16Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-25T02:59:23Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-25T06:46:53Z

/remove-lifecycle rotten
