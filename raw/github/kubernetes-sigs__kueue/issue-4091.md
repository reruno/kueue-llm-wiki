# Issue #4091: Add more logs to TAS

**Summary**: Add more logs to TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4091

**Last updated**: 2025-09-28T19:52:00Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-01-29T13:14:38Z
- **Updated**: 2025-09-28T19:52:00Z
- **Closed**: 2025-09-28T19:51:59Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to add more logs with e.g. 3 or 5 level of verbosity to TAS, so it's easier to debug an issue. In particular I believe it would be very useful to log:
- [nodes after listing them](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/tas_flavor.go#L95) so we can compare them with actual resource on a cluster, and check if nodeSelectors, taints work as intended;
- [state of domains](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/tas_flavor_snapshot.go#L242) to validate if domains have intended values

This list is not exhaustive though, I'm open to discuss further improvements. Those are the places I find valuable, and helped me with debugging 

**Why is this needed**:
Ease debugging TAS issues 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-29T13:15:57Z

cc @mimowo @tenzen-y @mbobrovskyi 

Are you aware of any code in TAS that could use more logs for debugging purposes?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T06:40:38Z

Not at the moment, I think for debuggability it would also be great to implement the snapshot dump for TAS https://github.com/kubernetes-sigs/kueue/issues/3493. This might overlap in some debugging use-cases, but more logs would be great anyway.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-08T17:57:48Z

> cc [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) [@mbobrovskyi](https://github.com/mbobrovskyi)
> 
> Are you aware of any code in TAS that could use more logs for debugging purposes?

I do not have any other potential places.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T13:45:28Z

I think we already have a function to log the state of domains after this PR lands https://github.com/kubernetes-sigs/kueue/pull/4295#discussion_r1987195979. We have two options to call it:
1. just after finished building the snapshot
2. from within Find function 

Now, 2. is more verbose in case of scheduling multiple workloads or performing preemptions.  OTOH if we do only do 1. then debugging assignment for 3rd workload might be hard, so I think we need 2, to control verbosity maybe we have 1. at V4 and 2. at V5.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T13:55:56Z

/assign @vladikkuzn 
PTAL

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-04-28T22:51:27Z

Slightly related request (let me know if you'd like me to create a separate feature request for this), it would be helpful for Kueue admins if more information about Kueue's current understanding of healthy capacity for TAS was available in the ClusterQueue status

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-29T09:47:49Z

> Slightly related request (let me know if you'd like me to create a separate feature request for this), it would be helpful for Kueue admins if more information about Kueue's current understanding of healthy capacity for TAS was available in the ClusterQueue status

Thanks for input! Since this requires API changes, I think it's better to track in a separate feature request. However, if you wanted to see logs with current Kueue's understanding of capacity, please see https://github.com/kubernetes-sigs/kueue/pull/4295

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T05:57:53Z

> Kueue's current understanding of healthy capacity for TAS

Could you provide more exact examples? Do you want to expose the topolog / group that TAS computed based on Node status?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-05-01T16:45:14Z

> > Slightly related request (let me know if you'd like me to create a separate feature request for this), it would be helpful for Kueue admins if more information about Kueue's current understanding of healthy capacity for TAS was available in the ClusterQueue status
> 
> Thanks for input! Since this requires API changes, I think it's better to track in a separate feature request. However, if you wanted to see logs with current Kueue's understanding of capacity, please see [#4295](https://github.com/kubernetes-sigs/kueue/pull/4295)

> > Kueue's current understanding of healthy capacity for TAS
> 
> Could you provide more exact examples? Do you want to expose the topolog / group that TAS computed based on Node status?

I created https://github.com/kubernetes-sigs/kueue/issues/5147 with some more concrete examples

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T18:46:57Z

> > > Slightly related request (let me know if you'd like me to create a separate feature request for this), it would be helpful for Kueue admins if more information about Kueue's current understanding of healthy capacity for TAS was available in the ClusterQueue status
> > 
> > 
> > Thanks for input! Since this requires API changes, I think it's better to track in a separate feature request. However, if you wanted to see logs with current Kueue's understanding of capacity, please see [#4295](https://github.com/kubernetes-sigs/kueue/pull/4295)
> 
> > > Kueue's current understanding of healthy capacity for TAS
> > 
> > 
> > Could you provide more exact examples? Do you want to expose the topolog / group that TAS computed based on Node status?
> 
> I created [#5147](https://github.com/kubernetes-sigs/kueue/issues/5147) with some more concrete examples

Thanks

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-30T19:23:09Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-29T19:31:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-28T19:51:55Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-28T19:52:00Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4091#issuecomment-3344195627):

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
