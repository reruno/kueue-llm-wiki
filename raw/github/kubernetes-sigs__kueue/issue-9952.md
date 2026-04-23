# Issue #9952: flaky test: Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Summary**: flaky test: Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9952

**Last updated**: 2026-04-03T04:44:04Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-17T16:27:29Z
- **Updated**: 2026-04-03T04:44:04Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description


**Which test is flaking?**:
Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9947/pull-kueue-test-integration-baseline-release-0-16/2033935424635801600
**Failure message or logs**:
```
Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit [feature:fairsharing] expand_less	14s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:225 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:225 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:945 @ 03/17/26 16:11:50.475
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2026-03-23T19:34:25Z

@mimowo is this something we need to look into

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-23T19:36:00Z

for sure, help with this flake is very welcome

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-03-28T08:52:07Z

@mimowo i did a check on this flaky test, tried to reproduce the issue in my local, but it seemed to be consistent and working, later i checked the CI logs 

The integration test sticky workload deleted, next workload can admit is experiencing a timing-related flake in Prow environments. The failure occurs because the 10-second Eventually timeout is reached before the sequence of 
**Delete Sticky -> Sync Cache -> Finish Eviction -> Reclaim Resources -> Admit Next** can complete under CI load.


**Evidence from Prow Logs**
A timestamp autopsy of the failed run (03/17/26 16:11:50) confirms that the Kueue controllers were functioning correctly, but were throttled by API event latency:

```
Test Failure (Timeout): 16:11:50.475

Borrowing Eviction Finished: 16:11:50.524 (+49ms after failure)

Sticky Workload Deletion Processed: 16:11:50.545 (+70ms after failure)

Resource Flavor Error: The logs show ResourceFlavor "on-demand" not found. This caused the Job reconciler to crash and retry multiple times (Cycles 930–937), consuming valuable time within the 10s window.

The Breakdown: The test reached its 10s limit exactly as the "roadblock" was being cleared. The scheduler was spinning in a tight loop (7 cycles in 72ms) waiting for the deletion event to propagate from the API server to the controller cache.
```
**Suggestion 1: Increase the Timeout (Immediate Mitigation)**
The 10-second timeout is too "tight" for complex preemption/deletion scenarios in a shared CI environment.

Action: Increase the timeout for the final admission check (util.ExpectAdmittedWorkloadsTotalMetric) to 20 or 30 seconds.

**Suggestion 2: Explicit Synchronization on Deletion**
Currently, the test triggers a deletion and immediately begins polling for the next workload's admission. This creates a race between the deletion sync and the admission timer.

Action: Add a synchronization step to wait until the stickyWorkload is confirmed as NotFound in the API server before starting the timer for the final admission check. This ensures the "Next" workload has a clean 10s window to be scheduled after the roadblock is removed.

Can we try and move forward with this approach ? cc @nerdeveloper please correct me if my analysis does not match with your inference ?

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-04-03T04:44:03Z

Hi @mimowo @nerdeveloper just checking if you had a chance to look onto the above analysis ?
