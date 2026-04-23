# Issue #77: Support dynamically sized (elastic) jobs

**Summary**: Support dynamically sized (elastic) jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/77

**Last updated**: 2026-03-02T05:23:57Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-26T19:37:17Z
- **Updated**: 2026-03-02T05:23:57Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `kind/grand-feature`
- **Assignees**: [@andrewsykim](https://github.com/andrewsykim), [@troychiu](https://github.com/troychiu)
- **Comments**: 23

## Description

We should have a clear path towards support spark and other dynamically sized jobs. Another example of this is Ray. 

One related aspect is to support dynamically updating the resource requirements of a workload, we can probably limit that to support changing the count of a PodSet in QueuedWorkload (in Spark, the number of workers could change during the runtime of the job, but not the resource requirements of a worker). 

One idea is to model it in a way similar to "in-place update to pod resources" [1], but in our case it would be the count that is mutable. The driver pod in spark would be watching for the corresponding QueuedWorkload instance and adjusts the number of workers when the new count is admitted.

[1] [https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1287-in-place-update-pod-resources](https://www.google.com/url?q=https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1287-in-place-update-pod-resources&sa=D&source=docs&ust=1645888625262668&usg=AOvVaw3AgbHiaK920CYg_pqAxRMn)

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T03:12:10Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-12T03:14:41Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T13:21:24Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T16:49:10Z

This will be easier to support with https://github.com/kubernetes/enhancements/tree/master/keps/sig-scheduling/3521-pod-scheduling-readiness

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-09-18T16:54:49Z

I am interested in working on this -- this probably needs some sort of design doc, will work with @alculquicondor and see if I can put something together in the next few weeks

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T06:31:38Z

> I am interested in working on this -- this probably needs some sort of design doc, will work with @alculquicondor and see if I can put something together in the next few weeks
> 
> /assign

Hi @andrewsykim! Is there any progress?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2023-12-07T18:11:02Z

@tenzen-y I was planning to work on this in a couple weeks during the holiday season, but feel free to start working on this if you're interested.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:17:08Z

@andrewsykim Thanks. I also don't have enough time now. So, when I can get enough time, I will ask for progress again.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-02-22T16:09:39Z

FYI @vicentefb and I are working on a proposal in a google doc, we will share it here soon when it's ready

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-03T18:16:59Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-03T18:17:03Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/77#issuecomment-2035287246):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@troychiu](https://github.com/troychiu) — 2024-12-19T18:59:58Z

Hi I would love to work on this issue, especially the ray autoscaling support. Would resuming https://github.com/kubernetes-sigs/kueue/pull/1852 be a good starting point?

### Comment by [@troychiu](https://github.com/troychiu) — 2024-12-20T23:34:53Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-10T06:04:56Z

> Hi I would love to work on this issue, especially the ray autoscaling support. Would resuming https://github.com/kubernetes-sigs/kueue/pull/1852 be a good starting point?

@troychiu sorry for the late reply. You are super welcome to work on that, but be aware the KEP and PR are old and some aspects have changed. Also, this is one of the more challenging KEPs. I think resuming the PR might be a good idea, but it requires a careful check.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-23T07:21:22Z

/remove-lifecycle frozen

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-23T07:25:47Z

Big update: @ichekrygin recently took the challenge, refreshed the [KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs) and [implemented](https://github.com/kubernetes-sigs/kueue/pull/5510) the support in Alpha 🚀

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-07-23T21:34:26Z

Thank you @ichekrygin for driving this! @weizhaowz could you follow-up with Illya's PR and ensure WorkloadSlices work with autoscaling Ray clusters?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-21T22:09:56Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-20T23:08:17Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T12:21:26Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T12:22:13Z

This is actively being worked on as part of the ElasticJobsViaWorkloadSlices currently.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T12:48:40Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-02T05:23:55Z

/remove-lifecycle stale
