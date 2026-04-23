# Issue #101: Integration test is flaky for status updates

**Summary**: Integration test is flaky for status updates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/101

**Last updated**: 2022-03-28T14:39:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-08T18:27:44Z
- **Updated**: 2022-03-28T14:39:24Z
- **Closed**: 2022-03-28T14:39:24Z
- **Labels**: `help wanted`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 42

## Description

see https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/90/pull-kueue-test-integration-main/1501214768197799936

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-08T18:35:38Z

I have been thinking about a possible flake that would affect all our status updates.

1. We get an event for the updated QueuedWorkload.
2. The queue controller picks it up, updates the Queue status.
3. The queuedworkloadcontroller picks it up, updates the queue manager.

Result: the Queue status is outdated and nothing will bring it back :(

The same could happen for ClusterQueue status and the cache.

If that's the case, we should look into a way for the queuedworkload controller to `Add` events to the Queue/ClusterQueue reconcilers' workerqueue.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T21:20:22Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-08T21:20:23Z

@ahg-g: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/101):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-09T16:06:27Z

Another one :(

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/100/pull-kueue-test-integration-main/1501589190414962688


Could it be specific to the queue controller?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-09T16:12:08Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/104/pull-kueue-test-integration-main/1501588334315573248

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-09T20:10:39Z

/priority important-soon

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-09T20:41:56Z

Spending today afternoon on this topic
might un-assign if not successful 
/assign

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-09T21:54:02Z

Managed to reproduce locally after several runs 
```bash
    STEP: Creating workloads 03/09/22 16:48:04.446
  << End Captured GinkgoWriter Output

  Timed out after 10.001s.
  Mismatch (-want,+got):
    v1alpha1.QueueStatus{
  -     PendingWorkloads: 3,
  +     PendingWorkloads: 2,
    }
  
  In [It] at: /home/eduardo/sdk/github/kubernetes-sigs/kueue/test/integration/controller/core/queue_controller_test.go:84
------------------------------
•

Ran 2 of 2 Specs in 17.084 seconds
FAIL! -- 1 Passed | 1 Failed | 0 Pending | 0 Skipped
--- FAIL: TestAPIs (17.08s)
```

Seems to alight with Aldo idea of it being around the Queue controller

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-09T22:44:48Z

I think #105 can help fix this, one of the issues is that we are not updating the queuedWorkload.Status enough, I could test by changing 
https://github.com/kubernetes-sigs/kueue/blob/611e10ea9eb8092ed55f503f5581058b94996ce9/pkg/controller/core/queue_controller.go#L136-L143

to

```go
func (h *queuedWorkloadHandler) Update(e event.UpdateEvent, q workqueue.RateLimitingInterface) {
	oldQW := e.ObjectOld.(*kueue.QueuedWorkload)
	newQW := e.ObjectOld.(*kueue.QueuedWorkload)
	if workloadStatus(oldQW) != workloadStatus(newQW) {
		q.Add(requestForQueueStatus(newQW))
	}
	if newQW.Spec.QueueName != oldQW.Spec.QueueName {
		q.Add(requestForQueueStatus(oldQW))
	}
}
```

Test now fails every time, meaning the old and new status are almost always the same

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T13:36:15Z

Did you observe any failures for the ClusterQueue controller?

>  one of the issues is that we are not updating the queuedWorkload.Status enough

I don't think we should solve this by "being more noisy". If there is a race condition, we should solve it.

Were you able to confirm if my theory in https://github.com/kubernetes-sigs/kueue/issues/101#issuecomment-1062084107 is the actual cause?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T14:43:08Z

After a long `while true` loop, the only test failing is always `queue_controller_test.go` , so it is probably around that place , always around `PendingWorkloads` not being what expected 

It feels like a race condition when calling 
https://github.com/kubernetes-sigs/kueue/blob/b40d12cb980faa3f6d3b308f93502a6acba3b8b9/pkg/queue/manager.go#L108-L115

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T15:01:08Z

🤔 
`go test -race -count=1 ./test/integration/... ` 

`-race` removes the error (while loop not triggered the error yet)

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T15:05:21Z

> thinking `go test -race -count=1 ./test/integration/... `
> 
> `-race` removes the error (while loop not triggered the error yet)

Take it back, the `while true` finally caught it 

```bash
------------------------------
• [FAILED] [10.302 seconds]
Queue controller
/home/eduardo/sdk/github/kubernetes-sigs/kueue/test/integration/controller/core/queue_controller_test.go:33
  [It] Should update status when workloads are created
  /home/eduardo/sdk/github/kubernetes-sigs/kueue/test/integration/controller/core/queue_controller_test.go:63

  Begin Captured GinkgoWriter Output >>
    STEP: Creating workloads 03/10/22 10:04:10.159
    1.6469246501720223e+09      ERROR   controller.queue        Reconciler error        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "name": "queue", "namespace": "core-queue-q4ghk", "error": "Operation cannot be fulfilled on queues.kueue.x-k8s.io \"queue\": the object has been modified; please apply your changes to the latest version and try again"}
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
        /home/eduardo/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:266
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
        /home/eduardo/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:227
    STEP: Finishing workloads 03/10/22 10:04:10.427
  << End Captured GinkgoWriter Output

  Timed out after 10.001s.
  Mismatch (-want,+got):
    v1alpha1.QueueStatus{
  -     PendingWorkloads: 0,
  +     PendingWorkloads: 1,
    }
  
  In [It] at: /home/eduardo/sdk/github/kubernetes-sigs/kueue/test/integration/controller/core/queue_controller_test.go:98
------------------------------

Ran 2 of 2 Specs in 17.943 seconds
FAIL! -- 1 Passed | 1 Failed | 0 Pending | 0 Skipped
--- FAIL: TestAPIs (17.94s)
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T15:17:50Z

If my theory is correct, we should also observe failures for cluster queues.

**But...**

The reason we don't might be because of the "assume" mechanism: Before we update the QW in the API, we update it in the cache, so the cache is up to date.

Maybe it could still fail for the case when a workload finishes (we do a CQ reconcile, but the cache update happens later).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T15:21:45Z

I think you should be able to verify my theory if you raise the log level to 2 or 3 (not sure how to do that on tests) to see the order in which we process events. If it's not easy to setup a flag, feel free to hardcode the level somewhere in test/integration/framework.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T16:07:34Z

> I think you should be able to verify my theory if you raise the log level to 2 or 3 (not sure how to do that on tests) to see the order in which we process events. If it's not easy to setup a flag, feel free to hardcode the level somewhere in test/integration/framework.

`--args --ginkgo.vv -test.v`

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-10T16:25:10Z

It seems that the different between Queue and ClusterQueue is that in ClusterQueue we always add an event when an admitted QW is updated https://github.com/kubernetes-sigs/kueue/blob/b40d12cb980faa3f6d3b308f93502a6acba3b8b9/pkg/controller/core/clusterqueue_controller.go#L147

While in Queue we do that only if the queue name changed
https://github.com/kubernetes-sigs/kueue/blob/b40d12cb980faa3f6d3b308f93502a6acba3b8b9/pkg/controller/core/queue_controller.go#L140

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-10T16:28:43Z

> I don't think we should solve this by "being more noisy". If there is a race condition, we should solve it.

@alculquicondor shouldn't we update the Queue status when a Workload finishes? currently this is not guaranteed, right?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T16:34:19Z

> While in Queue we do that only if the queue name changed

But if the queue name doesn't change, that's covered too:

https://github.com/kubernetes-sigs/kueue/blob/b40d12cb980faa3f6d3b308f93502a6acba3b8b9/pkg/controller/core/queue_controller.go#L139-L142

> shouldn't we update the Queue status when a Workload finishes? currently this is not guaranteed, right?

We do. But I think the queue manager might have old information, because the code to update it is in the queuedworkload_controller.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-10T16:52:58Z

ah, I missed the line above!

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-10T17:27:39Z

with verbosity activated

this can provide clues to this
```bash
    1.6469298507993455e+09      ERROR   controller.queue        Reconciler error        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "name": "queue", "namespace": "core-queue-sx92t", "error": "Operation cannot be ful
filled on queues.kueue.x-k8s.io \"queue\": the object has been modified; please apply your changes to the latest version and try again"}
```
This flake is indeed a race condition around queue controller

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T17:40:04Z

Those kind of errors are expected. We always load the object from the informer cache and then update. It's possible that we are trying to update a queue that just got updated and the informer cache didn't have the time to update. But that's fine, because we will try to reconcile again.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-10T17:49:07Z

> The queuedcontroller picks it up, updates the queue manager.

I got confused, I guess you mean queuedworkload_controller; if so, yes, I agree this is clearly the race condition.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-11T02:30:01Z

Agree, after a lot of back and forth , the race condition is on the `queuedworkload_controller` 
https://github.com/kubernetes-sigs/kueue/blob/14cc822119b2b7eb9bc8480e8d2088da263830ca/pkg/controller/core/queuedworkload_controller.go#L65-L170

During the integration tests, the race condition is seen after creating, updating or deleting (finishing) a workload, the queue.status or clusterqueue.status has still 1 or 2 pendingWorkloads.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T13:19:08Z

I am seeing this flake in ClusterQueue with real deployment.

The race is now clear, two events at the same time: one updating the internal state and one trying to update status. We need to synchronize them or merge those two

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T13:20:13Z

I actually wonder if we should simply have a timer that wakes up every few seconds to check if there was an update and reflect it, this should be simpler, reliable and fairly acceptable UX.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-15T13:39:30Z

We just need to trigger the Reconcile from queuedworkload_controller. @ArangoGutierrez is looking into how to do that with controller-runtime.

> I actually wonder if we should simply have a timer that wakes up every few seconds to check if there was an update and reflect it

How often? Iterate over all objects? It sounds like the kind of rabbit hole the old CronJob went into.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T13:49:19Z

/retitle Integration test is flaky for status updates

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T13:56:12Z

> We just need to trigger the Reconcile from queuedworkload_controller. @ArangoGutierrez is looking into how to do that with controller-runtime.

We need to throttle the update frequency and perhaps do some form of batching, issuing an update on every workload that starts or finish could be too much in a busy cluster.

> How often? Iterate over all objects? It sounds like the kind of rabbit hole the old CronJob went into.

I think this is different, and could be a reasonable short term solution; for one, we wouldn't be listing from the API server, the list is already indexed in memory; second, the scale is different: the number of Qs and CQs should be a lot less than number of jobs. We already iterate over all nodes and sometimes pods in the scheduler, which is far more than what we would have as Qs/QCs.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-15T13:59:52Z

> We need to throttle the update frequency and perhaps do some form of batching, issuing an update on every workload that starts or finish could be too much in a busy cluster.

That's not hard to do.

```golang
workqueue.AddAfter(key, batchPeriod)
```

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T14:03:05Z

> workqueue.AddAfter(key, batchPeriod)

How would that batch things? doesn't it just shift processing the events?

This actually might a good short term hack to fix the flake, just delay the status update a few seconds :)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T14:06:15Z

> How would that batch things? doesn't it just shift processing the events?

hmm, actually this would help because we don't need the other events to be processed to reflect on the status.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-15T14:19:23Z

so if at 00:00 you do `AddAfter(key, 1h)`

Any other calls between 00:00 and 01:00 are basically ignored.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:33:48Z

tried this solution by doing `s/Add/AddAfter` here
https://github.com/kubernetes-sigs/kueue/blob/fc647daae1b4ebe9e4cc9a438e1f068ff2fcd14b/pkg/controller/core/queue_controller.go#L129-L164

and up to 3 seconds, the e2e still fails :(

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:39:15Z

Yesterday I played around changing the controller watch from `kind` to `informer` but is still the same race.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T15:45:10Z

> and up to 3 seconds, the e2e still fails :(

did you do it to all of them? seems working better for me in a live cluster. Of course timing is never going to solve a flake, but I am surprised that it is still happening frequent enough for you to spot it.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:52:57Z

testing it on PROW infra.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:55:52Z

Here you go -> https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/120/pull-kueue-test-integration-main/1503761433379213312

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T15:58:21Z

#120 got 1/5 runs

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-15T16:30:00Z

Locally using `while true; do KUBEBUILDER_ASSETS="/home/eduardo/.local/share/kubebuilder-envtest/k8s/1.23.3-linux-amd64" go test -count=1 ./test/integration/...; done` 
Test fails 1/8 times

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-15T20:09:20Z

/reopen

this is mitigated, not fixed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-15T20:09:33Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/101#issuecomment-1068421146):

>/reopen
>
>this is mitigated, not fixed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
