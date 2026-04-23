# Issue #312: Add FlavorAssignmentStrategy or flavor priorities to ClusterQueue

**Summary**: Add FlavorAssignmentStrategy or flavor priorities to ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/312

**Last updated**: 2023-02-07T14:48:16Z

---

## Metadata

- **State**: open
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-04T20:52:07Z
- **Updated**: 2023-02-07T14:48:16Z
- **Closed**: —
- **Labels**: `kind/feature`, `kind/api-change`, `lifecycle/frozen`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 23

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A field in ClusterQueueSpec to influence how flavors are selected when there is already some quota in use.

**Why is this needed**:

Currently, we strictly go in the order determined by the ClusterQueue resource. But cluster administrators might need different optimization criteria, for example:
- `InOrder`: current behavior. It could be used to minimize cost. Cheaper resources can be listed first.
- `MinimizeBorrowing`: Choose the flavor that minimizes borrowing. Since a flavor could involve multiple resources, they borrowing can be expressed as percentage of the total request. This can be used to minimize disruptions once preemption is supported.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-04T20:53:02Z

/kind api-change

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T07:58:41Z

It seems like it's part of https://github.com/kubernetes-sigs/kueue/issues/171, I'd like to take a look so we can release 0.2.0 soon.
/assign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-19T08:00:39Z

Sorry, it actually should be https://github.com/kubernetes-sigs/kueue/issues/328, but I can also take a look of this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-19T13:33:05Z

This is not part of #328. Yes, it will need to be validated, but we don't have this field yet.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-22T10:29:44Z

I thought about it a little, I think `minimizeBorrowing` should be the default policy we should follow, we can borrow resources but we should avoid it if possible for sharing between clusterQueues can be break up.

Besides, rather than prioritize the flavors by the slice order, maybe we should a new field `priority`, this is a more common style and easy to organize the configurations. And yes, this should also be a default policy.

I don't know whether we should introduce policies like binpack/spread/balanced to FlavorAssignmentStrategy(or FlavorManageStrategy), if we do, it seems we reinvent the wheels in scheduling. I think we can let this fly for a while until community users really need it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-23T02:37:52Z

cc @alculquicondor for thoughts

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T13:12:18Z

We can only change the default behavior if we introduce a new API version. We can probably do it as we launch v1beta1.

> maybe we should a new field priority

I don't think that adds much value. Going in order is a clear API.

> I don't know whether we should introduce policies like binpack/spread/balanced to FlavorAssignmentStrategy

As long as there is a valid use case, we can consider it. Otherwise, I would start with the obvious ones: InOrder, MinimizeBorrowing.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-23T15:37:54Z


> > maybe we should a new field priority
> 
> I don't think that adds much value. Going in order is a clear API.
>
They can't express the meaning that two flavors are of the same priority. This is useful when we want to apply more policies on flavors, like minimizeBorrowing by priority.

But as you say, let's wait to see if we really need them.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T16:08:20Z

but if you use `minimizeBorrowing`, we would first sort by how much they borrow. If there are multiple flavors that borrow the same (or borrow nothing), we fallback to the order in the list. It is comprehensive enough, in my opinion.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T10:52:01Z

I think priority should be the first decision factor, then we apply other policies. 
Whatever, I'll try to implement these two strategies as mentioned and evolve gradually.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T13:44:15Z

I see what you mean. You want to do minimizeBorrowing within a group of flavors. Then, if it doesn't fit, go to the next group of flavors which have lower priority.

To keep some level of "backwards compatibility", we can add a validation rule that priorities can only be decreasing in the list.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T15:41:06Z

So the conclusion is:
1) Add a new field `Priority` to api field `Flavor`
```
type Flavor struct {
	Name ResourceFlavorReference `json:"name"`
	Quota Quota `json:"quota"`
        Priority `json:"priority"`
}
```

2) Add a strategy `minimizeBorrowing`. (We may consider it as a default policy when graduating to a new version)

3) Add a validation rule that priorities can only be decreasing in the list. (We may cancel this when graduating to a new version?)

Right?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T15:53:24Z

1. I agree, although probably a pointer.
2. Do we have another strategy? Once you add priority, minimizeBorrowing seems like the only reasonable option for flavors with the same priority.
3. I would always keep the validation. It makes the API easier to interpret by a human. Also it would be nice if you don't have to define priorities if you don't need them. Then I'm not sure if we should add default priorities (all zero or decreasing)?

Maybe worth a design doc after all? It doesn't have to be long.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T23:44:28Z

Yes, I'll write a simplify KEP for this.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-09-20T06:36:50Z

FYI: I'm already working on this, but considering the k/k KEP deadline is approaching and I'll have a holiday in Oct., let me focus on k/k first, and turn back ASAP.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-20T13:40:59Z

yup, k/k deadlines are tight

FYI #401

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-19T13:50:07Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-21T18:50:42Z

/lifecycle frozen

### Comment by [@maaft](https://github.com/maaft) — 2023-02-07T11:18:12Z

Hi, any eta for this? I'd really like to use preemption and as far as I see, this is the only blocker left for v0.3! :rocket:

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-07T11:53:33Z

This might be after https://github.com/kubernetes-sigs/kueue/pull/532/, and the design may also be changed(TBD) since we changed the API, so likely this will not be included in v0.3(preemption is already big enough), but I'll try my best, Let's see. I'm working on another feature now.

### Comment by [@maaft](https://github.com/maaft) — 2023-02-07T12:02:36Z

just to confirm: preemption will be included in v0.3 regardless of this feature? That'll be great :)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-07T12:38:21Z

> just to confirm: preemption will be included in v0.3 regardless of this feature? That'll be great :)

It's not great, it's my bad... :(

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-07T14:48:16Z

Yes, preemption is independent of this feature.
I'm also working on #532 before the release.
