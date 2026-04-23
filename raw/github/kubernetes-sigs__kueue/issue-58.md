# Issue #58: Validating that flavors of a resource are different

**Summary**: Validating that flavors of a resource are different

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/58

**Last updated**: 2022-07-14T14:52:47Z

---

## Metadata

- **State**: open
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-24T02:25:35Z
- **Updated**: 2022-07-14T14:52:47Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 11

## Description

What if we validate that the flavors of a resource in a capacity have at least on common label key with different values?

This practically forces that each flavor is pointing to different sets of nodes.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-24T02:52:07Z

Is the "common label key" officially defined or user-defined ?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-24T13:03:37Z

User defined, we can validate that on create.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T15:15:02Z

I worry that this could be limiting. In GKE, we don't have a label for non-spot VMs. They are rather defined by the absence of the label. Should we add a label selector instead?

I suspect there might be similar scenarios in other environments.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-01T19:34:06Z

Let me state the problem that I am trying to solve with this: 

We need to force the scheduler to place the pods on the selected flavor; currently this is done by injecting node affinity of the selected flavor labels, if a common label doesn't exist, then there is nothing forcing the scheduler to comply with Kueue's decision.

We discussed adding a selector to flavors instead of labels at the beginning; which would allow having `NotIn` selectors for the flavors that don't have the selected label, but I think selector is not intuitive to think about in this context and is not synonym with how we do that for nodes (which in a sense represent resource flavors).

Ideally flavors should have labels that uniquely distinguishes them, perhaps for flavors with missing labels we inject `NotIn` affinity constraints.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-02T18:50:29Z

We can have "flavors have labels that uniquely distinguish them" as a best practice, but it's actually not trivial to enforce if we add a ResourceFlavor CRD #59.

To increase generality of the API, we could still have a label selector but limit the operators to the ones that make sense.

>  is not synonym with how we do that for nodes (which in a sense represent resource flavors).

Can you expand on this?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T21:15:48Z

My problem is this: flavors look very artificial if we don't force that they are distinct and map to different types of nodes.  For example, even if we define a taint for spot flavor, without unique labels, jobs assigned to this flavor could land on on-demand nodes, this is not a good experience.

> To increase generality of the API, we could still have a label selector but limit the operators to the ones that make sense.

hmm, this will allow flavors with overlapping nodes and not necessarily force that flavors are different.

> Can you expand on this?

I think of different flavors as different types of nodes. We don't identify nodes with selectors, we do with labels.

Mapping flavors to different node types will be the most common case to using flavors, and I feel we need to be opinionated about it and I also think this will offer better out of the box experience.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-16T13:03:47Z

> I feel we need to be opinionated about it and I also think this will offer better out of the box experience.

How much of it should actually be enforced vs stated as best practices.

Since we are going to split ResourceFlavors into a CRD, it don't think it's easy to enforce.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-16T13:10:31Z

> How much of it should actually be enforced vs stated as best practices.

I think it needs to be enforced, at least the default should be to enforce it.

> Since we are going to split ResourceFlavors into a CRD, it don't think it's easy to enforce.

A bit aggressive, but we can do the following: each flavor will have a label added using a common key (`flavor.kueue.x-k8s.io/${resource}`) and a value of the flavor name (were ${resource} is "cpu", "memory" etc.).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-06-14T14:11:47Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-14T14:46:53Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-14T14:52:46Z

/lifecycle frozen
