# Issue #6587: Wall time limits for ClusterQueues

**Summary**: Wall time limits for ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6587

**Last updated**: 2026-04-02T16:44:18Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-08-15T03:35:38Z
- **Updated**: 2026-04-02T16:44:18Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to add a way to specify ClusterQueues and set a limit on wall time.

It would be ideal to be able to limit wall time per resourceFlavor in the ClusterQueue. ClusterQueues will then track the usage of walltime.

```yaml
type ClusterQueueSpec struct {
...
        // wallTimePolicy defines the wallTimePolicy for the ClusterQueue.
        // +optional
        WallTimePolicy *WallTimePolicy `json:"wallTimePolicy,omitempty"`
}
...
type WallTimePolicy struct {
        // WallTimeFlavors describes a group of resources that this wall time limits applies to.
        // flavors is the list of flavors that provide the resources of this group.
        // Typically, different flavors represent different hardware models
        // (e.g., gpu models, cpu architectures) or pricing models (on-demand vs spot
        // cpus).
        // Each flavor MUST list all the resources listed for this group in the same
        // order as the .resources field.
        // The list cannot be empty and it can contain up to 16 flavors.
        // +listType=map
        // +listMapKey=name
        // +kubebuilder:validation:MinItems=1
        // +kubebuilder:validation:MaxItems=16
        WallTimeFlavors []WallTimeFlavor `json:"wallTimeFlavors"`
}

type WallTimeFlavor struct {
        // name of this flavor. The name should match the .metadata.name of a
        // ResourceFlavor. If a matching ResourceFlavor does not exist, the
        // ClusterQueue will have an Active condition set to False.
        Name ResourceFlavorReference `json:"name"`

        // wallTimeAllocatedHours is the number of hours that this wall time quota applies to.
        // +kubebuilder:validation:Minimum=1
        WallTimeAllocatedHours int32 `json:"wallTimeAllocatedHours"`

        // actionWhenWallTimeExhausted defines the action to take when the budget is exhausted.
        // The possible values are:
        // +kubebuilder:validation:Enum=Hold;HoldAndDrain
        // +kubebuilder:default="Hold"
        ActionWhenWallTimeExhausted StopPolicy `json:"actionWhenWallTimeExhausted,omitempty"`
}

type ClusterQueueStatus struct{
...
        // wallTimeFlavorUsage contains the current wall time usage for this ClusterQueue.
        // +optional
        // +listType=map
        // +listMapKey=name
        // +kubebuilder:validation:MaxItems=16
        // +optional
        WallTimeFlavorUsage []WallTimeFlavorUsage `json:"wallTimeFlavorUsage,omitempty"`
}

type WallTimeFlavorUsage struct {
        // name of the flavor.
        Name ResourceFlavorReference `json:"name"`
        
        // wallTimeAllocated is the total number of hours allocated for this ClusterQueue.
        // +kubebuilder:validation:Minimum=1
        WallTimeAllocated int32 `json:"wallTimeAllocated,omitempty"`
        // wallTimeUsed is the number of hours used.
        // +kubebuilder:validation:Minimum=1
        WallTimeUsed int32 `json:"wallTimeUsed"`
}       
```


**Why is this needed**:

A popular feature for HPC schedulers is to limit users by wall time. A researcher gets x amount of compute hours and they are free to use the resource how they want until their allotment is full. 


**Budget Similarity**:

This is similar to https://github.com/kubernetes-sigs/kueue/issues/28.

Generally, budgets are a hard concept to abstract as many organizations have different requirements. I wanted to focus on something a little simpler instead of budgets. 

In this proposal, I'd like to track the wall time usage per resource flavor and set a hard limit for that ClusterQueue. Organizations could refill their "budget" how they see fit but at least Kueue can track wall time usage at ClusterQueue level without too much organizational complexity.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-15T23:34:28Z

So does this affect both guarantees and borrowingLimits? So you hit walltime allotment, and your CQ usage for this flavor is shut off?

Whats the expected lifecycle behavior of this CQ/flavor? Finance gives the user new budget, does the admin then need to make a new CQ/Flavor/allotment concept with a fresh walltime allotment? 

(for sure interesting concept that seems useful)

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-16T17:09:58Z

> So does this affect both guarantees and borrowingLimits?

