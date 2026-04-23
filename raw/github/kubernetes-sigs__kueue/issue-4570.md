# Issue #4570: TAS: Add TAS profiles that allows to pick a desired algorithm

**Summary**: TAS: Add TAS profiles that allows to pick a desired algorithm

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4570

**Last updated**: 2025-10-10T09:46:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-03-12T14:21:40Z
- **Updated**: 2025-10-10T09:46:27Z
- **Closed**: 2025-10-10T09:46:26Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 28

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to have a TAS configuration that would allow user to pick a desired algorithm, and maybe even set approriate parameters if they're any.
As an intermediate solution we could have feature gates that would act as switches between various algorithms, but after gathering users feedback we should invest into API

**Why is this needed**:
Different workloads might have different topological requirements. We should allow users to pick an algorithm which is the most suitable for their needs

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-12T14:22:30Z

cc @mimowo

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T15:01:16Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T15:09:43Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T15:29:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T18:18:01Z

/remove-lifecycle stale

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-26T12:46:12Z

May I ask what's the current status of this request?

I'm asking because, looking at the KEP (specifically [here](https://github.com/kubernetes-sigs/kueue/blob/d9f2f8615f6a4975d2fb92bf9d394e6d084783d0/keps/2724-topology-aware-scheduling/README.md?plain=1#L1051-L1061)), all existing "TAP profiles" are described as "deprecated", "not recommended" etc.

Then, the KEP says:

> Based on the collected feedback we will introduce TAS configuration (...)

So I guess this task is about this. \
But then - have we already collected the feedback? Do we understand what sorts of profiles would be useful? \
(And am I right that this task is not actionable without this knowledge?)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T12:55:25Z

> May I ask what's the current status of this request?

The task remains open and valid for 0.15

> But then - have we already collected the feedback? 

To some extent we already have feedback:
We hear from users who use default, and TASProfileMixed. I don't know we have users on TASProfileLeastFreeCapacity (I hope we have deprecate it and eventually delete). cc @mwysokin 

We also hear feedback from users requesting "balanced" mode: https://github.com/kubernetes-sigs/kueue/issues/6554 cc @pajakd @mwysokin 

So the config should be flexible enough to cover: Default, TASProfileMixed, and Balanced. We need to agree on the details of the API and naming. Once we conclude the design (in the KEP) and implement, then we can drop the feature gates.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T12:56:58Z

I guess we could even consider deprecation of TASProfileLeastFreeCapacity still for 0.14, wdyt @mwysokin ?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-29T09:45:16Z

We know about users that actually use LeastFreeCapacity algorithm, so I'd like to be careful about deprecating the `TASProfileLeastFreeCapacity`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T09:53:22Z

Actually, IIUC the users who providing this feedback are using TASProfileMixed. So while the algorithm is in use for the "unconstrained", I think we don't have any indication of the `TASProfileLeastFreeCapacity` to be useful as a config knob for "preferred and required".

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-29T10:03:30Z

> Actually, IIUC the users who providing this feedback are using TASProfileMixed. So while the algorithm is in use for the "unconstrained", I think we don't have any indication of the `TASProfileLeastFreeCapacity` to be useful as a config knob for "preferred and required".

Yes, I didn't mean we shouldn't drop the FG. I wanted to double check if anybody uses the FG itself, as there are users that use the algorithm

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-30T20:56:32Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-30T21:12:53Z

Before proceeding, I'd like to consult _where_ (on which object) this config should be defined.

Should it be a new property of `ResourceFlavorSpec`? \
This seems well in line with the original motivation in #6554:

> The main motivation is to provide great default experience for GB200.

(So, my reading is: "balanced vs. greedy" depends mainly on node type, which is best captured by ResourceFlavor).

---

Some alternatives I considered (and rejected):

- Per cluster, in Kueue `Configuration`. \
  That would be in line with various other settings, and closest to a "feature gate". However, the intro to this issue:

  > Different workloads might have different topological requirements. We should allow users to pick an algorithm which is the most suitable for their needs

  suggests that we may prefer sth more fine-grained.

