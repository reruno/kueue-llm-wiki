# Issue #8287: TrainJob integration: eliminate the post-processing code for Trainer helpers to handle numNodes correctly

**Summary**: TrainJob integration: eliminate the post-processing code for Trainer helpers to handle numNodes correctly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8287

**Last updated**: 2026-08-26T16:51:04Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T08:03:11Z
- **Updated**: 2026-08-26T16:51:04Z
- **Closed**: —
- **Labels**: `good first issue`, `help wanted`, `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz), [@NarayanaSabari](https://github.com/NarayanaSabari), [@SatishChoudhary642](https://github.com/SatishChoudhary642)
- **Comments**: 23

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to eliminate the special handling of numNodes inside Kueue code: https://github.com/kubernetes-sigs/kueue/pull/8135/changes#diff-eb30173c6ca84a779cd005d1c147a311b18a077bd35205dc64942fd824ffb3e4R181-R187

**Why is this needed**:

I think the correct numbers of Pods (and PodSets)  should already be returned by Kubeflow helpers. Other projects using the helpers will need to do the same

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T08:04:44Z

cc @kaisoz @NarayanaSabari ptal. Feel free to collab on this. It also will require an issue in Kubeflow I think, opened: https://github.com/kubeflow/trainer/issues/3042

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T08:11:39Z

cc @tenzen-y @andreyvelich

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T13:48:39Z

> cc [@kaisoz](https://github.com/kaisoz) [@NarayanaSabari](https://github.com/NarayanaSabari) ptal. Feel free to collab on this. It also will require an issue in Kubeflow I think, opened: [kubeflow/trainer#3042](https://github.com/kubeflow/trainer/issues/3042)

Sorry for not following this up earlier as I said I would. I'll chime in in the Trainer issue

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:28:16Z

/priority important-soon

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2025-12-24T10:36:38Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-24T10:57:22Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-04-07T21:12:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-07-06T21:32:58Z

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

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-07-13T13:56:53Z

We have this PR which should address this problem: https://github.com/kubeflow/trainer/pull/3651
Appreciate your feedback on the approach!

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-07-22T17:21:36Z

Given that this PR is merged, we can refactor Kueue integration to eliminate post-processing code: https://github.com/kubeflow/trainer/pull/3651
cc @kaisoz @h0pers

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-07-22T17:22:12Z

/remove-lifecycle stale
/good-first-issue

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-07-22T17:22:14Z

@andreyvelich: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8287):

>/remove-lifecycle stale
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-12T03:26:38Z

/assign

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-12T08:04:24Z

Hi @mimowo @andreyvelich, I'd like to take this on.

Traced how the fix in kubeflow/trainer#3651 reaches Kueue: SyncParallelCount only runs via the framework's RunComponentBuilderPlugins path, but Kueue's getChildJobSet() calls NewBuilder().Trainer().Build() directly, bypassing that path entirely. Confirmed empirically too deleting Kueue's manual loop and running TestReconciler fails the .Spec.Trainer.NumNodes case, so the sync logic genuinely never reaches Kueue's path.

Planning to have Kueue explicitly call SyncParallelCount as part of getChildJobSet() instead of keeping the hand-rolled loop, matching the framework's intended flow.

Will comment here if I get stuck.
Or do you have discord ?

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-08-12T16:32:49Z

Thank you for your help @SatishChoudhary642!
Please take a look at the latest PR where we introduce `PreComponentBuilder` phase: https://github.com/kubeflow/trainer/pull/3889
It has the `SyncParallelCount()` step now.

That should allow you to construct an appropriate Info object which contains the JobSet template needed for Kueue.

You can reach out to us on CNCF Slack: [#kubeflow-trainer](https://cloud-native.slack.com/archives/C0742LDFZ4K)

cc @kaisoz

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-12T18:04:12Z

Thanks for the pointer to kubeflow/trainer#3889!

Updated plan: bump Kueue's dependency to trainer v2.4 (once released), then delete the manual loop in getChildJobSet() 
RuntimeInfo() will call PreBuildSync() automatically and return an already-correct Info object. 

Will follow up here when v2.4 is out.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-08-12T18:17:16Z

Thank you for making progress on this one 👍

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-08-12T18:55:24Z

>Updated plan: bump Kueue's dependency to trainer v2.4 (once released), then delete the manual loop in getChildJobSet()
RuntimeInfo() will call PreBuildSync() automatically and return an already-correct Info object.

Sounds good, in the meantime @SatishChoudhary642 you can bump the dependency to the master branch of `kubeflow/trainer`, so your PR is ready for review.

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-15T10:18:37Z

Started working on the dependency bump

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-15T15:01:55Z

It's not good first time issue lol, 
Until someone bump the dependency I give up on this one till then, lol

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-08-26T14:44:19Z

 Sorry for not chiming in earlier

@SatishChoudhary642 I agree with you, this one might be a bit intimidating since it needs some controller-side changes. Would you be OK with me taking it over? Thanks for picking it up in the first place!

cc @andreyvelich @mimowo

### Comment by [@SatishChoudhary642](https://github.com/SatishChoudhary642) — 2026-08-26T16:46:11Z

Thanks @kaisoz! Happy to hand it over :)

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-08-26T16:51:04Z

/assign @kaisoz
