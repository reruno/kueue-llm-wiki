# Issue #2459: Panic when updateCqStatusIfChanged in function of Pending() in cluster_queue

**Summary**: Panic when updateCqStatusIfChanged in function of Pending() in cluster_queue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2459

**Last updated**: 2024-07-02T13:32:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GithubWangdf](https://github.com/GithubWangdf)
- **Created**: 2024-06-20T19:16:32Z
- **Updated**: 2024-07-02T13:32:41Z
- **Closed**: 2024-07-02T13:32:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Panic when updating cluster queue status, error logs below
panic: runtime error: invalid memory address or nil pointer dereference [recovered]
	panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0xa0 pc=0x195926c]

goroutine 1014 [running]:
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile.func1()
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:116 +0x1e5
panic({0x2402060?, 0x420b580?})
	/usr/local/go/src/runtime/panic.go:770 +0x132
sigs.k8s.io/kueue/pkg/queue.(*ClusterQueue).Pending(0x23d8420?)
	/workspace/pkg/queue/cluster_queue.go:283 +0x2c
sigs.k8s.io/kueue/pkg/queue.(*Manager).Pending(0xc064e6b788?, 0xc047b0bdc0?)
	/workspace/pkg/queue/manager.go:279 +0xa5
sigs.k8s.io/kueue/pkg/controller/core.(*ClusterQueueReconciler).updateCqStatusIfChanged(0xc064e12fa0, {0x2c2dda8, 0xc0671cb050}, 0xc064e6b600, {0x2804ec5, 0x5}, {0x2809bc0, 0x8}, {0x2824f6c, 0x16})
	/workspace/pkg/controller/core/clusterqueue_controller.go:647 +0xa8
sigs.k8s.io/kueue/pkg/controller/core.(*ClusterQueueReconciler).Reconcile(0xc064e12fa0, {0x2c2dda8, 0xc0671cae40}, {{{0x0?, 0xa32964?}, {0xc00100f530?, 0x41ac18?}}})
	/workspace/pkg/controller/core/clusterqueue_controller.go:198 +0x5eb
sigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile(0xc04f718a80, {0x2c2dda8, 0xc0671cae40}, {{{0x0?, 0x5?}, {0xc00100f530?, 0xc065035d10?}}})
	/workspace/pkg/controller/core/leader_aware_reconciler.go:77 +0x162
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile(0x2c363b8?, {0x2c2dda8?, 0xc0671cae40?}, {{{0x0?, 0xb?}, {0xc00100f530?, 0x0?}}})
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:119 +0xb7
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler(0xc064e13040, {0x2c2dde0, 0xc00069eb40}, {0x253e3a0, 0xc06520a360})
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:316 +0x3bc
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem(0xc064e13040, {0x2c2dde0, 0xc00069eb40})
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:266 +0x1be
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2()
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:227 +0x79
created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2 in goroutine 820
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:223 +0x50c

**How to reproduce it (as minimally and precisely as possible)**:

Not sure how to easily repro it yet. this is observed when we do the capacity updating for a cohort
 
**Anything else we need to know?**:
1. check further log, it saying the panic happens when updating the status for one cluster-queue, let’s say cq-a, there is only log related to this cq-a listed as below

{"level":"Level(-2)","ts":"2024-06-20T16:57:50.608225383Z","caller":"core/clusterqueue_controller.go:167","msg":"Reconciling ClusterQueue","controller":"clusterqueue","controllerGroup":"kueue.x-k8s.io",

**Environment**:
- Kubernetes version (use `kubectl version`): v1.28.9-eks-036c24b
- Kueue version (use `git describe --tags --dirty --always`): 0.7
- Cloud provider or hardware configuration: aws
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T23:17:53Z

/assign @mbobrovskyi

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T23:18:35Z

cc @mimowo

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T23:19:31Z

@GithubWangdf do you know if this was increasing or reducing the quotas?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-21T08:46:57Z

@GithubWangdf did the "capacity updating for a cohort" involve only changing the quotas, or also creating / deleting the CQs? 

I ask because it  appears to me there might be a race condition (bug) if the CQ is deleted (and the event is processed [here](https://github.com/kubernetes-sigs/kueue/blob/5be1c2037751fedbcca58f4c3834ee1b8da2fcc5/pkg/controller/core/clusterqueue_controller.go#L286)) before calling `Pending` from `updateCqStatusIfChanged` that can result in this error. 

I guess if this is the case then we could make the Pending function just throw a dedicated "non exist" error, rather than panic.

### Comment by [@GithubWangdf](https://github.com/GithubWangdf) — 2024-06-21T16:15:12Z

Seems I don’t need answer the question any more, thanks @mbobrovskyi , @mimowo for the quick action

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-21T17:40:33Z

It's still useful if you can confirm our suspicions, just in case we missed something.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-21T18:48:36Z

Image `gcr.io/k8s-staging-kueue/kueue:v20240621-v0.7.0-10-g6d2f00dc` contains the fix.

Please reopen with some more details about the steps you were performing during the panic, if the issue persists.

### Comment by [@GithubWangdf](https://github.com/GithubWangdf) — 2024-06-21T18:51:44Z

sure, here is the update, hope it helps.
1. we didn’t do any CQ deletion
2. we add one resource flavor to existing CQ
3. we add a few new CQs, but none of them are triggering any issues, from log, we see those new CQs are handled correctly, only the one which has new resource flavor added has the panic, and the one which has the issue is an existing CQ

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-21T19:09:33Z

I suspect a CQ could temporarily be unavailable in the cache while processing an update and that could have caused the issue. Although we should be removing and adding a CQ to the cache while holding the lock, to avoid this.

@mbobrovskyi can you double check?

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-21T19:09:37Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2459#issuecomment-2183309621):

>I suspect a CQ could temporarily be unavailable in the cache while processing an update and that could have caused the issue. Although we should be removing and adding a CQ to the cache while holding the lock, to avoid this.
>
>@mbobrovskyi can you double check?
>
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-02T06:47:03Z

I don't see any other problems that could have caused this issue. We are locking update of ClusterQueue and also we are not removing previous one.

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/clusterqueue_controller.go#L319-L321
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/queue/manager.go#L157-L158

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-02T13:32:36Z

/close

@GithubWangdf please reopen with any details about what the actions you performed, if you see the issue again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-02T13:32:40Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2459#issuecomment-2203176231):

>/close
>
>@GithubWangdf please reopen with any details about what the actions you performed, if you see the issue again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
