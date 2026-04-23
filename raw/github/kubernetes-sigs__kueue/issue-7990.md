# Issue #7990: Add a mechanism to consider preemption cost when finding preemption candidates

**Summary**: Add a mechanism to consider preemption cost when finding preemption candidates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7990

**Last updated**: 2026-03-17T17:43:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2025-11-28T10:15:37Z
- **Updated**: 2026-03-17T17:43:44Z
- **Closed**: 2026-03-17T17:43:44Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 40

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A mechanism to consider preemption cost when looking for and sorting candidates for preemption. The field would be set by some external controller (with a referential implementation of such controller included as part of the feature). Kueue should include a signal from that controller and should try to minimize the preemption cost.

Something that we need some feedback for would be whether the preemption cost parameter should be used only to sort/compare workloads with the same priority (e.g. 3 workloads A, B, C have workload priority medium, but A: has high preemption cost, B has medium preemption cost and C has low preemption cost, in this case the order of considering them for preemption should be: C, B, A) or whether it should be a combination of workload priority and the preemption cost (e.g. when having a low priority workload D with a critical preemption cost and a medium priority workload E having low preemption cost the order of preemptions should be: E, D).

**Why is this needed**:

Cost of preemption is not equal across pods. Pods which have a relatively long initialization time (minutes) are cheap to preempt if the initialization didn't finish but expensive to preempt when they already started carrying out some work. The same applies to checkpointing. If a pod carried out some work already but hasn't created a checkpoint yet it's costly to preempt it and its effort would be wasted, meanwhile a pod that just finished checkpointing is relatively cheap to preempt.

Since access to accelerators is so expensive and the accelerators are so scarce I think Kueue should try to care about the preemption cost and should use additional signals when looking for and sorting candidates for preemptions.

Also I don't think that Kueue itself should include some well defined policies how to calculate the cost of preemption but rather should allow external controllers to populate this information and Kueue should consider it during identifying and sorting the preemption candidates. We could offer a reference implementation of such controller that'd be a good example for folks trying to implement their own accordingly to the policies at their organizations and their business goals. I think a good referential example would be a controller that increases the preemption cost for every preemption that already happened. We store that number in the `schedulingStats` (thanks @PBundyra !) so it should be easy to use and react to this field to calculate the referential preemption cost field.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-11-28T10:21:02Z

CC @mimowo @tenzen-y @kannon92 @mwielgus @PBundyra @gabesaba @pajakd @amy @ichekrygin

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-01T02:20:31Z

/cc

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-01T02:59:02Z

This would be really a valuable feature for users to extend the preemptions.

---

> Something that we need some feedback for would be 

This is an interesting question. I'd vote to "it should be a combination of workload priority and the preemption cost".
I guess I'd use this feature _basically_ for tie-breaking among the workloads with the same priority. But, there could be some exception scenarios:
- If a low-priority workload has experienced too many preemptions, I would want to prioritize this low-priority job over a higher-priority workload at some point. I don't want low-priority jobs to keep being preempted and never complete.
- If a workload is very very close to complete/checkpoint, I might prefer to sacrifice a higher priority workload.

I was wondering if we can do `<WorkloadPriority.value> + <preemption cost>` for this sorting. 
Then, let's say if you have `value: 100/200/300` on your workload priorities. You can put `preemption_cost 1~99` if you want the cost to be used just for tie-breaking. And, you can put 100+ if you want the cost to break the boundary of priorities.

---

Also, one point from me on the API design: we should allow _multiple_ scores to be defined at a single workload (and Kueue would take a total at the calculation). Like @mwysokin mentioned, there're multiple use cases already, and they are not exclusive. i.e., people might want to use this preemption cost for both the num of preemptions and for the phase of workloads.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-01T03:04:42Z

> I think a good referential example would be a controller that increases the preemption cost for every preemption that already happened. 

