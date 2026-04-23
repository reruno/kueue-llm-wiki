# Issue #9483: LeaderWorkerSet integration when LeaderWorkerSet created Rolling update with maxSurge creates workloads for surge pods and completes successfully [area:singlecluster, feature:leaderworkerset]

**Summary**: LeaderWorkerSet integration when LeaderWorkerSet created Rolling update with maxSurge creates workloads for surge pods and completes successfully [area:singlecluster, feature:leaderworkerset]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9483

**Last updated**: 2026-03-05T05:34:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-25T16:19:49Z
- **Updated**: 2026-03-05T05:34:07Z
- **Closed**: 2026-03-05T05:34:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 18

## Description

**Which test is flaking?**:

LeaderWorkerSet integration when LeaderWorkerSet created Rolling update with maxSurge creates workloads for surge pods and completes successfully [area:singlecluster, feature:leaderworkerset]

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9464/pull-kueue-test-e2e-main-1-34/2026684207736033280

**Failure message or logs**:
```
End To End Suite: kindest/node:v1.34.3: [It] LeaderWorkerSet integration when LeaderWorkerSet created Rolling update with maxSurge creates workloads for surge pods and completes successfully [area:singlecluster, feature:leaderworkerset] expand_less	5m7s
{Timed out after 300.002s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:750 with:
Expected
    <int32>: 3
to equal
    <int32>: 4 failed [FAILED] Timed out after 300.002s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:750 with:
Expected
    <int32>: 3
to equal
    <int32>: 4
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:761 @ 02/25/26 16:08:04.057
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T16:21:35Z

I'm not sure this is related, but maybe the code around maxSurge support was modified recently: https://github.com/kubernetes-sigs/kueue/pull/9135

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T16:23:09Z

cc @PannagaRao @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-25T22:26:00Z

I looked into this. The kueue controller logs for the test window are lost. The Certs test (Serial) scales the kueue deployment to 0 right after the maxSurge test times out, so the exported logs are from replacement pods with no entries for the test namespace. Without logs I can't determine the root cause. If this flakes again, the key thing to check is whether Kueue deleted workloads for the surge indices (4, 5) while the rollout was still in progress.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-26T06:05:12Z

Again there https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-34/2026835580309999616

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-26T13:00:45Z

Good point @sohankunkerkar . I'm wondering what we could do better- maybe we move the certs_test.go to customconfigs, because:
1. in custom configs each test already dumps the logs per replica
2. the test is disruptive and now we are running e2e tests in parallel

This way we will have the logs next time for LWS failure.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-26T13:09:20Z

Opened: https://github.com/kubernetes-sigs/kueue/pull/9521

Btw, I believe this might be the reason why we observed varying size of the logs recorded for e2e tests in the past with @IrvingMg

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T15:54:36Z

another occurrence https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9528/pull-kueue-test-e2e-release-0-15-1-33/2027053479167528960

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-02T00:24:42Z

Ok,  I went through the logs. The initial workloads (indices 0-3) get created and admitted fine. The LWS reconciler handles the surge and stops running. After that, nothing happens for 5 minutes. Then the rolling update finishes replacing pods, GC cascade-deletes the old workloads, and new pods show up a second later with `prebuilt workload not found`. Nobody creates workloads for them, test times out.                                                                                          

The issue is that the LWS reconciler only watches LeaderWorkerSet objects. It has no idea when workloads get deleted. The LWS status isn't changing during the rollout window, so no reconcile fires, and the replacement pods just sit there waiting.

I think we can add a delete-only workload watch using a typed EventHandler (same pattern as pod_controller.go). Map deleted workloads back to the owning LWS via `JobOwnerNameAnnotation`, trigger a reconcile, let it recreate whatever is missing. `Create/Update/Generic` stay as no-ops to keep things quiet. Also we need to move the LWS predicate from global `WithEventFilter(r)` to `For(..., builder.WithPredicates(r))` so it doesn't accidentally filter out the workload events.

I ran that change locally 100 times, it looks fine.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T06:16:56Z

Thank you @sohankunkerkar for analyzing the issue. That sounds reasonable. One thing that caught my attention is the 5 minutes when nothing happens. Is that expected?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T08:05:51Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-33/2027741715586093056

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-02T14:17:29Z

> Thank you [@sohankunkerkar](https://github.com/sohankunkerkar) for analyzing the issue. That sounds reasonable. One thing that caught my attention is the 5 minutes when nothing happens. Is that expected?

The 5-minute gap is expected given the current code. The LWS reconciler only watches LWS objects. After the initial surge handling, the LWS object status stops changing (from Kueue's perspective), so no reconcile fires. The rolling update continues in the background (driven by the LWS controller, not Kueue), but Kueue's reconciler has no visibility into it until something triggers a reconcile on the LWS object.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T14:27:31Z

Ok, so adding an extra event handler for Deleted Workloads sounds reasonable. IIUC an alternative would be to add an event handler for updates to the leader STS? Because IIUC the rolling update would continuously trigger Update events on the leader STS?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-02T15:09:18Z

Yes, watching the leader StatefulSet updates would also work since the rolling update continuously triggers STS status changes. Either approach closes the gap. I went with workload deletions because it's more targeted. It only fires when a workload is actually removed, which is the exact event that requires action. Watching STS updates would fire on every pod replacement status change during rollout (most of which wouldn't need workload recreation).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T15:18:07Z

I see, this makes sense. The only benefit of watching  the leader STS is that we know there is only one, whilest we will have many workloads to watch. Having said that I dont have a clear winner approach here. Both sound reasonable.

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-03T02:48:19Z

/assign @PannagaRao

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T15:57:33Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-33/2028840202398601216

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-05T05:34:01Z

fixed by https://github.com/kubernetes-sigs/kueue/pull/9631
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-05T05:34:06Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9483#issuecomment-4002342036):

>fixed by https://github.com/kubernetes-sigs/kueue/pull/9631
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
