# Issue #4529: ProvisionRequest: GA Requirements

**Summary**: ProvisionRequest: GA Requirements

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4529

**Last updated**: 2025-08-11T15:59:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-03-08T16:05:04Z
- **Updated**: 2025-08-11T15:59:10Z
- **Closed**: 2025-08-11T15:59:10Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 6

## Description

I want to gather requirements on GA for ProvisiongRequests. The feature is beta in 0.5 and the graduation criteria in the KEP is vague.

Requirements: 

- [x] https://github.com/kubernetes-sigs/kueue/issues/2747
- [x] https://github.com/kubernetes-sigs/kueue/issues/3419

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-08T16:05:17Z

cc @elmiko @JoelSpeed

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-22T03:32:12Z

cc @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-24T20:07:50Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-25T05:54:08Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:14:47Z

@mimowo @tenzen-y 

Any reason why we can't graduate this to GA?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-11T15:30:03Z

> [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y)
> 
> Any reason why we can't graduate this to GA?

There is no blockers for graduation.
