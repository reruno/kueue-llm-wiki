# Issue #7783: JobSet: Expose the information in PodsReady event & condition messages which Jobs (or Pods) are not ready

**Summary**: JobSet: Expose the information in PodsReady event & condition messages which Jobs (or Pods) are not ready

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7783

**Last updated**: 2026-11-20T20:57:04Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-20T13:13:29Z
- **Updated**: 2026-11-20T20:57:04Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `lifecycle/rotten`
- **Assignees**: [@chethanv28](https://github.com/chethanv28), [@chethanuk](https://github.com/chethanuk)
- **Comments**: 11

## Description

**What would you like to be added**:

I would like to expose information which Jobs  in a JobSet are not ready, thus violating the PodsReady timeout.

Ideally we also get into the level of Pods, but this requires listing the Pods.

**Why is this needed**:

Currently users need to do an extra amount of work (reading logs etc) to know which Jobs and Pods violated the PodsReady timeout for JobSet.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T13:14:52Z

cc @tenzen-y @mwysokin

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T14:05:03Z

cc @GiuseppeTT @andreyvelich

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T21:03:34Z

cc @MaysaMacedo 

This may useful to keep in mind as you start thinking through https://github.com/kubernetes-sigs/kueue/issues/6796.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-11-20T23:44:50Z

Doesn't `replicatedJobsStatus.ready`  and `replicatedJobsStatus.active` expose this information ?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-21T01:35:54Z

I think PodsReady is a Kueue condition for WaitForPodsReady.

So the ask to bubble up information about Jobset to this condition.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:05:27Z

/priority important-soon
cc @mykysha who recently worked on observability issues so maybe this would fit him nicely
cc @mwysokin

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:24Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:55Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kannon92](https://github.com/kannon92) — 2026-11-19T14:12:21Z

@chethanv28 
can you please summarize your implementation plan here? I'd rather make sure we got agreement on the design before jumping into the PR.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-11-19T14:12:32Z

/assign @chethanv28

### Comment by [@chethanuk](https://github.com/chethanuk) — 2026-11-20T20:57:04Z

Hi @kannon92, sorry for the delay. @chethanv28 isn't me, I'm the one working on this.

/assign

Here's the plan, as implemented in #19117 (CI is green; happy to change anything before review):

- New optional interface in jobframework: `JobWithPodsNotReadyDetails { PodsNotReadyDetails() string }`. An empty string means nothing to add.
- When the reconciler builds the PodsReady=False condition (WaitForStart, WaitForScheduling, WaitForRecovery), it appends `"; " + details` if the job implements the interface.
- JobSet implements it by listing the replicatedJobs where ready + succeeded < replicas, using the same math as `PodsReady()`. Names only, no counts, so the Workload is only patched when the set of not-ready jobs changes, not on every pod update. Example:

      Not all pods are ready or succeeded; replicatedJobs not ready: workers, driver

- If only the message changes, the condition keeps its `lastTransitionTime`, so the WaitForPodsReady timeout isn't reset.
- No write once the workload is evicted, so the last message still says which jobs weren't ready.
- No API change. The eviction message and other integrations stay as they are.
- Pod-level detail is left out, since it needs listing Pods. Could be a follow-up if wanted.

Two questions:
1. Are you OK with an optional jobframework interface, or would you rather keep this JobSet-only?
2. Is jobs-level detail enough for now, or do you want pod names too?
