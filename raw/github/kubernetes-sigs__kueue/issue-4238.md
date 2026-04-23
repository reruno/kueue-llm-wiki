# Issue #4238: Prepare the FlavorFungibility feature to graduate to GA

**Summary**: Prepare the FlavorFungibility feature to graduate to GA

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4238

**Last updated**: 2026-01-16T20:18:22Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-12T09:32:32Z
- **Updated**: 2026-01-16T20:18:22Z
- **Closed**: 2026-01-16T20:18:21Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:

To prepare the feature graduation to GA, and potentially move on with the graduation.

KEP for reference: https://github.com/kubernetes-sigs/kueue/blob/main/keps/582-preempt-based-on-flavor-order/README.md

I'm not aware of blockers for the graduation, but let's start with KEP refresh.  Unfortunately there are no clear graduation criteria. 

**Why is this needed**:

- to eliminate the code complication related to maintaining two paths in code
- to build trust to users of the feature that it can be relied on
- to build trust to the users of Kueue by showing that features graduate to GA eventually
  

**Completion requirements**:



This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:23:02Z

+1

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-18T13:30:26Z

Should we wait until the dust settles in #3948 before promoting this to GA? FlavorFungibility will be impacted by its fix, as borrowing/preemption will no longer be a binary signal, but perhaps an integer - e.g. at how many levels in the CohortTree do we have to borrow; from which level is reclaim possible (more distant reclaim better, as it is not impacting more local Cohort Subtrees)

OTOH, the semantics are still the same - we _may_ try to find a better flavor if FlavorFungibility defines this policy. Though the definition of "better" is more complicated

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T14:22:44Z

> Should we wait until the dust settles in [#3948](https://github.com/kubernetes-sigs/kueue/issues/3948) before promoting this to GA? FlavorFungibility will be impacted by its fix, as borrowing/preemption will no longer be a binary signal, but perhaps an integer - e.g. at how many levels in the CohortTree do we have to borrow; from which level is reclaim possible (more distant reclaim better, as it is not impacting more local Cohort Subtrees)
> 
> OTOH, the semantics are still the same - we _may_ try to find a better flavor if FlavorFungibility defines this policy. Though the definition of "better" is more complicated

Does that mean we keep holding with the Beta stage until https://github.com/kubernetes-sigs/kueue/pull/4165 is merged?
In that case, that sounds reasonable.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-18T14:42:32Z

> > Should we wait until the dust settles in [#3948](https://github.com/kubernetes-sigs/kueue/issues/3948) before promoting this to GA? FlavorFungibility will be impacted by its fix, as borrowing/preemption will no longer be a binary signal, but perhaps an integer - e.g. at how many levels in the CohortTree do we have to borrow; from which level is reclaim possible (more distant reclaim better, as it is not impacting more local Cohort Subtrees)
> > OTOH, the semantics are still the same - we _may_ try to find a better flavor if FlavorFungibility defines this policy. Though the definition of "better" is more complicated
> 
> Does that mean we keep holding with the Beta stage until [#4165](https://github.com/kubernetes-sigs/kueue/pull/4165) is merged? In that case, that sounds reasonable.

Until #3948 is fixed, as it is slightly different issue - though related

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-18T15:19:22Z

> > > Should we wait until the dust settles in [#3948](https://github.com/kubernetes-sigs/kueue/issues/3948) before promoting this to GA? FlavorFungibility will be impacted by its fix, as borrowing/preemption will no longer be a binary signal, but perhaps an integer - e.g. at how many levels in the CohortTree do we have to borrow; from which level is reclaim possible (more distant reclaim better, as it is not impacting more local Cohort Subtrees)
> > > OTOH, the semantics are still the same - we _may_ try to find a better flavor if FlavorFungibility defines this policy. Though the definition of "better" is more complicated
> > 
> > 
> > Does that mean we keep holding with the Beta stage until [#4165](https://github.com/kubernetes-sigs/kueue/pull/4165) is merged? In that case, that sounds reasonable.
> 
> Until [#3948](https://github.com/kubernetes-sigs/kueue/issues/3948) is fixed, as it is slightly different issue - though related

Oh, that's right. Thank you for pointing it out. I guess that we can graduate FlavorFungibility once HierarchyCohort to Beta. Because we can assume to graduate HierarchyCohort to Beta once we support combinations between HierarchyCohort and other Beta or GA features.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-19T16:09:37Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T08:53:27Z

/remove-lifecycle stale

> Should we wait until the dust settles in [#3948](https://github.com/kubernetes-sigs/kueue/issues/3948) before promoting this to GA? FlavorFungibility will be impacted by its fix, as borrowing/preemption will no longer be a binary signal, but perhaps an integer - e.g. at how many levels in the CohortTree do we have to borrow; from which level is reclaim possible (more distant reclaim better, as it is not impacting more local Cohort Subtrees)

This still needs some thought, about how we will handle FlavorFungibility in the hierarchical case, after fixing #3948

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-18T09:02:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:55:06Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-17T19:35:13Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T19:45:04Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-16T20:18:17Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-16T20:18:22Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4238#issuecomment-3761655237):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
