# Issue #23: Graduate API to beta

**Summary**: Graduate API to beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/23

**Last updated**: 2023-03-08T16:01:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-18T15:23:56Z
- **Updated**: 2023-03-08T16:01:15Z
- **Closed**: 2023-03-08T16:01:15Z
- **Labels**: `kind/feature`, `priority/backlog`, `lifecycle/frozen`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 32

## Description

Currently, this would be very cumbersome due to the lack of support from kubebuilder https://github.com/kubernetes-sigs/controller-tools/issues/656

Once the support is added and we are ready to publish a v1beta1, we should consider renaming the api group. Note that this requires an official api-review https://github.com/kubernetes/enhancements/pull/1111

Summary doc: https://docs.google.com/document/d/1Uu4hfGxux4Wh_laqZMLxXdEVdty06Sb2DwB035hj700/edit?usp=sharing&resourcekey=0-b7mU7mGPCkEfhjyYDsXOBg (join https://groups.google.com/a/kubernetes.io/g/wg-batch to access)

Potential changes when graduating:
- [ ] Move `admission` from Workload spec into status (from #498)
- [ ] Rename `min`, `max` into something easier to understand.
- [ ] Support queue name as a label, in addition to annotation (makes it easier to filter workloads by queue).
- [ ] Add `ObjectMeta` into each `PodSet` template.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T15:24:08Z

/kind feature
/priority backlog

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-09T20:30:48Z

Using `sigs.k8s.io` as domain isn't necessary and doesn't add value. If this ever moves to core k8s, it would likely be under `batch.k8s.io` anyways.

For the time being, and to avoid the awkward `x-`, it seems reasonable to use the shorter `kueue.sh` domain.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-11T07:23:39Z

I think the value is the direct association to the Kubernetes project. I prefer having it in the API name. But what do others think?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-11T07:34:02Z

Anyway, it will be moved to core k8s in the future, so why not choose to use `batch.k8s.io` directly. This will reduce the work of users to change api groups in the future.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-11T07:42:42Z

Assuming that you don't mean `batch`, which would require the API to be part of k/k. 
Any `k8s.io` domain name requires an API review. This will take a week or two. Should we do it or just release the alpha APIs as-is? I think I prefer to release them sooner for more chances to get real-world feedback. And then we can go for an API review when we aim for beta.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-11T11:35:42Z

> I think the value is the direct association to the Kubernetes project. I prefer having it in the API name. 

The `x-` makes it look weird.

> Any k8s.io domain name requires an API review. This will take a week or two.

If that is a one time thing, then we can pursue it; but I am not sure if we want it if it requires a review for every change we make.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-11T11:48:43Z

It probably does. But maybe we can just rename to `batch.k8s.io` and mark it as unapproved for now https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/2337-k8s.io-group-protection#proposal

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-11T11:51:21Z

+1 We can mark it unapproved at the alpha version.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-11T12:04:02Z

This is discouraged, and it only adds to the confusion. Users don't look at CRD definitions.

ok, I don't want to delay things, I am fine with keeping the `x-k8s.io` domain just because it is used by other subprojects (it doesn't make it less weird though) and revisit when we go to Beta;

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-10T12:58:59Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-08-09T13:54:43Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-09T16:20:07Z

/remove-lifecycle stale

maybe for 0.3.0 :)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-09-08T17:15:04Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue or PR with `/reopen`
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-09-08T17:15:10Z

@k8s-triage-robot: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/23#issuecomment-1240995878):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues and PRs according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue or PR with `/reopen`
>- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-08T17:17:02Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-09-08T17:17:07Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/23#issuecomment-1240998004):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-10-08T17:58:12Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-08T17:58:15Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/23#issuecomment-1272368657):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-11T15:17:53Z

/reopen

/lifecycle frozen

we need to get back to this when targeting a v1beta1 API.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-10-11T15:17:57Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/23#issuecomment-1274865203):

>/reopen
>
>/lifecycle frozen
>
>we need to get back to this when targeting a v1beta1 API.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-05T16:48:06Z

I'm starting a list of potential changes to the API. See Issue description.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-05T16:49:08Z

cc @kerthcet for feedback (and anyone already in the thread, of course)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-06T08:53:00Z

> Move `admission` from Workload spec into status (from [Enforce timeout for podsReady #498](https://github.com/kubernetes-sigs/kueue/pull/498))

I'm ok with this, admission presents the actual state of a workload.

> Rename `min`, `max` into something easier to understand.

Before, we named them `requests/limits`? Anyway, I think reading document is always needed, whatever the name. So I'm fine with `min/max`, another pair maybe `guarantee/capacity`?

> Support queue name as a label, in addition to annotation (makes it easier to filter workloads by queue).

Can you provide some more context why we need this?  It looks like looking for workloads via label selector.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-06T13:33:00Z

> Before, we named them requests/limits?

No, that would have been very confusing because they already mean something in the pod spec. I'll start a separate doc to discuss options.

> Can you provide some more context why we need this? It looks like looking for workloads via label selector.

It's actually about filtering Jobs using the queue name.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-06T20:27:33Z

> No, that would have been very confusing because they already mean something in the pod spec. I'll start a separate doc to discuss options.

When I joined the kueue project, one of the most confusing of the kueue specification was the relationship between `min/max` and cohort.

IMO, the `guarantee/capacity` looks good rather than `min/max`.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-07T04:21:49Z

> It's actually about filtering Jobs using the queue name.

It made me think of adding queueName to job's spec https://github.com/kubernetes/enhancements/pull/3397, we can filter jobs with field-selector then.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-09T13:25:00Z

Yes, that would be ideal, but that KEP got significant push back, so I don't see it happening anytime soon.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-13T19:01:49Z

We might also need to add ObjectMeta into each PodSet template. Cluster autoscaler needs the metadata to properly scale up.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-16T08:11:23Z

Is this for scaling up in advance? Or autoscaler only watching the unschedulable pods, who contains the metadata.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-16T13:39:48Z

Yes, to scale up in advance

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-02T21:07:58Z

I've created a summary doc with the proposed changes as we graduate to beta (also available in the issue description): https://docs.google.com/document/d/1Uu4hfGxux4Wh_laqZMLxXdEVdty06Sb2DwB035hj700/edit?usp=sharing&resourcekey=0-b7mU7mGPCkEfhjyYDsXOBg

Some of the enhancements come from UX study sessions that we have conducted, see notes here: https://docs.google.com/document/d/1xbN46OLuhsXXHeqZrKrl9I57kpFQ2yqiYdOx0sHZC4Q/edit?usp=sharing

I have a WIP in #532

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-07T19:09:03Z

/assign @alculquicondor
