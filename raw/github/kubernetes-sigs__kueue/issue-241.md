# Issue #241: A workload may not be retried if setting the Admission field fails

**Summary**: A workload may not be retried if setting the Admission field fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/241

**Last updated**: 2022-05-07T09:18:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-05-01T03:16:48Z
- **Updated**: 2022-05-07T09:18:29Z
- **Closed**: 2022-05-07T09:18:29Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Test flake: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/227/pull-kueue-test-integration-main/1520594730851766272

From the [logs](https://storage.googleapis.com/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/227/pull-kueue-test-integration-main/1520594730851766272/build-log.txt) , the workload was assumed but we failed to set the `Admission`  field because the object has changed:

```
Could not admit workload and assigning flavors in apiserver	{"workload": {"name":"job","namespace":"core-67497"}, 
"clusterQueue": {"name":"cluster-queue-with-selector"}, "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io 
\"job\": the object has been modified; please apply your changes to the latest version and try again"}
```

and requeuing the workload didn't actually add it to the queue because the workload already existed, which is expected:

```
scheduler	Workload re-queued	{"workload": {"name":"job","namespace":"core-67497"}, "clusterQueue": 
{"name":"cluster-queue-with-selector"}, "workload": {"name":"job","namespace":"core-67497"}, 
"queue": {"name":"queue-for-selector","namespace":"core-67497"}, "added": false, "status": "assumed"}
```

but then the logs don't show that the workload was tried again, and so the scheduler never got to retry to set the admission field again in the apiserver.

**What you expected to happen**:

The workload to be retried and eventually admitted.

/kind bug

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-02T13:52:00Z

> and requeuing the workload didn't actually add it to the queue because the workload already existed, which is expected:

It existed because of the update event that happened during the scheduling cycle?
If so, wouldn't the pod be in the scheduling queue?

In any case, we need to prioritize SSA #164

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-02T22:52:15Z

/assign

Even without SSA, there should have been more retries. I can investigate.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T03:25:03Z

I am guessing this is starting to happen because we shifted to use BestEffortFIFO in all the integration tests.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T03:44:34Z

There is another flake, slightly similar, but not exactly: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/224/pull-kueue-test-integration-main/1521319895239757824

This case could be solved with SSA, but still why are we not trying with the newer version in the following attempts? 

btw, this potential bug is showing up probably because we are testing with the job-controller using Job, so there is certainly benefit to keep having those scheduler tests using jobs rather than workload only.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-03T10:59:14Z

I think this pr https://github.com/kubernetes-sigs/kueue/pull/245 maybe solve the problem. I just make sure that the element requeued is the newest. At least to me, I haven't meet this error after.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T14:06:40Z

I think this could happen with just one workload if it barely fits in the ClusterQueue. This is the sequence of events:

1. Create workload
2. Workload is updated with pending status because Queue doesn't exist
3. Create queue
4. Workload is assumed and goes into async admission.
5. Event for update in 2 is received.
6. Scheduler tries to schedule the workload again. Since another version of the same workload is already assumed, it doesn't fit again. The workload is put in the inadmissible set.
7. The async admission fails because the workload had changed.
8. The workload is requeued, but with an old version. The newer version remains in the inadmissible set.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T14:10:17Z

We could say that there are 2 bugs, as described in step 8 above. #245 only resolves the first part, but leaves a phantom workload in the inadmissible set.

Solving just the second bug might make the first problem a non-bug.  But maybe it's better to always try to re-queue the newer version?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T14:51:38Z

> btw, this potential bug is showing up probably because we are testing with the job-controller using Job, so there is certainly benefit to keep having those scheduler tests using jobs rather than workload only.

I think it's still independent of it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-03T15:24:37Z

> I think this could happen with just one workload if it barely fits in the ClusterQueue. This is the sequence of events:
> 
> 1. Create workload
> 2. Workload is updated with pending status because Queue doesn't exist
> 3. Create queue
> 4. Workload is assumed and goes into async admission.
> 5. Event for update in 2 is received.
> 6. Scheduler tries to schedule the workload again. Since another version of the same workload is already assumed, it doesn't fit again. The workload is put in the inadmissible set.
> 7. The async admission fails because the workload had changed.
> 8. The workload is requeued, but with an old version. The newer version remains in the inadmissible set.

The failing test is a StrictFIFO queue, and this problem might still happen. I have add some explains here https://github.com/kubernetes-sigs/kueue/pull/245#discussion_r863892663, maybe helpful.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T15:30:48Z

The error in the link above https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/224/pull-kueue-test-integration-main/1521319895239757824 is on a BestEffortFIFO queue.

I missed analyzing the original link https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/227/pull-kueue-test-integration-main/1520594730851766272. I'll do that now.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T17:45:58Z

Analysis for https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/227/pull-kueue-test-integration-main/1520594730851766272 is quite different.

1. Create workload
2. Admission attempt 1: fails because the namespace doesn't match. This produces a status update.
3. Workload is requeued immediately, because the queue is StrictFIFO
4. Admission attempt 2: enters the async admission.
5. Event for step 2 is receive, workload is queued again.
6. Admission attempt 3 starts, now the workload is not in the queue. The attempt fails because the workload is already assumed.
8.  Async admission from attemp 2 fails, because there was an update in the workload object. Requeue first version of the workload. Since there is no copy of the workload in the queues, it is accepted.
9. Requeue from admission attempt doesn't actually requeue, because the workload is already there. This version of the workload is lost.

With this analysis, I now agree that #245 is also necessary.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-03T18:31:17Z

> > btw, this potential bug is showing up probably because we are testing with the job-controller using Job, so there is certainly benefit to keep having those scheduler tests using jobs rather than workload only.
> 
> I think it's still independent of it.

May be, but this issue shows the tricky race conditions that could happen when objects are being updated by different controllers; the job controller is also involved in updating the workload object, and so it is beneficial to also have it in the test.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-07T09:18:29Z

With https://github.com/kubernetes-sigs/kueue/pull/245 being merged, I assume we can close this issue
