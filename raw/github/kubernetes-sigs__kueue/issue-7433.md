# Issue #7433: See a pod admitted but still schedule gated

**Summary**: See a pod admitted but still schedule gated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7433

**Last updated**: 2026-03-29T21:56:59Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-10-29T20:19:47Z
- **Updated**: 2026-03-29T21:56:59Z
- **Closed**: 2026-03-29T21:56:59Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

We see that a workload is admitted but the underlying pod still schedulegated.

**What you expected to happen**:
Either:
1. workload for pod is admitted and the underlying pod is `Pending`
2. OR workload for pod is not admitted

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
Potential problems: 
- the update for admission and schedulegate removal should happen atomically
- potentially an issue where kubernetes api will reject future changes to pod if you have previously changed a field outside of an allowed list of fields in the spec. (But overall for this, if kubernetes API fails, we want admission to fail as well)

Keep in mind: ScheduleGate cannot be re-added if its already been removed. So probably we don't need to look through any update path. 


**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-10-29T20:21:31Z

cc/ ^ @mwielgus @ichekrygin

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-29T22:21:24Z

Do you by chance have more info on how to reproduce this?

I've seen some issues where scheduling gates updates get rejected and that may not reflect the correct update.

I've also seen this behavior if you have multiple scheduling gates.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-29T22:22:52Z

For Openshift we get these problems for scc rules if we don't specify the right pod security context for raw pods and the admission plugin rejects the update of the pod.

### Comment by [@amy](https://github.com/amy) — 2025-10-30T17:57:37Z

> Do you by chance have more info on how to reproduce this?

no sorry 🥲 For us it was some storage thing. I don't know if the actual issue is as relevant. The main issue is why Kueue isn't doing the right thing. 

> have multiple scheduling gates

wait whats this one? As in, what do you mean by multiple? @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-30T18:14:04Z

> wait whats this one? As in, what do you mean by multiple? @kannon92

Scheduling gates are a list of strings.

Kueue adds one but if a pod has other scheduling gates I think kueue thinks it admitted the workload.

### Comment by [@amy](https://github.com/amy) — 2025-10-30T18:29:26Z

Ah I see this: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/pod/pod_controller.go#L1403
Where yeah it probably just checks if it gates/ungates `"kueue.x-k8s.io/admission"` 

@mimowo @kannon92 Before admission, do you think it makes sense to add an admission check:
- there's no remaining scheduling gates besides the kueue one?

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-30T19:38:39Z

> Ah I see this: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/pod/pod_controller.go#L1403 Where yeah it probably just checks if it gates/ungates `"kueue.x-k8s.io/admission"`
> 
> [@mimowo](https://github.com/mimowo) [@kannon92](https://github.com/kannon92) Before admission, do you think it makes sense to add an admission check:
> 
> * there's no remaining scheduling gates besides the kueue one?
> 
> /assign

I think a gate is added in cases of ManagedJobsWithoutQueueName.

I would think that maybe we should make kueue check all the scheduling gates and if there are other ones it shouldn't mark the workload as admitted.

### Comment by [@amy](https://github.com/amy) — 2025-10-30T20:19:22Z

> I think a gate is added in cases of ManagedJobsWithoutQueueName.

We heavily see ScheduleGated because we use the pod/podgroup workload type. So we send the pod (with Kueue annotations/labels) first. Then Kueue creates the workload from those annotations. So those pods are first `ScheduleGated` by Kueue until admission. Once ungated, we see the pods go to `Pending` then `Running` (with various failure reasons in the Pending phase from k8s)

But yeah, I'd like to propose adding an admission check
> add an admission check:
there's no remaining scheduling gates besides the kueue one?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-28T21:12:01Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-27T21:27:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-29T21:56:53Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-29T21:56:59Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7433#issuecomment-4151167121):

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