This is a good point. I'm not sure Cohorts make sense here as you would be borrowing from the same pool.

> So you hit walltime allotment, and your CQ usage for this flavor is shut off? Whats the expected lifecycle behavior of this CQ/flavor? Finance gives the user new budget, does the admin then need to make a new CQ/Flavor/allotment concept with a fresh walltime allotment?

I was thinking that when the allotment is over, there can be a policy to set StopPolicy for ClusterQueue to Hold or HoldAndDrain.

I think refreshing the allotment could  be done as an external controller (cron job that sets status of WallTimeUsage back to 0).

Or one can create new CQ.

What do you think? I can see refreshing based on a cron syntax (daily, weekly, monthly, yearly).

### Comment by [@amy](https://github.com/amy) — 2025-08-16T19:19:35Z

Sounds interesting! Probably want a combination of setting wallTimeUsage back to 0 and new CQs when you want the size of the allotments to change. So like: originally give a team an allotment with 10 GPUs. Then you realize after that expires, theres 2 teams that want allotments with 5GPUs. 

Something tricky which I assume most organizations that use Kueue have is... an external way to validate that the sum of the nominalQuota is <= cluster resources (ie general quota management). So if CQs are going to change often, they should just make sure that's pretty robust especially if there's an automated cron. 

In your description, I like that it seems like youre explicitly gating against this to be implemented within Kueue: "Team can use this quota starting on X future date". And that this should be external to Kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-18T10:56:08Z

@kannon92 Why not use Admission FairSharing?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-24T16:07:37Z

