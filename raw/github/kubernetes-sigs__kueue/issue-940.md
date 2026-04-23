# Issue #940: Dashboard support in Kueue

**Summary**: Dashboard support in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/940

**Last updated**: 2025-05-15T17:26:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-07-03T09:16:58Z
- **Updated**: 2025-05-15T17:26:28Z
- **Closed**: 2025-05-15T17:26:26Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 45

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

It would be great if we can have an insight about what's our queueing system looks like at real time
- for administrators, it helps to understand the total resource usages in-between cluster queues and whether we should make them a cohort
- for batch users, they will have an overview about the job queueing, how many jobs are pending for scheduling, how long jobs are waiting.

Overall, it's a great enhancement especially for production env.

**Why is this needed**:

A big enhancement and a great insight of kueue system.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

Some advices here:
- For administrators:
  - clusterQueue resource groups
  - clusterQueue resource utilizations
  - localQueues
  - cohorts
- For users:
  - jobs with their status

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-04T14:44:02Z

Do you have a high level idea of how to get there?

For example, would metrics + grafana yamls be enough for the administrative side?

For end users, certainly grafana wouldn't be viable. But what could be the MVP that would keep kueue largely non-opinionated and reusable (so you can integrate it with your own UI, if you already have one). Could we offer a CLI instead?

### Comment by [@moficodes](https://github.com/moficodes) — 2023-07-07T17:53:15Z

Kueue already spits out prometheus metrics. Building a UI based on that can be useful and the UI should be optional to deploy. 

I do wonder if it is more useful for us to provide general purpose grafana dashboard and make it available in https://grafana.com/grafana/dashboards/

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-10T07:22:54Z

Building on metrics is helpful I think, but the dashboard is more than that, like it will display the basic information about the system, how many queues there, what their names are, how many jobs inside the queue, it can be interactive. We can get the information via the apis directly or we can have a lightweight database inside for cache, like sqlite. 

We may need some frontend volunteers if we want to finish this work. As a MVP, IMHO, I think it should include
- Most of the API objects(clusterQueue, localQueue, Job, resourceFlavor, workload) at least, also including their relationships
- Some exported metrics

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-07-11T17:50:01Z

+1000, this is a much needed experience gap, I would be happy to review proposals.

@kerthcet may be we start by looking at similar batch schedulers and see what "screens" they offer to inform and help seed what we need to build?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-18T07:36:00Z

> @kerthcet may be we start by looking at similar batch schedulers and see what "screens" they offer to inform and help seed what we need to build?

Yes, that's a good approach, let me make a research first and then I'll share with your guys. I know YuniKorn has a dashboard. Also cc @BinL233

### Comment by [@zeddit](https://github.com/zeddit) — 2023-11-03T11:29:54Z

@ahg-g 
it's a core feature which will make kueue easy to use.
A alternative would be airflow, and its UI looks like below
![image](https://github.com/kubernetes-sigs/kueue/assets/30164206/afc164a3-2b6f-4285-b000-ef1a197f07cf)
it contains task status, code, and audit logs which would be useful information for user to inspect their jobs.
besides, airflow integrates with idp like ldap or oidc and provides access control and permission managment features.

However, airflow doesn't provide an API to submit one-time run jobs like ml training jobs, which is the core application for kueue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-06T02:48:46Z

cc @B1F030 we also did some research around the popular queueing systems, I think we can provide a summary about the   essential elements in dashboard, or even a prototype. Can you help with this @B1F030 ?

### Comment by [@samzong](https://github.com/samzong) — 2023-11-07T03:28:34Z

Hi guys, I want to try involved in the prototyping part of the dashbaord Desgin, and provide the prototype like figma.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T03:57:20Z

Thanks @samzong 
We can provide a based design, and share with the community for feedbacks and then involve the developments, any concerns? @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-07T13:56:09Z

Maybe we can start with a list of views you would like to have and do priority sorting

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-08T01:30:13Z

> Maybe we can start with a list of views you would like to have and do priority sorting

@B1F030 is doing this.

### Comment by [@Sharpz7](https://github.com/Sharpz7) — 2023-12-11T02:16:14Z

Hey folks, https://github.com/armadaproject/armada has a UI in the form of lookout.

Our demo UI is here: https://ui.demo.armadaproject.io/

Let us know what you think of it - I think many parts of it could be suitable for lookout and we would be interested in contributing.

Thanks!

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-11T02:36:28Z

Thanks @Sharpz7 that's helpful, and we have a general idea now, @samzong is doing the prototyping, once we've done, we'll share a google doc/figma with your guys, hope to work together.

### Comment by [@Sharpz7](https://github.com/Sharpz7) — 2023-12-11T03:06:12Z

Great, Thank you :))

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-11T15:15:13Z