- Per each workload (= the opposite extreme). \
  Most powerful but least elegant. (As Workloads are auto-generated, we'd need to put it on the owner resources - Jobs, JobSets etc. - and because these have different types, we'd likely end up using annotations - like for topology requests - which isn't nicely typed).
  * BTW, _if_ we choose to have it per workload, _then_ I'll propose to drop the concept of "TAS Profiles" and instead let the users specify "TAS Algorithms" directly. This would have some benefit of simplicity - though I'm still not enthusiastic about introducing new annotations. Feels too prone for typos, hard to debug on user's side.

- Per ClusterQueue. \
  Avoids the cons of both extremes - but, as long as "balanced vs. greedy" depends mostly on node type, ResourceFlavors seem just a better fit.

---

Does this make sense, so far?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-10-01T13:31:10Z

I agree with what you've said about alternatives, and I think there are better options than any of these 3. When it comes to where to place the API, `Topology` was my first thought, to keep all the whole topology-related API in one place.

Nevertheless, this change definitely deserves changes to KEP, and I think it's the best place to keep all the proposal and alternatives

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-10-01T13:33:12Z

> Yes, I didn't mean we shouldn't drop the FG. I wanted to double check if anybody uses the FG itself, as there are users that use the algorithm

I've done it and the user doesnt use the FG, they use `Mixed` profile just like mimowo had said before. Hence, we're good to go with removing the `LeastFreeCapacity` profile

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:40:52Z

I like simplicity, so I would like to reconsider thee global configuration option which was rejected so far. 

> Different workloads might have different topological requirements. We should allow users to pick an algorithm which is the most suitable for their needs

These can be expressed by the annotations too. So, I don't think it undermines the global config as default.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:44:33Z

> When it comes to where to place the API, Topology was my first thought, to keep all the whole topology-related API in one place

Actually, Topology is the last option I'm thinking about :). I think Topology name suggests it is only static description of the  cluster, not scheduling profiles or algos. Actually, Topology is discussed as an API to follow  by other orchestrating schedulers, like maybe core  k8s  scheduler. I imagine these will want to have scheduling configuration outside of the Topology object.

My first thought is global Mixed, but overridable by Workloads.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-01T13:45:19Z

@mimowo So your proposal would be to have it _both_ 

* in the global config (to specify the global default), and
* in the job's annotations (as an optional one-off override)

Am I getting it right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:45:52Z

My  second choice is  probably ResourceFlavor level, next to spec.TopologyName field we could maybe have `spec.tasConfig`, but I'm not sure  if this is not overkill.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:46:41Z

> [@mimowo](https://github.com/mimowo) So your proposal would be to have it _both_
> 
> * in the global config (to specify the global default), and
> * in the job's annotations (as an optional one-off override)
> 
> Am I getting it right?

Exactly, this is already happening in the Mixed mode - required and preferred is using BestFit, while unconstrained is using LeastFreeCapacity.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:53:36Z

As a nice-to-have I would like to freeze introducing new APIs for 0.15. So that  we can just graduate all v1beta1 to v1beta2 for simplicity. Still, if we have a good reason to introduce TASConfig API as Alpha this is possible, but would like like to consider this as a "fallback" option if the global Configuration is not enough.

EDIT: but overall +1 for deeper discussion of available  options

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-02T09:09:41Z

> _Still, if we have a good reason to introduce TASConfig API as Alpha this is possible, but would like like to consider this as a "fallback" option if the global Configuration is not enough._

I'm not sure how to understand this. \
Wouldn't "[adding a field to] the global Configuration" already count as "introducing TASConfig API"?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T11:50:24Z

Actually Confguration API is just golang struct that is serialized into the configMap as text, and saved onto the Kueue's Pod volume. In that case TASConfig is just a struct inside. In other words this Configuration API is not represented as CRD.

We can consider extending the Topology API or ResourceFlavor API with TASConfig as a struct (not a top-level API). When I was posting the comment I was assuming TASConfig API would be another top-level API. 

I would like to also take a step back and think if we need the configuration at all this point. I'm thinking that maybe we should instead just make the TASPofileMixed our default. It aligns on "preferred" and "required" with current default, and for "unconstrained" the user "does not care", and so Kueue can optimize for fragmentation. If we eliminate the current default, and TASProfileLeastFreeCapacity, then we stay with just TASPofileMixed as the new default, and the need for configuration is not clear any longer.

Now, the need for configuration will come with the Balanced Placement policy.

So, my proposal would be:
1. make `TASPofileMixed` as the new default and deprecate all other currently existing
2. design how to introduce configuration for Balanced Placement

For (1.)  we would need to have a "safety feature gate" to bailout when users complain about changing the default, but I think it is very unlikely.

For (2.) in 0.15 we can go with feature gate. Long term either Topology API or Configuration API make sense to me. Actually, Topology makes sense, because likely balanced placement is need for specific hardware, which likely will have dedicated Topology (although I'm not totally clear at this point).

cc @mwysokin @PBundyra for thoughts

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-02T14:30:53Z

> 1. make TASPofileMixed as the new default and deprecate all other currently existing
> 
> For (1.) we would need to have a "safety feature gate" to bailout when users complain about changing the default, but I think it is very unlikely.

I'm focusing on this part. For the start, PTAL at #7144 if such an interface change would make sense.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-09T07:41:57Z

I created #7214 to track step 1 (switch the default profile).

Then, this issue can track step 2 (which it was originally about).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-10T09:17:45Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T09:46:21Z

/close
To avoid distractions, as with https://github.com/kubernetes-sigs/kueue/issues/7214 we don't have any indication that the configuration is currently needed. Sure, we are going to work on balanced placement, but we can think of the dedicated configuration for that problem: https://github.com/kubernetes-sigs/kueue/issues/6554. 

I don't see a need for now for "rule them all" configuration.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-10T09:46:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4570#issuecomment-3389118357):

>/close
>To avoid distractions, as with https://github.com/kubernetes-sigs/kueue/issues/7214 we don't have any indication that the configuration is currently needed. Sure, we are going to work on balanced placement, but we can think of the dedicated configuration for that problem: https://github.com/kubernetes-sigs/kueue/issues/6554. 
>
>I don't see a need for now for "rule them all" configuration.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
