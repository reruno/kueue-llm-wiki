# Issue #3211: Admission Check controller to verify node capacity before admitting workloads

**Summary**: Admission Check controller to verify node capacity before admitting workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3211

**Last updated**: 2025-04-07T07:45:35Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@varshaprasad96](https://github.com/varshaprasad96)
- **Created**: 2024-10-10T02:14:22Z
- **Updated**: 2025-04-07T07:45:35Z
- **Closed**: 2025-04-06T17:39:25Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 22

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to use an Admission Check Controller which admits a job only if there is at least 1 Node with enough available resources to support the execution of the workload without oversubscribing the node. This admission check could be made optional. 

**Why is this needed**:
Kueue does not check if there are nodes with enough available resources for incoming workloads by default and that can lead to Kueue jobs taking up resources from the ClusterQueue even though they cannot actually run on the cluster. The proposed Admission Check Controller could help increase the hardware utilization by only admitting workloads that actually have a chance to schedule on a Node.
Here is an example scenario that motivates the use of the proposed AdmissionCheck Controller:
- System = 4 nodes with 4 cores each
- ClusterQueue with a quota of 8 cores
- There are some DaemonSets running on the cluster without interacting with Kueue at all. They currently consume 1 core on each node.
- There are some existing Kueue jobs taking up 4 cores out of the Quota of 8 cores.
The current system capacity is:
- Node 0 → 2/4 cores available
- Node 1 → 2/4 cores available
- Node 2 → 2/4 cores available
- Node 3 → 2/4 cores available

At this point a user creates a new workload for a Job for a single Pod that requests 3 Cores.

Currently, Kueue will admit this workload because the available capacity of the ClusterQueue is 4 cores which is greater than the CPU request of the Job. However, there are no nodes which have enough available cores for this workload.

Even though pod preemption is a possibility by the kube scheduler, the user would typically not like to change the order of execution after submitting workloads. This ACC would serve as a guard rail to ensure that.

**Completion requirements**:

This enhancement requires the following artifacts:

- [X] Design doc
- [ ] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-10T02:16:14Z

cc: @VassilisVassiliadis @srikumar003

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-10T05:22:52Z

This looks very similar to what we do in [Topology Aware Scheduling](https://github.com/kubernetes-sigs/kueue/issues/2724). IIUC this could be a special case for a topology with a single level corresponding to an individual pod (the hostname label). PTAL and let us know if there are some relevant differences / gaps.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2024-10-11T11:36:38Z

Thank you @mimowo , we'll take a look at the KEP and let you know.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T12:44:54Z

> This looks very similar to what we do in [Topology Aware Scheduling](https://github.com/kubernetes-sigs/kueue/issues/2724). IIUC this could be a special case for a topology with a single level corresponding to an individual pod (the hostname label). PTAL and let us know if there are some relevant differences / gaps.

Only my concern for expanding and extending the TAS feature is the fact that the TAS depends on the PodSchedulingGates.
While depending on the PodSchedulingGate, Kueue with TAS can not work with MultiKueue.

So, before extending the TAS feature or beta graduation, I would like to seek another solution instead of PodSchedulingGates.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2024-11-04T12:58:17Z

After going through https://github.com/kubernetes-sigs/kueue/issues/2724 and its KEP PR https://github.com/kubernetes-sigs/kueue/pull/2725 we think that Topology Aware Scheduling (TAS) could be used to offer a similar functionality to the proposed AdmissionCheck controller. There is a small difference which depending on the use case can be insignificant. My interpretation of TAS is that it aims to control where the workload pods are placed so as to improve some metric (e.g. throughput due to increased bandwidth between the pods as opposed to scheduling pods on distant nodes).

Our proposed AdmissionCheck controller doesn't necessarily decide where the pods should be placed. It aims to increase the resource utilization of a cluster by way of rejecting the creation of pods which simply cannot be scheduled on any available node and thus increasing the chances that the quota of a ClusterQueue is reserved for workloads which have a chance of getting scheduled on some node that the Kubernetes scheduler (or other scheduler) decides.

Without delving into too many implementation details we were thinking of the following this 3-step algorithm:

1. the AdmissionCheck controller has an understanding of the available resource capacity of nodes (this is something that TAS is also doing https://github.com/mimowo/kueue/tree/2ab5bb3a6b0af6be4fe11e2d36a06b8c43e105fa/keps/2724-topology-aware-schedling#computing-the-assignment)
2. on an incoming workload, it decides whether its pod(s) could fit onto the available nodes. If that's the case it admits the workload
3. when the pod(s) get scheduled on some node(s) (even if those node(s) are other than the ones that the AdmissionCheck controller computed the workload could be scheduled on), it updates its internal view of the available capacity of nodes

We could extend this basic algorithm by propagating the scheduling decisions of the controller to the Kubernetes scheduler but that could be an optional action, perhaps controlled by some kind of flag.

What we find interesting is that this slight difference effectively means that our proposed AdmissionCheck controller is simpler than TAS. There's also a bit of overlap between the 2 proposals: figuring out the allocatable capacity of nodes. We're thinking that we could use our proposed AdmissionCheck controller as a way of figuring out a good-enough recipe to compute the available allocatable resources of nodes which TAS could re-use down the line.

Another way to describe the proposed AdmissionCheck controller is that it provides similar functionality to the existing provisioning check admission controller (https://github.com/kubernetes-sigs/kueue/tree/main/pkg/controller/admissionchecks/provisioning). Except this new admission controller will use an alternate (simpler) mechanism to track available capacity and not assume that a cluster autoscaler is enabled. 

So to summarize, we're proposing that we contribute the proposed AdmissionCheck controller under the experimental controllers (in path: https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental). We're planning on architecting the solution in a way that it doesn't have any assumptions about optional cluster features and that other solutions could make use of the code we implement (e.g. TAS).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T21:14:49Z

It looks like you are trying to provide the functionality the same as the cluster-autoscale, but the solution is different.
As a basic principle, we do not implement the same functionality as other core kube components as we described in the following:

> A core design principle for Kueue is to avoid duplicating mature functionality in Kubernetes components and well-established third-party controllers. Autoscaling, pod-to-node scheduling and job lifecycle management are the responsibility of cluster-autoscaler, kube-scheduler and kube-controller-manager, respectively. Advanced admission control can be delegated to controllers such as gatekeeper.

https://kueue.sigs.k8s.io/docs/overview/#why-use-kueue

TAS is accepted since the cluster-autoscaler and kube-scheduler can not decide the scheduling Nodes based on the Quota as we described in https://github.com/mimowo/kueue/tree/2ab5bb3a6b0af6be4fe11e2d36a06b8c43e105fa/keps/2724-topology-aware-schedling#implement-it-in-clusterautoscaler-or-kube-scheduler

So, my root question is the reason why the existing components like kube-scheduler and cluster-autoscaler can not satisfy this feature.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T14:02:45Z

I see, so the new proposed AdmissionCheck is somewhere between TAS and check-capacity in CA:

differences with TAS:
- simpler (faster) scheduling than TAS
- compatible with other features (but TAS is also going to be in the future)
- does not support topology information for scheduling

differences with ProvReq check-capacity in CA:
- allows to run without CA
- would need to solve probably the same problems we solve for ProvReq as https://github.com/kubernetes-sigs/kueue/pull/3375

I think that while it is a valid point that differences exist and may matter for some use cases (for example for users who are ultra sensitive about scheduling time and cannot use TAS, or cannot use CA for some reason, what would it be?), these seem edge cases not enough to justify a new controller. 

Note that the controller seems easy at the surface, but when you need to deal with negative scenarios (like retries) then it becomes complex to maintain, as demonstrated by https://github.com/kubernetes-sigs/kueue/pull/3375. I believe sooner or later we would need to solve the analogous problems again. 

So, I'm leaning to support @tenzen-y PoV and stick to improving the two mechanisms we have.

### Comment by [@hy00nc](https://github.com/hy00nc) — 2024-11-06T04:55:55Z

> This looks very similar to what we do in [Topology Aware Scheduling](https://github.com/kubernetes-sigs/kueue/issues/2724). IIUC this could be a special case for a topology with a single level corresponding to an individual pod (the hostname label). PTAL and let us know if there are some relevant differences / gaps.

Hi @mimowo , I have been following up this issue to make pods in PyTorchJob/MPIJob to be scheduled only when there are nodes with sufficient capacity. As you mentioned above, I tested TAS released in v0.9.0 with this single level topology and noticed that for PyTorchJob/MPIJob (possibly also the others that have multiple pods), this topology configurations applies to all the pods within the job. That said, if we use single level topology with hostname label to PyTorchJob/MPIJob, unless there is a node that can schedule all the pods in the job, it will not be admitted.

Is there a plan to extend TAS to handle this scenario? Thank you very much.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T05:45:37Z

@hy00nc thank you for being one of the early testers or TAS. 

I think what is want is already achievable if you use the 'preferred' annotation on your PodSet. Then TAS will try to fit them all on a single node, but if not possible it will try to optimize the number of nodes used. It may also be helpful for you to have a deeper topology with the lowest level being a node . Please also consult the new docs we have for TAS.

Let me know if this helps or you encounter more issues, or I didn't exactly understand your use case.

### Comment by [@hy00nc](https://github.com/hy00nc) — 2024-11-06T05:56:32Z

@mimowo , thank you for the quick response!

> I think what is want is already achievable if you use the 'preferred' annotation on your PodSet.

If done with 'preferred' I think that means even if the node does not have sufficient capacity to schedule a pod, it will be admitted, which doesn't seem to align with the original purpose? The original intention is to never let pod be admitted if there is no node that can schedule it. For example, there are two nodes with 4 GPUs each, but a pod is requesting 8 GPUs. With normal Kueue setup, this pod is admitted because we have sufficient quota but will never get scheduled. This is the problem that we want to solve.

> It may also be helpful for you to have a deeper topology with the lowest level being a node .

I also tried this, however this also does not meet the original intention because even if we meet the higher level of topology (e.g. topology-rack), this doesn't mean there is a node that can schedule a pod because capacity is summed up for the higher topology nodes which doesn't necessarily reflect the actual individual node capacity. Only the hostname topology seems to be able to do this.. 

Please let me know if I'm missing something.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T06:15:31Z

"preferred" still means you need to have enough capacity, it just means that multiple nodes can be used (but their number will remain optimized). TAS operates on pod counts more than on just additive capacity, So, in your example Kueue would see 0 pods fits in Node1, and 0 pods fits in Node2, and thus it sees 0 pods can fit on Node1+Node2. So it would not admit the workload.

More precisely the setup I mean (based on the example in [docs](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#example)):
```yaml
 levels:
  - nodeLabel: "cloud.provider.com/topology-block"
  - nodeLabel: "cloud.provider.com/topology-rack"
  - nodeLabel: "kubernetes.io/hostname"
```
Then, the user sends the workload using `kueue.x-k8s.io/podset-preferred-topology: kubernetes.io/hostname`.

If this works we definitely need to improve documentation.

### Comment by [@hy00nc](https://github.com/hy00nc) — 2024-11-06T07:34:59Z

> "preferred" still means you need to have enough capacity, it just means that multiple nodes can be used (but their number will remain optimized)

I see, thanks for the clarification. I think I misunderstood the term empirically by the tests I conducted using PyTorchJob which looks to have a bug in the integration with TAS.

Just to describe here shortly, when the cluster queue has no workloads at all, I could see that pods still go to different hosts even when using `kueue.x-k8s.io/podset-preferred-topology: kubernetes.io/hostname` using PyTorchJob. However, if there are already scheduled pods (by TAS) in the cluster queue, it looks to have trouble calculating the resources available.

I can't bring specific manifests for some reason, but I could see event when I describe the PyTorchJob workload (2 worker pods with 4 GPUs each, and there are nodes in cluster each having 4 GPUs left) which is not correct:
`Warning  Pending  49s (x2 over 49s)  kueue-admission  couldn't assign flavors to pod set worker: topology "default" allows to fit only -3 out of 2 pod(s)`

I also see some ungating bug in MPIJob integration.. It'd be good for me to create an issue but I'm afraid I can't raise specific issues in Github at the moment..

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T07:45:08Z

Cool, this -3 is obviously a bug. I will try to repro and fix for 0.9.1, but in the meanwhile any additional repro steps will be very helpful for us. Is this just a bad logging or you think the workloads should get admitted?

Same for the ungatibg bug. Any details you can share would be greatly useful and could shorten the time for fixes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T08:38:12Z

> > "preferred" still means you need to have enough capacity, it just means that multiple nodes can be used (but their number will remain optimized)
> 
> I see, thanks for the clarification. I think I misunderstood the term empirically by the tests I conducted using PyTorchJob which looks to have a bug in the integration with TAS.
> 
> Just to describe here shortly, when the cluster queue has no workloads at all, I could see that pods still go to different hosts even when using `kueue.x-k8s.io/podset-preferred-topology: kubernetes.io/hostname` using PyTorchJob. However, if there are already scheduled pods (by TAS) in the cluster queue, it looks to have trouble calculating the resources available.
> 
> I can't bring specific manifests for some reason, but I could see event when I describe the PyTorchJob workload (2 worker pods with 4 GPUs each, and there are nodes in cluster each having 4 GPUs left) which is not correct: `Warning Pending 49s (x2 over 49s) kueue-admission couldn't assign flavors to pod set worker: topology "default" allows to fit only -3 out of 2 pod(s)`
> 
> I also see some ungating bug in MPIJob integration.. It'd be good for me to create an issue but I'm afraid I can't raise specific issues in Github at the moment..

Could you open another issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T13:55:25Z

+1 for opening an issue

I understand the full yamls might be confidential, but you could probably share some of the most important bits of information for repro:
- size of the Job and PodSets
- resources used
- user-observable scenario which indicates the problem (none of the pods are ungated? a subset if ungated? are they stuck ungating forever?
- log lines indicating the problem
- anything else I didn't think about but you see as useful to repro

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-07T15:09:43Z

Circling back to this point by @mimowo 
> I think that while it is a valid point that differences exist and may matter for some use cases (for example for users who are ultra sensitive about scheduling time and cannot use TAS, or cannot use CA for some reason, what would it be?), these seem edge cases not enough to justify a new controller.

As open source developers, we tend to think "just upgrade to the new version that has the feature you want".  But the reality of production use is quite different.  The CA feature that is needed (the `check-capacity.autoscaling.x-k8s.io` provisioningClassName) requires Kubernetes 1.30.1 or better as I understand it.  OpenShift 4.16 is based on Kubernetes 1.29 and will be supported through mid 2026.  So CA is not an option for it.  

That leaves TAS, which may be able to fill the need even though it isn't really its intended design point.  But, features such as preemption and cohorts are also required and not yet supported by TAS.  TAS may also be overkill when the "topology" is totally flat (just nodes) and all that is desired is to prevent the churn/waste of useless admission of workloads that contain individual pods that can't possibly be scheduled because no node has the requested capacity.  Perhaps there is a simple version  where the TAS node monitoring controller is enabled, but there is a degenerate case "scheduling" that just does a capacity check on individual pods as an admission check and doesn't activate the whole pod gating machinery.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T15:41:41Z

Thank you for the summary. I totally understand the production reality where you need to support users on 1.29 whilst it is not yet supported by CA check-capacity.

In principle TAS should be enough in the degenerative single-level case, but making it compatible with preemption and cohorts is non-trivial and will take probably till Q2 2025.

So, I can see some options:
1. let you develop the AC in a separate repo from Kueue
2. make the new AC under experimental folder in Kueue

I would be leaning towards (2.) as this would also serve a role of an example of creating an external AC. 

It will also let us learn what are the obstacles when doing an external AC, and we could reference it in the docs, so win-win IMO.

In fact, we did it in the past for the very similar reasons we developed [Pod-integration based on taints and tolerations](https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental/podtaintstolerations) which was needed quickly for our users on 1.25 (IIRC, prior to the introduction of scheduling gates).

WDYT @tenzen-y ?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T16:09:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-07T17:05:57Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-06T17:39:21Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-06T17:39:26Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3211#issuecomment-2781527336):

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

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-04-07T07:45:34Z

We put together a prototype of this here: https://github.com/CarloGem/ACC-POConcept

The functionality of the controller is there. The missing bit is about integrating it with kueue (under the experimental folder) and gating the AdmissionController behind a feature flag.