> [@kannon92](https://github.com/kannon92) Why not use Admission FairSharing?

Hmm. https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/

I don't think this exactly matches what I was thinking.

I wanted to start thinking about way to support Budgets but take a smaller step.

For AFS, is it possible to block the CQ if usage limit is exceeded? It looks like admission fair sharing prioritizes people who use less resources but it doesn't block admission once the usage limit has been exceeded.

### Comment by [@itsomri](https://github.com/itsomri) — 2025-09-16T10:39:50Z

IMO, it can be very useful for many use cases: either when budgeting expensive resources for research (i.e, department X in a university would like to reserve X GPU-hours needed for running experiments), or for recurring batch workloads (queues that run ETLs at known times, e.g a spark workloads starts at 02:00AM every day, uses 64 CPUs and is expected to have a 1h runtime)

Can you expand more on "ActionWhenWallTimeExhausted"? Ideally, there would be a way to not disrupt over-budget workloads if the resources are not in contention.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T15:19:19Z

> Can you expand more on "ActionWhenWallTimeExhausted"? Ideally, there would be a way to not disrupt over-budget workloads if the resources are not in contention.

That was my thought. I had options `Hold` and `HoldAndDrain` which just mean don't accept new workloads or remove existing workloads.

I was thinking there may be options that people want based on what happens if you exceed wall time limits.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T16:51:49Z

> A popular feature for HPC schedulers is to limit users by wall time. 

In the context of `WallTime` and flavors, what exactly represents the "user"? Is it intended to be tied to a namespace, a `LocalQueue`, or something else?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-18T16:57:06Z

Generally, I've heard that "users" in HPC could be a research group which researchers would share that time together.

But your point is valid. In Slurm I see that we can have partitions and user wall time limits.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-21T16:18:37Z

I don't have a fully functional POC yet but I drafted up the idea in a KEP.

https://github.com/kubernetes-sigs/kueue/pull/6933/commits/a70d89b3c98030a386cec42a27aa7a84b53f454e

### Comment by [@dubmarm](https://github.com/dubmarm) — 2025-09-27T00:48:20Z

HPC administrator here. I was directed to this discussion when I was trying to think of SLURM use cases vs Kueue.

From a SLURM / HPC use case coming into K8s, KUEUE's lack of WallTime holds back a key situation for management.

When I host a big computer, I let various groups / accounts / projects use the big computer. I do not allow unlimited access to each of these groups. I generally use Compute Hours to account for group access.

1 Compute Hour == 1 Node being used for 1 Hour

I mostly manage jobs by NODES. So 1 Job will have complete access to an entire compute node. Yes, some folks will run multiple user jobs on a single node, but I dont (things get messy if one user's code bleeds into the performance of other cores).

So in this discussion we see that I have a concept of 
1. User
2. Group
3. Node
4. Job
5. Hours

In k8s this is similar to:
1. User == RBAC
2. Group == RBAC
3. Node ~= Pod (one pod per computer, a pod cannot span multiple computers)
4. Job ~= Jobset
5. Hours == this discussion

If we can hash out this discussion then we are well on our way to using K8s similar to traditional SLURM batch processing.

Consider the following:
1. Run Job for 1hr and kill the job if it goes over time== [activeDeadlineSeconds](https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup)
2. Allocate 100hrs per year for Group == [PR](https://github.com/kubernetes-sigs/kueue/pull/6933/files#diff-1dc04bc1caa84e2eccfdd68ae8b34c4250f8f756fd3131721166326850c57ef8R31) for WallTime
3. Max Nodes Per User == [JobSet](https://github.com/kubernetes-sigs/jobset), a VAP or MAP requireing pods to specify a full node
4. Max Jobs Per User == Resource Quota on [object-count](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-on-object-count) based on jobset
5. Account has 1500 total hours == see `#2` - [PR](https://github.com/kubernetes-sigs/kueue/pull/6933/files#diff-1dc04bc1caa84e2eccfdd68ae8b34c4250f8f756fd3131721166326850c57ef8R31) for WallTime; use NameSpace or Queue for Account
6. Users are member of Account == RBAC for user for NameSpace `#5`
7. User resources can be overwritten from Account == Additional RBAC to allow User Overwrite from group; RBAC for user for NameSpace `#5`

The key thing to take away is Hour / Time management is big in Traditional HPC since in the early years the method of sharing a big expensive machine was through time management. (you get 1hr with the machine for this job, you can only use 100 hrs in a year for this project, your team members gets 1hr with the machine for this job but because I deem you special I will give you 5 hrs for the same job)

Time / Hours are a very common demoninator in HPC, this is a valid discussion.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-27T02:36:57Z

Thanks for that write up!

In your center, what do you do when people reach their wall time limits?

Do they go to a lower priority or you forbid submission?

And do you refill computer hours on a periodic basis?

### Comment by [@dubmarm](https://github.com/dubmarm) — 2025-09-28T03:26:24Z

In my facility, when people reach their limits its up to the discretion of me and my team (among principal investigators). The point is, time on a machine is fluid at an authoritive body's discrection.

Simply put, and this is for simplicity:
1. if they have 1hr left in their account and they schedule a 2hr job, it will fail to start
2. if they have 1hr left in their account and they schedule a 1hr job, it will run (assuming that was enough for the computation to complete otherwise the job will be turned off)
3. if the user / group / project needs more than 1hr, they kindly ask us or their superiors and we discuss whether this is feasible given other people's needs

I do refill hours, usually every fiscal year. I can add "credit hours" as ad-hoc if approved. I am the gate keeper of hours on my machine and its up to a few key-holder's agreement to direct me to provide them more time.

1. I'm the admin of the machine, when told I can reduce time an entity and when told I can offer more time to an entity
2. An entity is a User or Group or Research Project or Organization
3. Time on machine is how we communicate (1hr compute with 1 Compute Node = 1hr, 1hr compute with 24 Compute Nodes = 24hrs; we have a ledger balance in mariadb)
4. We require users to state how long they desire on the machine, if it finishes early they are billed for the time used. If they needed more time, the job will die at the pre-determined time.
5. We manage QOS groups where if you are member of Group == Short, you can only run for 2 Days. If you are a member of Group == Long, you can run for 7 days *example). Point is, time is divided into resource groups for convienence. These resource groups can also throttle other resources such as how many nodes to use or how many jobs/pods are allowed to exist at a given time, my prior post shows alternatives to these contraints but TIME is also a groupable resource much like NODES or JOB COUNTS.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-28T16:59:55Z

Do you require that all jobs must have a timelimit?

> We manage QOS groups where if you are member of Group == Short, you can only run for 2 Days. If you are a member of Group == Long, you can run for 7 days *example). Point is, time is divided into resource groups for convienence. These resource groups can also throttle other resources such as how many nodes to use or how many jobs/pods are allowed to exist at a given time, my prior post shows alternatives to these contraints but TIME is also a groupable resource much like NODES or JOB COUNTS.

I guess in this case someone submits to a certain group and a time limit is added.

And if the entity runs out of hours on an existing job, does your scheduler terminate the job?

### Comment by [@dubmarm](https://github.com/dubmarm) — 2025-09-29T17:44:23Z

Yes, a group will define your MAX RUN TIME ... but there is still the discussion of time between 0 AND MAX ( see below, this is a key concept in HPC )

Yes, the scheduler will terminate. 

==========
There is a lot to think about between 0 and MAX RUNTIME...

We require users to specifiy their job runtime when they submit a job. They have to do this even though their QOS technically has an uppper limit of runtime.

The reasoning for this is because we do "backfilling". What backfilling says, if a faster job can sneak into the cluster between two other jobs, then backfill.

Example:
Job 1: Running for 2 days (20 out 30 nodes)
Job 2: In Queue to run for 2 days (asking for 20 out of 30 nodes; in queue because not enough nodes are available at the moment.
Job 3: Requested for 5 hours (5 out of 30 nodes)

Job1 is running already. It's using 20 nodes of the cluster, so we only have 10 free for work for the next two days.

Job2 is stuck waiting until there are enough nodes available for it to run it's 2 day job, it's in a QUEUE

Job3 was submitted after Job2, but it only needs 5 nodes and a few hours and THEREFORE it can sneak ahead of Job2 and do it's quick compute on the un-untilized nodes. THIS CONCEPT IS CALLED BACKFILLING

Because of backfilling, we require users to define how LONG their job will run. If they get their estimate wrong, the scheduler will forcefully terminate the job. The job is forcefully terminated because we use backfilling, and their over running of estmated time isn't fair to other users. Likewise, it's an incentive to the user to know how long their job will run, because if they just request MAX TIME in their QOS than they may be stuck in queue waiting for enough nodes to be available.

We all compete for time. We have hard rules because we all have to share a machine.

### Comment by [@dubmarm](https://github.com/dubmarm) — 2025-09-30T18:46:25Z

Note: without backfilling, Job3 would be stuck waiting on Job2 to complete. You'd have an underutilized machine (20/30 nodes running) for 2 days on Job1 + 2 days on Job2 (4 days total at 66% utilization... i lost 33% of productivity!) and then the simple Job3 will get to run it's very simple job.

In order for backfilling to work you have to have assumptions. I ASSUME my job will take 5hrs. I ASSUME I will have jobs free at a specified time in the future (a waiter kicking guests out of tables because of they went over their resevation time). I ASSUME the strong hand of Time because we must all share a limited resource.

In order to have ASSUMPTIONS, we must have stead-fast rules to hold assumptions accountable. Hence, immediate termination of jobs should they go over estimate.

Philosophy: Is the stead-fast ideal? NO, sometimes the machine is under-utilized and so a stead-fast rule is silly (let the job go over estimate, I have the resources open now). But machines are binary, and it's a 0 or 1 in a flag on a config. The amount of time lost due to the false-case of under-utilized macines with stead-fast terminating jobs past estimate requires the administrator to ponder, "how long do my users wait in a QUEUE before their job is run". The wait time is discretionary to the Admin, perhaps hours of wait is okay and so the concern of stead-fast termination to under-utilization is good enough. To this point , these are FLAGS and CONFIGS with their own binary settings of True/False. So, we call this a compromise of the situation. I'd say, at a minimum we should endorse this general rule of functionality, but accept that fluidity of utilization on a machine is constant on a machine.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-30T18:54:04Z

A few areas I have been thinking through:

How does compute hours work with accelerators? If a node has 8 GPUs, do you just count the time running on the node?

And for HPC sites, do you compute hours the same if one uses GPUs or a CPU only job? In my days of HPC, I knew that a lot of scientic apps may not use GPUs (but this was 7 years ago)

Do you weight hours differently (ie count GPU hours more aggressively than cpu hours)?

### Comment by [@dubmarm](https://github.com/dubmarm) — 2025-09-30T19:03:15Z

When I think of resources I think of the hardware structure.

Node has Sockets, Sockets have CPUS ...
Node has PCI Slots, PCI Slots have GPUS ...

For SIMPLICITY, when someone asks for a workload on a NODE, they get THE ENTIRE NODE for that time. Whether they use the GPU is up to them, whether they use all the CPUs is up to them.

For reality, every site breaks their resources up differently. I cant speak for everyone. Stick to simplicity and you will be 90% there.

Another key term in HPC is "SHARING". I dont use SHARING because it has hurt me more than helped. Sharing says, if user1 is using 50% of computer1 ... why not have user2 use the other 50% of computer1. Yes, you can do this, yes other sites do this. I do not do this. I have had issues where user1's code can bog down all cores and impact user2's code (Kernel Panics, Out-Of-Memory, File-Locks, GPU resource locks, can all impact everyone else). Additionally, HPC jobs are very GEOMETRIC, we use concepts of MESH and GRID and VECTOR and it really really helps when fundamental elements are equal in size (same blocks in RAM, reduced networking, homogenous geometry). Its not fun to have 1 CORE on NODE1, 30 CORES on NODE2, and 15 CORES on NODE3... it is often better to have every NODE have the same CORE count ( or any other divisable resource for that matter). SO, you get a node and the entire node is yours. I will work with you to make sure you are getting the most out of my node, because what you dont use is keeping user2 from running, and I want to keep my machine processing.

We help users out with CPUs vs GPUs. For instance, we may have a QOS or Partition that has GPUs vs No-GPUs. So if a user knows they don't need to run their workload on GPUS we just have them assign their job to the CPU-Only QOS or Partition (symantics in names of QOS vs Partition; call it resource groups)

Likewise, we monitor our jobs all the time and if we find a user using 1 NODE but only 1 Core out of 48 on a Node... we will work with them to get the parallel actions to use all CORES. we desire for our nodes to melt, 100% Utilization is valued

IN this end, 1 HR on a GPU QOS is 1HR, and 1HR on a CPU QOS is 1HR...
HOWEVER, there aren't enough GPUS to go around (limited resource) and so, even though the billing of 1HR is the same as 1HR CPU ... you may be stuck in a QUEUE waiting on everyone else's GPU job to finish. So, it's an incentive to a user to know what workloads can be CPU vs GPU and to allocate their jobs to the right resources. JUST as it's important to know their job run-times so that they are not stuck in QUEUE due to backfilling.

I believe what you are pondering is the reconciliation of SHARING vs BACKFILLING in a node.

1. How do I share TIME on a machine?
   - have an account balance of time
   - time can be weighted based on fancy hardware used, but most likely 1HR on Node == 1HR
   - how strict am I with time enforcement? Do I hard kill their job, even if they only need 1 more minute? How do I know it was only 1 more minute?
2. How do I ensure one user is not held up by another user? (BACKFILLING)
3. How do I get maximum utilization out of my machine? (To do SHARING or not to do SHARING)
   - if a machine is using CPUs only, could I allocate GPUs to another user? (dangerous)
   - if a machine is using 50% CPUs, could I allocate 50% CPUs to another user? (less dangerous)
   - do I just accept that if a user asks for a NODE, it is theirs to slap around how they please for the next 1HR (least dangerous, not always utilized)
   - even if I do all the fancy work of maximum utilization, who's to say my machine wont be sleepy at sometime. What do I do then? SETI@HOME?


The point is, when we have to manage a machine. We come to compromises. These compromises are reflected in the 0's and 1's we choose in our configs. How many 0's and 1's we have available is up to the community. For this discussion, getting the simple Walltime concepts hashed do us 80-90% of circumstances which is a heck of a lot better than what's current there ... 0%.

So,
1. Can we associate Walltime with a User and/or Group and/or Project and/or Organization?
2. Can we overwrite Walltime based on hieracrchy? Group says 1HR, User says 10HR, use USER
3. Can we track a ledger of time? You started the year with 100HRs, you used 90HRs. I will only allow a 10HR or less job, unless an ADMIN adds more hours

Stretch goal:
1. Have concept of weights. Perhaps a GPU NODE == 2HRs and a CPU NODE == 1 hour (messy but I see why someone things like this, again, a queue speaks for itself... a queue is the actualization of Supply vs Demand)

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T15:59:26Z

TBH adding this at CQ was a bit harder than I thought.

I updated my POC to focus on LocalQueue setup as I figure out how to enable this.

So right now, my POC does the following:

- Workloads will track wall time usage if feature gate is enabled
- LocalQueue has a spec and status field for setting wall time limits on namespace queue resources
- Aiming to implement StopPolicy based on wall time being exhausted on local queue.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-03T16:16:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-02T16:44:14Z

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
