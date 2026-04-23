# Issue #8561: MultiKueue: allow 20 clusters per MultiKueueConfig

**Summary**: MultiKueue: allow 20 clusters per MultiKueueConfig

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8561

**Last updated**: 2026-01-15T16:57:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-13T15:22:33Z
- **Updated**: 2026-01-15T16:57:41Z
- **Closed**: 2026-01-15T16:57:41Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 13

## Description


**What would you like to be added**:

I would like to increase the limit on the max number of clusters used by MultiKueueConfig: 

This is currently 10: https://github.com/kubernetes-sigs/kueue/blob/ed6de75d1716058baa520bc0e19a33cfc810bb04/apis/kueue/v1beta2/multikueue_types.go#L143

**Why is this needed**:

We already observe deployments for 5 clusters, and we expect the demand to grow soon, especially as we start supporting ClusterProfiles. Since the bump cannot be done in patch releases, it is better to anticipate the increased demand.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T15:22:49Z

cc @tenzen-y @gabesaba @mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T15:23:00Z

cc @kshalot

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-13T15:51:36Z

For the record, I started wondering where the initial value of 10 came from. I found this https://github.com/kubernetes-sigs/kueue/pull/1631#discussion_r1466679001 in the PR when this API was still in alpha (it was reduced from 100).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T15:58:32Z

In the case of the AllAtOnce strategy, users might face performance issues.
@mimowo @kshalot Do you have any MultiKueue performance tests in your side?

It might be better to expand our document to recommend that they select another strategy (NOT AllAtOnce) in case of many workload clusters.
Anyway, if your team doesn't see a significant performance impact, agree to relax validation.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:07:02Z

> For the record, I started wondering where the initial value of 10 came from. I found this https://github.com/kubernetes-sigs/kueue/pull/1631#discussion_r1466679001 in the PR when this API was still in alpha (it was reduced from 100).

Good point, thanks for the archeology. So, 10 was chosen to be conservative, but over time:
1. MultiKueue become more mature (beta now)
2. we see actual adoption starting, and people asking more questions about it 
3. we have the incremenal mode which allows users to try the clusters sequentially.

So I think 20 can be justified now.

> In the case of the AllAtOnce strategy, users might face performance issues.

Yes, this is one reason why we introduced the Incremental mode. 

> @mimowo @kshalot Do you have any MultiKueue performance tests in your side?

We are working on some internal testing for this, but don't yet have results to share. We are planning testing at the scale of 6  worker clusters for now.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:13:08Z

We start with internal testing on gke, but could also maybe put the testing in the oss using kind, but then it would be probably more like sanity testing at 3 worker clusters (on kind) max. Still, it might be worth doing so that the community also can see the results easily. wdyt @tenzen-y ? I could open an issue in the oss if you think this is good idea

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T16:16:52Z

> > In the case of the AllAtOnce strategy, users might face performance issues.
> 
> Yes, this is one reason why we introduced the Incremental mode.
> 

> > @mimowo @kshalot Do you have any MultiKueue performance tests in your side?
> 
> We are working on some internal testing for this, but don't yet have results to share. We are planning testing at the scale of 6 worker clusters for now.

Do we want to relax the validations with 20 clusters only when the strategy is NOT AllAtOnce for now?
The reason why I am asking is that we can not restrict validations later, so we can relax the validations later.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T16:21:28Z

> We start with internal testing on gke, but could also maybe put the testing in the oss using kind, but then it would be probably more like sanity testing at 3 worker clusters (on kind) max. Still, it might be worth doing so that the community also can see the results easily. wdyt @tenzen-y ? I could open an issue in the oss if you think this is good idea

Yeah, both (community-driven and vendor-reported) performance testing sounds great. If we want to release this relaxing w/o performance tests, we might want to have some limitations (strategy) as described above.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:35:21Z

Awesome I opened https://github.com/kubernetes-sigs/kueue/issues/8564

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:39:29Z

> Do we want to relax the validations with 20 clusters only when the strategy is NOT AllAtOnce for now?

Maybe, but it feels like it will require extra code complication - like relaxing to 20 in schema, but using webhook validation to have it at 10 for AllAtOnce. I think 20 isn't that many anyway, so for simplicity I would just bump to 20. 

Still, the expectation is that the prod systems will soon require more than we can test in performance tests, especially in the oss testing >5 doesn't sound feasible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T16:52:20Z

> > Do we want to relax the validations with 20 clusters only when the strategy is NOT AllAtOnce for now?
> 
> Maybe, but it feels like it will require extra code complication - like relaxing to 20 in schema, but using webhook validation to have it at 10 for AllAtOnce. I think 20 isn't that many anyway, so for simplicity I would just bump to 20.
> 
> Still, the expectation is that the prod systems will soon require more than we can test in performance tests, especially in the oss testing >5 doesn't sound feasible.

Alright, that sounds good to me. I think the combination of the number of clusters and the MultiKueue Workload creation strategy deeply depends on the user environment. So, we can just mention performance concerns in our documentation when AllAtOnce and a large number of clusters scenario.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:10Z

/priority important-soon

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-15T13:40:07Z

/assign
