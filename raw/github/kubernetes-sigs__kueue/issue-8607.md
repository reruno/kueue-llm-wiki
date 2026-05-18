# Issue #8607: MultiKueue: invesigate alternative API for dispatcher API which does not suffer the SSA issues

**Summary**: MultiKueue: invesigate alternative API for dispatcher API which does not suffer the SSA issues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8607

**Last updated**: 2026-05-17T11:20:53Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-15T11:17:32Z
- **Updated**: 2026-05-17T11:20:53Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 6

## Description

**What would you like to be added**:

To investigate if we can design (or re-design the API) for the Dispatcher API which wouldn't suffer the issues for MultiKueue dispatcher API, that the external controllers need to use SSA with the `kueue-admission` as manager.

**Why is this needed**:

To simplify using MultiKueue Dispatcher API, see the docs: https://kueue.sigs.k8s.io/docs/concepts/multikueue/#external-custom-implementation

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T11:17:45Z

/priority important-longterm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:19:50Z

AFAIK, eliminating the limitation of the `kueue-admission` field manager is one of our motivations for MergePatch instead of SSA in Kueue Admission, right?

Why do we need to investigate alternatives?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T11:23:58Z

> AFAIK, eliminating the limitation of the kueue-admission field manager is one of our motivations for MergePatch instead of SSA in Kueue Admission, right?

Yes, that's right. 

> Why do we need to investigate alternatives?

Because if we manage to redesign the API which eliminates the problem, then we don't have currently any other motivation to use Patch, see: https://github.com/kubernetes-sigs/kueue/issues/7035#issuecomment-3754250002.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:33:46Z

> > AFAIK, eliminating the limitation of the kueue-admission field manager is one of our motivations for MergePatch instead of SSA in Kueue Admission, right?
> 
> Yes, that's right.
> 
> > Why do we need to investigate alternatives?
> 
> Because if we manage to redesign the API which eliminates the problem, then we don't have currently any other motivation to use Patch, see: [#7035 (comment)](https://github.com/kubernetes-sigs/kueue/issues/7035#issuecomment-3754250002).

Thank you for updating that. As I commented on #7035, I'm with you.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:19Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-17T11:20:51Z

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
