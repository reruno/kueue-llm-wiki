# Issue #6554: TAS: support balanced placement

**Summary**: TAS: support balanced placement

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6554

**Last updated**: 2025-11-13T07:17:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-12T08:20:34Z
- **Updated**: 2025-11-13T07:17:39Z
- **Closed**: 2025-11-13T07:17:39Z
- **Labels**: `kind/feature`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 11

## Description


**What would you like to be added**:

The new option aside from BestFit for balanced placement which tries to "balance" the split for the number of Pods between a pair of domains. 

For example, assume we have a Job with 16 Pods which cannot all fit into a single rack, but two.

We found experimentally that the split 8:8 into racks performs better than 1:15.

Some open questions which would be good to clarify:
- what to do if perfect split is not possible, for example, should we go with 9:7 or 10:6?
- is 3 racks "balanced"  6:6:4 better than two skewed 15:1?
- what to do about 2-level scheduling, should we balance at the level of Pods or PodSlices?

We can already start prototyping to guide some of the decisions to see what is easily available and assessing the gain  / effort ration.

However, I expect a KEP update with the finalized proposal regarding the open-questions. 

We can introduce the new policy behind an Alpha feature gate to collect feedback.

**Why is this needed**:

To optimize performance by balancing the counts of Pods when possible.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T08:20:49Z

cc @mwysokin @tenzen-y @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-12T08:30:17Z

Basically, LGTM. Actually, I requested a similar profile, previously, for Inference workloads.
What is the key difference from the previous TASProfileLeastFreeCapacity profile?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-08-12T15:26:52Z

@tenzen-y The main motivation is to provide great default experience for GB200. According to our internal research the difference in performance is really significant based on whether compact placement (BestFit) or some kind of Balanced/Symmetrical placement is used. Some NCCL primitives seem to be really sensitive to how many host network interfaces are available in multi-NVL72 setups and cross-rack traffic. This of course comes at a price of cluster fragmentation that's why we should probably start with the feature hidden behind a feature flag and if we see some positive feedback we could maybe allow to configure placement policies at the topology level to support heterogenous clusters. I can imagine that future hardware architectures are going to be more and more convoluted. WDYT?

For the required topology request this is probably not needed since an expert AI engineer who's using the required mode should do some kind of direct mapping of PodSlices/WorkerGroups to NVL72 domains. But for preferred and unconstrained (implicit) this would provide great default experience.

Some examples of what we currently think this should behave like:

```py
  # balanced placement pseudo function accepts a list of blocks with racks with available GPUs as values of each block list
  >>> balanced_placement(blocks=[[18, 18]], requested_gpu_blocks=20)
  [[10, 10]]
  >>> balanced_placement(blocks=[[18, 2]], requested_gpu_blocks=20)
  [[18, 2]]
  >>> balanced_placement(blocks=[[18, 18], [18, 18, 18], [18]], requested_gpu_blocks=54)
  [[0, 0], [18, 18, 18], [0]]
  >>> balanced_placement(blocks=[[18, 15, 10]], requested_gpu_blocks=25)
  [[0, 15, 10]]
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-13T15:27:06Z

> [@tenzen-y](https://github.com/tenzen-y) The main motivation is to provide great default experience for GB200. According to our internal research the difference in performance is really significant based on whether compact placement (BestFit) or some kind of Balanced/Symmetrical placement is used. Some NCCL primitives are really sensitive to how many host network interfaces are available and . This of course come at a price of cluster fragmentation that's why we should probably start with the feature hidden behind a feature flag and if we see some positive feedback we could maybe allow to configure placement policies at the topology level to support heterogenous clusters. I can imagine that future hardware architectures are going to be more and more convoluted. WDYT?


@mwysokin Thank you for sharing an interesting performance problem for GB200. I didn't know that the GB200 interconnect architecture does not have full bisection bandwidth. Does that mean GB200 has oversubsdcibed bandwidth, right?
Anyway, I'm fine with introducing new TAS profile and FG to enable / disable the profile across cluster-wise, first.

> > For the required topology request this is probably not needed since an expert AI engineer who's using the required mode should do some kind of direct mapping of PodSlices/WorkerGroups to NVL72 domains. But for preferred and unconstrained (implicit) this would provide great default experience.

That makes sense. Let's consider that as another feature request. I think we could consider that as a finegrained Topology Assignment Algorithm per Workload as opposed to the current cluster-wide one.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-08-13T16:16:00Z

> [@mwysokin](https://github.com/mwysokin) Thank you for sharing an interesting performance problem for GB200. I didn't know that the GB200 interconnect architecture does not have full bisection bandwidth. Does that mean GB200 has oversubsdcibed bandwidth, right? Anyway, I'm fine with introducing new TAS profile and FG to enable / disable the profile across cluster-wise, first.

Sounds great. I don't know full technical details behind this behavior. But we've seen it in our internal benchmarks.
Maybe @klueska could shed some light on it. I think he's involved in GB200 and DRA work.

> 
> > > For the required topology request this is probably not needed since an expert AI engineer who's using the required mode should do some kind of direct mapping of PodSlices/WorkerGroups to NVL72 domains. But for preferred and unconstrained (implicit) this would provide great default experience.
> 
> That makes sense. Let's consider that as another feature request. I think we could consider that as a finegrained Topology Assignment Algorithm per Workload as opposed to the current cluster-wide one.

SGTM 🖖

### Comment by [@YamasouA](https://github.com/YamasouA) — 2025-08-24T12:06:28Z

Hello, I'd like to work on this feature.

@mimowo @tenzen-y @mwysokin 
Can I discuss it here and start implementation? or need KEP?
I have no experience of KEP, so, I may not be the right person for this, if we need KEP. (Of course, I'd like to challenge, if it is OK.)

/assign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-08-25T20:20:53Z

So in order not to duplicate the effort AFAIK @pajakd is already working on it. I'm not sure why he's not assigned to the task. Maybe both of you could figure out how to divide the scope of this task and work on it together?

There're also multiple follow-ups to this particular task ready to be grabbed like extending the API with configurable placement and refactoring the code to even allow configurable placement in the first place. I think at the moment we have a bit of spaghetti with multiple branches in the same function depending on the placement policy used and it'd be awesome if we could untangle it. The first one though requires updates to the KEP.

Or we could compare both solutions  and potentially take best parts from both but I'm not sure if you'd be interested in that.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T09:32:46Z

> Hello, I'd like to work on this feature.
> 
> [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) [@mwysokin](https://github.com/mwysokin) Can I discuss it here and start implementation? or need KEP? I have no experience of KEP, so, I may not be the right person for this, if we need KEP. (Of course, I'd like to challenge, if it is OK.)
> 
> /assign

@YamasouA Thank you for your interest in this issue. This issue requires much deeper Kueue knowledge based on code. So, this might not match for the first-time contributor. I would like to offer to start with a non-difficult issue.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-08-26T12:38:49Z

Hi as @mwysokin wrote. I already started some work on this (sorry for not assigning myself to it). I hope it is fine @YamasouA 

I'm happy to share the task but I would like to provide the first implementation of the balanced placement algorithm.

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T12:43:47Z

> Hi as [@mwysokin](https://github.com/mwysokin) wrote. I already started some work on this (sorry for not assigning myself to it). I hope it is fine [@YamasouA](https://github.com/YamasouA)
> 
> I'm happy to share the task but I would like to provide the first implementation of the balanced placement algorithm.
> 
> /assign

@pajakd Could you update KEP as well?

### Comment by [@YamasouA](https://github.com/YamasouA) — 2025-08-26T14:45:41Z

Please let me know if there is anything I can help with.

/unassign
