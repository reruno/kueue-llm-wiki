# Issue #6498: Release 0.14 Plan

**Summary**: Release 0.14 Plan

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6498

**Last updated**: 2025-09-30T10:32:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-08-07T21:08:19Z
- **Updated**: 2025-09-30T10:32:05Z
- **Closed**: 2025-09-30T10:32:03Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 19

## Description

Hello,

Now that release 0.13 is behind us, we should have list of committed features for 0.14.

# Nice to Haves

- https://github.com/kubernetes-sigs/kueue/issues/2941
- https://github.com/kubernetes-sigs/kueue/issues/4529
- https://github.com/kubernetes-sigs/kueue/issues/3450
- https://github.com/kubernetes-sigs/kueue/issues/2349
- https://github.com/kubernetes-sigs/kueue/issues/3258
- https://github.com/kubernetes-sigs/kueue/issues/6158
- https://github.com/kubernetes-sigs/kueue/issues/3884
- https://github.com/kubernetes-sigs/kueue/issues/6454
- https://github.com/kubernetes-sigs/kueue/issues/6335
- https://github.com/kubernetes-sigs/kueue/issues/6334
- https://github.com/kubernetes-sigs/kueue/issues/6488
- https://github.com/kubernetes-sigs/kueue/issues/6184
- https://github.com/kubernetes-sigs/kueue/issues/6489
- https://github.com/kubernetes-sigs/kueue/issues/5313
- https://github.com/kubernetes-sigs/kueue/pull/6141
- https://github.com/kubernetes-sigs/kueue/issues/5704

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T07:15:19Z

Thank you for opening, let me ping some folks who I remember working on or prioritizing features for 0.14:
cc @tenzen-y @gabesaba @mwysokin  @ichekrygin @amy @khrm @kaisoz @dgrove-oss

We are planning the release on 15th September according to the 2-monthly cadence in https://github.com/kubernetes-sigs/kueue/issues/3588#issuecomment-2615210474. If there are some important feature ongoing "almost done" we can postpone by 2weeks, beyond that we release without the features, and they have a next chance in November.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T07:26:22Z

I let myself put the Issues which I'm tracking directly. Likely I missed something, let us know if this is the case, we still have time to add more items for tracking.

### Comment by [@amy](https://github.com/amy) — 2025-08-08T11:20:57Z

I don't want to block release 0.14 for this, but I want the chance to squeeze it in: https://github.com/kubernetes-sigs/kueue/issues/6489

So I'll check in closer to the date.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T11:26:28Z

Sure, let me add it to keep track. These issues aren't really blockers for the release, but we can delay 2w for them.

### Comment by [@amy](https://github.com/amy) — 2025-08-10T22:03:21Z

Also do we want to include this one as a release candidate: https://github.com/kubernetes-sigs/kueue/pull/6141 `[kep-4400] Add preemptionPolicy to WorkloadPriorityClass #6141`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T07:40:15Z

Sure. The major comment I have there currently is about the "side effect" of the new preemption policy on scheduling: https://github.com/kubernetes-sigs/kueue/pull/6141/files#r2256532913.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T15:08:30Z

> Also do we want to include this one as a release candidate: [#6141](https://github.com/kubernetes-sigs/kueue/pull/6141) `[kep-4400] Add preemptionPolicy to WorkloadPriorityClass #6141`

Good call, SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-14T14:28:17Z

I added https://github.com/kubernetes-sigs/kueue/issues/5704 to the list. That is a good step to enhance the MultiKueue feature.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T13:23:47Z

The tentative release date is Sep 15. We probably can shift it by a week or two, but please prioritize completing the ongoing work.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-15T19:53:31Z

@mimowo @tenzen-y As we are hitting Sep 15th, should we revisit musts for this release?

We have a lot of items not finished so I'm not sure what is a must for 0.14 and what we can push to 0.15.

In my organization, we are interested in https://github.com/kubernetes-sigs/kueue/issues/2941, https://github.com/kubernetes-sigs/kueue/issues/3884 and https://github.com/kubernetes-sigs/kueue/issues/2349.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-16T01:39:03Z

@kannon92 As we discussed in last week's community meeting, we are currently focusing on DRA support, TAS graduation, AdmissionCheck retry mechanism, and MultiKueue integration for external Jobs.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-16T01:57:56Z

> [@kannon92](https://github.com/kannon92) As we discussed in last week's community meeting, we are currently focusing on DRA support, TAS graduation, AdmissionCheck retry mechanism, and MultiKueue integration for external Jobs.

And trainer integration?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-16T02:00:02Z

> > [@kannon92](https://github.com/kannon92) As we discussed in last week's community meeting, we are currently focusing on DRA support, TAS graduation, AdmissionCheck retry mechanism, and MultiKueue integration for external Jobs.
> 
> And trainer integration?

Mostly yes. But, that is not a must-have in my mind. The top priority is DRA and TAS graduation.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-17T15:28:45Z

I updated this issue to show what we are considering must haves versus nice to have for release.

It is my understanding that when the Must haves are complete, we should be able to do a release.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T15:51:55Z

> It is my understanding that when the Must haves are complete, we should be able to do a release.

Technically they are all "nice to haves" I think. We've decided on the fixed release schedule, rather than "once all done", right? So, we try very much to help contributors complete their work, we may consider extending in exceptional cases for important features "almost done", but I wouldn't like to delay beyond September.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2025-09-17T16:14:25Z

> Technically they are all "nice to haves" I think. We've decided on the fixed release schedule, rather than "once all done", right? So, we try very much to help contributors complete their work, we may consider extending in exceptional cases for important features "almost done", but I wouldn't like to delay beyond September.

+1

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-17T19:23:03Z

Updated to reflect that they are all nice to haves.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T10:31:58Z

/close
Today we are moving with what we have. Thanks to everyone involved 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-30T10:32:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6498#issuecomment-3351239735):

>/close
>Today we are moving with what we have. Thanks to everyone involved 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
