# Issue #8521: LWS: Use client interceptor instead of bypassing veirifications

**Summary**: LWS: Use client interceptor instead of bypassing veirifications

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8521

**Last updated**: 2026-03-03T14:19:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-10T07:03:13Z
- **Updated**: 2026-03-03T14:19:23Z
- **Closed**: 2026-03-03T14:19:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@dpanshug](https://github.com/dpanshug)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This is a follow-up of https://github.com/kubernetes-sigs/kueue/pull/8508/changes#r2678382388

I'd propose following the fake client interceptor pattern in LWD pod reconciler UTs in the following:

https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_pod_reconciler_test.go#L153-L158

https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672

This is one of interceptor pattern example:
https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobframework/reconciler_test.go#L870-L877

**Why is this needed**:

Better test verifications.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-10T07:03:45Z

@j-skiba

### Comment by [@dpanshug](https://github.com/dpanshug) — 2026-01-10T16:24:23Z

Hi @tenzen-y, I'd like to work on this. I can replace the conditional error checks with client interceptors similar to what's used in `jobframework/reconciler_test.go`. 

Can you assign this to me? Thanks!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-11T01:42:40Z

> Hi [@tenzen-y](https://github.com/tenzen-y), I'd like to work on this. I can replace the conditional error checks with client interceptors similar to what's used in `jobframework/reconciler_test.go`.
> 
> Can you assign this to me? Thanks!

Thank you for your interest in this issue.
Feel free to assign you to this issue with `/assign`.

### Comment by [@dpanshug](https://github.com/dpanshug) — 2026-01-11T07:12:10Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-12T04:58:48Z

I think it would be better to compare the PodList here instead of handling the NotFound error. If the Pod is not found, we’ll just get an empty list, so there’s no need for an interceptor at all.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-12T05:03:35Z

> I think it would be better to compare the PodList here instead of handling the NotFound error. If the Pod is not found, we’ll just get an empty list, so there’s no need for an interceptor at all.

As a Kubernetes control-plane PoV, it would be better to avoid the LIST operation as much as possible.
Especially Pods. In case of having thousands and 10s thousands of nodes in a large ML cluster, the kube-apiserver and etcd are bottlenecks in general.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-12T05:15:57Z

> As a Kubernetes control-plane PoV, it would be better to avoid the LIST operation as much as possible.
Especially Pods. In case of having thousands and 10s thousands of nodes in a large ML cluster, the kube-apiserver and etcd are bottlenecks in general.

I mean on unit tests.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-12T06:34:56Z

> > As a Kubernetes control-plane PoV, it would be better to avoid the LIST operation as much as possible.
> Especially Pods. In case of having thousands and 10s thousands of nodes in a large ML cluster, the kube-apiserver and etcd are bottlenecks in general.
> 
> I mean on unit tests.

I'm ok with that, then 👍

### Comment by [@dpanshug](https://github.com/dpanshug) — 2026-01-12T16:53:45Z

Hi @mbobrovskyi @tenzen-y, what do you think about using `client.IgnoreNotFound()` pattern here instead of List? It's more concise and consistent with how [statefulset_reconciler_test.go](https://github.com/dpanshug/kueue/blob/fix/lws-client-interceptor/pkg/controller/jobs/statefulset/statefulset_reconciler_test.go#L294-L299) handles the same scenario. Or do you think List approach would be better?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-12T17:28:44Z

> Hi [@mbobrovskyi](https://github.com/mbobrovskyi) [@tenzen-y](https://github.com/tenzen-y), what do you think about using `client.IgnoreNotFound()` pattern here instead of List? It's more concise and consistent with how [statefulset_reconciler_test.go](https://github.com/dpanshug/kueue/blob/fix/lws-client-interceptor/pkg/controller/jobs/statefulset/statefulset_reconciler_test.go#L294-L299) handles the same scenario. Or do you think List approach would be better?

Yes, this approach works for me as well.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-12T19:09:21Z

> Hi [@mbobrovskyi](https://github.com/mbobrovskyi) [@tenzen-y](https://github.com/tenzen-y), what do you think about using `client.IgnoreNotFound()` pattern here instead of List? It's more concise and consistent with how [statefulset_reconciler_test.go](https://github.com/dpanshug/kueue/blob/fix/lws-client-interceptor/pkg/controller/jobs/statefulset/statefulset_reconciler_test.go#L294-L299) handles the same scenario. Or do you think List approach would be better?

I still urge you to add an interceptor or use List. If we keep using the GET operation during UTs, we should prove if the incoming errors are caused by specific GET errors.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T16:14:41Z

/reopen
We haven't yet addressed LWS reconciler: https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-15T16:14:47Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8521#issuecomment-3755642828):

>/reopen
>We haven't yet addressed LWS reconciler: https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T16:15:12Z

@dpanshug would you mind to address remaining one as I described above?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-15T16:40:11Z

> /reopen We haven't yet addressed LWS reconciler:
> 
> [kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go](https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672)
> 
> Lines 669 to 672 in [6daefef](/kubernetes-sigs/kueue/commit/6daefefb76cc7b5de60342a95d7694d15f0e9cb6)
> 
>  if !errors.IsNotFound(err) { 
>  	t.Fatalf("Could not get LeaderWorkerSet after reconcile: %v", err) 
>  } 
>  gotLeaderWorkerSet = nil

Do we need to update this? We have only one LWS, and after reconciliation there can still be only one. That’s why I don’t think we need to update it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T11:20:35Z

> > /reopen We haven't yet addressed LWS reconciler:
> > [kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go](https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672)
> > Lines 669 to 672 in [6daefef](/kubernetes-sigs/kueue/commit/6daefefb76cc7b5de60342a95d7694d15f0e9cb6)
> > if !errors.IsNotFound(err) {
> > t.Fatalf("Could not get LeaderWorkerSet after reconcile: %v", err)
> > }
> > gotLeaderWorkerSet = nil
> 
> Do we need to update this? We have only one LWS, and after reconciliation there can still be only one. That’s why I don’t think we need to update it.

As much as possible, we should eliminate hidden preconditions while testing. In this case, you are assuming LWS exists only one. So, I think we should verify https://github.com/kubernetes-sigs/kueue/blob/6daefefb76cc7b5de60342a95d7694d15f0e9cb6/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler_test.go#L669-L672 as well.

### Comment by [@dpanshug](https://github.com/dpanshug) — 2026-03-03T13:23:56Z

@mbobrovskyi @tenzen-y I've addressed the remanining part here #9654, please review
