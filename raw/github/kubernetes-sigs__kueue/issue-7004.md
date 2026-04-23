# Issue #7004: [flaky FairSharing] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload

**Summary**: [flaky FairSharing] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7004

**Last updated**: 2025-11-13T13:11:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-09-25T09:13:43Z
- **Updated**: 2025-11-13T13:11:42Z
- **Closed**: 2025-11-13T13:11:42Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 19

## Description

**What would you like to be cleaned**:
Scheduler Fair Sharing Suite: [It] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:441 with:
Not enough workloads are preempted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:441 with:
Not enough workloads are preempted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:726 @ 09/25/25 08:37:00.544
}
```

See https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6986/pull-kueue-test-integration-baseline-main/1971128077861785600

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T09:16:17Z

/kind bug
/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T09:20:09Z

/retitle [flaky FairSharing] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload 

It makes very useful for deduplicating to add the bug and flake labels. I often use that fileter, then look for matching title

https://github.com/kubernetes-sigs/kueue/issues?q=is%3Aissue%20state%3Aopen%20label%3Akind%2Fflake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T11:02:33Z

/remove-kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T14:54:09Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7086/pull-kueue-test-integration-baseline-release-0-12/1973034863619477504

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-03T06:34:24Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T09:37:19Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1986507375833518080

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:49:14Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-14/1987911641877975040

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1988500528350367744

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:49:51Z

It seems also quite common recently, added to: https://github.com/kubernetes-sigs/kueue/issues/7471

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-12T16:46:53Z

> It seems also quite common recently, added to: [#7471](https://github.com/kubernetes-sigs/kueue/issues/7471)

Ack, I will treat it with priority

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T07:57:30Z

@mszadkow is the problem because the code is choosing occasionally the workload from LQA instead of LQB as expected?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T08:01:38Z

It seems so, looking at the logs in https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1988500528350367744/build-log.txt

I can see `workload-vvvdg` is the preemption target
```
  2025-11-12T07:16:22.618871885Z	LEVEL(-3)	scheduler	preemption/preemption.go:186	Preemption ongoing	{"schedulingCycle": 585, "workload": {"name":"workload-z2x9k","namespace":"core-kpdzd"}, "clusterQueue": {"name":"guaranteed"}, "parentCohort": {"name":"all"}, "rootCohort": {"name":"all"}, "targetWorkload": {"name":"workload-vvvdg","namespace":"core-kpdzd"}, "preemptingWorkload": {"name":"workload-z2x9k","namespace":"core-kpdzd"}}
```
However, it comes from the LQA based on this log line:
```
 2025-11-12T07:16:22.03375673Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:815	Workload update event	{"workload": {"name":"workload-vvvdg","namespace":"core-kpdzd"}, "queue": "best-effort-a", "status": "admitted", "prevStatus": "pending", "clusterQueue": "best-effort-a"}
```
The question remains why this happens, maybe WaitForNextSecondAfterCreation is not enough.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T09:39:44Z

Hm, looking at the timestamps of the Workload create event it seems like indeed they were created in the same second:
`2025-11-12T07:16:22.003431628Z` and `2025-11-12T07:16:22.287078622Z`. It remains unclear what were the exact creationTimestamps though.

```
2025-11-12T07:16:22.003431628Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:729	Workload create event	{"workload": {"name":"workload-vvvdg","namespace":"core-kpdzd"}, "queue": "best-effort-a", "status": "pending"}
...
2025-11-12T07:16:22.287078622Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:729	Workload create event	{"workload": {"name":"workload-2jf8g","namespace":"core-kpdzd"}, "queue": "best-effort-b", "status": "pending"}
```
EDIT: since the new workload was created quickly it seems that the first one had to have `2025-11-12T07:16:21` as the creation timestamp.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T09:44:56Z

Maybe in case of fair sharing we don't use creation timestamp for tie-breaking? Or we made the decision before the DRS got updated yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T09:53:23Z

Hm, in case of equal DRS we call `preemptioncommon.CandidatesOrdering`: https://github.com/kubernetes-sigs/kueue/blob/49141c9889b85093c1c519732187c5897cee29f5/pkg/scheduler/preemption/fairsharing/ordering.go#L155-L160

but this function is not using CreationTimestamp for tie-breaking indeed, but this function is using quotaReservation timestamps which are equal in this case `  2025-11-12T07:16:22`: https://github.com/kubernetes-sigs/kueue/blob/49141c9889b85093c1c519732187c5897cee29f5/pkg/scheduler/preemption/common/ordering.go#L73

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T09:56:47Z

So, the call to WaitForNextSecondAfterCreation is actually not directly relevant. It helps in most cases by separating the two workloads in different seconds for their CreationTimestamps, but it does not imply different QuotaReservation timestamps.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T10:05:06Z

For the fix I could see two approaches:
1. introduce `util.WaitForNextSecondAfterReservation(wlBestEffortA)` and use it after WorkloadA has quota reservation to delay creatiion of Workload B, 
2. use priorities for tie-breaking

I would rather be leaning to (2.) as simpler, but in that case just verify that the test still pick up the changes done in this PR, so that we still capture the intention of the test: https://github.com/kubernetes-sigs/kueue/pull/6764/files#diff-c791c7f8f43735ff11274e29bfe6eb9320dfc913d4a5a0f14b3ba03038b076b4L144-R158

I think checking priorities would still capture the intention of the test, because prior to the PR we wouldn't have a special case for `case drs == highestCqDrs:` at all.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T10:05:47Z

cc @mszadkow @mbobrovskyi please check if this makes sense, if so I would try following (2.)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T10:29:18Z

Ok I could repro the issue fairly often with this snippet:

```golang
ginkgo.FIt("Guaranteed workloads cause preemption of a single best effort workload", func() {
	now := time.Now()
	nowTruncated := now.Truncate(time.Second)
	waitTime := nowTruncated.Add(time.Second - 5*time.Millisecond).Sub(now)
	time.Sleep(waitTime)
```
EDIT: it basically waits until 0.995 before the next second. This makes the creation timestamps likely to differ, but the quotaReservetion timestamps to be the same

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-13T11:19:36Z

The snippet works and helped to test the solution.
The solution 2., so priority was added to the workloads of best-effort cqs.
