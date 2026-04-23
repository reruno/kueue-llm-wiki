# Issue #8829: ☂️ Release 0.17 plan

**Summary**: ☂️ Release 0.17 plan

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8829

**Last updated**: 2026-03-18T12:07:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T15:56:47Z
- **Updated**: 2026-03-18T12:07:37Z
- **Closed**: 2026-03-17T16:26:05Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 10

## Description

The release is planned tentatively for 16th March, let's discuss the scope.

Nice to haves:
- https://github.com/kubernetes-sigs/kueue/issues/8160
- https://github.com/kubernetes-sigs/kueue/issues/8691
- https://github.com/kubernetes-sigs/kueue/issues/8303
- https://github.com/kubernetes-sigs/kueue/issues/8860
- https://github.com/kubernetes-sigs/kueue/issues/8095
- https://github.com/kubernetes-sigs/kueue/issues/8729
- https://github.com/kubernetes-sigs/kueue/issues/6915
- https://github.com/kubernetes-sigs/kueue/issues/8830
- https://github.com/kubernetes-sigs/kueue/issues/7539
- https://github.com/kubernetes-sigs/kueue/pull/8734
- https://github.com/kubernetes-sigs/kueue/issues/7990
- https://github.com/kubernetes-sigs/kueue/issues/7513
- https://github.com/kubernetes-sigs/kueue/issues/9775
- https://github.com/kubernetes-sigs/kueue/issues/4915
- https://github.com/kubernetes-sigs/kueue/issues/8855
- https://github.com/kubernetes-sigs/kueue/issues/3899
- https://github.com/kubernetes-sigs/kueue/pull/8971
- https://github.com/kubernetes-sigs/kueue/issues/8826
- https://github.com/kubernetes-sigs/kueue/issues/8522
- https://github.com/kubernetes-sigs/kueue/issues/8607

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:57:04Z

cc @tenzen-y @gabesaba @mwysokin @kannon92 @sohankunkerkar

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-27T16:04:56Z

Could we include https://github.com/kubernetes-sigs/kueue/issues/6915?

This seems to have slipped radar and missed reviews the last two cycles.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T16:06:05Z

We would like to make progress on the DRA side as well. Can you add these items in the release plan as well?
- https://github.com/kubernetes-sigs/kueue/pull/8775
- https://github.com/kubernetes-sigs/kueue/pull/8734

I will also add a design document for the partitionable devices.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T16:12:04Z

> We would like to make progress on the DRA side as well. Can you add these items in the release plan as well?

Sure, progress with DRA is quite important, but I will add the second only, because here we focus on functional changes.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T16:17:00Z

Cool, ok we have a long list. Please remind us if something else should be watched :)

As usual - these are nice to haves - we will not block the release because of one of the features. We may still consider delaying the release for up to 2 weeks if some important features are "almost done".

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-12T10:07:18Z

As the release is just a month away, @mimowo and I discussed the priorities for our KEP reviews, and decided on the following:

**Priority**
- #8691
- #8303
- #8729 
- #7990
- #8830

**Nice to Have**
- #7513
- #8734
- #8303
- #6915
- #8522
- #8826

Please let us know if you have any feedback/concerns

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T10:14:06Z

+1, but be aware that the categorization is just a "direction", which means:
- no features in the **Priority** are blocking for the release anyway if not done on time
- features if the **Nice to Have** section are best effort, but can be included if reviewed actively, and maintainers assess they are good to go

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-12T10:33:31Z

IMO, https://github.com/kubernetes-sigs/kueue/pull/8734 would be supportive since extended resources could mitigate migration costs from device plugin to DRA ecosystem, which means it can accelerate DRA introduction in production. I believe that DRA is a big point for native WAS / TAS enhancements.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T16:25:59Z

/close
Let me replace with the actual release issue already, I will cross reference: https://github.com/kubernetes-sigs/kueue/issues/9951

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-17T16:26:07Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8829#issuecomment-4076281115):

>/close
>Let me replace with the actual release issue already, I will cross reference: https://github.com/kubernetes-sigs/kueue/issues/9951


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
