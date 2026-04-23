# Issue #8651: Path to Beta for ElasticJobsViaWorkloadSlices - Ray Autoscaling

**Summary**: Path to Beta for ElasticJobsViaWorkloadSlices - Ray Autoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8651

**Last updated**: 2026-04-14T17:06:04Z

---

## Metadata

- **State**: open
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-01-17T17:13:45Z
- **Updated**: 2026-04-14T17:06:04Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 19

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A path to graduate the ElasticJobsViaWorkloadSlices feature gate to beta for Ray (RayCluster/RayJob) autoscaling support.

**Why is this needed**:
  We have customer demand for autoscaling Ray workloads managed by Kueue. The Ray-specific implementation has already landed:
  - RayCluster autoscaling: #6662 (v0.14)
  - RayJob autoscaling: #7605 / #8082 (backported to v0.14 via #8229)

 However, this functionality is gated behind ElasticJobsViaWorkloadSlices, which is alpha and disabled by default.

The current https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs bundles requirements that span multiple integrations (GC policies, metrics, JobSet, PyTorchJob, etc.). This creates a situation where Ray autoscaling may be ready but blocked waiting on unrelated work.

  I had an initial conversation with @mimowo about this. Some points that came up:

  - The current ElasticWorkloads implementation has minimal validation, meaning users can hit issues with unsupported combinations (e.g., TAS + Elastic) late in the process. For beta, we'd need to either support these combinations or add validation to reject them upfront.
  - One option discussed was introducing scoped feature gates for specific integrations that aren't ready (e.g., `ElasticJobsViaWorkloadSlicesForTAS`), allowing the core functionality to graduate while deferring others.
  - Strengthening validation now is preferred since it can be relaxed later, whereas the reverse is harder.

The suggestion was to revisit after 0.17 to assess progress and decide on the graduation path. Sharing this for context. I would love to hear other perspectives on how to approach this.

Looking for feedback on how we can move this forward. I'm willing to actively work on the remaining pieces once we align on an approach.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-18T01:04:31Z

cc @tenzen-y @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-18T01:39:48Z

cc @ichekrygin

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:24:26Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T17:56:39Z

I'm wondering what the right way is to establish supporting ElasticJobs. (WorkloadSlice vs [WorkloadResize](https://github.com/kubernetes-sigs/kueue/issues/5897))

The WorkloadSlice is a slightly non-declarative approach (no API schema safe), and I'm worried about potential debt in the future.

I can understand that the WorkloadSlice approach could be easily shipped because basic implementations have already been completed, but I'd like to revisit if this is truly the right direction.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-20T16:38:38Z

> The WorkloadSlice is a slightly non-declarative approach (no API schema safe), and I'm worried about potential debt in the future.

Could you please elaborate a bit more on "non-declarative" part?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-30T17:05:05Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-06T15:12:17Z

I followed up with Sohan and I'm not sure he will get to this this month. Going to unassign for now.

/unassign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-06T15:14:33Z

@hiboyang
Would you be interested in taking this work?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-06T16:10:06Z

I can take this work as a side project (I am working on other projects at the same time). Agree to add scoped feature gates (e.g., ElasticJobsViaWorkloadSlicesForTAS). Also we need to add more E2E testing to prevent future regression. I am working on RayService autoscaling e2e test right now, get some weird issue that there is not RayService pod, still debugging.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-06T16:12:37Z

At the same time, there is a lot of discussion in https://github.com/kubernetes-sigs/kueue/issues/9015, are we open to other alternatives for elastic job?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-06T18:17:06Z

Thank you @hiboyang!

I'm not really sure on other alternatives. Is there a lot of issues with Elastic jobs and Ray?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-06T22:17:08Z

