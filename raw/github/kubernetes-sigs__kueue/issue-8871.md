# Issue #8871: ☂️ Integration with WAS in kube-scheduler

**Summary**: ☂️ Integration with WAS in kube-scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8871

**Last updated**: 2026-10-25T13:44:47Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-29T13:42:58Z
- **Updated**: 2026-10-25T13:44:47Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `wg/workload-aware-scheduling`, `area/was`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 23

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make sure Kueue is compatible with WAS, and can delegate node-level scheduling to kube-scheduler.

This is an umbrella issue with a lot of work we need to identify as WAS is graduating.

Some of the related items:
- https://github.com/kubernetes-sigs/kueue/issues/13541
- https://github.com/kubernetes-sigs/kueue/issues/3755
- https://github.com/kubernetes-sigs/kueue/issues/13149
- https://github.com/kubernetes-sigs/kueue/issues/13151
- https://github.com/kubernetes-sigs/kueue/issues/13150
- https://github.com/kubernetes-sigs/kueue/issues/10548


Done:
- https://github.com/kubernetes-sigs/kueue/issues/8858

**Why is this needed**:

To leverage kube-scheduler primitives for:
- Gang Scheduling
- Dynamic Resource Allocation
- Topology-Aware Scheduling

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T13:43:18Z

cc @tenzen-y @gabesaba @sohankunkerkar @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-29T13:55:59Z

For those that are interested, there is a weekly call on Mondays at 1 pm EST to sync on WAS.

Right now my hope is to get workload controller support for gangs but there is a lot of changes for WAS.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-11T21:57:05Z

One area we may want to explore is using WAS to enforce gang scheduling for bare pods integration (https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#running-a-group-of-pods-to-be-admitted-together).

I think most controllers should handle gang scheduling in their own way but this is the one integration that kueue may need to create its own PodGroups/Workloads so that the grouping of pods can be gang scheduled together.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-12T12:55:48Z

> One area we may want to explore is using WAS to enforce gang scheduling for bare pods integration (https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#running-a-group-of-pods-to-be-admitted-together).
> 
> I think most controllers should handle gang scheduling in their own way but this is the one integration that kueue may need to create its own PodGroups/Workloads so that the grouping of pods can be gang scheduled together.

Yes, exactly. But the discussion point is how to handle if controllers create PodGroups / Workloads.
We might be able to just skip handling such a group of Pods if we are not missing any stuff.

### Comment by [@44past4](https://github.com/44past4) — 2026-02-24T07:38:46Z

I've drafted a proposal outlining the next steps for the WAS and Kueue integration: https://docs.google.com/document/d/13I3bMY-abBtsWmDhCl4RdDHKchHeB3G8zMSTpplmxHA/edit?usp=sharing

Please take a look and leave your feedback directly in the document.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T07:40:21Z

cc @tenzen-y @gabesaba @kannon92 @sohankunkerkar ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-14T09:17:58Z

Here is the discussion doc, including the integration with Kueue: https://docs.google.com/document/d/1MASczp_dvKXjrbhExePxMZfasZN8ukaHopP7y_bNom4

And we already have the scheduler-library: https://github.com/kubernetes-sigs/scheduler-library

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-15T16:34:30Z

/assign @kshalot 
who is already working on the integration

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-06-01T14:27:24Z

@helayoty: The label(s) `wg/workload-aware-scheduling` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8871#issuecomment-4593522427):

>/wg workload-aware-scheduling


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@helayoty](https://github.com/helayoty) — 2026-06-02T16:32:41Z

/wg workload-aware-scheduling

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-06-10T15:50:17Z

@kshalot, could you provide some updates on where we are with the scheduler library effort? I haven't seen any activity in the codebase for the last two months.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-06-15T13:47:38Z

@sohankunkerkar I wrote a proof-of-concept minimal integration back in May before I had to temporarily drop this in favor of bigger priorities.

Today I got back to this and I opened https://github.com/kubernetes-sigs/kueue/pull/12256 where the plan is to get a foot in the door with the `scheduler-library` package and do some naive state tracking to have a baseline performance reading that we can iterate on (nodes only with pods tracking and a full fit check coming next).

Meanwhile, we also have to wait for https://github.com/kubernetes-sigs/scheduler-library/pull/2 to be merged so we don't merge code which relies on a fork.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-01T14:03:41Z

/area was

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-07-01T14:03:45Z

@mimowo: The label(s) `area/was` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8871#issuecomment-4855907785):

>/area was


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-15T07:06:06Z

We are going to include the first set of integration PRs in 0.19, behind an Alpha feature gate, and with very limited scope. As summarized in https://github.com/kubernetes-sigs/kueue/pull/13045#issuecomment-4973037163, in 3 steps:
1. scheduler-library depenency
2. refactor of our scheduling code to use SchedulerSimulation interface (ortoghonal to 1, could be merged independently). The objective is to have all the integration code as the interface impl, scoped to one package. This way if we need to bailout we will be able to eaily delete the package or comment the code out.
3. small use of the SchdulerSimulation library just to check feasibility of nodes in TAS (behind a Alpha feature gate)

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-07-15T12:13:54Z

Thanks for driving this forward! I think this integration would eventually benefit from a KEP, as it opens the door to a number of additional integration use cases for Kueue, such as https://github.com/kubernetes-sigs/kueue/issues/12422.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-15T12:55:22Z

Sure, I want to have a KEP too, @kshalot has it in tasks. However the initial phase for 0.19 is  very minimal (dep, interface and feasibility check)- as posted in the comment.  So I think in this case we can add the KEP post 0.19

### Comment by [@kannon92](https://github.com/kannon92) — 2026-07-15T13:37:31Z

I've been thinking of drafting something for Kueue for WAS also.

I was going to focus on controller integrations with WAS (Job, JobSet, Kueue's PodGroups) and maybe sketch a path forward for 1.37.

The other areas that are relevant for WAS are Workload aware preemption and Workload Priority Class (Kueue). Should I consider dedicated KEPs for each of these?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-15T15:23:13Z

Maybe we can dicuss that in wg-batch how to devide the work into smaller KEP pieces

### Comment by [@44past4](https://github.com/44past4) — 2026-07-20T07:05:23Z

/area was

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-20T07:17:10Z

Updated the list of issues with the newly created work streams by @44past4

### Comment by [@kshalot](https://github.com/kshalot) — 2026-07-21T20:41:26Z

Now that https://github.com/kubernetes-sigs/kueue/pull/13261 is merged I think we should focus on streamlining the work around WAS in Kueue. I created https://github.com/kubernetes-sigs/kueue/pull/13261 to start by creating a KEP/KEPs for the ongoing work/north-star.

> Maybe we can dicuss that in wg-batch how to devide the work into smaller KEP pieces

Agreed.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-10-25T13:44:44Z

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
