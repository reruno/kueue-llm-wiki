# Issue #1622: Add the possibility to define bucket sizes for kueue_admission_wait_time_seconds_bucket

**Summary**: Add the possibility to define bucket sizes for kueue_admission_wait_time_seconds_bucket

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1622

**Last updated**: 2024-05-29T06:04:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2024-01-19T17:18:14Z
- **Updated**: 2024-05-29T06:04:50Z
- **Closed**: 2024-05-29T06:04:50Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

It would be great if you could define the bucket sizes of the `kueue_admission_wait_time_seconds_bucket` metric

**Why is this needed**:

Currently the buckets are fixed to the following ranges:

![Bildschirmfoto 2024-01-19 um 18 16 11](https://github.com/kubernetes-sigs/kueue/assets/2535856/17f498ce-6b97-4f66-a8b9-63dd8d0ed628)

It shows that you only have a granularity of up to 10 seconds, which is way too short in our case. It can be that a job is queued for multiple minutes. They currently all end up in the `+inf` bucket.

It would be great if you could define those buckets, eg. as a arg to the commandline `prometheus-wait-time-buckets=1,5,10,60,120,360,+inf`

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-19T19:11:14Z

Uhmm... I think we choose the current buckets poorly. In most job queuing scenarios, anything under 100ms is probably useless.

I would be happy to accept a configuration option for this, but also to change the defaults to something more reasonable.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-18T20:23:48Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-18T20:52:23Z

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

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-05-29T06:04:50Z

Fixed by having better default values via #1977
