# Issue #2244: Flaky integration test: Should preempt Workloads with lower priority when there is not enough quota

**Summary**: Flaky integration test: Should preempt Workloads with lower priority when there is not enough quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2244

**Last updated**: 2024-05-23T08:31:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-21T07:39:32Z
- **Updated**: 2024-05-23T08:31:47Z
- **Closed**: 2024-05-22T15:51:08Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 12

## Description

/kind flake

**What happened**:

The test failed on the periodic build of the main branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1791517099273752576

**What you expected to happen**:

No flake

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build

**Anything else we need to know?**:

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:456 with:
Expected
    <int>: 3
to equal
    <int>: 2 failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:456 with:
Expected
    <int>: 3
to equal
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/preemption_test.go:139 @ 05/17/24 17:21:11.919
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-21T07:39:45Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T09:24:19Z

This looks to the result of a race condition between the processing of an evicted workload update event and a new scheduling cycle:

```
  2024-05-17T17:21:06.631421089Z	LEVEL(-3)	scheduler	preemption/preemption.go:189	Preempted	{"workload": {"name":"high-wl-2","namespace":"preemption-k4742"}, "clusterQueue": {"name":"cq"}, "targetWorkload": {"name":"low-wl-1","namespace":"preemption-k4742"}, "reason": "InClusterQueue", "message": "Preempted to accommodate a workload (UID: a7186187-5b4f-4fc4-814f-e12cd51b37fb) in the ClusterQueue"}

  2024-05-17T17:21:06.63151412Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:577	Workload update event	{"workload": {"name":"low-wl-1","namespace":"preemption-k4742"}, "queue": "q", "status": "admitted", "clusterQueue": "cq"}

  2024-05-17T17:21:06.632144739Z	LEVEL(-3)	scheduler	preemption/preemption.go:189	Preempted	{"workload": {"name":"high-wl-2","namespace":"preemption-k4742"}, "clusterQueue": {"name":"cq"}, "targetWorkload": {"name":"low-wl-2","namespace":"preemption-k4742"}, "reason": "InClusterQueue", "message": "Preempted to accommodate a workload (UID: a7186187-5b4f-4fc4-814f-e12cd51b37fb) in the ClusterQueue"}

  2024-05-17T17:21:06.645738775Z	LEVEL(-3)	scheduler	queue/manager.go:475	Obtained ClusterQueue heads	{"count": 1}

  2024-05-17T17:21:06.645972158Z	LEVEL(-3)	scheduler	preemption/preemption.go:193	Preemption ongoing	{"workload": {"name":"high-wl-2","namespace":"preemption-k4742"}, "clusterQueue": {"name":"cq"}, "targetWorkload": {"name":"low-wl-1","namespace":"preemption-k4742"}}

  2024-05-17T17:21:06.64691226Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:577	Workload update event	{"workload": {"name":"low-wl-2","namespace":"preemption-k4742"}, "queue": "q", "status": "admitted", "clusterQueue": "cq"}

  2024-05-17T17:21:06.665511962Z	LEVEL(-3)	scheduler	preemption/preemption.go:189	Preempted	{"workload": {"name":"high-wl-2","namespace":"preemption-k4742"}, "clusterQueue": {"name":"cq"}, "targetWorkload": {"name":"low-wl-2","namespace":"preemption-k4742"}, "reason": "InClusterQueue", "message": "Preempted to accommodate a workload (UID: a7186187-5b4f-4fc4-814f-e12cd51b37fb) in the ClusterQueue"}
```

The situation (setting the eviction condition for `low-wl-2`)  is not ideal however since the call is idempotent it has no impact on the overall scheduling mechanics, the only problem being an additional increment done to the `EvictedWorkloadsTotal` metric.

Making the `applyPreemptionWithSSA` use strict patch should cover this scenario. 

One alternative could be to increment the Eviction metric only from the workload controller's update handler when a eviction transition is detected.

/cc @alculquicondor @lowang-bh

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T11:59:26Z

