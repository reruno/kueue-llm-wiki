# Issue #8809: [flaky test] Workload controller with resource retention when manager is setup with tiny retention period should delete the workload after retention period elapses [slow]

**Summary**: [flaky test] Workload controller with resource retention when manager is setup with tiny retention period should delete the workload after retention period elapses [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8809

**Last updated**: 2026-02-02T15:04:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T08:34:05Z
- **Updated**: 2026-02-02T15:04:31Z
- **Closed**: 2026-02-02T15:04:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar), [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 14

## Description


**Which test is flaking?**:

Workload controller with resource retention when manager is setup with tiny retention period should delete the workload after retention period elapses [slow]

**First observed in** (PR or commit, if known):
don't know
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8594/pull-kueue-test-integration-extended-main/2016057539640168448
**Failure message or logs**:
```
Core Controllers Suite: [It] Workload controller with resource retention when manager is setup with tiny retention period should delete the workload after retention period elapses [slow] expand_less	47s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/workload_controller_test.go:873 @ 01/27/26 08:02:56.24
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T08:34:16Z

cc @mykysha @mbobrovskyi @sohankunkerkar ptal

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-27T13:59:00Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T09:18:17Z

one more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8885/pull-kueue-test-integration-extended-main/2017162522699763712

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-30T09:26:25Z

I think the fix could be to add:
```go
		// Proactively purge this workload from in-memory caches as soon as we decide
		// to delete it. This avoids relying solely on a later delete event/reconcile
		// to unblock ClusterQueue/Flavor finalizers.
		//
		// This is safe because finished workloads are not schedulable and should not
		// block cache-based garbage collection once their retention has elapsed.
		r.deleteWorkloadFromCaches(ctx, req.Namespace, req.Name)
```
before https://github.com/kubernetes-sigs/kueue/blob/3b37ca3b9f11d86ec07a04a362cd1b48d59035e3/pkg/controller/core/workload_controller.go#L212

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T09:56:47Z

@vladikkuzn do you want to propose PR?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-30T12:28:01Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:04:12Z

Lovely, so it seems we have both alternatives fixing the flake based on the experiments:
- https://github.com/kubernetes-sigs/kueue/pull/8912
- https://github.com/kubernetes-sigs/kueue/pull/8910

Both look reasonable to me, but I see no point merging both. Given that https://github.com/kubernetes-sigs/kueue/pull/8910 is less code this is my preference. 

Let me know @mbobrovskyi @sohankunkerkar @Singularity23x0 @gabesaba if you have another opinion here.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-30T14:35:55Z

  Fundamentally, these approaches differ:                                                                                                                                    
                                                                                                                                                                             
  - **#8910** changes when the cache is cleared (earlier in the retention path)                                                                                            
  - **#8839** adds the missing trigger for CQ reconcile when cache becomes empty                                                                                           
                                                                                                                                                                             
In this test, the workload is deleted once retention elapses (test waits for it), then AfterEach deletes the CQ. #8910 can reduce the race window by clearing cache before `client.Delete()`, making it more likely CQ deletion sees an empty cache but it doesn't add a new trigger, so the race still exists with a smaller window.                                                                                                                                                                                                                                                                     
                                                                                                                                                         
Consider:                                                                                                                                                                  
  1. CQ deletion starts, CQ reconcile runs, cache non-empty → returns without requeue                                                                                        
  2. Later, last workload deleted, cache becomes empty                                                                                                                       
  3. **#8910:** No new CQ trigger → finalizer can stick until another event                                                                                                  
  4. **#8839:** Cache-empty watcher fires → CQ reconciles immediately                                                                                                        
                                                                                                                                                                             
 IIUC, #8910 clears cache before confirming `client.Delete()` succeeds. If delete fails, cache diverges from API state temporarily.                                                                                                                                                                                                                 
                                                                                                                                                                             
  IMO, #8910 may reduce the flake. #8839 fixes the root cause.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:51:19Z

Thank you for the feedback, and analysis, I will be investigating.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T15:32:37Z

Ok, I have analyzed the code a bit more, and I understand why https://github.com/kubernetes-sigs/kueue/pull/8910 doesn't work in principle, because of the follow inteleaving:
1. the CQ has one workload which transitions to Finished
2. the Workload now gets deleted, and workload_controller Reconcile is scheduled
3. CQ receives delete request and typically after the PR it will see empty cache, but this is not guaranteed, if the code is delayed
Issue: if the Reconcile at (2.) takes time, then CQ may decide "not-empty", and still keep the finalizer.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T15:49:05Z

However, what I'm not understanding still, is that the Delete on the ClusterQueue should trigger Reconcile for the clusterqueue_controller.go, and also the Update on the ClusterQueue to see `DeletionTimestamp` triggers the reconcile. So, I expect the Reconcile to step here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/clusterqueue_controller.go#L173C15-L187

Now, the intention of the code is clearly to allow removal of the ClusterQueue when there are no "active" worklaods, regardless of finished workloads, see comment:
```
			// The clusterQueue is being deleted, remove the finalizer only if
			// there are no active reserving workloads.
```
So I understand that the condition shouldn't be "empty clusterqueue", but "no active workloads".

So, while I understand why https://github.com/kubernetes-sigs/kueue/pull/8839 helps with the flake, I suppose we may have a bigger issue that now finished workloads are blocking ClusterQueue deletion.

I think this might be due to our recent changes around tracking finished workloads.

Could you please investigate that @sohankunkerkar and try to verify the hypothesis: we now have a regression and finished workloads are now blocking ClusterQueue deletion (removal of the finalizer). 

If we can confirm the regression, then I think the fix might be rather in the conditions inside the Reconcile for the finalizer removal to make sure "finished workloads are exluded from the analysis"

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T15:58:26Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8746/pull-kueue-test-integration-extended-main/2017263541026820096

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-30T16:54:58Z

> However, what I'm not understanding still, is that the Delete on the ClusterQueue should trigger Reconcile for the clusterqueue_controller.go, and also the Update on the ClusterQueue to see `DeletionTimestamp` triggers the reconcile. So, I expect the Reconcile to step here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/clusterqueue_controller.go#L173C15-L187
> 
> Now, the intention of the code is clearly to allow removal of the ClusterQueue when there are no "active" worklaods, regardless of finished workloads, see comment:
> 
> ```
> 			// The clusterQueue is being deleted, remove the finalizer only if
> 			// there are no active reserving workloads.
> ```
> 
> So I understand that the condition shouldn't be "empty clusterqueue", but "no active workloads".
> 
> So, while I understand why [#8839](https://github.com/kubernetes-sigs/kueue/pull/8839) helps with the flake, I suppose we may have a bigger issue that now finished workloads are blocking ClusterQueue deletion.
> 
> I think this might be due to our recent changes around tracking finished workloads.
> 
> Could you please investigate that [@sohankunkerkar](https://github.com/sohankunkerkar) and try to verify the hypothesis: we now have a regression and finished workloads are now blocking ClusterQueue deletion (removal of the finalizer).
> 
> If we can confirm the regression, then I think the fix might be rather in the conditions inside the Reconcile for the finalizer removal to make sure "finished workloads are exluded from the analysis"

Yeah, you are right! 
There's an inconsistency between the initial cache rebuild which correctly excludes finished workloads with              `!HasQuotaReservation(&w) || IsFinished(&w)`, and the update path in `addOrUpdateWorkloadWithoutLock` which only checks `!HasQuotaReservation(wl)` Since Finish() doesn't clear quota reservation, finished workloads linger in the cache until explicitly deleted. This means ClusterQueueEmpty can return false even when only finished  workloads remain, which blocks finalizer removal.                                                                                                                               
                                                                                                                                                                             
PR #8839 addressed the symptom by adding a watcher to trigger CQ reconcile when the cache becomes empty, which handles the race but doesn't fix the underlying cause as @mimowo mentioned.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:57:26Z

> Since Finish() doesn't clear quota reservation, finished workloads linger in the cache until explicitly deleted.

That is not good!
