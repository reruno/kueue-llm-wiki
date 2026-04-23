# Issue #2297: Enable randomization in the queuing strategy

**Summary**: Enable randomization in the queuing strategy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2297

**Last updated**: 2024-06-25T21:19:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@shaowei-su](https://github.com/shaowei-su)
- **Created**: 2024-05-28T17:49:40Z
- **Updated**: 2024-06-25T21:19:22Z
- **Closed**: 2024-06-25T21:19:21Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Aside from `StrictFIFO` and `BestEffortFIFO `, allow randomized admission of queued workloads.

**Why is this needed**:
Today, we encourage users to submit as many workloads as possible to saturate the queue resources. However, this could lead to imbalanced admission of workloads based on FIFO for preemptible workloads.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T06:37:54Z

> Today, we encourage users to submit as many workloads as possible to saturate the queue resources. However, this could lead to imbalanced admission of workloads based on FIFO for preemptible workloads.

This is interesting, I would like to explore your setup to better understand the expectations. 

Do you mean that userA is faster to send the jobs than userB and they block the queue of userB for a prolonged time? If so, is it because userA and userB are in different time-zones? 

Resolving this type of imbalances is one of the objectives of the [Fair Sharing](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1714-fair-sharing) - it will be released in 0.7, we are yet going to add some user-facing docs.

I would also like to know if you have generally short- or long-running jobs? Do you use same priority for all of them?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T06:38:02Z

/cc @mwielgus @alculquicondor

### Comment by [@shaowei-su](https://github.com/shaowei-su) — 2024-05-29T15:54:48Z

> Do you mean that userA is faster to send the jobs than userB and they block the queue of userB for a prolonged time? If so, is it because userA and userB are in different time-zones?

Yes, userA could submit all his jobs all at once to the preemptible queues prior to userB; it's not necessarily time zone based issue, since a lot of the jobs are adhoc runs.

> I would also like to know if you have generally short- or long-running jobs? Do you use same priority for all of them?

Jobs tend to be long running ~ 10 hr, and currently we set the same priority for preemptible jobs.

Thanks @mimowo , could you point me to the PRs for this feature? I can test it out on our end as well.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T15:59:33Z

> Thanks @mimowo , could you point me to the PRs for this feature? I can test it out on our end as well.

I think a good entry point might be the API PR: https://github.com/kubernetes-sigs/kueue/pull/2070.
AFAIK @alculquicondor is working on some docs for 0.7.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:19:16Z

Fair sharing is documented here https://kueue.sigs.k8s.io/docs/concepts/preemption/#fair-sharing

I suppose that, with that, this feature request is no longer needed.

Please reopen with more details if you disagree.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T21:19:21Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2297#issuecomment-2189988461):

>Fair sharing is documented here https://kueue.sigs.k8s.io/docs/concepts/preemption/#fair-sharing
>
>I suppose that, with that, this feature request is no longer needed.
>
>Please reopen with more details if you disagree.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