> One alternative could be to increment the Eviction metric only from the workload controller's update handler when a eviction transition is detected.

This sounds like a reliable solution which could be used for other eviction reasons, allowing for less code.  Any drawbacks of the approach?

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T12:08:39Z

> > One alternative could be to increment the Eviction metric only from the workload controller's update handler when a eviction transition is detected.
> 
> This sounds like a reliable solution which could be used for other eviction reasons, allowing for less code. Any drawbacks of the approach?

Just on timing maybe, the update event is visible some milliseconds later, but when it comes to observability this should not be an issue. 

There also cold be other reasons @lowang-bh  choose this approach.  @lowang-bh?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T12:25:20Z

> Just on timing maybe, the update event is visible some milliseconds later, but when it comes to observability this should not be an issue.

yeah, I don't think this is any issue. I would suggest refactoring the code to use this approach.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T12:33:03Z

Thinking about it , in case of multiple kueue-manager running, the non-leaders can "see" the same change multiple times, this could be a problem. 

I think going with #2254 is the easiest path for now.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T12:37:17Z

> Thinking about it , in case of multiple kueue-manager running, the non-leaders can "see" the same change multiple times, this could be a problem.

Ah, good point

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T13:03:25Z

OTOH, I'm not sure if incrementing non-leading replicas is an issue. When such a replica becomes leading it will not start from 0, but it should be fine since counter metrics are usually observed via `rate`, rather than absolute values.

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T13:24:12Z

I'd expect the Prometheus to scrape all the replicas , leader or not at any point in time.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T14:28:29Z

> I'd expect the Prometheus to scrape all the replicas , leader or not at any point in time.

Yeah, but Prometheus itself does not aggregate the values, so aggregation is still up to the admin.

I actually checked it using the [ai on gke](https://github.com/GoogleCloudPlatform/ai-on-gke) project, and could see that the metrics are incremented by controller-runtime per replica, also for non-leading replicas. 

Also, inside kueue we are not very consistent, for example `kueue_admitted_active_workloads` is bumped also for all replicas (via cache) (in this case I have only one workload admitted):
![image](https://github.com/kubernetes-sigs/kueue/assets/10359181/a615ed82-167d-45af-814c-74c778989975)

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T18:57:00Z

> > I'd expect the Prometheus to scrape all the replicas , leader or not at any point in time.
> 
> Yeah, but Prometheus itself does not aggregate the values, so aggregation is still up to the admin.
> 
> I actually checked it using the [ai on gke](https://github.com/GoogleCloudPlatform/ai-on-gke) project, and could see that the metrics are incremented by controller-runtime per replica, also for non-leading replicas.
> 
> Also, inside kueue we are not very consistent, for example `kueue_admitted_active_workloads` is bumped also for all replicas (via cache) (in this case I have only one workload admitted): ![image](https://private-user-images.githubusercontent.com/10359181/332837699-a615ed82-167d-45af-814c-74c778989975.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTYzOTcyOTQsIm5iZiI6MTcxNjM5Njk5NCwicGF0aCI6Ii8xMDM1OTE4MS8zMzI4Mzc2OTktYTYxNWVkODItMTY3ZC00NWFmLTgxNGMtNzRjNzc4OTg5OTc1LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA1MjIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNTIyVDE2NTYzNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTNiZmIyODIzOGUyZTY0OWQ1NzM3YmI2NjBkZDdlM2NmYmIxN2FlYzY0YWU0ZGMyMTcwYTE1NzIxMjVkN2JmYzImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Cbh6CfL5D4QhbW8cthOduv2QfIszgVK5OGNiDc7w4Vs)

In a real life dashboard is very likely that the end user doesn't want to take into account which of the replicas is the leader at some point in time, so some kind of aggregation capability is expected. Maybe we should think about this for all the metrics we are producing.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-23T08:31:46Z

I guess we can park this for now. We have another good (or even better) solution to the issue.
