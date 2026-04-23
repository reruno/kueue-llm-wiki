# Issue #6161: [flaky integration test] Job with elastic jobs via workload-slices support when ElasticJobsViaWorkloadSlices is enabled when Job is opted in Should support job scale-down and scale-up

**Summary**: [flaky integration test] Job with elastic jobs via workload-slices support when ElasticJobsViaWorkloadSlices is enabled when Job is opted in Should support job scale-down and scale-up

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6161

**Last updated**: 2025-07-28T14:44:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-24T08:43:06Z
- **Updated**: 2025-07-28T14:44:31Z
- **Closed**: 2025-07-28T14:44:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 11

## Description

/kind flake

**What happened**:
failure on nighlty build: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1948271619319271424
**What you expected to happen**:
no failures
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:3211 with:
Expected
    <resource.Quantity>: {
        i: {value: 300, scale: -3},
        d: {Dec: nil},
        s: "300m",
        Format: "DecimalSI",
    }
to be equivalent to
    <resource.Quantity>: {
        i: {value: 200, scale: -3},
        d: {Dec: nil},
        s: "200m",
        Format: "DecimalSI",
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:3211 with:
Expected
    <resource.Quantity>: {
        i: {value: 300, scale: -3},
        d: {Dec: nil},
        s: "300m",
        Format: "DecimalSI",
    }
to be equivalent to
    <resource.Quantity>: {
        i: {value: 200, scale: -3},
        d: {Dec: nil},
        s: "200m",
        Format: "DecimalSI",
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:3212 @ 07/24/25 06:48:02.774
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-24T08:43:18Z

cc @ichekrygin

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-24T17:00:04Z

After a successful verification run locally, I suspect that the `10s` timeout may not be large enough for this functionality. WDYT? I can create a PR to bump it up to say `30s`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-24T17:09:51Z

Can you run locally in a loop? Maybe it fails something like 1% of the times? 

What I usually do is somthing like

```golang
for i  := range 100 {
  ginkgo.It(fmt.Sprintf("test %d", i), func() {
```
> WDYT? I can create a PR to bump it up to say 30s.

sure if we cannot repro just by looking it is likely due to timeout, in that case I would just use the LongTimeout=45s. Sometimes the machines on CI are loaded and admission may take time

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-24T19:19:19Z

> What I usually do is somthing like
> 
> ```for i  := range 100 {
>   ginkgo.It(fmt.Sprintf("test %d", i), func() {```

The failure rate with ^ is 3%, e.g., (3 failures out of 100 runs). I still think this is due to some environmental issues that result in a delay triggering the timeout failure.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T00:02:52Z

So... I am digging into an integration test failure, and I am a bit stuck.
It appears that the **ClusterQueue** does not always record workload removal, which results in incorrect flavor utilization.

I am focusing on this code path:
[https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/clusterqueue.go#L493](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/clusterqueue.go#L493)

```go
if admitted {
	updateFlavorUsage(frUsage, c.AdmittedUsage, op)
	c.admittedWorkloadsCount += op.asSignedOne()
}
```

If I understand this correctly, we only update flavor usage and increment **or, more importantly, decrement** `c.admittedWorkloadsCount` **if and only if** the workload is `admitted`.

Is that the intended behavior?

The issue I see is: if the **"old" workload slice** transitions to `Finished` and its `Admitted` condition is reset **before** `updateWorkloadUsage` has a chance to process it, the count in `admittedWorkloadsCount` might drift out of sync.

---

### **Observed State**

When dumping the ClusterQueue status in the integration test assertion (when this issue occurs), I see:

```
cluster queue is retrieved {
  [{default [{cpu {{200 -3} {<nil>} 200m DecimalSI} {{0 0} {<nil>} 0 DecimalSI}}]}] <-- cq usage
  [{default [{cpu {{300 -3} {<nil>} 300m DecimalSI} {{0 0} {<nil>} 0 DecimalSI}}]}] <-- flavor usage
  0 1 2 <-- admitted count
  [{Active True 1 2025-07-24 16:25:07 -0700 PDT Ready Can admit new workloads}]
  <nil> <nil>
}
```

* **Note:** Different CPU usage values between the cluster queue (200m) and the resource flavor (300m),
* **Also note:** The last `2` indicates `admittedWorkloadsCount` (which was not decremented).

---

### **Logs to Confirm Behavior**

To verify `updateWorkloadUsage` was called for a **de-admitted** workload, I added the following log statements:

```go
log = log.WithName("update.usage").WithValues("op", op.asSignedOne())
admitted := workload.IsAdmitted(wi.Obj)
log.V(1).Info("admitted count", "current", c.admittedWorkloadsCount)
frUsage := wi.FlavorResourceUsage()
for fr, q := range frUsage {
	if op == add {
		addUsage(c, fr, q)
	}
	if op == subtract {
		removeUsage(c, fr, q)
	}
}
c.updateWorkloadTASUsage(log, wi, op)
if !admitted && op == subtract {
	log.V(1).Info("admitted count", "SKIPPED", c.admittedWorkloadsCount)
}
if admitted {
	updateFlavorUsage(frUsage, c.AdmittedUsage, op)
	c.admittedWorkloadsCount += op.asSignedOne()
}
log.V(1).Info("admitted count", "new", c.admittedWorkloadsCount)
```

**Observed logs:**

```
2025-07-24T16:25:08.334401-07:00	DEBUG	workload-reconciler.update.usage	cache/clusterqueue.go:484	admitted count	
	{"workload": {"name":"job-job1-483bb","namespace":"core-5lpsd"}, "queue": "default", 
	 "status": "finished", "prevStatus": "admitted", "clusterQueue": "default", "op": -1, "current": 1}

2025-07-24T16:25:08.334426-07:00	LEVEL(-3)	scheduler	scheduler/scheduler.go:823	Replaced	
	{"schedulingCycle": 68, "workload": {"name":"job-job1-5cbe3","namespace":"core-5lpsd"}, 
	 "clusterQueue": {"name":"default"}, "old slice": {"name":"job-job1-483bb","namespace":"core-5lpsd"}, 
	 "new slice": {"name":"job-job1-5cbe3","namespace":"core-5lpsd"}, "reason": "WorkloadSliceReplaced", 
	 "message": "Replaced to accommodate a workload (UID: ec270e53-fc1c-42a0-980f-9adc2ec3e34d, JobUID: ae22e616-8526-43eb-a2cc-2069adfe969a) 
	             due to workload slice aggregation", "old-queue": {"name":"default"}}

2025-07-24T16:25:08.33447-07:00	DEBUG	workload-reconciler.update.usage	cache/clusterqueue.go:496	admitted count	
	{"workload": {"name":"job-job1-483bb","namespace":"core-5lpsd"}, "queue": "default", 
	 "status": "finished", "prevStatus": "admitted", "clusterQueue": "default", "op": -1, "SKIPPED": 1}

2025-07-24T16:25:08.334482-07:00	DEBUG	workload-reconciler.update.usage	cache/clusterqueue.go:503	admitted count	
	{"workload": {"name":"job-job1-483bb","namespace":"core-5lpsd"}, "queue": "default", 
	 "status": "finished", "prevStatus": "admitted", "clusterQueue": "default", "op": -1, "new": 1}
```


The skipped subtraction is what causes the admitted workload count and flavor utilization to be off.

This manifests later when processing the **new slice**:

```
2025-07-24T16:25:08.33783-07:00	DEBUG	workload-reconciler.update.usage	cache/clusterqueue.go:484	admitted count	
	{"workload": {"name":"job-job1-5cbe3","namespace":"core-5lpsd"}, "queue": "default", 
	 "status": "admitted", "prevStatus": "pending", "clusterQueue": "default", "op": 1, "current": 1}

2025-07-24T16:25:08.337837-07:00	DEBUG	workload-reconciler.update.usage	cache/clusterqueue.go:503	admitted count	
	{"workload": {"name":"job-job1-5cbe3","namespace":"core-5lpsd"}, "queue": "default", 
	 "status": "admitted", "prevStatus": "pending", "clusterQueue": "default", "op": 1, "new": 2}
```

It is possible that we see this issue being triggered by workload slice "old" slice removal. 

Unlike the "traditional" workload preemption, the workload slice removal process is more direct, as we directly apply(activate) the "Finished" condition. This may have shortened the duration between the `eviction` event and the `Admitted` condition reset, which is missed during the ClusterQueue’s `updateWorkloadUsage`.

Again, it is hard to comment with a degree of certainty without knowing the rationale behind:
```golang
if admitted {
	updateFlavorUsage(frUsage, c.AdmittedUsage, op)
	c.admittedWorkloadsCount += op.asSignedOne()
}
```

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T01:01:20Z

Just for the record, 

If I remove the above-mentioned `if admitted` condition, and update flavor usage and admitted workloads count for all workloads (admitted or not) - I don't encounter this problem even after 1000 consecutive back-to-back runs.

```Ran 1000 of 1051 Specs in 2732.614 seconds
SUCCESS! -- 1000 Passed | 0 Failed | 0 Pending | 51 Skipped
PASS
```

but it fails
```Summarizing 1 Failure:
  [FAIL] ClusterQueue controller when Reconciling clusterQueue usage status [It] Should update status and report metrics when workloads are assigned and finish [slow]
  /Users/ichekrygin/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/clusterqueue_controller_test.go:294

Ran 28 of 28 Specs in 49.195 seconds
FAIL! -- 27 Passed | 1 Failed | 0 Pending | 0 Skipped
```
an possibly others.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T11:46:25Z

> If I understand this correctly, we only update flavor usage and increment or, more importantly, decrement c.admittedWorkloadsCount if and only if the workload is admitted.
> Is that the intended behavior?

The intention of the code is to discriminate if the deleted workload was admitted or just "quota reserved". It is possible that the old workload was jut quota reserved, an d

> The issue I see is: if the "old" workload slice transitions to Finished and its Admitted condition is reset before updateWorkloadUsage has a chance to process it, the count in admittedWorkloadsCount might drift out of sync.

I'm actually surprised the Admitted condition would be reset in the process. Could you log all conditions which are on a workload when the test fails, and when we handle the delete in updateWorkloadUsage?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T16:53:34Z

After adding additional log messages (per @mimowo suggestion), I now have a better understanding of what’s happening.

Contrary to my initial assumption that the `Admitted` condition is getting reset (too quickly or otherwise), the actual issue appears to be the opposite: the workload conditions (`QuotaReserved`, `Admitted`, and `Finished`) are **not being propagated fast enough**, resulting in **inconsistent updates** within the ClusterQueue.

Here’s a code snippet with the added log messages:

```go
// updateWorkloadUsage updates the usage of the ClusterQueue for the workload
// and the number of admitted workloads for local queues.
func (c *clusterQueue) updateWorkloadUsage(log logr.Logger, wi *workload.Info, op usageOp) {
	log = log.WithName("update.usage").WithValues("op", op.asSignedOne())
	admitted := workload.IsAdmitted(wi.Obj)
	if !admitted {
		log.Info("NOT ADMITTED INITIAL", "conditions", wi.Obj.Status.Conditions)
	}
	frUsage := wi.FlavorResourceUsage()
	for fr, q := range frUsage {
		if op == add {
			addUsage(c, fr, q)
		}
		if op == subtract {
			removeUsage(c, fr, q)
		}
	}
	c.updateWorkloadTASUsage(log, wi, op)
	if admitted {
		updateFlavorUsage(frUsage, c.AdmittedUsage, op)
		c.admittedWorkloadsCount += op.asSignedOne()
	} else {
		log.Info("NOT ADMITTED LATER", "conditions", wi.Obj.Status.Conditions)
	}
}
```

Here are the corresponding outputs from the log messages:

**`NOT ADMITTED INITIAL`:**

```json
{
  "workload": {
    "name": "job-job1-2b100",
    "namespace": "core-z77k9"
  },
  "queue": "default",
  "status": "finished",
  "prevStatus": "admitted",
  "clusterQueue": "default",
  "op": -1,
  "conditions": null
}
```

**`NOT ADMITTED LATER`:**

```json
{
  "workload": {
    "name": "job-job1-2b100",
    "namespace": "core-z77k9"
  },
  "queue": "default",
  "status": "finished",
  "prevStatus": "admitted",
  "clusterQueue": "default",
  "op": -1,
  "conditions": [
    {
      "type": "QuotaReserved",
      "status": "True",
      "observedGeneration": 1,
      "lastTransitionTime": "2025-07-25T16:40:44Z",
      "reason": "QuotaReserved",
      "message": "Quota reserved in ClusterQueue default"
    },
    {
      "type": "Admitted",
      "status": "True",
      "observedGeneration": 1,
      "lastTransitionTime": "2025-07-25T16:40:44Z",
      "reason": "Admitted",
      "message": "The workload is admitted"
    },
    {
      "type": "Finished",
      "status": "True",
      "lastTransitionTime": "2025-07-25T16:40:44Z",
      "reason": "WorkloadSliceReplaced",
      "message": "Replaced to accommodate a workload (UID: 08f58c66-b86c-4ab4-b406-e96c7a00ef80, JobUID: 1b85839a-8400-4765-9c60-d299fc23f112) due to workload slice aggregation"
    }
  ]
}
```

From this, it appears that by the time `updateWorkloadUsage` is called, the workload’s status conditions have not yet fully propagated. This leads to stale or partial state being used to update resource usage in the ClusterQueue, resulting in inconsistent accounting.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T17:52:11Z

This is very interesting, so it seems a bit of a corner case which is unlikely in practice where the Job is resized immediately after admission before the Admitted condition is observed by scheduler, but already observed by the test code.

I'm not worried about this as for alpha feature, but I'm wondering it may be uncovering also a gap in regular workloads that could lead to leaking capacity, just never tested.

We should continue investigating. I will try to book time next week as well.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T17:56:49Z

iiiuc if the test failures become annoying as too frequent we can just plumb them temporarily by injecting time.Sleep 200ms after admission. However, I don't think they are that frequent yet, let's observe and maybe we can fix properly

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T18:38:24Z

> temporarily by injecting time.Sleep 200ms

My thoughts as well. That said, I want to dig a little deeper into this to understand why it is happening.
