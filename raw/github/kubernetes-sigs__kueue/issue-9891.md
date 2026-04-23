# Issue #9891: Automatic scale-up for elastic jobs when cluster resources become available

**Summary**: Automatic scale-up for elastic jobs when cluster resources become available

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9891

**Last updated**: 2026-03-18T20:12:42Z

---

## Metadata

- **State**: open
- **Author**: [@tradeqvest](https://github.com/tradeqvest)
- **Created**: 2026-03-16T11:04:43Z
- **Updated**: 2026-03-18T20:12:42Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

Hello :wave: thanks for all the work on Kueue so far. I'd like to propose a feature and raise awareness again that this would be very helpful for our workloads. Thanks in advance for your insights and considerations.

**What would you like to be added**:

Elastic jobs (`ElasticJobsViaWorkloadSlices`) support dynamic scaling, but require an external actor to patch `spec.parallelism`. Kueue itself does not watch for freed resources and trigger scale-up.

Kueue should automatically increase the parallelism of an elastic job when idle quota becomes available in the ClusterQueue, up to a declared maximum.

A possible approach could use a new annotation like `kueue.x-k8s.io/max-parallelism` alongside `kueue.x-k8s.io/elastic-job: "true"`:

1. A job is submitted with `spec.parallelism: 4` and `kueue.x-k8s.io/max-parallelism: "64"`.
2. 4 GPUs are free. Kueue admits the job with `parallelism: 4`.
3. Later, 32 more GPUs become idle.
4. Kueue detects the freed quota and scales the job up to 36 via WorkloadSlices.
5. If a higher-priority workload arrives, Kueue can preempt some or all of the expanded pods.

This would eliminate the need to combine partial admission with elastic jobs, and remove the dependency on an external controller (KEDA, custom sidecar, manual patching) to trigger the scale-up.

**Why is this needed**:

We run embarrassingly parallel GPU batch jobs. These jobs are low-priority and designed to be preemptable by higher-priority gang-scheduled training jobs.

We want jobs to start with whatever GPU capacity is currently free and automatically grow as more becomes available. Today there are three options, none of which solve this:

1. **Partial admission** (`job-min-parallelism`): Job starts with available resources but cannot grow. Wastes idle cluster capacity for the remainder of its runtime.
2. **Elastic jobs** (`ElasticJobsViaWorkloadSlices`): Supports dynamic scaling but requires an external controller to trigger the parallelism change. Kueue does not watch for free resources. Also incompatible with partial admission.
3. **Plain Kubernetes**: The native scheduler handles elasticity and preemption, but jobs are invisible to Kueue's quota management and cannot be preempted by Kueue-managed workloads.

**Related issues and PRs and documentation**:

- https://github.com/kubernetes-sigs/kueue/issues/77 - Parent feature for dynamically sized jobs
- https://github.com/kubernetes-sigs/kueue/issues/1243 - frozen since Sep 2024 pending #77
- https://github.com/kubernetes-sigs/kueue/pull/5510 - Implements elastic scaling via WorkloadSlices
- https://github.com/kubernetes-sigs/kueue/issues/2964 - requested Kueue-native auto-scaling triggers, closed as `not_planned`
- https://github.com/kubernetes-sigs/kueue/issues/4927 - KEDA integration via Workload API scale subresource, closed as `not_planned`
- https://github.com/kubernetes-sigs/kueue/issues/9411 - Elastic JobSet support
- https://kueue.sigs.k8s.io/docs/concepts/elastic_workload/ - Elastic Workloads documentation

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T11:07:24Z

@tradeqvest you may want to check our work on RayJob where we already support autoscaling based on demand. In that case the autoscaling is delagated to the RayCluster capabilities. I agree it does not solve the issue for the k8s batch Jobs, but maybe it could already satisfy your needs

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T11:08:09Z

cc @hiboyang

### Comment by [@tradeqvest](https://github.com/tradeqvest) — 2026-03-16T11:14:40Z

Thanks for the pointer to `RayJob` autoscaling! Unfortunately our workloads are plain `batch/v1.Job` with `completionMode: Indexed` - each pod processes independent shards. Switching to `Ray` just for autoscaling would add significant complexity.

For batch Jobs, there is currently no equivalent of Ray's autoscaler to delegate to. Would Kueue consider supporting this natively for elastic batch Jobs, or is the expectation that users build an external controller to patch parallelism?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T11:23:40Z

We have not yet thought / discussed it so far, wg-batch community meeting would be a great place to discuss it: https://github.com/kubernetes/community/tree/master/wg-batch

Still, I would say it is rather outside of the core Kueue responsibilities, and rather a third-party controller, similarly as done for the RayJob. At the same time, we could consider, before there is the project, incubating it inside Kueue experimental directory, but I'm not yet bought on that.

### Comment by [@tradeqvest](https://github.com/tradeqvest) — 2026-03-16T16:26:32Z

I'd push back slightly on it being outside Kueue's core responsibilities. In my opinion, the primitives are already there - admission, preemption, re-queuing. In fact, you can approximate this today by submitting N independent workflows into the queue (one per data partition, effectively SIMD). Each gets admitted and preempted individually. It works, but it forces indexing overhead and coordination complexity onto the user that arguably belongs in Kueue: tracking partial progress across N quasi-independent jobs that are semantically one unit of work.

That said, happy to bring this to the wg-batch community meeting for a broader discussion.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-16T20:50:42Z

This could be another use case for #9792.

cc @VassilisVassiliadis 

In this case though, an external controller would need to read the cluster capacity and patch workloads. 

edit: I guess you want resizing as a Job is running. So maybe not the same.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-17T16:44:30Z

It sounds like what you want is Job to support HPA/Keda.

Seems very similar to https://github.com/kubernetes-sigs/kueue/issues/2964.

It was closed just because no one removed the lifecycle label not because there isn't interest.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2026-03-18T09:05:36Z

This is very interesting, I'd love to hear about it in a WG-Batch meeting as well!

### Comment by [@tradeqvest](https://github.com/tradeqvest) — 2026-03-18T19:57:18Z

Thanks @kannon92! Good to know #2964 was closed only due to the lifecycle bot.

I'm not fully an expert on KEDA, but from what I understand: HPA is demand-driven (scales on resource utilization like CPU/memory), KEDA is event-driven (scales on external signals like queue depth or custom metrics). Both react to workload demand in some form.

What we're after is capacity-driven - scale based on how much quota is free in the ClusterQueue. For our embarrassingly parallel batch Jobs the demand is always maximal, the only constraint is available cluster resources. Kueue already tracks this internally.

Please correct me if I'm seeing this incorrectly, but it seems like neither HPA nor KEDA naturally fit that model without essentially reimplementing Kueue's quota awareness in an external controller.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-18T20:12:09Z

> What we're after is capacity-driven - scale based on how much quota is free in the ClusterQueue. For our embarrassingly parallel batch Jobs the demand is always maximal, the only constraint is available cluster resources. Kueue already tracks this internally.

Why couldn't you use KEDA with the metric that reflects how much quota is unused in ClusterQueue?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-18T20:12:42Z

The main blocker for you is that Job does not actually support /scale subresource so you can't actually use HPA/KEDA anyway.
