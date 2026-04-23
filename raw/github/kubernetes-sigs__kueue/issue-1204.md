# Issue #1204: Support vcjob in kueue

**Summary**: Support vcjob in kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1204

**Last updated**: 2025-05-09T06:08:35Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-10-12T06:19:37Z
- **Updated**: 2025-05-09T06:08:35Z
- **Closed**: 2025-05-09T06:08:33Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 23

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support volcano job(aka. vcjob)

**Why is this needed**:

As we know, volcano also supports job queueing, but in a cluster with multi schedulers or in a multi-cluster scenario, we hope we can have a resource management component in the front. AFAIK, volcano also supports suspend semantic.

also cc @GhangZh who has some experiments on this. 

This can be an experimental support.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-16T14:39:41Z

sgtm

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2024-01-25T13:38:22Z

I see in #1269 @kerthcet mentioned

> but this involves contributions to volcano upstream, still WIP.

anyone have additional context? I'd be interested in seeing this land and would like to understand current blockers/if the community can help? I found https://kueue.sigs.k8s.io/docs/tasks/integrate_a_custom_job/ and other implementations but it wasn't clear to me if there are any missing dependencies/or quirks in functionality (I see some called out for Ray)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-26T02:12:20Z

Yes, we have a friend @GhangZh who already has some practice with this, but this requires supporting `Suspend` in volcano project, but I didn't have enough time right now, we need volunteers.

By the way, can you describe your scenarios which can help us better understand the feature. @alexeldeib

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2024-01-27T19:51:25Z

We use volcano plugins to do some automatic field injection today (pytorch, ssh for mpirun, similar stuff), we can probably do it the manual way with kueue + jobsets, although it's a nice convenience layer to write simpler manifests.

I see Suspend exists in Volcano APIs/CLI today? What's actually missing?

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2024-01-27T20:48:28Z

looks like it's an issue of the kueue <-> volcano APIs? volcano uses commands but kueue expected a spec field to edit with no return value to pass to client.Update() https://github.com/kubernetes-sigs/kueue/blob/3b37fbf0a06f7778d40bc656bbe312aeaabcc2e9/pkg/controller/jobframework/reconciler.go#L252-L253

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T23:12:53Z

You can also try to run PyTorch and MPI with kubeflow, for which the support is already there.

> kueue expected a spec field to edit with no return value to pass to client.Update()

Kueue needs to be able to tell Volcano when it's time to create Pods (because the job was admitted) or when it's time to delete pods (because the job was preempted).

> volcano uses commands

Not sure what you mean.

### Comment by [@ace-cohere](https://github.com/ace-cohere) — 2024-01-31T00:20:37Z

>> volcano uses commands

>Not sure what you mean.

I was trying to follow the issue with Suspend. Maybe there's no issue :D 

It looked to me like kueue expects a declarative way to do things like [`job.Suspend`](https://github.com/kubernetes-sigs/kueue/blob/3b37fbf0a06f7778d40bc656bbe312aeaabcc2e9/pkg/controller/jobframework/reconciler.go#L252-L253)

volcano has some [commands](https://github.com/volcano-sh/volcano/blob/a566d48f54b7f31513efa51045a6492a946430fc/cmd/cli/vsuspend/main.go#L48) which create [separate CRDs](https://github.com/volcano-sh/volcano/blob/a566d48f54b7f31513efa51045a6492a946430fc/pkg/cli/job/util.go#L69-L95) which a reconciler acts on to mutate Job state accordingly (something like a shared bus for communication?). I don't see how that can fit into the suspend model kueue expects.

I see volcano [can](https://github.com/volcano-sh/volcano/blob/a566d48f54b7f31513efa51045a6492a946430fc/pkg/controllers/job/job_controller.go#L354) do it [declaratively too](https://github.com/volcano-sh/volcano/blob/a566d48f54b7f31513efa51045a6492a946430fc/pkg/controllers/job/state/factory.go#L75-L76) though, if you just [set](https://github.com/volcano-sh/volcano/blob/a566d48f54b7f31513efa51045a6492a946430fc/pkg/controllers/job/job_controller.go#L338) `.status.state.phase = aborted`? or similar

Honestly, I'm leaning kueue + jobset + a thin layer to replace volcano plugins to avoid human errors in yaml-ing. maybe kustomize functions or helm or something, not sure...

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-31T00:36:57Z

That is a very uncommon design 🤔 

I would imagine that at some point the "command" translates into a change into a Job CRD. But I could be mistaken.

In any case, the job reconciler supports a few different interfaces that allows you modify how multiple actions are performed that don't necessarily assume a declarative API.

### Comment by [@ace-cohere](https://github.com/ace-cohere) — 2024-01-31T01:03:25Z

for posterity for future aspirational users/issue solvers

> I would imagine that at some point the "command" translates into a change into a Job CRD. But I could be mistaken.

yeah, it looks like the second set of links might work, and I think all the actions controller does is translate that into the status field like you said. I haven't tried manually setting aborted/aborting phase from volcano. frankly that design confused me too. It _looks_ like it'd work as I described declaratively, but you're effectively driving desired state from status, which is weird. Maybe that's why it's a separate CRD? I'd personally do a spec field, but I see the semantics are weird -- something like "suspend" is a user-initiated spec/action change, while you want to track status of the job separately _shrugs_

I probably will not personally pursue this path further but sharing my thoughts for anyone who chooses to, and thanks @alculquicondor and @kerthcet for the quick replies/tips 🙂 

(and I’ll check out kubeflow — sounds like maybe that’s along the lines of what I want)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-31T06:50:17Z

> I was trying to follow the issue with Suspend. Maybe there's no issue :D

I checked the volcano code, the aborted action is somehow similar to `Suspend` as you said, I think we can use that directly.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-31T06:55:55Z

> We use volcano plugins to do some automatic field injection today (pytorch, ssh for mpirun, similar stuff), we can probably do it the manual way with kueue + jobsets

Then if I understood correctly, heading with this way, you're no longer need the volcano anymore, what we want to do here is we hope kueue can manage vcjob as well.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-30T07:15:49Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-04-30T07:22:32Z

Will talk with @GhangZh offline to see how to push this forward.
/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-29T07:23:37Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-08-05T02:37:36Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-03T03:26:55Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-03T04:20:16Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-03T07:05:43Z

/remove-lifecycle rotten

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-12-10T03:44:16Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-10T04:29:59Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-09T05:30:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-09T06:08:28Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-09T06:08:34Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1204#issuecomment-2865251493):

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
