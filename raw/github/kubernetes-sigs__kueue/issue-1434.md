# Issue #1434: PodSets for RayJobs should account for submitter Job Pod

**Summary**: PodSets for RayJobs should account for submitter Job Pod

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1434

**Last updated**: 2024-12-13T18:00:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2023-12-11T15:27:15Z
- **Updated**: 2024-12-13T18:00:27Z
- **Closed**: 2024-12-13T18:00:27Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 13

## Description

**What would you like to be added**:

Since v0.6.0, KubeRay creates one Job for each RayJob it reconciles, that's used to submit the actual Ray job to the Ray cluster.

Some context is available in ray-project/kuberay#1177.

**Why is this needed**:

The submitter Job resources can be customised, and should be accounted for into the overall RayJob resources request.

**Completion requirements**:

The Pods corresponding to the submitter Jobs should not be managed by Kueue.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-11T15:27:24Z

/assign

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-11T16:22:18Z

/cc @andrewsykim

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-05T13:56:21Z

@kevin85421 FYI

### Comment by [@kevin85421](https://github.com/kevin85421) — 2024-01-05T18:40:54Z

> PodSets for RayJobs should account for submitter Job Pod

This makes sense to me. Btw, after completing the RayJob refactoring, we may consider adding the [lightweight submission](https://github.com/ray-project/kuberay/issues/1558) (i.e. KubeRay sends an HTTP request to the Ray head to create the job) back. That is, KubeRay may support both submission methods at the same time.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-04T19:07:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-04T20:05:22Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-05T02:14:16Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-03T02:46:51Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-14T16:22:46Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-12T16:52:01Z

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

### Comment by [@pingsutw](https://github.com/pingsutw) — 2024-12-02T19:13:16Z

@astefanutti are you working on this issue? or do you know anyone working on it?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-12-03T03:25:53Z

Spoke with @pingsutw on Slack today, I can open a PR this week with a fix

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-12-03T07:33:31Z

@pingsutw @andrewsykim thanks. I confirm I haven't worked on it yet.
