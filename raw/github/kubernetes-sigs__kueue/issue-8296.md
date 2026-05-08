# Issue #8296: TrainJob integration: Job should be unsuspended and updated in a single API request

**Summary**: TrainJob integration: Job should be unsuspended and updated in a single API request

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8296

**Last updated**: 2026-05-07T21:55:01Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T10:05:10Z
- **Updated**: 2026-05-07T21:55:01Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@NarayanaSabari](https://github.com/NarayanaSabari)
- **Comments**: 18

## Description

/kind bug
I think this is also a small performance bug.

**What would you like to be cleaned**:

Currently when we are starting a TrainJob instance we need to send two API requests to start it:
1. to set unsupend=false
2. to inject the NodeSelectors

**Why is this needed**:

1. To avoid race conditions as the one found here: https://github.com/kubernetes-sigs/kueue/pull/8255#discussion_r2626391001
2. To optimize the number of API request sent to the API server

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T10:05:40Z

cc @kaisoz @j-skiba @NarayanaSabari

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T13:45:41Z

The Trainjob admission webhook [requires the Trainjob to be suspended to modify the podTemplateOverrides](https://github.com/kubeflow/trainer/blob/eaa3d859d313824374badbf4c327802639b9fc40/pkg/runtime/framework/plugins/jobset/jobset.go#L167). This is why we first call the API server to update the podTemplateOverrides and then unsuspend the job.

I don't think doing just one API call is possible without Trainer modifications... I remember asking the maintainers about the reason.. let me open an issue in there

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T13:51:13Z

Thank you for the context. It seems reasonable to me to discuss this more under Kubeflow issue.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T14:22:24Z

Issue in Trainer: https://github.com/kubeflow/trainer/issues/3043

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:31:57Z

/priority important-soon

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-01-22T08:47:12Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-22T09:16:37Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-22T09:26:08Z

/remove-lifecycle stale
cc @kaisoz any progress here?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-04-23T19:11:17Z

> /remove-lifecycle stale
> cc @kaisoz any progress here?

So I talked with @andreyvelich offline and given that the `podTemplateOverrides` API was replaced by the `RuntimePatches` API, we'll need to adjust the Trainer PR.

@NarayanaSabari since you are the author of that PR, would you have time to take care of this? I can review it as soon as it's ready ☺️. Otherwise I can draft a PR for next week

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-04-25T09:50:09Z

Sounds good, I’ll take care of updating the PR to use the RuntimePatches API. I’ll have it ready by tomorrow EOD and will tag you for review once it’s up 👍

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-04-30T06:09:24Z

Quick status update - apologies for the delay past my earlier ETA.

PR is up on the Trainer side, ported to the new `RuntimePatches` API: kubeflow/trainer#3469.

Summary of what's in it:
- Relaxes `checkRuntimePatchesImmutability` to consult `oldObj.Spec.Suspend` instead of `newObj.Spec.Suspend`, mirroring the [k/k Job validation pattern](https://github.com/kubernetes/kubernetes/blob/86b66f6f333a/pkg/registry/batch/job/strategy.go#L191) - same approach as the closed #3122, just on the new API surface.
- The downstream JobSet activity check (`Active > 0`) is preserved, so updates while pods are running still fail.
- Split into 3 bisect-friendly commits (validation + unit test, new unit case for the atomic transition, integration test against envtest).
- Locally: `make fmt`/`vet` clean, full `make test-integration` passes (46/46).

Once the Trainer PR lands, follow-up on the Kueue side will collapse the two-step update at [`trainjob_controller.go#L305-L309`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/trainjob/trainjob_controller.go#L305-L309) into a single atomic `client.Update`, which closes this issue.

cc @kaisoz @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-30T06:13:19Z

Thank you @NarayanaSabari for the status update and the PR 👍 Let me check that

EDIT: left review comments there.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-05T09:47:15Z

FYI we have already the TrainJob fix merged: https://github.com/kubeflow/trainer/pull/3469, and are waiting for the cherrypick to 2.2 branch: https://github.com/kubeflow/trainer/pull/3469 and patch release. Once we have that we can update Kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-05-05T16:57:18Z

> FYI we have already the TrainJob fix merged: [kubeflow/trainer#3469](https://github.com/kubeflow/trainer/pull/3469), and are waiting for the cherrypick to 2.2 branch: [kubeflow/trainer#3469](https://github.com/kubeflow/trainer/pull/3469) and patch release. Once we have that we can update Kueue.

@mimowo The patch version release is not planned at this time. So, could we (Kueue) use 2.2 branch for a while?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-05T17:15:19Z

> @mimowo The patch version release is not planned at this time. So, could we (Kueue) use 2.2 branch for a while?

We could certainly use the branch for prototyping, but I'm not sure we can merge and release Kueue against branch build of TrainJob, because users of TrainJob (I assume) would use what is released, and that would not be compatible with the new runtime of Kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-05-06T15:46:06Z

> > [@mimowo](https://github.com/mimowo) The patch version release is not planned at this time. So, could we (Kueue) use 2.2 branch for a while?
> 
> We could certainly use the branch for prototyping, but I'm not sure we can merge and release Kueue against branch build of TrainJob, because users of TrainJob (I assume) would use what is released, and that would not be compatible with the new runtime of Kueue.

Uhm, that's a good point, indeed. In that case, resolving this problem probably be delayed due to KF trainer release capabilities...

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-05-06T21:50:01Z

If this is critical bug for Kueue to support Trainer v2.2, we can release patch version v2.2.1
Thoughts @astefanutti @tenzen-y @kaisoz ?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-05-07T21:55:01Z

> If this is critical bug for Kueue to support Trainer v2.2, we can release patch version v2.2.1 Thoughts [@astefanutti](https://github.com/astefanutti) [@tenzen-y](https://github.com/tenzen-y) [@kaisoz](https://github.com/kaisoz) ?

I don't think is that critical since the current implementation, although suboptimal, does the job, and there's a workaround for the race condition (please @mimowo correct me if I'm wrong)
