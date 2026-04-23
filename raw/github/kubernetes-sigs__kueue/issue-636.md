# Issue #636: ☂️ Requirements for v0.4

**Summary**: ☂️ Requirements for v0.4

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/636

**Last updated**: 2023-07-07T15:15:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-15T15:59:23Z
- **Updated**: 2023-07-07T15:15:54Z
- **Closed**: 2023-07-07T15:15:53Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 14

## Description

Targeting end of June

```[tasklist]
### Committed
- [ ] #510 
- [ ] #599 
- [ ] #610
- [ ] #612
- [ ] https://github.com/kubernetes-sigs/kueue/issues/534
- [ ] https://github.com/kubernetes-sigs/kueue/issues/738
```

```[tasklist]
### Nice to have (will not block the release)
- [ ] #78 
- [ ] #297
- [ ] #666
- [ ] #420
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-15T15:59:52Z

cc @denkensk @ahg-g @mwielgus @kerthcet @tenzen-y

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-03-16T21:01:56Z

are the candidates listed in some rough priority?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-17T03:08:32Z

Thanks for bringing this in! @alculquicondor 🎉

One concern is about the release cycle. This is a long term before we release v0.4.0, hope we can release minor versions regularly, users can experiment with the newest features randomly rather than building with master branch.  We haven't released any versions since August last year, I think it's not a good signal. I recalled we talked about this before but couldn't find the records.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-17T03:40:41Z

I will vote for them as they're the shortcomings Kueue has
- https://github.com/kubernetes-sigs/kueue/issues/599
- https://github.com/kubernetes-sigs/kueue/issues/534
- https://github.com/kubernetes-sigs/kueue/issues/510
- https://github.com/kubernetes-sigs/kueue/issues/78

Also good to have:
- https://github.com/kubernetes-sigs/kueue/issues/610
- https://github.com/kubernetes-sigs/kueue/issues/582
- https://github.com/kubernetes-sigs/kueue/issues/77
- https://github.com/kubernetes-sigs/kueue/issues/420

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-17T13:10:07Z

> are the candidates listed in some rough priority?

Not yet. I just grabbed everything from the backlog that might be feasible in 3-4 months (individually).

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-03-31T14:20:59Z

After some chat with @alculquicondor we agreed to aim at 2-3 month release cycle. The project is still young and more frequent, narrow-scoped releases will probably both work better and look better. Thus the list can be roughly prioritised into three categories: 
* Will do - we will postpone release if the task is not finished.
* Maybe - we will try/strongly consider but will not postpone the release if the task is not finished.  
* For next releases - was considered for the release but most likely the task will not even be started.

Will do:
* #534
* #510 
* #599 
* #610 
* #612

Maybe:
* #78 
* #666 - the work has already been started - https://github.com/ray-project/kuberay/pull/926 but due to some refactoring the important dependency is on-hold
* #297 - depends on https://github.com/kubeflow/common/pull/196

For next releases:
* #77 - the needed infrastructure will land in 1.27 (https://github.com/kubernetes/kubernetes/pull/116161) and it will be a while before 1.27 is actually in use.
* #582 - nice optimisation but no explicit need at this moment. 
* #420 - not sure about proper UX, most likely won't fit anyway.
* #28 - won't fit, too big, no clear API/UX yet.
* #74 - 2 frameworks already in the pipeline, will wait for the next release(s).

### Comment by [@denkensk](https://github.com/denkensk) — 2023-03-31T14:40:01Z

> The project is still young and more frequent, narrow-scoped releases will probably both work better and look better. 

By the way, can we collect the cases used by some companies in the production environment, which will encourage more people to use and participate in this project?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-31T14:42:27Z

For sure! If you know of any particular case, please share. Some of the requests above come from our customers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-03T19:23:06Z

I have updated the issue description. @kerthcet @denkensk anything else you would like to add?
I will also share this list in the next WG meeting and in kubecon.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-04T09:35:12Z

LGTM.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T18:36:52Z

I meant to add #534 as well

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-24T19:38:12Z

I added #738 to the committed list

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-07T15:15:48Z

/close
with https://github.com/kubernetes-sigs/kueue/releases/tag/v0.4.0

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-07T15:15:53Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/636#issuecomment-1625566398):

>/close
>with https://github.com/kubernetes-sigs/kueue/releases/tag/v0.4.0


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