There are several issues with Elastic jobs for Ray. We fixed some issue, like workload slice name conflicting. There is another open PR (https://github.com/kubernetes-sigs/kueue/pull/10272) which @sohankunkerkar is working on.

Current two workload slice design did bring a lot of discussion in https://github.com/kubernetes-sigs/kueue/issues/9015, which contains several options.

Maybe we can have have some community meeting to discuss this, or discuss it in next wg-batch meeting?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-06T23:27:35Z

Yea this sounds like a good item for a community call.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-09T17:03:04Z

We had some discussion regarding https://github.com/kubernetes-sigs/kueue/issues/9015, feel the right solution is to solve the resource usage/quota counting inconsistency when there are two workloads triggered by autoscaling. @ichekrygin will check what it takes to bring that solution. Thanks @ichekrygin!

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-10T20:43:41Z

cc @mimowo @tenzen-y @ichekrygin 

I'm having a hard time following if ElasticJobsViaWorkloadSlices for Ray should be promoted to beta or we should keep this functionality in alpha.

It seems there are concerns about the stability of this feature and we are not yet sure we want to commit to supporting this long term.

We have some customers asking for this but I'm leaning towards saying this feature is stable enough yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-13T08:37:27Z

> I'm having a hard time following if ElasticJobsViaWorkloadSlices for Ray should be promoted to beta or we should keep this functionality in alpha.

There is no specific feature gate currently for elastic Ray, so this is essentially the same as going to beta with ElasticJobsViaWorkloadSlices. The list of Beta graduation criteria is super long https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs#beta, so I think we should re-evaluate some of the points and move to GA rather. 

> It seems there are concerns about the stability of this feature and we are not yet sure we want to commit to supporting this long term.

A lot of the stability issues have been solved recently thanks to the effort of @hiboyang and @sohankunkerkar .
The open issues I know about:
- https://github.com/kubernetes-sigs/kueue/issues/9015, but I think solving this is not a blocker, because this is a corner case, as long as we document this issue
- https://github.com/kubernetes-sigs/kueue/issues/5897 - as much as I like this atomic model, I don't think this is a blocker. We can still develop the alternative while WorkloadSlices are in Beta, because that should be transparent to the end-users if done well.

> We have some customers asking for this but I'm leaning towards saying this feature is stable enough yet.

I think @hiboyang or @ns-sundar may share some more info about the real usage stability already.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-14T16:56:00Z

I think ElasticJobsViaWorkloadSlices for RayJob is stable now after recent few fixes.

ElasticJobsViaWorkloadSlices for RayService still has critical issue with KubeRay 1.6.0, see https://github.com/ray-project/kuberay/issues/4686 . This is a very basic scenario (running a RayService with autoscaling), and reproducable with my this Kueue PR (https://github.com/kubernetes-sigs/kueue/pull/10252). I am also trying to see whether there is work around inside Kueue, but so far, did not find good options.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-14T16:57:50Z

> ElasticJobsViaWorkloadSlices for RayService still has critical issue with KubeRay 1.6.0, see https://github.com/ray-project/kuberay/issues/4686 . This is a very basic scenario (running a RayService with autoscaling), and reproducable with my this Kueue PR (https://github.com/kubernetes-sigs/kueue/pull/10252). I am also trying to see whether there is work around inside Kueue, but so far, did not find good options.

Do you think it would be to odd to promote this feature to beta for RayJob/RayCluster but alpha for RayService?

Seems hard to explain so should we wait for this bug to be fixed?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-04-14T17:06:03Z

> > ElasticJobsViaWorkloadSlices for RayService still has critical issue with KubeRay 1.6.0, see [ray-project/kuberay#4686](https://github.com/ray-project/kuberay/issues/4686) . This is a very basic scenario (running a RayService with autoscaling), and reproducable with my this Kueue PR ([#10252](https://github.com/kubernetes-sigs/kueue/pull/10252)). I am also trying to see whether there is work around inside Kueue, but so far, did not find good options.
> 
> Do you think it would be to odd to promote this feature to beta for RayJob/RayCluster but alpha for RayService?
> 
> Seems hard to explain so should we wait for this bug to be fixed?

Yes, would suggest to wait for this bug to be fixed. This bug is blocking people to user RayService autoscaling right now. Also better to package workload slicing feature together for RayJob/RaySerivce/RayCluster to avoid fragement.
