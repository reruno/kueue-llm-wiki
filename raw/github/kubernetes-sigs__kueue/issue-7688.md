# Issue #7688: [flaky test] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Summary**: [flaky test] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7688

**Last updated**: 2025-11-26T14:12:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-17T07:25:34Z
- **Updated**: 2025-11-26T14:12:39Z
- **Closed**: 2025-11-26T14:12:39Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 11

## Description

/kind flake 

**What happened**:
failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1990131289172217856
**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited expand_less	18s
{Timed out after 10.006s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.006s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:1057 @ 11/16/25 19:16:39.271
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T07:25:48Z

cc @IrvingMg @PBundyra ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:06:46Z

Actually, this looks to me as a bug in the entry penalties. After the quota in cq1 indeed we observe:

so we have scheduling:
```
  2025-11-16T19:16:29.191107966Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:631	Workload assumed in the cache	{"schedulingCycle": 507, "workload": {"name":"workload-mqfzr","namespace":"core-wgjxw"}, "clusterQueue": {"name":"cq1"}}
```
and the entry penalty is taken into account: `"Usage": 5.95`
```
  2025-11-16T19:16:29.197543159Z	LEVEL(-3)	cluster-queue-reconciler	queue/cluster_queue.go:563	Resource usage from LocalQueue	{"clusterQueue": {"name":"cq1"}, "LocalQueue": "lq-a", "Usage": 5.9510000000000005}
```
however this is lost very quickly in the scheduling cycle:
```
  2025-11-16T19:16:29.241861737Z	LEVEL(-3)	cluster-queue-reconciler	queue/cluster_queue.go:563	Resource usage from LocalQueue	{"clusterQueue": {"name":"cq1"}, "LocalQueue": "lq-a", "Usage": 3.951}
```
so the entry penalty was not accounted just 60ms later.

So the usage quickly went up, but then fall down to the exactly same value: 3.951 -> 5.951 -> 3.951

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:11:27Z

but the used configuration is :

```golang
UsageHalfLifeTime: metav1.Duration{
	Duration: 1 * time.Second,
},
UsageSamplingInterval: metav1.Duration{
	Duration: 1 * time.Second,
},
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:11:52Z

Given we are going with AFS to Beta in 0.15 I would really like to understand and fix the issues

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T09:15:01Z

Given that the entry penalty is indeed accounted for a short while we could probably make the test stable by putting the CQ on hold rather than by releasing the quota by finishing workloads. However, this could probably just swipe the issue under the rug.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T13:11:54Z

One more thing is that before the usage used for comparison dropped `5.951 -> 3.951` there was a LQ reconcile:

```
  2025-11-16T19:16:29.207332994Z	LEVEL(-3)	localqueue-reconciler	core/localqueue_controller.go:311	Updated LocalQueue fair sharing status	{"namespace": "core-wgjxw", "name": "lq-a", "consumedResources": {"cpu":"5957m"}}
```
The hypothesis I discussed as likely with @PBundyra is that the LQ status was updated with the new value, but we prematurely removed the penalty entry from the cache, and thus until the new LQ status is observed via informer, the usage of `3.951` is used for comparison, which allows the workload from LQb to slip in.

If this hypothesis is confirmed then one idea to fix is to not remove the entryPenalty until the new LQ status is actually observed. One way to achieve that is to stemp the penalty instead of removing with the LQ version after each it should be removed. So, whenever we currently remove it now we would add in cache the stamp `discardAfterResourceVersion`, set just after the request to update LQ status succeeds. I'm not sure this solution is simplest, but it should work ok.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-11-19T14:05:06Z

I've synced with @mimowo offline and we both agreed that this flake would be addressed by introducing cache for ConsumedResources stored in LQ's status. This issue describes it: https://github.com/kubernetes-sigs/kueue/issues/6710 and we'd like to converge into this direction

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T14:21:24Z

/assign @IrvingMg 
as this will be resolved by https://github.com/kubernetes-sigs/kueue/issues/7693

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-19T15:04:31Z

I've tried to reproduce the flakiness locally, and after ~300 repetitions the error didn’t occur. To try to validate the hypothesis, I forced the race condition a bit by deleting the penalty before the status update, like this:

```go
func (m *AfsEntryPenalties) updateWithPenalty(lqKey utilqueue.LocalQueueReference, fn func(penalty corev1.ResourceList) error) error {
	m.Lock()
	defer m.Unlock()
	penalty, found := m.penalties.Get(lqKey)
	if !found {
		penalty = corev1.ResourceList{}
	}
	// FORCE RACE: Delete penalty BEFORE status update
	m.penalties.Delete(lqKey)
	if err := fn(penalty); err != nil {
		return err
	}
	return nil
}
```

And this caused the test to fail after 13 attempts with:
```
• [FAILED] [19.496 seconds]
Scheduler when Using AdmissionFairSharing at ClusterQueue level [It] admits one workload from each LocalQueue when quota is limited
/Users/Irving_Mondragon/Documents/git/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:1026

  [FAILED] Timed out after 10.000s.
  The function passed to Eventually failed at /Users/Irving_Mondragon/Documents/git/kueue/test/util/util.go:375 with:
  Not enough workloads are admitted
  Expected
      <int>: 0
  to equal
      <int>: 1
  In [It] at: /Users/Irving_Mondragon/Documents/git/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:1057 @ 11/19/25 15:27:30.09
------------------------------
SSSSSSSS
------------------------------
[AfterSuite] 
/Users/Irving_Mondragon/Documents/git/kueue/test/integration/singlecluster/scheduler/fairsharing/suite_test.go:67
  STEP: tearing down the test environment @ 11/19/25 15:27:32.295
[AfterSuite] PASSED [1.082 seconds]
------------------------------
[DeferCleanup (Suite)] 
/Users/Irving_Mondragon/Documents/git/kueue/test/integration/framework/framework.go:157
[DeferCleanup (Suite)] PASSED [0.000 seconds]
------------------------------

Summarizing 1 Failure:
  [FAIL] Scheduler when Using AdmissionFairSharing at ClusterQueue level [It] admits one workload from each LocalQueue when quota is limited
  /Users/Irving_Mondragon/Documents/git/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:1057

Ran 1 of 26 Specs in 24.430 seconds
FAIL! -- 0 Passed | 1 Failed | 0 Pending | 25 Skipped
--- FAIL: TestScheduler (24.43s)
FAIL

Tests failed on attempt #13


Ginkgo ran 1 suite in 3m40.05684375s

Test Suite Failed
```

I'll address the issue as @PBundyra suggests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T15:18:28Z

Yeah, the race is unlikely because the following is possible:
1. we update the status LQ
2. we remove the penalty entries
3. we read the new LQ status from informer

Typically the event at (3.) is very quickly after (1.), but it may take even seconds on a busy system.

Yes, solution we discussed would be to follow the pattern we do for regular usage. Here, the entry penalties play the role of the "assumed usage". Once a workload is transitioned from assumed -> admitted, then we can merge the entry penalities into the cached usage. Then, the status plays only informational role. We may also use the status in CREATE event to initialize the cache after restart.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T11:20:33Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7879/pull-kueue-test-integration-baseline-main/1993269609586757632