I was considering one thing on this usecase actually: we need to be careful not to introduce a preemption flapping by this. Like: jobA is preempted and get a higher preemption cost -> jobB is preempted by jobA and get a higher preemption cost -> jobA is preempted by jobB (because jobB's preemption cost is increased) ... 
Some better algorithm is necessary here..

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:25:24Z

Yes, introducing different ordering functions for admission and preemption creates the risk of infinite preemption cycles. So this should be an important consideration for the design.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-12-01T10:37:59Z

> I was considering one thing on this usecase actually: we need to be careful not to introduce a preemption flapping by this. Like: jobA is preempted and get a higher preemption cost -> jobB is preempted by jobA and get a higher preemption cost -> jobA is preempted by jobB (because jobB's preemption cost is increased) ...
> Some better algorithm is necessary here..

To handle cycles like that we can use the following mechanism. JobA should calculate JobB's "preemption priority" **after** the hypothetic preemption and admission of JobA and preempt only if JobB's "preemption priority" would not increase beyond its own. Similar mechanism is used to prevent cycles in fair sharing preemption (see https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/#proof-that-two-workloads-wont-preempt-each-other).

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-02T03:53:06Z

> To handle cycles like that we can use the following mechanism. JobA should calculate JobB's "preemption priority" after the hypothetic preemption and admission of JobA and preempt only if JobB's "preemption priority" would not increase beyond its own. 

Is that even possible? What if it's a cycle involving many jobs? like jobA preempts jobB, which will make jobB preempt jobC, which will then make jobC preempt jobD .... which will make jobZ preempt jobA?
Also, if I understand what [@mwysokin](https://github.com/mwysokin) meant correctly, we'll implement a controller for this preemption cost calculated by the num of preemptions _externally_ outside Kueue as a "referential example". But, your proposal requires Kueue itself to understand how much a score will be increased by each preemption. i.e., Kueue's preemption needs to somehow know how much a jobB's cost is increased after a preemption by the external controller managing these preemption costs.

---

I was imagining a simpler (but not-beautiful?) solution: increase the preemption cost not every after a preemption but every after a few preemptions. Then, such a flapping could occur once at the most in the worst case, but won't recur.
The worst case scenario for example is: jobA preempts jobB -> jobB's cost is increased -> jobB preempts jobA -> jobA's cost is increased -> jobA preempts jobB -> (jobB's cost shouldn't be increased this time).

### Comment by [@pajakd](https://github.com/pajakd) — 2025-12-02T14:25:18Z

> Is that even possible? What if it's a cycle involving many jobs? like jobA preempts jobB, which will make jobB preempt jobC, which will then make jobC preempt jobD .... which will make jobZ preempt jobA?

It is possible (at least it should be). If there is some "preemption priority", then this sequence of preemptions jobA -> jobB -> jobC ... defines a decreasing sequence of such priorities. Which will prevent jobZ from preempting jobA. We have to make sure that the "preemption priority" is well-defined.

> Also, if I understand what [@mwysokin](https://github.com/mwysokin) meant correctly, we'll implement a controller for this preemption cost calculated by the num of preemptions externally outside Kueue as a "referential example". But, your proposal requires Kueue itself to understand how much a score will be increased by each preemption. i.e., Kueue's preemption needs to somehow know how much a jobB's cost is increased after a preemption by the external controller managing these preemption costs.

This is how I imagined it. The external controllers might set some cost of preemptions (based on some checkpointing, time-to-complete etc.). But in some fixed time, Kueue should be able to simulate the preemption jobA->jobB to verify that jobB will not be able to immediately "strike back". It is fine (I think) if this changes after some time (because eg jobA's cost is lowered by the external controller). 

If the cost might be changed in an unpredictable way by some external controller after each preemption, then we risk the infinite preemption cycles.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-03T00:58:26Z

>  I think a good referential example would be a controller that increases the preemption cost for every preemption that already happened.

To be clear, I'm specifically talking about this ^ usecase: preempting jobB increases a preemption cost of jobB immediately, which may allow jobB to preempt jobA. However, Kueue cannot simulate that by itself, unless somehow involving the external controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T02:32:55Z

I basically agree with introducing such a mechanism.
We should care about the following points when we introduce this mechanism:

- Avoid introducing batch users facing API (like annotation) since the evil users can exploit this mechanism so that their Job has never been preempted by others. The workload API field would be better.
- How to prioritize between the new scoring mechanism and the existing preemption mechanism. 
  - What if the workload is higher priority based on DRS, but the new scoring mechanism says that the workload is lower priority?
  - What if workload A has a higher cost and B has a lower cost, but workload A is consuming borrowed quotas, and B is consuming a nominal quota?
  - etc...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T02:39:52Z

> > I think a good referential example would be a controller that increases the preemption cost for every preemption that already happened.
> 
> To be clear, I'm specifically talking about this ^ usecase: preempting jobB increases a preemption cost of jobB immediately, which may allow jobB to preempt jobA. However, Kueue cannot simulate that by itself, unless somehow involving the external controller.

Right, this could happen. So, I think that we probably need to introduce a lock time, which means the workload cost can not be changed during a fixed time if we want to allow drastic changes in cost based on preemptions. Or we might be able to just ignore admitted workloads recently when the Kueue selects preemptees. Anyway, we might need to have some safety mechanisms.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-03T03:44:29Z

> Avoid introducing batch users facing API (like annotation) since the evil users can exploit this mechanism so that their Job has never been preempted by others. The workload API field would be better.

+1

> What if the workload is higher priority based on DRS, but the new scoring mechanism says that the workload is lower priority?

Does a fair sharing consider a priority today? IIUC, a job can preempt other high-priority jobs on a different CQ if that's necessary for a fair sharing, right?
My core idea is `<WorkloadPriority.value> + <preemption cost>` that I mentioned at first. That means basically the preemption cost just influences the priority value, which means the cost can do what priorities can do (and cannot do what priorities cannot do) 

> What if workload A has a higher cost and B has a lower cost, but workload A is consuming borrowed quotas, and B is consuming a nominal quota?

So, ditto here: it should behave the same as if today workloadA has a higher priority and B have a lower priority. That's my mental model here.

> So, I think that we probably need to introduce a lock time, which means the workload cost can not be changed during a fixed time if we want to allow drastic changes in cost based on preemptions. 

No, I do not agree. The costs can be changed frequently and hugely based on job's phase. Your idea would make a new risk that jobA has a low cost right now, users need to increase the cost for some reason but cannot due to this lock time, and jobA ends up being preempted although it shouldn't.
So, IMO, we should allow the costs to be changed as frequent as users want, and we can just say it's a responsibility for users to avoid this kind of preemption flapping on their controller implementation. And, I'm talking about how we should implement the referential example controller to avoid this problem. 

> Or we might be able to just ignore admitted workloads recently when the Kueue selects preemptees. Anyway, we might need to have some safety mechanisms.

Yup, it might be nicer as a safe guard.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-03T03:55:55Z

EDIT: I meant to say `<WorkloadPriority.value> + <preemption cost>` 🙃 (the higher cost it is, the less probability a job should be preempted)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-03T04:16:21Z

> > What if the workload is higher priority based on DRS, but the new scoring mechanism says that the workload is lower priority?
> 
> Does a fair sharing consider a priority today? IIUC, a job can preempt other high-priority jobs on a different CQ if that's necessary for a fair sharing, right?
> My core idea is <WorkloadPriority.value> + <preemption cost> that I mentioned at first. That means basically the preemption cost just influences the priority value, which means the cost can do what priorities can do (and cannot do what priorities cannot do)

AFAIK, priorities are considered regardless of fair sharing to evaluate if the situation satisfies preemptionPolicy. IIUC, if we specify the Always preemption policy, the priority will not be considered. So the primary problem is the situation for preemptionPolicy × fairSharing × preemption cost.

> > What if workload A has a higher cost and B has a lower cost, but workload A is consuming borrowed quotas, and B is consuming a nominal quota?
> 
> So, ditto here: it should behave the same as if today workloadA has a higher priority and B have a lower priority. That's my mental model here.

Yes, kueue considers whether or not the workload consumes nominal quota or borrowed quota when it computes DRS.
So, AFAIK, mentioned conflict situation could happen.

> > So, I think that we probably need to introduce a lock time, which means the workload cost can not be changed during a fixed time if we want to allow drastic changes in cost based on preemptions.
> 
> No, I do not agree. The costs can be changed frequently and hugely based on job's phase. Your idea would make a new risk that jobA has a low cost right now, users need to increase the cost for some reason but cannot due to this lock time, and jobA ends up being preempted although it shouldn't.
> So, IMO, we should allow the costs to be changed as frequent as users want, and we can just say it's a responsibility for users to avoid this kind of preemption flapping on their controller implementation. And, I'm talking about how we should implement the referential example controller to avoid this problem.

That sounds reasonable. The cost changes should be allowed, but we might need to consider ignoring the recently admitted workloads for the preemptee, as I mentioned.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-12-03T04:30:33Z

Can we just say preemptionPolicy is applied for `<WorkloadPriority.value> + <preemption cost>` then? So, we would change a definition of "priority" essentially: Today "priority" equals WorkloadPriority.value, but if a workload has a cost, priority would be `<WorkloadPriority.value> + <preemption cost>`. Then, e.g., `LowerPriority` would be applied a workload's priority+cost is lower.

If we say that's not straightforward for users, I can even propose we can name the cost differently, maybe like `RuntimePriority`, to make it clearer to express this is also yet-another priority that Kueue considers during the preemption.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:52:36Z

/priority important-soon

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-12T17:05:38Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T17:08:14Z

This requires still some design as a KEP, would you like to take that Vlad? Otherwise I was going to take that in the near future

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-12T17:24:53Z

Yes, ptal at [KEP](https://github.com/kubernetes-sigs/kueue/pull/8551)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T17:26:54Z

Thank you, I will review tomorrow that

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T10:52:32Z

@sanposhiho @tenzen-y thank you for the discussion! 

As we already have a KEP I want to summarize and consider open questions:

Summary for "closed questions":
1. the new formula for the "effective priority" makes sense as  `workload.priority + preemptionCost` makes perfect sense to me, as in comment https://github.com/kubernetes-sigs/kueue/issues/7990#issuecomment-3604986036
2. I would also stay away from the "preemptionCost" to impacting DRS in subtle ways, just use it for what "priority" is currently used for - ordering within CQ
3. We can stay with the annotation at the Workload level for Alpha, and re-consider Job level for the future.

Open question about the scope of the new annotation:
1. "effective priority for preemption candidate ordering" (original intention of the Issue)
2. "effective priority for scheduling & preemption" 

I think both are technically possible, but (1.) seems to match better the name and original intention. If we are going to go with (2.) we probably need to name the annotation differently to make that clear, maybe `kueue.x-k8s.io/priority-boost`, to influece the "effective priority" as  `workload.priority + priority-boost`. 

Myself I'm leaning to (1.) , because I think option (2.) may cause a lot of chaos if the controller has a bug, and potentially infinite preemption loops. Option (1.) seems like much safer - I don't see  here a risk for infinite preemption loops.

Let me know folks here, or under the KEP.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-11T10:25:17Z

Glad to see the progress! 

> Open question about the scope of the new annotation:

This is the difficult point. 

On k/k side, https://github.com/kubernetes/enhancements/pull/5711 _was_ going to implement workload's `PreemptionPriority` that only impacts the preemption (i.e., similar to (1)), but we dropped it, at least from the first scope. See [this comment of mine](https://github.com/kubernetes/enhancements/pull/5711#discussion_r2661846978) about that, which made us drop it. So, I actually would suggest (2) `priority-boost` for the same reason I argued there. But, I'm not an expert on Kueue side, so I'd defer to you and the team about the final decision.

Maybe you can also check what @wojtek-t was thinking about that there. He might have some more insights in his mind that made him propose `PreemptionPriority` first.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-11T10:36:59Z

One important point - If you end up choosing (1), you need to think how to prevent a preempted job from preempting back a preemptor job.
For that, I think `preemption-cost` has to be limited to a positive value, similar to what the KEP originally proposed with `PreemptionPriority` -
> So address that we will extend additional the `Priority` admission plugin to validate that
`spec.Priority <= spec.PreemptionPriority`.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T18:14:08Z

> One important point - If you end up choosing (1), you need to think how to prevent a preempted job from preempting back a preemptor job.

Hm, maybe we have some other view on (1.) In my understanding of the option we wouldn't touch the priorities for scheduling - the `set` of candidates would not be changed, just the ordered `list` of them.

So, if `JobA` is preempting it can choose to order `JobB` and `JobC` according to the adjusted `preemptionCost`. However, it will not be able to preempt `JobD` regardless of the `preemptionCost`. That ability to preempt `JobD`, making it a "candidate" is only dependent on the "priorities".

So in my understanding of the options, it is rather a concern for `priority-boost` which would go beyond just ordering of candidates.

IIUC your comment in k/k you are rather looking for something like `priority-boost` which could impact the priority of both scheduling and preemption. 

If this is the case I think we could:
1. implement in Alpha both, because they are both implementation-wide easy, and 
2. pick to adopt to Beta based on real world adoption, for example by your organization
3. I think we would just not allow them to set them both at the same time - this would be too confusing to users.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-11T20:26:52Z

Please help me understand what's the diff between boost and cost, since formula is basically the same:
`workload.priority + preemptionCost` /  `workload.priority + priority-boost`

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-12T01:00:19Z

> That ability to preempt JobD, making it a "candidate" is only dependent on the "priorities".

Yeah, we're on different assumptions then apparently. I thought both `cost` and `boost` are taken into consideration not only when ordering the victim candidates, but also when deciding the victim candidates too. I thought the difference between `cost` and boost` are just whether it's added to the workload priority value when it's victim pods vs it's used all the time when the workload priority is used anyhow.

IMHO, `boost` is still better and simpler. Because, let's say your `high` priority job preempt `medium` instead of `low` job because of the high cost put on `low`: If we go with the `cost` idea, this preempted `medium` job will preempt `low` immediately, because `making it a "candidate" is only dependent on the "priorities"` i.e., `low` jobs will be candidate of the preemption for `medium` jobs, regardless of how big the cost is. That doesn't make sense.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T06:59:26Z

> If we go with the cost idea, this preempted medium job will preempt low immediately, because making it a "candidate" is only dependent on the "priorities" i.e., low jobs will be candidate of the preemption for medium jobs, regardless of how big the cost is. That doesn't make sense.

Correct, but only assuming that the cost is allowing to cross boundaries between priority classes, that is greater than one. We could use fractional costs using eesourceQuantity, to say "100m".  Then effectively would be the tie breaker for preemption candidates which does not impact other scheduling decisions, which read as the original motivation for the issue. Maybe @mwysokin could clarify.

Do you think the preemption cost mechanism just as a tie breaker does not have an appeal?

I noted your comment about priority-boost.

I'm leaning in Alpha to implement both approaches and in graduation criteria decide which we graduate and which drop, WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T07:01:03Z

> Please help me understand what's the diff between boost and cost, since formula is basically the same:
> `workload.priority + preemptionCost` /  `workload.priority + priority-boost`

the difference is not about formula, but semantics - the scope of operation of the adjusted priorities. As I mentioned before, one option is to influence all scheduling decisions with the 'priority-boost', another is just to tie-break preemption candidates.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-14T09:50:55Z

> Do you think the preemption cost mechanism just as a tie breaker does not have an appeal?

For us, I do think we could want crossing the boundaries between priority classes. That's the intent behind the fomula workload.priority + preemptionCost. (if not, I wouldn't use this formula because it doesn't make any difference adding priority because it doesn't cross the boundaries, i.e., `+priority` just adds the same value to everyone when comparing)
Use case is like, if some `low` priority jobs are preempted too frequently by `medium` and `high` jobs and haven't made any progress for a too long time, we might want to prioritize it over `medium` jobs. If cost wouldn't allow us to cross the boundary, nothing would change by the cost; they will keep being preempted by `medium` jobs, even with a big cost value.

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-14T09:52:07Z

> I'm leaning in Alpha to implement both approaches and in graduation criteria decide which we graduate and which drop, WDYT?

But, of course, I'm fine both to be implemented. Up to the Kueue team.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T10:01:44Z

@sanposhiho Thank you for the input, let me follow up on some remaining topics.

> But, of course, I'm fine both to be implemented. Up to the Kueue team.

We will re-evaluate the need for the "preemption cost when finding preemption candidates". Input from @mwysokin and other community members will be valuable here.

> For us, I do think we could want crossing the boundaries between priority classes. 

As you prefer using "preemption-boost" let me ask some clarifying questions: why the need for "preemption-boost" annotation, since the priority class label  `kueue.x-k8s.io/priority-class` is mutable? Essentially, setting `priority-boost` mutates the effective priority. 

These are the reasons I could see to justify the `priority-boost`:
1. visibility to the user and the external controller that the priority is boosted, otherwise the controller may try to do this multiple times (because it doesn't see it was already boosted)
2. allow to boost priorities out of pre-defined classes of priorities, say you have "low=100", "mid=200", "high=300". With the "priority-boost" you can easily achieve high granularity like "150" or "156", without creating a zoo of priority classes
3. convenience, the controller needs to only operate on the Kueue's Workload API, otherwise it would need to operate on different Kinds of schedulable objects (Jobs, JobSets, Deployments, etc).

Can you confirm we are on the same page for the reasons of why to introduce the "priority-boost" vs mutating priorities by the `kueue.x-k8s.io/priority-class` label?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T13:42:50Z

cc @mwysokin @sanposhiho wdyt about the conclusion to introduce "priority-boost" which impacts the "effective workload priority" and about the motivation about it: https://github.com/kubernetes-sigs/kueue/issues/7990#issuecomment-3907539679

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-02-18T08:30:02Z

`boost` will be convenient for us exactly because of (1) + (2) that you shared.
If we don't have boost and just mutate the priority, I need to prepare a lot of additional priority classes. e.g., `high/just-after-checkpoint-ok-to-get-preempted`, `low/preempted-a-lot--lets-prioritize-it-more-than-other-low`, `low/preempted-too-much--lets-prioritize-it-even-more-than-medium`... and each of them have to be created per the original priority classes (low, medium, high, and potentially more in the future). The more jobset stages we want to have to influence the priority, the more we need to create the priority classes. ...Yes, that's technically possible, but that doesn't look clean.
Basically, I would love to & it looks the cleanest for me to manage the states of jobs and hence the priority boost separately from the original priority classes.

That also allows us to expand it further / more complex in the future; e.g., if a `medium` job is preempted a lot (result in the boost to increase), but also it's crashed a lot (result in the boost to decrease), our controller might be able to do a math and put the boost number dynamically based on those two factors. like, if we want to boost +100 on jobs that have preempted a lot and want to boost -50 on jobs that have crashed a lot, then the controller would put +50 after all for this job. That is almost impossible to do just with the priority annotation.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2026-02-18T13:27:24Z

SGTM 🖖 I think it's slightly something else than I originally had in mind but if it works and meets the expectations I'm fine with changing the scope slightly. It'd be awesome if @amy @varunsyal or @ichekrygin could chime in whether the new solution would meet their expectations too as we discussed it at some point.

### Comment by [@amy](https://github.com/amy) — 2026-02-19T23:05:22Z

Remind me if there was more specific user scenarios. Refreshing my memory on past discussions. One that I remember is... because of the way DRS values work, we can have situations where 1 large workload in CQ-A could lose against 1 small workload in CQ-B. So this is a way to boost the importance / "cost of preemption" for the larger workload with similar DRS value. (for some definition of "similar")

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-20T08:49:24Z

> Remind me if there was more specific user scenarios. Refreshing my memory on past discussions. One that I remember is... because of the way DRS values work, we can have situations where 1 large workload in CQ-A could lose against 1 small workload in CQ-B. So this is a way to boost the importance / "cost of preemption" for the larger workload with similar DRS value. (for some definition of "similar")

Oh, if we are talking FairSharing and DRS this is much more complex, because ignoring Workload priority across CQs is a fundamental design decision for [FairSharing](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1714-fair-sharing).

So while the use cases look similar on the surface, I think there is a fundamental difference between priority-boost within CQ, and amending of DRS calculation, as mentioned by @sanposhiho in the [comment](https://github.com/kubernetes-sigs/kueue/issues/7990#issuecomment-3604947243): `My core idea is <WorkloadPriority.value> + <preemption cost> that I mentioned at first. That means basically the preemption cost just influences the priority value, which means the cost can do what priorities can do (and cannot do what priorities cannot do)`. 

Now, having said that I can totally understand the motivation for boosting workloads within FairSharing across ClusterQueues. One idea I'm thinking about tackling this challenge is to somehow mix the priorities into the DRS calculation, or by scoping DRS calculation within the same priority levels. Once we incorporate the priorities into FairSharing, then the same priority-boost annotation should work. However, I feel a separate design is needed here, and probably long discussion.

Wdyt @amy @mwysokin ? Maybe we should open a dedicated issue to track boosting priorities for FairSharing to de-couple a little bit - the discussion here is already very long and hard to catch up.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2026-02-23T10:15:18Z

Maybe we could do it as a follow up at some point? I'd focus on delivering what we already have a pretty good understanding of and if there's a KEP or KEP modification to extend this behavior as deep as to the DRS level it could potentially have even bigger impact but maybe let's leave it for milestone 2? @amy WDYT? I think the feature in its current form will already have some value.

### Comment by [@amy](https://github.com/amy) — 2026-02-24T19:09:07Z

LGTM, yeah don't want to block progress!

### Comment by [@lukasmrtvy](https://github.com/lukasmrtvy) — 2026-02-28T07:26:18Z

Hi 👋 referencing this https://github.com/kubernetes-sigs/kueue/issues/9596 for visibility

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T02:38:21Z

> > Remind me if there was more specific user scenarios. Refreshing my memory on past discussions. One that I remember is... because of the way DRS values work, we can have situations where 1 large workload in CQ-A could lose against 1 small workload in CQ-B. So this is a way to boost the importance / "cost of preemption" for the larger workload with similar DRS value. (for some definition of "similar")
> 
> Oh, if we are talking FairSharing and DRS this is much more complex, because ignoring Workload priority across CQs is a fundamental design decision for [FairSharing](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1714-fair-sharing).
> 
> So while the use cases look similar on the surface, I think there is a fundamental difference between priority-boost within CQ, and amending of DRS calculation, as mentioned by [@sanposhiho](https://github.com/sanposhiho) in the [comment](https://github.com/kubernetes-sigs/kueue/issues/7990#issuecomment-3604947243): `My core idea is <WorkloadPriority.value> + <preemption cost> that I mentioned at first. That means basically the preemption cost just influences the priority value, which means the cost can do what priorities can do (and cannot do what priorities cannot do)`.
> 
> Now, having said that I can totally understand the motivation for boosting workloads within FairSharing across ClusterQueues. One idea I'm thinking about tackling this challenge is to somehow mix the priorities into the DRS calculation, or by scoping DRS calculation within the same priority levels. Once we incorporate the priorities into FairSharing, then the same priority-boost annotation should work. However, I feel a separate design is needed here, and probably long discussion.
> 
> Wdyt [@amy](https://github.com/amy) [@mwysokin](https://github.com/mwysokin) ? Maybe we should open a dedicated issue to track boosting priorities for FairSharing to de-couple a little bit - the discussion here is already very long and hard to catch up.

That sounds typical large workload starvation problem in fair sharing. So, I fully agree with @amy use cases.
OTOH, I also agree with @mimowo 's proposal that we will handle this FS scheduling problem as another enhancement proposal.