@Sharpz7 what is a lookout in this context?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-10T16:10:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-10T23:11:58Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-08T23:13:34Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-06-11T02:22:39Z

Are you still following this @samzong ?

### Comment by [@samzong](https://github.com/samzong) — 2024-06-12T05:04:01Z

@kerthcet 

Absolutely, I'm still very interested in this. The good news is that I'll have more time to contribute to open source in the coming period. I'll make sure to push this forward as soon as possible.

### Comment by [@trashadewan](https://github.com/trashadewan) — 2024-07-11T16:55:18Z

Hey, 
there is a grafana dashboard shown in https://www.youtube.com/watch?v=B63vT2_UYE4, would you know if this is avialble for use. somewhere?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-11T17:16:07Z

I think it might be this one https://github.com/GoogleCloudPlatform/ai-on-gke/blob/main/best-practices/gke-batch-refarch/02_platform/monitoring/deploy-dashboard.yaml

but @moficodes and @alizaidis to confirm

### Comment by [@alizaidis](https://github.com/alizaidis) — 2024-07-18T19:09:36Z

Yep that's the one!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-17T19:36:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-16T20:13:36Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-16T20:13:40Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/940#issuecomment-2353851432):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@akram](https://github.com/akram) — 2024-11-18T11:16:31Z

Hi everyone,

As a side project to just run a demo I have contributed kueue-viz : as a kueue dashboard.
The project is availabe here: https://github.com/akram/kueue-viz

It is still very basic , but every contribution and feedback are welcome.


<img width="1511" alt="image" src="https://github.com/user-attachments/assets/5728e0cf-2aad-4c27-9511-78da1d995347">

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-18T15:41:50Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-18T15:41:57Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/940#issuecomment-2483413102):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-18T15:42:17Z

@mwielgus has mentioned that this is still of interest to the Kueue project.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-11-19T02:26:18Z

Thanks @akram for the work!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T09:59:36Z

/reopen
let's use this issue to continue with the next steps of productazing the kueue-viz sub-project. I post some steps in the [comment](https://github.com/kubernetes-sigs/kueue/pull/3727#issuecomment-2519804009):
- I think it would be good to publish the image
- move it out of the cmd/experimental
- align the release process with the main Kueue
(possibly more)
- reference the project from the kueue main documentation page (https://kueue.sigs.k8s.io/), for starter we can do similar as for kueuectl plugin, but later it deserves more advertisement I think
- e2e tests for the dashboard backend and frontend

I'm also open to track the improvements as dedicated issue, just listing them here as a starting point.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-05T09:59:40Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/940#issuecomment-2519815489):

>/reopen
>let's use this issue to continue with the next steps of productazing the kueue-viz sub-project. I post some steps in the [comment](https://github.com/kubernetes-sigs/kueue/pull/3727#issuecomment-2519804009)


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T10:20:10Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-05T10:47:15Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-05T10:54:59Z

/remove-lifecycle stale
This is being actively worked on

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-17T08:48:15Z

@mimowo @akram Looks like we have the Dashboard now. Can we close this issue, or is there still something pending?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-17T09:02:20Z

For the functional requirements I will defer to @akram and @kannon92 the question. For the technical I would like to complete this https://github.com/kubernetes-sigs/kueue/issues/3796 too.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-28T16:51:17Z

Let's keep this open until 0.12 release. I think technically we don't yet have this as it is not released.

### Comment by [@shaharelys](https://github.com/shaharelys) — 2025-05-14T19:57:23Z

Hey guys! We would really like to try this one for our use case. I saw this is on the roadman for 2025 but I realize now this is already available? Is that correct?

Would love to be an alpha user. Could also contibute from the usecase POV of an administrator for a 50 H100s k8s cluster with 10 ClusterQueues :)

Is that possible? Thanks!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T20:19:44Z

> Hey guys! We would really like to try this one for our use case. I saw this is on the roadman for 2025 but I realize now this is already available? Is that correct?
> 
> Would love to be an alpha user. Could also contibute from the usecase POV of an administrator for a 50 H100s k8s cluster with 10 ClusterQueues :)
> 
> Is that possible? Thanks!

It is available in main right now. We do not yet publish this in a release. For 0.12 it will be released.

Please feel free to test or be an alpha user. Feedback is welcome!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T20:20:23Z

I change my mind on this. We should close it. It will be released in 0.12.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T20:20:30Z

/close

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T17:26:21Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-15T17:26:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/940#issuecomment-2884562246):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
