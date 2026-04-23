# Issue #4959: TAS: support ProvisioningRequests

**Summary**: TAS: support ProvisioningRequests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4959

**Last updated**: 2025-05-20T10:31:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-14T14:00:27Z
- **Updated**: 2025-05-20T10:31:52Z
- **Closed**: 2025-05-14T12:49:21Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 13

## Description

**What would you like to be added**:

Support for ProvisioningRequests .

**Why is this needed**:

To make TAS work with autoscaling.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T14:00:46Z

cc @tenzen-y @mwielgus @mwysokin 
/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-04-17T15:54:28Z

@mimowo, can I pick up some of the stuff here? I'm happy to shadow you if possible.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-17T16:20:58Z

Hi @sohankunkerkar , sounds great. Currently I'm prototyping the following high-level idea:

If the workload requires TAS and ProvRequest, then:
1. skip computation of TAS assignment in the first pass of scheduler, just assign let it assign QuotaReservation
2. force scheduler to do another pass on the workload when QuotaReserved and all checks are green (incl. ProvReq)
3. the second (delayed) scheduling pass will be consistent with the choices about quota reservation, but more detailed (will include TAS assignments)

When I have something working in a publishable state (hopefully tomorrow) I will push it as a draft PR. I will appreciate working together on the design details, review, testing and other spin off tasks.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-04-25T17:06:43Z

@mimowo Is there anything I can help you with apart from reviewing the KEP? I’d love to get more involved!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-25T17:13:54Z

@sohankunkerkar sure, some early feedback on the impl would be nice. FYI I'm ooo next week.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-25T17:25:06Z

Since I'm ooo next week, aside from reviewing, if you want to code a little bit, then we still need the requeuing with exponential delay. Feel free to prototype on your branch (PR based on top of mine). For that I was thinking of either extend the Workload.Info struct with `secondPass {requeueCount, requeueAt}`, or embedded mapping inside the queue. Be aware that the feature is a priority for 0.12, so addressing remarks and merging both PRs will be time sensitive.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-25T17:43:51Z

Also, I have another ask, and more isolated and important - prepare a PR which extracts the fix in this code fragment: https://github.com/kubernetes-sigs/kueue/pull/5052/files#diff-fb3d6b36d3cd727e1dd2353fb86c0aee0bfaae1c900e0f005ab913620021d551R213-R228

This bug was discovered by this test: https://github.com/kubernetes-sigs/kueue/pull/5052/files#diff-95ef2b4868044a4fbcc96fcda6df858f3b79548d2e4548fafcd9280114928dfcR1705.

Basically, after restart sometimes the cache is not yet populated, and cq might be still nil. The idea of the fix is to skip based on NoFit, before we call cq.Parent(). 

Ideally, I would like to extract the fix to a separate PR with dedicated test (either TAS or pure quota), so that we can cherry-pick if previous releases are affected., and I think 0.11 is affected: https://github.com/kubernetes-sigs/kueue/blob/ebc7ad9b840fa40ed20e070197fc08e5e5d980b1/pkg/scheduler/scheduler.go#L216. So, ideally, we can write a test which is independent of the new code changes.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:04:02Z

> Also, I have another ask, and more isolated and important - prepare a PR which extracts the fix in this code fragment: https://github.com/kubernetes-sigs/kueue/pull/5052/files#diff-fb3d6b36d3cd727e1dd2353fb86c0aee0bfaae1c900e0f005ab913620021d551R213-R228
> 
> This bug was discovered by this test: https://github.com/kubernetes-sigs/kueue/pull/5052/files#diff-95ef2b4868044a4fbcc96fcda6df858f3b79548d2e4548fafcd9280114928dfcR1705.
> 
> Basically, after restart sometimes the cache is not yet populated, and cq might be still nil. The idea of the fix is to skip based on NoFit, before we call cq.Parent().
> 
> Ideally, I would like to extract the fix to a separate PR with dedicated test (either TAS or pure quota), so that we can cherry-pick if previous releases are affected., and I think 0.11 is affected:
> 
> [kueue/pkg/scheduler/scheduler.go](https://github.com/kubernetes-sigs/kueue/blob/ebc7ad9b840fa40ed20e070197fc08e5e5d980b1/pkg/scheduler/scheduler.go#L216)
> 
> Line 216 in [ebc7ad9](/kubernetes-sigs/kueue/commit/ebc7ad9b840fa40ed20e070197fc08e5e5d980b1)
> 
>  if cq.HasParent() { 
> . So, ideally, we can write a test which is independent of the new code changes.

I think this failure is related: https://github.com/kubernetes-sigs/kueue/pull/5287#issuecomment-2893436998

Did we fix for FairSharing too?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T10:07:19Z

> Did we fix for FairSharing too?

Fixing for FairSharing was not considered. It might have been fixed as a side effect of the PR: https://github.com/kubernetes-sigs/kueue/pull/5138, but I didn't check.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:15:24Z

I observe that no unit tests fail (running integration tests now, but I suspect they won't either) when we remove this line https://github.com/kubernetes-sigs/kueue/blob/7da8e0a2ea64c026ed3daf28aec63d711c1d1f72/pkg/scheduler/scheduler.go#L361-L362

I think that should be the centralized place that we do this validation, rather than having some ad-hoc check later in the scheduling code

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:19:50Z

One idea is that once we get entries (step 3), we split that list into "validEntries" and "invalidEntries". We only pass validEntries to the iterator

https://github.com/kubernetes-sigs/kueue/blob/7da8e0a2ea64c026ed3daf28aec63d711c1d1f72/pkg/scheduler/scheduler.go#L198-L202

and requeue invalidEntries

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T10:22:07Z

@gabesaba I suggest you open an issue for this proposal(s). This does not refer directly to the issue we are currently discussing in. It was just discovered while working on the issue.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-20T10:31:51Z

> [@gabesaba](https://github.com/gabesaba) I suggest you open an issue for this proposal(s). This does not refer directly to the issue we are currently discussing in. It was just discovered while working on the issue.

Ack. Created https://github.com/kubernetes-sigs/kueue/issues/5291
