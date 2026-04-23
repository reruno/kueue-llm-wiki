# Issue #330: Rename the namespaced resource "Queue"

**Summary**: Rename the namespaced resource "Queue"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/330

**Last updated**: 2022-08-26T20:52:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-08-13T13:17:51Z
- **Updated**: 2022-08-26T20:52:17Z
- **Closed**: 2022-08-26T20:52:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Rename the namespaced resource `Queue`. Possible alternatives: LocalQueue

and if we feel bold about an even bigger refactor, may be we also rename `ClusterQueue` to `GlobalQueue` to have consistent naming with `LocalQueue` :)

Other naming alternatives?

**Why is this needed**:
Kueue has two types of queues, namespaced and cluster-scoped. Naming the former just Queue gives the impression that it is the main resource governing queueing, including execution order and quotas, while in reality it is the ClusterQueue that enforces those semantics.

Renaming Queue would help clarify that the namespaced resource is secondary to the cluster-scoped one.


**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-15T14:30:33Z

An additional question is whether it's worth the effort doing this for the 0.2.0 release.

It is a breaking change, so we should add it as v1alpha2. However, we should probably not support v1alpha1 at the same time. 

Do you think the name change would be beneficial? Can we make it a breaking change?

cc @ArangoGutierrez @denkensk @kerthcet

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-15T15:38:23Z

It is a breaking change, but one that is allowed by k8s's deprecation policy of v1alpha1 (assuming we are following that policy). I don't think we need to base our decision on this, but focus on whether this will make the API better longer term.

My feeling is that introducing the prefix `Local` will 
-  clarify the confusion about the purpose of the namespaced resource; `Queue` alone gives the impression that it is THE queue, but in reality it is not.
-  make the distinction between the two queue types clearer since each will now have a prefix; which will also make it easier to communicate in both docs and conversations

### Comment by [@mrozacki](https://github.com/mrozacki) — 2022-08-15T15:48:32Z

I like  the change to local queue. Helps clarify the purpose. Switching the cluster queue to global queue is less appealing. At some point we might want to manage multi-cluster queues. We'd run into confusion problems with global and multi cluster queues.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-15T15:52:24Z

> An additional question is whether it's worth the effort doing this for the 0.2.0 release.

If we want to do it, I think we should do it in 0.2.0

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-16T09:21:42Z

For alpha API if it really benefits, I think we can deprecate it right now. It follows the rule documented by the `Kubernetes Deprecation Policy`. 

Honestly, when I first read the designs, I'm also confused. I thought the queue controls the queueing and the clusterQueue acts like a resource pool for sharing. But that's why documents exist, naming is hard and people may have different understandings by their knowledges.

From my point of view, `LocalQueue` doesn't eliminates confusions a lot, for we still have the word `queue`, people may still think it's a semantic queue and maybe mess this up with the clusterQueue, but actually they're different things. The good thing is that it's easy to tell localQueue is a namespace-scoped resource.

Considering we only published two releases, kueue is  not mature enough, we should gather more feedbacks and maybe the scope of `queue` and `clusterQueue` will change in the near future. So alternatively we can change the name uniformly before a mature one, like v1.0.0, I don't know.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-16T13:31:35Z

Changing the name now (before 0.2) has the benefit that we wouldn't be breaking too many users if we don't maintain both APIs (v1alpha1 and v1alpha2).

It sounds like just adding `Local` at least makes users think twice. Then they can clarify from the docs.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-16T18:15:11Z

Note that the namespaced `Queue` is an actual queue, it does influence the order of the jobs submitted to it. Moreover, we can potentially add queueing strategy to it that is different from the ClusterQueue one, which could include a simple workflow strategy where only one job can start at a time.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-18T16:02:27Z

/assign @ahg-g

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-26T20:52:17Z

this is done
