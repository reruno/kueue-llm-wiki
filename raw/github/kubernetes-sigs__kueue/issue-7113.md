# Issue #7113: ☂️ Graduate API to v1beta2

**Summary**: ☂️ Graduate API to v1beta2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7113

**Last updated**: 2025-11-17T08:02:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-01T08:22:22Z
- **Updated**: 2025-11-17T08:02:48Z
- **Closed**: 2025-11-17T08:02:47Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 20

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to graduate the API to v1beta2.

I've done preliminary review of the wishlist in the [doc](https://docs.google.com/document/d/1UK_DnZ1Q4sUz8u9hYUTJexfw79z8pYwd9dtXEvXoEuE/).

This is going to be an interim step before [v1 graduation](https://github.com/kubernetes-sigs/kueue/issues/768).

**Why is this needed**:

To eliminate the API issues reported in the [v1beta2 wishlist](https://github.com/kubernetes-sigs/kueue/issues/768).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T08:22:28Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T08:22:55Z

cc @tenzen-y @gabesaba @mwysokin @mwielgus @kannon92 @amy

### Comment by [@amy](https://github.com/amy) — 2025-10-01T12:09:54Z

(maybe as a separate thread) would it be possible to also discuss a conversion webhook?

If there's any API change that involves changing CRD versions and underlying field types in the CRD, upgrading would be complicated and interrupting without one.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T12:11:54Z

Yes, conversion webhook is going to be part of the solution. I think we will need to maintain v1beta1 for 2 releases at least.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T13:09:20Z

Before we open the final PR for graduation, we could open a PR that has just new Go scheme just for API review which does not have conversion webhooks, and controller code changes.

After we reviewed the PR, we can open new final PR which has every scheme and implementation changes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:23:47Z

Yes, my goal is to make reviewing easy, so my idea for PRs is something like:
1 v1beta2 is just copy of v1beta1
2. update changes for v1beta2 (main diff)
3. implementation is using v1beta2
4. conversion webhooks

To make this happen fully we should start in two weeks or so.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T14:04:38Z

> Yes, my goal is to make reviewing easy, so my idea for PRs is something like: 1 v1beta2 is just copy of v1beta1 2. update changes for v1beta2 (main diff) 3. implementation is using v1beta2 4. conversion webhooks
> 
> To make this happen fully we should start in two weeks or so.

SGTM, thanks.

### Comment by [@amy](https://github.com/amy) — 2025-10-01T14:24:11Z

This may be too teeny of a detail to add here. But let's fold this in for workload version upgrade: https://github.com/kubernetes-sigs/kueue/issues/6938#issuecomment-3356598779

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T16:26:10Z

Here is a refined [graduation plan doc](https://docs.google.com/document/d/1VpSKMZP5cWXvr7NbVM2ay2HyQA6XeymwVGXxdqdhE6Q/) we discussed today on wg-batch. PTAL

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-15T17:06:28Z

Looking at the KAI linter, one item I see is that our spec fields are essentially optional.

Should we make spec fields required? What was the motivation behind not requiring a spec?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-17T05:13:24Z

I created the Google Documentation to describe the API differences intuitively so that it can help with migration and API review.
Please let me know if  I am missing anything else.

https://docs.google.com/document/d/1-PNiVsSr-gETw1QSXSHfqYkQhWYvvMMYwZZ_J6ffkzs/edit?usp=sharing

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T11:21:19Z

As the conversion webhooks are merged I open issues / tasks for the remaining conversions needed:
- https://github.com/kubernetes-sigs/kueue/issues/7362
- https://github.com/kubernetes-sigs/kueue/issues/7361

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T12:26:17Z

Also x-refrencing this API change: https://github.com/kubernetes-sigs/kueue/issues/7342

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T06:41:35Z

I have also extracted two parts:
- https://github.com/kubernetes-sigs/kueue/issues/7373
- https://github.com/kubernetes-sigs/kueue/issues/7374
Since they can be worked on independently.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T11:55:12Z

Also opened the task for documentation update:
- https://github.com/kubernetes-sigs/kueue/issues/7408

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T08:32:33Z

another follow up:
- https://github.com/kubernetes-sigs/kueue/issues/7437

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T08:37:23Z

Summary of the remaining tasks:
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7119
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7342
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7361
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7362
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7437
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7472
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7220
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7394
- [ ] https://github.com/kubernetes-sigs/kueue/issues/5032
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7584
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7547
- [ ] https://github.com/kubernetes-sigs/kueue/issues/7656

Ofc let me know if something is missing.

cc @kannon92 @mbobrovskyi  @nerdeveloper

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T14:29:37Z

FYI: I did an experiment of testing what will happen in 0.16 when we change storage to v1beta2 and all tests passed: https://github.com/kubernetes-sigs/kueue/pull/7484, so seems like we are good to go (had to only tweak importer which only operates on the storage version).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T08:02:42Z

/close
All the tasks are complete for the umbrella issue. 

Let us know if something is missing we can address it in a dedicated issue.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T08:02:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7113#issuecomment-3540434640):

>/close
>All the tasks are complete for the umbrella issue. 
>
>Let us know if something is missing we can address it in a dedicated issue.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
