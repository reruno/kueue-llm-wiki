# Issue #477: Use information about last checkpoint on preemption

**Summary**: Use information about last checkpoint on preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/477

**Last updated**: 2026-04-12T03:59:47Z

---

## Metadata

- **State**: open
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-14T16:11:14Z
- **Updated**: 2026-04-12T03:59:47Z
- **Closed**: —
- **Labels**: `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 11

## Description

This is known as cooperative preemption

If the workload does checkpointing, then we can assume they are able to communicate the latest checkpoint via a status condition. We can take that into account when selecting victims and prioritize ones that checkpointed lately.

We can update the existing design doc for preemption to include this.

_Originally posted by @ahg-g in https://github.com/kubernetes-sigs/kueue/issues/83#issuecomment-1332484563_

## Discussion

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-03T15:11:46Z

That may potentially create a bad incentive to not publish the checkpoints in low priority jobs or the job will have a higher chances of being preempted (vs those that doesn't do it).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T16:29:59Z

We could devise a policy to provide incentive to setting the checkpoint.

For example: the assumed checkpoint of a workload that doesn't define any is equal to it's the maximum of its startTime and the median of the startTime of the workloads that define one.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T16:33:18Z

Although that might give an incentive to publish one checkpoint and never do it again. But any system where there is cooperative preemption has the same issue. I suppose it is called cooperative for a reason :)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-03T18:47:47Z

Right, cooperative preemption by design assumes that the jobs play nicely. This is not uncommon in environments where researchers share a cluster and use common libraries in their jobs that have builtin support for checkpointing.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-03T23:55:58Z

I'm wondering how much cooperativeness should assumed in the system. In the extreme, exaggerated case we wouldn't need any quotas and queues if everyone tried to play nicely. 
People are nice up to a point when they learn that their goodwill is being exploited to their disadvantage. And here, publishing the status works against them, unless there is some other benefit that can balance the chances of being preempted first.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-04T06:08:01Z

>  In the extreme, exaggerated case we wouldn't need any quotas and queues if everyone tried to play nicely.

You will still need quotas and queues to automate "playing nice".

> People are nice up to a point when they learn that their goodwill is being exploited to their disadvantage. And here, publishing the status works against them, unless there is some other benefit that can balance the chances of being preempted first.

Users have a strong incentive to checkpoint if their jobs run for a long time. 

As for setting the status, a common setup is that users use sdks to deploy their workloads, those sdks are generally controlled by the batch admin / platform team and probably use common libraries for checkpointing that will force setting this value. 

Having said that, I think we want to distinguish between having the status and the incentives of setting it, the later can be improved as a followup if needed and based on user feedback.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-04-04T16:41:45Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-05T09:15:32Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-05T12:21:52Z

/lifecycle frozen

### Comment by [@amy](https://github.com/amy) — 2025-11-14T20:08:45Z

/cc

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-04-12T03:59:47Z

With WG Checkpoint/Restore now active and Workload Aware Scheduling landing in alpha, I think it's a good time to revisit this. 

Kueue already suspends rather than deletes preempted workloads, and pods get SIGTERM so applications can checkpoint during shutdown. But the coordination is entirely on the application side. Kueue doesn't know if a checkpoint happened, how recent it is, or how to restore from it on re-admission. If upstream C/R pieces mature, Kueue could close that gap, i.e., signal ahead of preemption, allow time for checkpointing, pick smarter preemption victims based on interruption cost, and signal the job controller to restore rather than restart.                            
                                                                                                                                                  
Some questions worth thinking about: how does a workload communicate that it supports checkpointing? How do we estimate interruption cost when selecting preemption victims? What should the preemption flow look like when a checkpoint grace period is involved? How should quota accounting work while a workload is draining? And how does Kueue distinguish `restore from checkpoint` from `start fresh` on re-admission?                 
              
Some of these probably belong on the upstream WAS PodGroup API rather than as Kueue-specific annotations. [KEP-5710](https://github.com/kubernetes/enhancements/issues/5710) already acknowledges checkpoint-aware preemption cost as a user story, but defers it from alpha. Kueue could help shape those APIs by providing requirements from the batch scheduling side.

This also connects to #3758. If we know a workload's checkpoint state, the decision about when to preempt becomes better informed, and checkpoint-capable workloads with recent checkpoints can be preempted sooner at lower cost, while workloads without checkpoints benefit more from delayed preemption.                                                                                                                       
              
I'm planning to follow both the WG Checkpoint/Restore and SIG Scheduling WAS discussions for this.

cc @mimowo
