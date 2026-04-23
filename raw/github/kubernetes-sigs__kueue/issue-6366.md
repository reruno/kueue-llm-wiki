# Issue #6366: WorkloadSlices: add integration test or consider if we need WorkloadFinishedReasonOutOfSync

**Summary**: WorkloadSlices: add integration test or consider if we need WorkloadFinishedReasonOutOfSync

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6366

**Last updated**: 2025-08-11T16:27:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-01T15:22:30Z
- **Updated**: 2025-08-11T16:27:08Z
- **Closed**: 2025-08-11T16:27:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add integration test to prove this code is needed: https://github.com/kubernetes-sigs/kueue/blob/9ad7a2b09cfe4983cd5dee86ad62e874f1f3af46/pkg/workloadslicing/workloadslicing.go#L217-L221

or consider if we really need it. Maybe it can be moved at least to workload_controller.

The issue statement is open ended because I don't fully understand the need for this currently.

Also note that the code isn't really "Job CRD" specific, so it would be better to move it to workload_controller, even if we conclude we need it. Job controller CRD ideally should only contain Job-specific code.

**Why is this needed**:

This code is not covered by testing as proved by the introduced regression https://github.com/kubernetes-sigs/kueue/issues/6216.

I believe this code should be proven useful by integration tests to prevent future regressions.

I discussed some alternatives with @ichekrygin, like finishing on eviction, so maybe we don't need it after all.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T15:23:34Z

cc @ichekrygin I think it will be great for the maintainability of Kueue and the feature to resolve this issue (either by integration test or revisiting the need for the code.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-01T16:41:26Z

Hello @mimowo, thank you for raising this question.

> The issue statement is open ended because I don't fully understand the need for this currently.

To clarify, this specific scenario is documented directly in the code. Here's a slightly broader snippet to provide context:

```go
// There is also an edge case when the old slice was preempted or evicted by the scheduler
// to make room for a different workload (not the new slice). This can result in two
// "pending" workloads. In such a case, it is safe to deactivate the old slice.
oldWorkload := workloads[0]
if !workload.HasQuotaReservation(&oldWorkload) {
	if err := Finish(ctx, clnt, &oldWorkload, kueue.WorkloadFinishedReasonOutOfSync, "The workload slice is out of sync with its parent job"); err != nil {
		return nil, true, err
	}
}
```

I believe the in-line comments already articulate the motivation behind this logic. However, if anything remains unclear or still feels “open-ended,” I’d be happy to elaborate further.

---

> Also note that the code isn't really "Job CRD" specific, so it would be better to move it to workload\_controller, even if we conclude we need it. Job controller CRD ideally should only contain Job-specific code.

While I agree that this code isn't strictly tied to the *Job* CRD, it is very much *Workload*-specific. In this case, we're manipulating the Workload object, specifically, marking it as finished, which, in my view, is aligned with the responsibilities of the *generic job reconciler*.

In fact, this follows established precedent, as we already perform similar actions such as updating or even deleting Workloads from within the job reconcilers. So, I’d argue this placement is consistent with current patterns and the intended separation of concerns.

Moreover, in this context, the reconciler is *context-aware*, it “knows” that it is handling a *scale-up* event, and therefore understands that multiple (two) workloads may exist. This allows it to assess which workload slice is “old” and which is “new.”

In contrast, the `workload-controller` currently lacks this contextual awareness. It doesn’t have knowledge of scale-up events or the concept of workload slices. Moving this functionality to the `workload-controller` would therefore require introducing that context explicitly.

For example, the `workload-controller` would need to, for every workload, determine whether it is an “out-of-sync old” slice and whether a newer replacement exists. I'm not sure this added complexity is justified or worth the effort, especially given the relatively scoped and context-specific nature of the current implementation.

---

> This code is not covered by testing as proved by the introduced regression #6216.

The regression in question affected the broader logic responsible for identifying eligible candidates for processing. While this is related, its impact goes beyond the specific area we're discussing here.

That said, we do currently have integration tests that validate the handling of multiple workloads, including scenarios with two coexisting ones. I believe the concern being raised is that we lack coverage for the specific case of *two not-admitted* workloads. That’s a fair point, and I agree this is an area where we can strengthen our test coverage.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T16:58:54Z

~My point is that we don;t have an integration test that would exercise this logic. Comments in code will never be a full replacement to integration testing :). All layers of the coding are important, comments, unit tests, integration tests. None of the layers is replacement to another fully.~

EDIT: crossed the comment as unnecessary based on the last paragraph of the previous comment.

Regarding job reconciler vs workload controller, fair, you are probably right. 

Still we could consider moving this code to the code which handles eviction, wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T17:05:32Z

I believe the test will also play a great documenting role for the scenario. The scenario involves a couple of steps and requires non-trivial reasoning

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T04:44:32Z

> Still we could consider moving this code to the code which handles eviction, wdyt?

Just to get some clarity about "code", do we mean the "Finish" function or something else?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T05:54:09Z

I want to test the scenario reflecting the intention for adding this code. IIUC this code is added to prevent re- admission of two slices at the same time. It does not work ideally because the race condition is still possible, but we could test that it prevents readmission of both slices at the same time provided that we waited long enough - this could be checked by the interim step of checking one of the received the Finished condition.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-07T15:44:37Z

/assign
