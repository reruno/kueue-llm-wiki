# Issue #14: Need to improve the readability of the log

**Summary**: Need to improve the readability of the log

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/14

**Last updated**: 2022-11-28T17:00:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@denkensk](https://github.com/denkensk)
- **Created**: 2022-02-18T08:40:34Z
- **Updated**: 2022-11-28T17:00:10Z
- **Closed**: 2022-11-28T17:00:10Z
- **Labels**: `help wanted`, `priority/important-soon`, `lifecycle/stale`, `priority/backlog`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 26

## Description

```bash 
1.6451684909657109e+09	INFO	controller-runtime.metrics	Metrics server is starting to listen	{"addr": "127.0.0.1:8080"}
1.6451684909663508e+09	INFO	setup	starting manager
1.6451684909665146e+09	INFO	Starting server	{"kind": "health probe", "addr": "[::]:8081"}
1.645168490966593e+09	INFO	Starting server	{"path": "/metrics", "kind": "metrics", "addr": "127.0.0.1:8080"}
I0218 07:14:51.066639       1 leaderelection.go:248] attempting to acquire leader lease kueue-system/c1f6bfd2.gke-internal.googlesource.com...
I0218 07:15:07.705977       1 leaderelection.go:258] successfully acquired lease kueue-system/c1f6bfd2.gke-internal.googlesource.com
1.6451685077060497e+09	DEBUG	events	Normal	{"object": {"kind":"ConfigMap","namespace":"kueue-system","name":"c1f6bfd2.gke-internal.googlesource.com","uid":"e70e4b9b-54f4-4782-a904-e57d3001c8e6","apiVersion":"v1","resourceVersion":"264201"}, "reason": "LeaderElection", "message": "kueue-controller-manager-7ff7b759bf-nszmb_05445f7f-a871-4a4c-83c1-af075b850e49 became leader"}
1.6451685077061899e+09	DEBUG	events	Normal	{"object": {"kind":"Lease","namespace":"kueue-system","name":"c1f6bfd2.gke-internal.googlesource.com","uid":"72b48bf0-20e0-42a4-823b-2a6edcb3288a","apiVersion":"coordination.k8s.io/v1","resourceVersion":"264202"}, "reason": "LeaderElection", "message": "kueue-controller-manager-7ff7b759bf-nszmb_05445f7f-a871-4a4c-83c1-af075b850e49 became leader"}
1.6451685077062488e+09	INFO	controller.queue	Starting EventSource	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "source": "kind source: *v1alpha1.Queue"}
1.645168507706281e+09	INFO	controller.queue	Starting Controller	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue"}
1.6451685077062566e+09	INFO	controller.queuedworkload	Starting EventSource	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "QueuedWorkload", "source": "kind source: *v1alpha1.QueuedWorkload"}
1.6451685077063015e+09	INFO	controller.queuedworkload	Starting Controller	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "QueuedWorkload"}
1.6451685077062776e+09	INFO	controller.capacity	Starting EventSource	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Capacity", "source": "kind source: *v1alpha1.Capacity"}
1.6451685077063189e+09	INFO	controller.capacity	Starting Controller	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Capacity"}
1.6451685077064047e+09	INFO	controller.job	Starting EventSource	{"reconciler group": "batch", "reconciler kind": "Job", "source": "kind source: *v1.Job"}
1.6451685077064307e+09	INFO	controller.job	Starting EventSource	{"reconciler group": "batch", "reconciler kind": "Job", "source": "kind source: *v1alpha1.QueuedWorkload"}
1.6451685077064393e+09	INFO	controller.job	Starting Controller	{"reconciler group": "batch", "reconciler kind": "Job"}
1.6451685078075259e+09	INFO	controller.queuedworkload	Starting workers	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "QueuedWorkload", "worker count": 1}
1.6451685078075113e+09	INFO	controller.capacity	Starting workers	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Capacity", "worker count": 1}
1.645168507807566e+09	INFO	controller.queue	Starting workers	{"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "worker count": 1}
1.6451685078076618e+09	INFO	controller.job	Starting workers	{"reconciler group": "batch", "reconciler kind": "Job", "worker count": 1}
1.645168507807886e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"ingress-nginx-admission-create","namespace":"kube-system"}}
1.645168507808418e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"ingress-nginx-admission-patch","namespace":"kube-system"}}
1.6451685078085716e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"kube-eventer-init-v1.6-a92aba6-aliyun","namespace":"kube-system"}}
1.6451706903900485e+09	LEVEL(-2)	capacity-reconciler	Capacity create event	{"capacity": {"name":"cluster-total"}}
1.6451706904384277e+09	LEVEL(-2)	queue-reconciler	Queue create event	{"queue": {"name":"main","namespace":"default"}}
1.6451707150770907e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"sample-job-jjbq2","namespace":"default"}}
1.6451707150895817e+09	LEVEL(-2)	queued-workload-reconciler	QueuedWorkload create event	{"queuedWorkload": {"name":"sample-job-jjbq2","namespace":"default"}, "queue": "main", "status": "pending"}
1.645170715089716e+09	LEVEL(-2)	scheduler	Workload assumed in the cache	{"queuedWorkload": {"name":"sample-job-jjbq2","namespace":"default"}, "capacity": "cluster-total"}
1.6451707150901928e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"sample-job-jjbq2","namespace":"default"}}
1.6451707150984285e+09	LEVEL(-2)	scheduler	Successfully assigned capacity and resource flavors to workload	{"queuedWorkload": {"name":"sample-job-jjbq2","namespace":"default"}, "capacity": "cluster-total"}
1.6451707150985863e+09	LEVEL(-2)	queued-workload-reconciler	QueuedWorkload update event	{"queuedWorkload": {"name":"sample-job-jjbq2","namespace":"default"}, "queue": "main", "capacity": "cluster-total", "status": "assigned", "prevStatus": "pending", "prevCapacity": ""}
1.6451707150986767e+09	LEVEL(-2)	job-reconciler	Job reconcile event	{"job": {"name":"sample-job-jjbq2","namespace":"default"}}
```


We can chose to switch to klog/v2.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T08:40:54Z

/cc @ahg-g @alculquicondor

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T08:41:57Z

/kind cleanup

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-18T14:08:27Z

much agree, klog is soo much better

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-18T14:11:46Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T14:38:15Z

Let's reach to some level of agreement before we jump into implementing :)

If this is juts about format, I believe there are different zap configurations we can use. This is actually my first time using zap, so I'm not really sure what's possible.

While klog format might be better, the framework doesn't currently support contextual logging, which simplifies building structured logging a lot.
But this is changing soon https://github.com/kubernetes/enhancements/tree/master/keps/sig-instrumentation/3077-contextual-logging

In the meantime, if we stick with logr for now, I think it will be easier to switch to klog (v3?) once it supports contextual logging.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-18T15:15:14Z

let's defer this to klog/v3 but keep circling back here. I am a klog fan for sure

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T15:16:52Z

is there a better format we can use for zap?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-21T22:41:06Z

This is why I don't like logr
```bash
1.6454820377420967e+09  ERROR   job-reconciler  Unsuspending job        {"job": {"name":"sample-job","namespace":"default"}, "error": "Operation cannot be fulfilled on jobs.batch \"sample-jo
b\": the object has been modified; please apply your changes to the latest version and try again"}                                                                                            sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile                 
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:114                                
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler          
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:311
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem       
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:266
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2             
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:227
1.6454820377421455e+09  ERROR   controller.job  Reconciler error        {"reconciler group": "batch", "reconciler kind": "Job", "name": "sample-job", "namespace": "default", "error": "Operat
ion cannot be fulfilled on jobs.batch \"sample-job\": the object has been modified; please apply your changes to the latest version and try again"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem       
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:266
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2             
        /go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:227
```
had the similar erro/logs on NFD when using logr, and got rid by moving to klog/v2

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T15:15:01Z

Can you try to migrate to https://github.com/kubernetes/klog/tree/main/klogr?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T16:58:41Z

I'm fine waiting for v3 or replacing zapper with klogr.

I don't want to loose contextual logging.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-16T13:44:22Z

> I'm fine waiting for v3 or replacing zapper with klogr.
> 
> I don't want to loose contextual logging.

Since we are on a hold here
/unassign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-16T14:08:17Z

You could always give klogr a try

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-05T15:40:17Z

/kind cleanup

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T13:44:19Z

What is the status of this?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T14:07:49Z

I disabled the dev mode for the binary, so the output is all structured now:

```
{"level":"Level(-2)","ts":1649793642.0015297,"logger":"controller.clusterqueue","msg":"Reconciling ClusterQueue","reconciler group":"kueue.x-k8s.io","reconciler kind":"ClusterQueue","name":"cluster-total","namespace":"","clusterQueue":{"name":"cluster-total"}}
```

It looks like klog made progress towards contextual logging https://github.com/kubernetes/klog/blob/main/contextual.go

Let me ask what's the status of it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T14:19:13Z

Documentation is up here:

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/migration-to-structured-logging.md

Kueue using it will help it mature.

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-13T14:19:15Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/14):

>Documentation is up here:
>
>https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/migration-to-structured-logging.md
>
>Kueue using it will help it mature.
>
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T14:23:14Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:32:26Z

/help
to migrate to klog's contextual logging.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:32:48Z

/remove-lifecycle stale
/priority backlog

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-09T21:49:41Z

I just realized that kubernetes uses zap to do json output through klog.

klog's contextual logging implements the logr.Logger interface. So it doesn't look like we benefit much migrating to klog, given that controller-runtime already expects a Logger.

However, there are some logs for which we are receiving the wrong call reference. I'll see if there is something we can do https://github.com/kubernetes-sigs/controller-runtime/issues/1737

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-10T22:18:48Z

I managed to fix it, but we'll have to leave this until there's a controller-runtime release kubernetes-sigs/controller-runtime#1975

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T21:07:27Z

/help cancel

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-11-09T21:33:56Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-10T13:08:59Z

/lifecycle stale

We should be able to upgrade controller-runtime to have the fix

/help

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-25T19:55:14Z

I'll take a look at this. /assign @kannon92
