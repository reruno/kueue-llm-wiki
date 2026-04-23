# Issue #974: ☂️ Requirements for v0.5

**Summary**: ☂️ Requirements for v0.5

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/974

**Last updated**: 2023-10-26T13:01:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-11T13:32:20Z
- **Updated**: 2023-10-26T13:01:58Z
- **Closed**: 2023-10-26T13:01:57Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 22

## Description

```[tasklist]
### Accepted
- [ ] #970
- [ ] #922
- [ ] #972
- [ ] #973
- [ ] https://github.com/kubernetes-sigs/kueue/issues/297
- [ ] #168
- [ ] https://github.com/kubernetes-sigs/kueue/issues/976
- [ ] https://github.com/kubernetes-sigs/kueue/issues/582
- [ ] https://github.com/kubernetes-sigs/kueue/issues/993
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T13:35:49Z

This is very much work-in-progress.

Ideally, we should aim for a release in mid September.

I also acknowledge that there are a few feature requests and open KEPs for more policies. I want to discuss with folks which of those policies are most important and can be implemented in a maintainable way. Alternatively, we could look into interfaces that would allow folks to implement their own policies.

cc @tenzen-y @Gekko0114 @KunWuLuan @vsoch @ahg-g for feedback

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-11T15:20:44Z

@alculquicondor Thanks for creating this issue. I would like to add https://github.com/kubernetes-sigs/kueue/issues/297.

> I also acknowledge that there are a few feature requests an open KEPs for more policies. I want to discuss with folks which of those policies are most important and can be implemented in a maintainable way. Alternatively, we could look into interfaces that would allow folks to implement their own policies.

I agree. It would be nice to define interfaces for queueing and expose extensible points like the kube-scheduler scheduling framework.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-11T16:46:12Z

I was planning on starting the plugin soon, although I can't give a proper ETA until I dig in a bit. I will try to post an update on that soon.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-07-11T17:36:18Z

A couple of features to consider:
1) https://github.com/kubernetes-sigs/kueue/issues/976
2) https://github.com/kubernetes-sigs/kueue/issues/975

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T17:50:03Z

We probably should start with #976.

I don't think we can fit that and partial preemption in one release.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-07-11T17:51:58Z

I agree that #976 is the higher priority

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-07-12T02:48:20Z

#963 can be a candidate I think
#849 I will work on this, try to complete before August

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-12T17:36:39Z

I'm currently hesitant about #963 unless we answer the question about arbitrary hierarchies.

I think we can add #849 as a non-blocking feature for the release.

What do others think?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-15T15:54:41Z

See updated list. I'm leaving out #963 for now, as we already have a lot in our plates.
I think we can consider it for release 0.6

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-15T20:01:09Z

LGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-12T12:04:25Z

@alculquicondor What are the remaining tasks? I guess it's only https://github.com/kubernetes-sigs/kueue/issues/297?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-16T14:41:56Z

I'm hoping we can also get https://github.com/kubernetes-sigs/kueue/issues/1136, as proof that two-stage admission works. But there are some delays in the cluster-autoscaler side.

Which APIs are we missing in #297?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-16T17:08:25Z

> I'm hoping we can also get https://github.com/kubernetes-sigs/kueue/issues/1136, as proof that two-stage admission works. But there are some delays in the cluster-autoscaler side.

I see. I'm ok with including #1136 in this release. However, it might be better to cut a new release by KubeCon.

> Which APIs are we missing in https://github.com/kubernetes-sigs/kueue/issues/297?

All APIs had been done.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-16T18:07:45Z

I agree, kubecon is an important deadline. Let's take it out if it's not done by the end of this week.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-17T04:43:23Z

> I agree, kubecon is an important deadline. Let's take it out if it's not done by the end of this week.

SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T18:45:38Z

Are these required PRs?

- https://github.com/kubernetes-sigs/kueue/pull/1154
- https://github.com/kubernetes-sigs/kueue/pull/1220
- https://github.com/kubernetes-sigs/kueue/pull/1232
- https://github.com/kubernetes-sigs/kueue/pull/1181
- https://github.com/kubernetes-sigs/kueue/pull/1226

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T18:49:54Z

The last 2 (documentation) could be merge afterwards.
But yes, the list is accurate.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T18:50:18Z

I think they can all merge by Monday.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T18:51:16Z

SGTM

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-21T13:29:58Z

cc @B1F030

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-26T13:01:53Z

:rocket: 

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-26T13:01:58Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/974#issuecomment-1781079344):

>:rocket: 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
