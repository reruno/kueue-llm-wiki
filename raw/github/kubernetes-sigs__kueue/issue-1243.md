# Issue #1243: Support assign more resources to Partial Admitted job when there are some idle resources

**Summary**: Support assign more resources to Partial Admitted job when there are some idle resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1243

**Last updated**: 2024-09-11T17:49:30Z

---

## Metadata

- **State**: open
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2023-10-23T12:16:54Z
- **Updated**: 2024-09-11T17:49:30Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
If there is no pending workloads in ClusterQueue, a partial admitted workload can get more resource by a reclaiming schedule.

**Why is this needed**:
For example, two workloads are running in cluster. Both of them have 2 pods and each pod uses 1 GPU. When one of the workload completed, the other workload should have 4 GPUs to use.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-10-23T12:17:44Z

If needed, I can work on this issue. 👋 👋 👋

### Comment by [@trasc](https://github.com/trasc) — 2023-10-23T12:30:03Z

There main  issue , in my opinion , is that the changes in pod counts to the actual job is done in `RunWithPodSetsInfo`, pass this point, at least for batch/job to change the count we'll need to Stop and Restart the job.

Also just changing the counts in the Quota Reservation, without Eviction, can have implications to Admission Checks also.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-23T15:09:55Z

I'm supportive, but please prepare a KEP. Note some work in this direction https://github.com/kubernetes-sigs/kueue/issues/1038

The tricky part is preventing this race condition:
1. The scheduler creates a snapshot and is admitting a new workload
2. The new partial admission with resize feature increases the size of the job.
3. Resources are over-committed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-23T15:10:49Z

cc @andrewsykim, as this relates to #77

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-30T22:31:13Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-07T21:32:44Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-08T13:30:50Z

cc @andrewsykim @vicentefb

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-08T13:58:28Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-07T14:38:32Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:03:45Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:04:06Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-10T12:38:30Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T17:13:31Z

/lifecycle frozen

I guess that this depends on https://github.com/kubernetes-sigs/kueue/issues/77.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T17:49:29Z

>I guess that this depends on https://github.com/kubernetes-sigs/kueue/issues/77.

It matches my understanding.
