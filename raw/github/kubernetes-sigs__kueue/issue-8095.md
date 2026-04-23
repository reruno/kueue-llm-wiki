# Issue #8095: Asynchronous Inadmissible Workload Requeueing [rate limiting by 1s]

**Summary**: Asynchronous Inadmissible Workload Requeueing [rate limiting by 1s]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8095

**Last updated**: 2026-03-06T13:38:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-12-05T13:42:23Z
- **Updated**: 2026-03-06T13:38:51Z
- **Closed**: 2026-02-25T18:44:26Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@gabesaba](https://github.com/gabesaba), [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 11

## Description

**What happened**:

Too many api server writes cause slow admission processing on best effort queues with heterogenous CQ (for example containig workloads both requiring and not requiing gpus and corresponding RF with and without GPUs)

**What you expected to happen**:

Fast processing and admission.

**How to reproduce it (as minimally and precisely as possible)**:

Create large number of CPU and GPU workloads queuing in CQ with 2 RF - one with GPU, one without. Stucked GPU workloads slow down CPU workloads processing.

cc: @mimowo

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T13:49:24Z

I think this is duplicate / closely related to https://github.com/kubernetes-sigs/kueue/issues/8081. Im not totally sure we have excessive number of api server writes. Thus i marked the issue as investigation

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-08T16:30:57Z

/assign @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-08T17:01:51Z

I reproduced it locally. GPU workloads blocked the `BestEffortFIFO` queue, delaying CPU-only jobs and causing excessive API updates. I’m thinking of a fix that tackles both throughput and API noise.

First, for throughput, the scheduler could look at a small batch of workloads at the front of the queue instead of just one. That way, CPU-only workloads stuck behind GPU-heavy ones aren’t blocked unnecessarily. We’d still enforce same-priority rules so higher-priority jobs always come first.

Second, to reduce API writes, we could skip status updates if nothing has actually changed. That should cut down on repeated “pending” events caused by workloads being retried over and over (`UnsetQuotaReservationWithCondition` always writes the `QuotaReserved=False` condition, even if the workload already has that exact condition with the same reason and message).

So overall, this keeps the BestEffort semantics intact while letting the queue make forward progress and reducing unnecessary load.

@mimowo @mwielgus Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T17:14:20Z

> First, for throughput, the scheduler could look at a small batch of workloads at the front of the queue instead of just one.

That is a possibility, but it is tricky. Some environments may have a CPU workload as deep as say 200 positions, so look ahead in scheduler for 200 positions would be costly in itself. Also, it is a complex change than it seems in the context of cohorts.

> Second, to reduce API writes, we could skip status updates if nothing has actually changed. That should cut down on repeated “pending” events caused by workloads being retried over and over (UnsetQuotaReservationWithCondition always writes the QuotaReserved=False condition, even if the workload already has that exact condition with the same reason and message).

This sounds interesting and relatively easy, so we could start here. How does it happen if we have this code in place? https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L800-L804 the intention of the code is specifically to avoid sending the request if nothing changed.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-08T20:19:59Z

>This sounds interesting and relatively easy, so we could start here. How does it happen if we have this code in place? https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L800-L804 the intention of the code is specifically to avoid sending the request if nothing changed.

IIUC, the existing check is right, but it only patches when something actually changes. The issue is that the inadmissible message content changes between scheduling cycles. The message from https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L988-L989 contains dynamic values like "X more needed" which changes as cluster state changes (e.g., "3 more needed" → "2 more needed" when quota frees up). Since `SetStatusCondition` compares Status, Reason, Message, and ObservedGeneration, a change in any of these fields triggers an API write, and the Message changes frequently.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-09T17:32:22Z

Great news @sohankunkerkar !

I think the next step should be to somehow summarize the baseline timings so that we can assess the improvements etc.

--- 

Can you please provide some numbers you use for the experiments? Or even it would be great if you could script the experiment, then we can observe the improvements in a quantitative way.

For example, I'm thinking about:
- saturated GPU quota and 100 GPU workloads in the queue
- 1000 CPU workloads running quickly

Then we could measure how long it takes to process the queue of the CPU workloads. Before / after changes.

---

Once we have the experimental setup which demonstrates the issue, I would like to have also results for two experiments:
1. code modified so that the message is always the same (updates skipped)
2. code modified so that the message is always the same, and no event is sent 

---

As for the actual fix I think we could for example maintain some in-memory state, and make sure we only send one update in  O(1) seconds, say 5s.  Yes, this will mean that sometimes the messages for "Pending" are outdated, but (1.) we are always accurate about the "Status" and "Reason", just message might be lagging.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-09T17:32:32Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:06:13Z

/priority important-soon

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T13:51:26Z

FYI we have debugged the case a bit more, and the issue is not so much with the excessive number of writes but with the constant re-queue of workloads which are constrained on quota (eg. GPU workloads). 

Imagine GPU workloads are blocked on quota, so they get NoFit mode and are put from heap into the inadmissible queue when BestEffortFIFO is used. This gives scheduler a chance to "drill" the heap to get to some CPU workloads (not constrained by quota), but in the meanwhile any finishing workload is triggering `QueueInadmissibleWorkloads`, and scheduler needs to "start over" before reaching any CPU workload. 

At scale this `QueueInadmissibleWorkloads` may happen like 20 / sec. So the fix we are currently working on, @gabesaba , is to throttle the calling of `QueueInadmissibleWorkloads`, similarly as in https://github.com/kubernetes-sigs/kueue/pull/8709 by @sohankunkerkar 

/assign @gabesaba 

Let me also re-title to generalize as the issue isn't exactly with writes (at least in our case).
/retitle Fix throughput issues at scale for BestEffortFIFO CQs with CPU and GPU flavors

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-07T07:17:00Z

Thanks for the updates @mimowo. Since this issue is moving forward, I wanted to share some additional context from our side that might be useful for the ongoing fix. We've been running fairly extensive performance experiments around this problem with help from the Red Hat perf and scale team, mainly because they were able to reproduce scenarios that are hard to set up locally and exercise Kueue under sustained inadmissible pressure. Below is a summary of what we tested and what we learned, in case it helps validate or refine the current direction.                                                                                                                            
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## Test Configuration                                                                                                                                                      
                                                                                                                                                                             
  We ran two rounds of experiments on an OpenShift 4.20.8 cluster:                                                                                                           
                                                                                                                                                                             
  | Parameter | Round 1 | Round 2 (Scaled) |                                                                                                                                 
  |-----------|---------|------------------|                                                                                                                                 
  | CPU Jobs | 1000 | 2000 |                                                                                                                                                 
  | CPU Job Slots | 600 | 10 |                                                                                                                                               
  | GPU Jobs | 100 | 400 |                                                                                                                                                   
  | GPU Job Slots | 1 | 1 |                                                                                                                                                  
  | CPU Worker Nodes | m6i.2xlarge | m6i.2xlarge |                                                                                                                           
  | GPU Worker Nodes | g4dn.xlarge | g4dn.xlarge |                                                                                                                           
  | Master Nodes | 3x m6i.xlarge | 3x m6i.xlarge |                                                                                                                           
                                                                                                                                                                             
The second round was intentionally designed to keep inadmissible workloads under sustained pressure. With only one GPU slot and 400 GPU jobs, 399 workloads remain permanently stuck in the pending/inadmissible loop.                                                                                                                        
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## Approach 1: Status Update Throttling                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                 
  I prototyped a 5-second throttling window for `Pending` status updates in the scheduler, which is also described in [this                                                  
  comment](https://github.com/kubernetes-sigs/kueue/issues/8095#issuecomment-3633433243).                                                                                    
                                                                                                                                                                             
The main observation here is that even when a workload's fundamental state hasn't changed, the inadmissible message content often does (for example, `"3 more needed"` →`"2 more needed"`). That alone triggers frequent `PATCHes` and events.                                                                                                     
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## Approach 2: Stateful Inadmissibility Tracking                                                                                                                           
                                                                                                                                                                             
  ### What it does                                                                                                                                                           
                                                                                                                                                                             
 Beyond simple throttling, I prototyped a more semantic approach that tracks *why* a workload is inadmissible instead of applying uniform handling across all cases.        
                                                                                                                                                                             
  Examples of tracked categories:                                                                                                                                            
  - Insufficient quota                                                                                                                                                       
  - Flavor not found                                                                                                                                                         
  - Preemption pending                                                                                                                                                       
  - Admission check pending                                                                                                                                                  
                                                                                                                                                                             
The key idea is that workloads blocked on insufficient GPU quota, for example, don't need to be reconsidered on every cluster change and only when GPU quota is actually freed.                                                                                                                                                                     
                                                                                                                                                                             
  This enables:                                                                                                                                                              
  - **Semantic throttling** – Skip requeue when the reason and constrained resources haven't changed                                                                         
  - **Targeted requeue** – Only requeue workloads when relevant resources change                                                                                             
  - **Better observability** – Clear, structured reasons for why workloads are stuck                                                                                         
                                                                                                                                                                             
The stateful approach reduced PATCH calls by ~39%. This is lower than pure throttling (62%) because it still updates status when the reason meaningfully changes, but it preserves accuracy and avoids stale messaging.                                                                                                                             
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## Results                                                                                                                                                                 
                                                                                                                                                                             
  ### Controller Log Analysis (Round 1)                                                                                                                                    
                                                                                                                                                                             
  | Config | Total Log Lines | "Pending" Status Writes | Reduction |                                                                                                         
  |--------|-----------------|-------------------------|-----------|                                                                                                         
  | Baseline | 63,966 | 4,037 | – |                                                                                                                                          
  | Throttle | 60,088 | 99 | **97.5%** |                                                                                                                                     
  | Stateful | 61,164 | 1,299 | 67.8% |                                                                                                                                      
                                                                                                                                                                             
  ### API Server Metrics – Workload PATCH Rate (Round 2)                                                                                                                     
                                                                                                                                                                             
  | Config | PATCH req/s | Reduction |                                                                                                                                       
  |--------|-------------|-----------|                                                                                                                                       
  | Baseline | 18.94 | – |                                                                                                                                                   
  | Throttle | 7.26 | **62%** |                                                                                                                                              
  | Stateful | 11.62 | 39% |                                                                                                                                                 
                                                                                                                                                                             
  ### Full KAS Throughput Comparison (req/s)                                                                                                                                 
                                                                                                                                                                             
  | Config | GET | LIST | POST | PATCH | PUT | DELETE |                                                                                                                      
  |--------|-----|------|------|-------|-----|--------|                                                                                                                      
  | Baseline | 46.32 | 2.65 | 19.85 | 18.94 | 16.19 | 0.26 |                                                                                                                 
  | Throttle | 48.53 | 2.95 | 19.87 | **7.26** | 16.50 | 0.67 |                                                                                                              
  | Stateful | 48.15 | 2.74 | 19.78 | 11.62 | 16.34 | 0.46 |                                                                                                                 
                                                                                                                                                                             
  ### Latency (P99, ms) – No Degradation                                                                                                                                     
                                                                                                                                                                             
  | Config | GET | LIST | POST | PATCH | PUT |                                                                                                                               
  |--------|-----|------|------|-------|-----|                                                                                                                               
  | Baseline | 23 | 207 | 30 | 28 | 28 |                                                                                                                                     
  | Throttle | 23 | 214 | 29 | 30 | 26 |                                                                                                                                     
  | Stateful | 23 | 201 | 29 | 30 | 28 |                                                                                                                                     
                                                                                                                                                                             
  ### Job Scheduling Metrics (Round 2)                                                                                                                                       
                                                                                                                                                                             
  **CPU Jobs:**                                                                                                                                                              
                                                                                                                                                                             
  | Config | Count | p50 Start | p99 Start | p50 Complete | p99 Complete |                                                                                                   
  |--------|-------|-----------|-----------|--------------|--------------|                                                                                                   
  | Baseline | 2000 | 1280s | 2578s | 1293s | 2591s |                                                                                                                        
  | Throttle | 2000 | 1279s | 2576s | 1292s | 2589s |                                                                                                                        
  | Stateful | 2000 | 1280s | 2587s | 1292s | 2600s |                                                                                                                        
                                                                                                                                                                             
  **Overall Runtime:**                                                                                                                                                       
                                                                                                                                                                             
  | Config | Total Runtime | Achieved QPS |                                                                                                                                  
  |--------|---------------|--------------|                                                                                                                                  
  | Baseline | 2720s | 0.882 |                                                                                                                                               
  | Throttle | 2720s | 0.882 |                                                                                                                                               
  | Stateful | 2732s | 0.878 |                                                                                                                                               
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## Key Takeaways                                                                                                                                                           
                                                                                                                                                                             
  **API write reduction is real**                                                                                                                                            
  - Throttling: ~62% fewer PATCHes                                                                                                                                           
  - Stateful: ~39% fewer PATCHes                                                                                                                                             
                                                                                                                                                                             
  **No throughput gains observed**                                                                                                                                           
                                                                                                                                                                             
Even with fewer writes, overall scheduling throughput didn't change. This aligns with the current understanding that the dominant bottleneck is `QueueInadmissibleWorkloads` churn, not API write pressure alone.                                                                                                          
                                                                                                                                                                             
  ---                                                                                                                                                                        
                                                                                                                                                                             
  ## On the Batched Requeue Approach                                                                                                                                         
                                                                                                                                                                             
The controller-based batching approach that @gabesaba is prototyping looks like the right direction for addressing the `QueueInadmissibleWorkloads` churn directly. Using controller-runtime's workqueue with `AddAfter` provides natural deduplication and batching, and as @mimowo noted, it also gives visibility through controller-runtime metrics. The stateful inadmissibility tracking could potentially complement this by enabling more targeted requeue decisions in the future but the batched approach should address the immediate throughput issue.                                                         
                                                                                                                                                                             
  ---   

Here's the pdf with all the details:  Coutsey (https://github.com/avasilevskii)

[Upstream Kueue Results - Issue 8095 - 2026.02.03.pdf](https://github.com/user-attachments/files/25143152/Upstream.Kueue.Results.-.Issue.8095.-.2026.02.03.pdf)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T13:38:24Z

/retitle Asynchronous Inadmissible Workload Requeueing [rate limiting by 1s]

Let me scope/retitle the issue to reflect what was done. Let's keep https://github.com/kubernetes-sigs/kueue/issues/9715 as the dedicated umbrella.
