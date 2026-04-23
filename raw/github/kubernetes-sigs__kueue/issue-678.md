# Issue #678: Flaky test:  Scheduler when Queueing with StrictFIFO Should schedule workloads by their priority strictly

**Summary**: Flaky test:  Scheduler when Queueing with StrictFIFO Should schedule workloads by their priority strictly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/678

**Last updated**: 2023-04-06T19:37:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-06T12:32:25Z
- **Updated**: 2023-04-06T19:37:37Z
- **Closed**: 2023-04-06T19:37:37Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 10

## Description

**What happened**:

Flaky integration test: `Scheduler when Queueing with StrictFIFO Should schedule workloads by their priority strictly`

```
{Timed out after 30.000s.
Expected
    <int>: 2
to equal
    <int>: 1 failed [FAILED] Timed out after 30.000s.
Expected
    <int>: 2
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/scheduler_test.go:894 @ 04/05/23 17:36:19.251
}
```

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/667/pull-kueue-test-integration-main/1643666314289483776

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-06T12:45:17Z

/assign
/priority important-soon

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-06T13:04:29Z

@tenzen-y can you pass it to me?

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-06T13:05:31Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-06T13:13:39Z

I talked with @mcariatm. And I agreed @mcariatm will work on this issue.

/unassign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T15:30:31Z

Relevant log lines:

First admission:
```
  2023-04-05T17:35:45.991228857Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:279	Workload assumed in the cache	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "clusterQueue": {"name":"strict-fifo-cq"}}
  2023-04-05T17:35:46.001364015Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:272	Workload update event	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "queue": "strict-fifo-q", "status": "admitted", "prevStatus": "pending", "clusterQueue": "strict-fifo-cq"}
  2023-04-05T17:35:46.000531317Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:295	Workload successfully admitted and assigned flavors	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "clusterQueue": {"name":"strict-fifo-cq"}}
  2023-04-05T17:35:46.001364015Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:272	Workload update event	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "queue": "strict-fifo-q", "status": "admitted", "prevStatus": "pending", "clusterQueue": "strict-fifo-cq"}
```

Then random flipping back to pending:
```
  2023-04-05T17:35:46.0070339Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:272	Workload update event	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "queue": "strict-fifo-q", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "strict-fifo-cq"}
```

Then admitted again:
```
  2023-04-05T17:35:46.013543285Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:279	Workload assumed in the cache	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "clusterQueue": {"name":"strict-fifo-cq"}}
  2023-04-05T17:35:46.023153745Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:295	Workload successfully admitted and assigned flavors	{"workload": {"name":"wl1","namespace":"foo-9twnv"}, "clusterQueue": {"name":"strict-fifo-cq"}}
```


The question is why it went back to pending.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-06T17:27:45Z

I'm investigating.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T17:52:30Z

I have a theory:
It's a `WorkloadReconciler.Reconcile` routine that runs super slow and still has old information about the world (or maybe the API call takes too long to reach the apiserver). This call sets Admitted=false via SSA, possibly overriding the admission by scheduler in a different routine.

I think the fix is just to add the `resourceVersion` into the SSA patch when setting `Admitted=false`. Although this is almost the same as doing a regular Update. This should be fine as Workload reconciliation is best effort and doesn't need to be performant.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T18:08:35Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-06T18:10:38Z

Umm. It's a distributed system :(
It sounds reasonable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-06T18:47:58Z

/unassign @mcariatm
