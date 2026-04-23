# Issue #7035: Graduate WorkloadRequestUseMergePatch to Beta

**Summary**: Graduate WorkloadRequestUseMergePatch to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7035

**Last updated**: 2026-04-15T11:40:44Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-29T07:47:47Z
- **Updated**: 2026-04-15T11:40:44Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

To enable graduation of the WorkloadRequestUseMergePatch to Beta we need ensure the Workload conditions are not lost due to patches sent by scheduler: 

https://github.com/kubernetes-sigs/kueue/pull/6765/files#diff-fb3d6b36d3cd727e1dd2353fb86c0aee0bfaae1c900e0f005ab913620021d551R663-R666

Introduced in the https://github.com/kubernetes-sigs/kueue/pull/6765

One idea is to use "strict=true" mode, but for that we need to:
1. investigate the performance impact, analyze the results from the perf tests
2. introduce some retry strategy so that the scheduler could Get the new workload (from informer cache) before patching. See related: https://github.com/kubernetes-sigs/kueue/issues/6992

**Why is this needed**:

Overriding conditions set on workload by other controllers is very tricky.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T07:49:05Z

cc @tenzen-y @mszadkow @mbobrovskyi @mwysokin I think we need to think more how to solve this issue before going to Beta. The implementation in Alpha can "remove" any conditions added to the Workload concurrently by other controllers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T17:19:24Z

Ok I synced with @mwysokin . I think the first step should be to test actually the current behavior with `WorkloadRequestUseMergePatch` enabled, and document the risks. Otherwise it remains unclear if we can recommend it already for the users to use or not. 

cc @mszadkow would it be possible to list the remaining user-observable issues when WorkloadRequestUseMergePatch is enabled?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-09-30T08:38:02Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T07:11:59Z

Actually, I have an idea that we could introduce another feature gate and graduate Patch as the default mechanism for Eviction already. This will fix the second point here: https://github.com/kubernetes-sigs/kueue/issues/6158 already, and using  Patch from controllers is easy and safe. This is worth doing IMO even if SSA is fixed upstream.

The only currently known complication about Patch is in Scheduler, so we would handle that problem separately.

wdyt @mszadkow @mbobrovskyi @tenzen-y @mwysokin ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T07:19:59Z

Ok, I spent some more time playing with the status quo of WorkloadRequestUseMergePatch, and I could confirm that enabling the feature risks dropping some conditions set on the Workload by a controller, or user. 

The options I can see:
1. keep as is,
2. use strict=true mode (comparing ResourceVersion)  in scheduler and let it retry on the next scheduling cycle
3. use strict=true mode in scheduler, and re-try the same patch after fetching the new version in a loop (as proposed in https://github.com/kubernetes-sigs/kueue/issues/6992)

Here is my assessment:
(1.) makes me anxious to recommend as default (moving to Beta). Users may have custom controllers and code interacting with the Workload objects, dropping the conditions will be tricky for them. Also, it makes us long term always wonder during reviews "is it compatible with the dropping of conditions". 
(2.) I think the main concern raised is performance, however I tested it with the PR https://github.com/kubernetes-sigs/kueue/pull/7171 and our scheduler performance tests didn't detect any noticeable impact.
(3.) this will complicate the code noticeable, which is already tricky. Seems like premature optimization at this point. Also, it might be slower in some cases. Say, the generated patch will always conflict, and so we will retry the bad patch multiple times, wasting time. To make sure the patch is correct we need to re-do the entire scheduling cycle.

So my proposed path forward:
Let's go with (2.) as we don't have any experimental evidence the performance of scheduling is significantly worsened. It will keep the code simple to reason about. Then we go with that to Beta. If we have reports saying the performance is worsened (I think unlikely) we can recommend disabling WorkloadRequestUseMergePatch as mitigation, and work on the improvements a'la (3.). 

Please let me know @mwysokin @tenzen-y @gabesaba if you are ok with this plan

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-09T08:10:43Z

@mimowo I'd go with 2 and consider 3 as graduation criteria to GA if we hear feedback that there are issues with 2.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-11T12:38:20Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-15T10:55:50Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T11:20:36Z

We have this feature planned for 0.16, but I'm considering to postpone that.

First, let's review the motivation from https://github.com/kubernetes-sigs/kueue/issues/6158:
1. It causes this bug: https://github.com/kubernetes-sigs/kueue/issues/3540 (the upstream https://github.com/kubernetes/kubernetes/issues/113482 is unsolved for 3 years and unlikely to be solved any time soon)
2. It makes some features harder than expected, for example MultiKueue clearing of nominatedClusterNames field. This field is expected to be set by external controller, and so Kueue cannot clear it on eviction, or when setting clusterName using SSA. Ticketed under: https://github.com/kubernetes-sigs/kueue/issues/6185

Re 1: this still remains an open issue in k8s core, but we have mitigated the problem for environment variables in Kueue by https://github.com/kubernetes-sigs/kueue/pull/7425. Still, the problem remains for Ports, but I haven't heard a user being affected by this yet.

Re 2: this remains an issue for Kueue, but (1) there exists a workaround - the MultiKueue dispatcher users can use SSA also with the specific manager field, (2) maybe we can restructure the API so that SSA is not a problem here (for v1 or v1beta3). I opened https://github.com/kubernetes-sigs/kueue/issues/8607 to do so.

Also, I'm hesitant because once this feature is enabled on a cluster it is tricky to disable, because SSA may have trouble clearing some fields (eg. status.admission) if this was set by the PATCH.

So for the time being I suggest to (a) stay on SSA by default, (b) consider API for Dispatcher API (current status.nominatedClusterNames) which does not suffer the problem, (c) maintain both mechanisms for the time being.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:28:34Z

> Also, I'm hesitant because once this feature is enabled on a cluster it is tricky to disable, because SSA may have trouble clearing some fields (eg. status.admission) if this was set by the PATCH.

AFAIK, yes. The PATCH doesn't add a field manager. client-side apply (PATCH) manages the object as a unit (does not manage each field separately).

> So for the time being I suggest to (a) stay on SSA by default, (b) consider API for Dispatcher API (current status.nominatedClusterNames) which does not suffer the problem, (c) maintain both mechanisms for the time being.

I agree with this.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T11:36:52Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-15T11:40:42Z

/remove-lifecycle stale
let's keep the idea open for a while longer. I haven't thought about this recently
