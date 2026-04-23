# Issue #3599: ☂️ Release v0.10.0 requirements

**Summary**: ☂️ Release v0.10.0 requirements

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3599

**Last updated**: 2024-12-16T11:35:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-20T08:12:47Z
- **Updated**: 2024-12-16T11:35:05Z
- **Closed**: 2024-12-16T11:35:01Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 12

## Description

We are targeting the release for the first week of Dev 2024. Since the date is close and 0.9 was not so long ago we may skip release candidate.

```[tasklist]
### Must Haves
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3487
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3533
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3658
```

```[tasklist]
### Nice To Haves
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3232
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3616
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3589
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1833
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2936
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3671
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3663
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3645
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3602
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T08:14:53Z

It is going to be a smaller release than before, but we make it to release the TAS rank-based ordering which is awaited by users. Let me know if we you know about some other candidate features that could make it

cc @tenzen-y @mwielgus @mwysokin @dgrove-oss @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T08:19:43Z

@dgrove-oss @tenzen-y Maybe we could consider graduating ConfigurableResourceTransformations to Beta?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-20T22:43:14Z

> Maybe we could consider graduating ConfigurableResourceTransformations to Beta?

It's relatively low risk (changing the feature gate to enable by default) and doesn't add/change any API.  There hasn't been much time to get user feedback, but that's probably ok.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-22T07:59:03Z

> @dgrove-oss @tenzen-y Maybe we could consider graduating ConfigurableResourceTransformations to Beta?

Does this indicate that we will graduate both ConfigurableResourceTransformations and WorkloadResourceRequestsSummary to beta?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-22T08:04:18Z

Yes, I see no blockers for that

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-22T08:09:58Z

> Yes, I see no blockers for that

SGTM, let us collect feedbacks by graduating those to beta

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-22T08:11:49Z

@dgrove-oss feel free to submit a PR for that

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-28T08:08:32Z

I have updated the nice-to-haves with 3 related KEPs:
- https://github.com/kubernetes-sigs/kueue/issues/3589
- https://github.com/kubernetes-sigs/kueue/issues/1833
- https://github.com/kubernetes-sigs/kueue/issues/2936

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-28T09:11:25Z

Also, updated the list with TAS-related pending issues.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T10:31:34Z

I'm ok to slightly postpone the original release target date to try to include the PRs which look almost ready:
- https://github.com/kubernetes-sigs/kueue/issues/1833
- https://github.com/kubernetes-sigs/kueue/issues/2936

cc @yaroslava-serdiuk @KPostOffice

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T11:34:57Z

/close
We are in progress of preparing 0.10 already.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-16T11:35:03Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3599#issuecomment-2545379774):

>/close
>We are in progress of preparing 0.10 already.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
