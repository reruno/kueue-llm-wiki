# Issue #8309: StrictFIFO blocks workloads requesting different ResourceFlavors in same ClusterQueue

**Summary**: StrictFIFO blocks workloads requesting different ResourceFlavors in same ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8309

**Last updated**: 2026-04-22T02:09:38Z

---

## Metadata

- **State**: open
- **Author**: [@sfc-gh-raravena](https://github.com/sfc-gh-raravena)
- **Created**: 2025-12-17T21:38:47Z
- **Updated**: 2026-04-22T02:09:38Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/stale`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

We have a ClusterQueue configured with queueingStrategy: StrictFIFO and multiple ResourceFlavors (B200 and B300 GPU pools) with independent quotas. A workload requesting B300 GPUs (position 0 in queue) cannot be admitted because B300 is fully utilized. However, this single stuck workload is blocking all subsequent workloads requesting B200 GPUs, even though B200 has 40 available GPUs.

_Observed queue state:_
  - Position 0: job-1  (B300-raid0, 8 GPUs) - Cannot admit (B300: 16/16 used)
  - Position 1: job-2  (B200-raid0, 8 GPUs) - BLOCKED, never evaluated
  - Position 2: job-3   (B200-raid0)         - BLOCKED, never evaluated
  - Position 3: job-4  (B200-raid0, 2 GPUs) - BLOCKED, never evaluated

_Evidence:_
- Only the head workload (position 0) appears in Kueue controller logs
- Zero log entries exist for positions 1-3 workloads
- B200 has 0/40 GPUs used, B300 has 16/16 GPUs used

Controller log shows only the head workload:
```json
{"msg":"couldn't assign flavors to pod set main: insufficient unused quota for nvidia.com/gpu in flavor pool-b300, 8 more needed", "object":{"name":"job-1"}}
```
**What you expected to happen**:

- Option A (per-flavor FIFO): Workloads requesting B200 should be evaluated and admitted even when the B300 workload at the head cannot be admitted, since they're using completely independent resource pools.
- Option B (current global FIFO): If cross-flavor blocking is intentional, this should be clearly documented as it has significant operational implications.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a ClusterQueue with StrictFIFO and multiple flavors:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: test-cq
  spec:
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources:
    - nvidia.com/gpu
    flavors:
    - name: flavor-a
      resources:
      - name: nvidia.com/gpu
         nominalQuota: "16"
    - name: flavor-b
      resources:
      - name: nvidia.com/gpu
        nominalQuota: "40"
```
2. Submit a workload requesting flavor-a (will consume all 16 GPUs)
3. Submit workload-1 requesting flavor-a (8 GPUs) - will be blocked due to no capacity
4. Submit workload-2 requesting flavor-b (8 GPUs) - should fit but will be blocked
5. Observe that workload-2 never gets evaluated despite flavor-b having 40 available GPUs

Code reference:
From `pkg/cache/queue/manager.go:688-710`, the scheduler pops ONE workload per ClusterQueue per cycle:
```go
func (m *Manager) heads() []workload.Info {
    for cqName, cq := range m.hm.ClusterQueues() {
        wl := cq.Pop()  // Pops only one workload per CQ per cycle
    }
}
```

With StrictFIFO, Pop() returns workloads in strict creation order regardless of ResourceFlavor.


**Anything else we need to know?**:

_Impact:_
- Head-of-line blocking across independent resource pools
- Poor resource utilization (40 idle B200 GPUs while jobs wait)
- Defeats the purpose of multiple flavors with separate quotas

_Documentation gap:_
- The current docs state: "Older workloads that can't be admitted will block newer workloads, even if the newer workloads fit in the available quota"

_This is ambiguous regarding whether blocking applies:_
- Within the same flavor only, or
- Across all flavors in the ClusterQueue

_Questions:_
1. Is cross-flavor blocking the intended behavior of StrictFIFO?
2. If yes, what's the recommended architecture for multi-flavor setups requiring FIFO ordering?
3. Should separate ClusterQueues be created per flavor family to avoid this?
4. Would a per-flavor FIFO mode be considered as a feature enhancement?

_Workarounds considered:_
  - BestEffortFIFO: Loses strict ordering guarantees
  - Separate ClusterQueues per flavor: Management overhead, prevents inter-flavor borrowing
  - Delete blocking workload: Not operationally sustainable

**Environment**:
- Kubernetes version: v1.31.13-eks-ecaa3a6
- Kueue version: v1beta1 (ClusterQueue API version)
- Cloud provider: AWS EKS
- Hardware: p6-b200.48xlarge (B200 GPUs), p6-b300.48xlarge (B300 GPUs)
- OS: Amazon Linux 2023
- Install tools: Deployed via ArgoCD

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-17T23:52:54Z

 > Is cross-flavor blocking the intended StrictFIFO behavior? 

Yes. `StrictFIFO` uses a single queue per `ClusterQueue` with no flavor awareness. When the head workload is blocked, all subsequent workloads are blocked regardless of flavor. The documentation could be more explicit about this though.

 > What's the recommended architecture for multi-flavor setups requiring FIFO ordering? 

IIUC, creating separate `ClusterQueues` per flavor family solves the blocking problem. Placing them in a Cohort enables sharing of any common resources, though GPU quota can only be borrowed for flavors defined in both ClusterQueues. Alternatively, `BestEffortFIFO` allows workloads to bypass blocked ones while still respecting priority.

 > Should separate ClusterQueues be created per flavor family? 

Yes. This provides independent FIFO ordering per resource type while allowing cohort-based sharing of common resources.

> Would a per-flavor FIFO mode be considered? 

Flavor assignment currently happens at scheduling time, not queueing time, which makes per-flavor ordering architecturally complex. Separate ClusterQueues is the recommended solution as it avoids ambiguity around workloads that can use multiple flavors. But I would certainly like to get @mimowo and @tenzen-y thoughts on this.

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-18T06:37:58Z

Thanks for the input, @sohankunkerkar! This does feel like a pretty significant drawback to me. We currently have around five cluster queues with three to four flavors each, and to make this work we'd end up needing to introduce another ~15 cluster queues, which feels quite heavy

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T07:32:47Z

@sfc-gh-raravena thank you for opening the issue. The summary in https://github.com/kubernetes-sigs/kueue/issues/8309#issuecomment-3667626124 matches my understanding. In particular I agree that StrictFIFO by flavor is architecturally complex.

So far our go-to recommendation for all prod deployments is BestEffortFIFO. 

In the workarounds considered section you say "BestEffortFIFO: Loses strict ordering guarantees", but is there any specific scenario that would be problematic for you? 

Asking cause maybe instead of making StrictFIFO per flavor we could consider strengthening BestEffortFIFO to cover those cases.

cc @mwysokin @mwielgus

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-18T08:01:26Z

@mimowo Imagine a very busy GPU environment - basically, GPUs are almost never idle. New jobs usually sit in the queue for a while before they can run. Most jobs request 8 GPUs in a single pod, which fits perfectly on one node. From time to time, though, people submit gang jobs that need 2 or 3 pods, each requesting 8 GPUs.

In this kind of setup, with a `BestEffortFIFO` configuration, those larger gang jobs are almost impossible to schedule. While they're waiting for multiple nodes to become available at the same time, new single-pod jobs keep showing up. As soon as a node frees up, one of those single-pod jobs grabs it immediately, so the gang job never quite gets a chance to run

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-18T18:00:42Z

After digging into this, I think the core issue is that neither `StrictFIFO` nor `BestEffortFIFO` matches the behavior we need here. `BestEffortFIFO` avoids cross blocking, but as @rooty0 noted, gang jobs can starve indefinitely as smaller workloads keep moving ahead. What you are really after is FIFO ordering within each resource pool, without blocking across independent pools.

Building on @mimowo’s suggestion to strengthen `BestEffortFIFO`, Kueue already has logic to keep a workload pinned at the head of the queue, and scheduler logic that can hold resources for a waiting workload so others cannot consume them. Today, both of these are only used during preemption. If we extended this behavior to also apply when a head workload is repeatedly blocked due to resource shortage, the result would effectively be per flavor FIFO.

A blocked B300 workload would become sticky and reserve B300 resources. B200 workloads do not compete for those resources, so they would continue to admit normally. Other B300 workloads would wait behind the sticky head, preserving ordering within that pool. Once B300 capacity becomes available, the head workload admits and normal scheduling resumes.

This avoids cross flavor blocking while still protecting gang workloads from starvation. It also stays within the current BestEffortFIFO model and reuses existing infrastructure, rather than adding new APIs or queue types.

@mimowo Does this direction align with what you had in mind?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-12-18T19:08:46Z

How are you using priorities today? I didn't find any relevant info about it here. Some Kueue users solve this issue by assigning priorities based on the size of a workload. If bigger workloads have higher priority than smaller ones you could use BestEffortFIFO. If a bigger workload is at the head of the queue but needs to wait smaller ones could hop over and if enough of them accumulate at some point there might be enough capacity to accommodate the bigger one and it'll just preempt remaining small ones (maybe some will accomplish their task in the meantime).

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-18T20:53:56Z

@mwysokin We use priorities to express how important a job is. For example, imagine we have 3 gang jobs, and each of them creates 2 pods requesting 8 GPUs each. Priorities are what we use to influence admission decisions - basically, which job gets scheduled first - and to control the preemption behavior, like which workloads should be preempted first when resources are tight. Also, basically, in our scenario, a gang job isn't necessarily more important than a regular job. That being said, I think the main idea here is that we need to distinguish between same-size gang jobs based on their priority

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-12-18T21:13:10Z

Yes, I'm afraid in the current model priorities and BestEffortFIFO are the only way to get the behavior you want. 

Also please take a look at this issue: https://github.com/kubernetes-sigs/kueue/issues/7990 I'm proposing to add another level of priorities for preemption consideration. Please let me know if it'd help your use case in any way.

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-18T22:05:30Z

I actually saw your issue #7990 about a week ago. We've been discussing something very similar on our team as well - specifically, how to preempt workloads not only based on time and priority, but also using additional signals. I think this would be super useful, and it's definitely something we'd take advantage of. That said, it doesn't quite solve this particular problem.

Regarding priorities and BestEffortFIFO. In the case when both jobs use the same flavor (flavor A) the issue is that a high-priority gang job sitting at the head of the ClusterQueue is actually hard to schedule, because it needs multiple pods to land at once. Meanwhile, medium-priority single-pod jobs can fit much more easily and tend to get scheduled first whenever capacity briefly becomes available. As a result, the gang job keeps getting stuck, even though it has higher priority.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T07:15:12Z

> Meanwhile, medium-priority single-pod jobs can fit much more easily and tend to get scheduled first whenever capacity briefly becomes available. As a result, the gang job keeps getting stuck, even though it has higher priority.

But why wouldn't the "high-priority" Job be able to preempt those which got in the meanwhile? While it is preempting it would be use sticky "head".

What about using `LowerOrNewerEqualPriority` instead of `LowerPriority`? Then the small jobs (newer) will still be preempted by the older job. 

Also answering ideas like from @sohankunkerkar in [comment](https://github.com/kubernetes-sigs/kueue/issues/8309#issuecomment-3671463492), yes I'm pretty sure there are some improvements possible, but this code is quite complex, and there are many many scenarios to consider. 

I'm pretty sure improvements in scheduling which are possible because I already spent hours discussing some with @PBundyra and @gabesaba and definitely there is potential, but we would often get tricked by some corner cases. So, we need to be sure fixing has good gain / effort and the risk is under control. 

So most likely we need to do it behind a feature gate to have a bailout mechanism when something goes wrong. Having some prototype and seeing which tests are affected will also be helpful. At this point I'm not able to commit to "let's go with that". I will return to thinking about it after holiday, so probably Jan or Feb next year.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:30:54Z

/priority important-longterm

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-23T03:18:16Z

> But why wouldn't the "high-priority" Job be able to preempt those which got in the meanwhile? While it is preempting it would be use sticky "head".

Sorry, I'm now following. Here's example configuration:
```
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never

```
So, if resource flavor **B** still has available capacity, why would we want to preempt anything in the first place?

> So most likely we need to do it behind a feature gate to have a bailout mechanism when something goes wrong. Having some prototype and seeing which tests are affected will also be helpful.

[Here's my proposal/PR](https://github.com/kubernetes-sigs/kueue/pull/8393). I've run a bunch of tests so far and everything looks good, but I'm not 100% sure I'm not missing something. Basically, instead of putting this behind a feature gate, we could use a different `queueingStrategy` so the current behavior stays the same for users who rely on `StrictFIFO`.

### Comment by [@phoenix1712](https://github.com/phoenix1712) — 2025-12-26T18:57:57Z

I agree with @mimowo, if the issue is starvation for large jobs, using  `LowerOrNewerEqualPriority` instead of `Never` as `withinClusterQueue` would definitely solve the problem.

### Comment by [@rooty0](https://github.com/rooty0) — 2025-12-27T05:57:20Z

> I agree with @mimowo, if the issue is starvation for large jobs, using  `LowerOrNewerEqualPriority` instead of `Never` as `withinClusterQueue` would definitely solve the problem. 

Sure, but in this case we'd be assuming that gang jobs should have higher priority than single-pod jobs, which isn't necessarily true.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-02T21:40:02Z

I'm not sure adding a new `StrictFIFOPerFlavor` strategy is the right approach. The underlying issue is that `StrictFIFO` blocks workloads that aren't actually competing for the same resources. Adding a new strategy enum to fix this feels like the wrong layer. We'd be fragmenting the API, and users would have to understand the difference between `StrictFIFO` and `StrictFIFOPerFlavor` to make the right choice.
What if instead we add an experimental field on CQ, something like `flavorAwareBlocking: true`? When enabled, StrictFIFO would only block subsequent workloads if they compete for the same flavors. Workloads targeting non-overlapping flavors would proceed independently.

 This keeps the queueing strategy as StrictFIFO, gives users explicit per-CQ control, and doesn't force any default behavior change on existing setups. Users who need the new behavior can opt-in on specific ClusterQueues.

### Comment by [@rooty0](https://github.com/rooty0) — 2026-01-07T20:23:40Z

> What if instead we add an experimental field on CQ, something like `flavorAwareBlocking: true`? 

Sounds good to me. I'd like to get some feedback from @mimowo and @tenzen-y on this and see if we want to move forward with the PR

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-20T14:36:01Z

> > I agree with [@mimowo](https://github.com/mimowo), if the issue is starvation for large jobs, using  `LowerOrNewerEqualPriority` instead of `Never` as `withinClusterQueue` would definitely solve the problem.
> 
> Sure, but in this case we'd be assuming that gang jobs should have higher priority than single-pod jobs, which isn't necessarily true.

The `LowerOrNewerEqualPriority` doesn't necessarily mean the gang jobs should have higher priority. If there are two Jobs with the same priority, and the older one is pending while the newer one is running, the older one preempts the newer one. In your setup with potential BestEffortFIFO the flow could look like this:

1. The whole GB300 capacity is occupied
2. Workload-A requesting 16 GB300 GPUs is created
3. Workload-B requesting 8 GB300 is created with the same priority as Workload-A
4. 8 GB300 has been released
5. Workload-B is admitted and can make some progress
6. Another 8 GB300 has been released
7. Now Workload-A preempts Workload-B (because it was created earlier) and gets admitted
8. Workload-B gets back to the queue but it got a chance to make some progress

I believe this leads to even better cluster utilization than StrictFIFO, as Workload-B has some time to make progress and utilize those 8 free GPUs for some time

### Comment by [@sfc-gh-srudenko](https://github.com/sfc-gh-srudenko) — 2026-01-20T17:36:13Z

@PBundyra There are a few different use cases here. In our environment we intentionally use `StrictFIFO` together with `withinClusterQueue: Never` (happy to keep the "why" out of this thread to avoid making it too bulky)

The key part I think is missing from your example is *cross-flavor head-of-line blocking*: a workload at the head of the queue that can't be admitted for **flavor A** ends up blocking later workloads that request **flavor B**, even when flavor **B** has plenty of unused quota/capacity. That behavior is pretty surprising (and in practice feels like a design gap), because those flavors are independent resource pools.

With that behavior, `StrictFIFO` becomes hard to use for multi-flavor ClusterQueues unless you add workarounds like "one flavor per queue / ClusterQueue". But that kind of defeats the whole point of supporting multiple flavors in a single queue in the first place.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-21T10:25:22Z

The setup I've proposed assumes `BestEffortFIFO` policy so there won't be an issue with cross-flavor head-of-line blocking. 

The purpose of my example was to show how using `LowerOrNewerEqualPriority` can be used to avoid starvation of larger jobs in `BestEffortFIFO`.

To sum up:
- `BestEffortFIFO` fixes the issue with cross-flavor head-of-line blocking;
- `LowerOrNewerEqualPriority` fixes the issue with starvation of larger jobs of equal priority when `BestEffortFIFO` is used

### Comment by [@rooty0](https://github.com/rooty0) — 2026-01-22T01:36:52Z

Ok, I think we might be talking about workarounds here, while I was suggesting an actual fix to make `StrictFIFO` with multiple flavors truly usable.

First, I agree the proposed setup should address the starvation issue for larger jobs.

For our environment specifically, the main concern with `LowerOrNewerEqualPriority` is that it still preempts lower-priority workloads. We run with `withinClusterQueue: Never` because we don't want to disrupt workloads once they're running - even if they're lower priority.

The one exception is cross-queue borrowing: if a queue is borrowing from another, we do want fairness so team A still gets the GPU share it's entitled to.

That said, I'll discuss this option with my team. Thank you

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-22T02:09:36Z

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
