# Issue #7605: Support RayJob InTreeAutoscaling

**Summary**: Support RayJob InTreeAutoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7605

**Last updated**: 2025-12-11T07:34:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hiboyang](https://github.com/hiboyang)
- **Created**: 2025-11-11T19:37:21Z
- **Updated**: 2025-12-11T07:34:48Z
- **Closed**: 2025-12-11T07:34:47Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 38

## Description

**What would you like to be added**:

Support RayJob InTreeAutoscaling. Kueue Elastic Workloads (Workload Slices) feature does not support RayJob right now, need code change to enable it for RayJob.

**Why is this needed**:

RayCluster supports [AutoScaling](https://docs.ray.io/en/master/cluster/kubernetes/user-guides/configuring-autoscaling.html), which is useful for notebook users, e.g. removing idle Ray worker nodes when notebook code not running.

Kueue supports RayJob and RayService with RayCluster running underlying them. RayService AutoScaling is already supported via Elastic Workloads feature. It is natural to extend the support to RayJob AutoScaling.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-11-12T10:49:55Z

/cc

### Comment by [@kryanbeane](https://github.com/kryanbeane) — 2025-11-12T12:10:13Z

hey @Future-Outlier, saw you involved in docs for the RayCluster and RayService support for this [KEP](https://github.com/VassilisVassiliadis/kueue/tree/main/keps/77-dynamically-sized-jobs). Thought you'd be the right person to @ here

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-12T13:33:26Z

Thanks @kryanbeane 
from kuberay side, we really need this, and happy to help or provide any information if needed

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T14:24:47Z

I think the main question is how this should work, two ideas we discussed with @andrewsykim, both are based on ElasticWorkloads:

1. when the RayJob has spec.RayClusterSpec.EnableInTreeAutoscaling set, then it creates the RayCluster, and the RayCluster has the Kueue Workload which conforms to autoscaling. Then, the size of the RayCluster is changed by autoscaler and it should be reflected into the RayJob object. This reflection should be done by a controller inside Ray KubeRay, but I would also be ok to put it under Kueue if it is problematic in KubeRay.

2. when the RayJob has spec.RayClusterSpec.EnableInTreeAutoscaling set, then we create the Workload object for the RayJob object. Then again there should be a controller which will reflect the change of the size of the RayCluster into the RayJob.

In both cases we need a controller which will reflect the RayCluster size to RayJob.

I think (1.) might be simpler to get going, but it seems like (2.) may give us more flexibility in the long run if Kueue is aware of both layers. However, I don't have a strong view between them

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-11-12T14:34:02Z

@mimowo I think we also discussed a third option, which is updating the Kueue object inheritance logic such that RayJob with autoscaling just delegates to the underlying RayCluster, similar to what we do for RayService.  This approach wouldnt' require a new controller that reflects the updated state back to RayJob

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T14:58:36Z

Yeah, this is a variation of (1.) where we don't have the controller, but then we have an inconsistency (IIUC) between the size of the cluster in RayJob and RayCluster. Leaving this Inconsistency might be a pragmatic shortcut, but I think it might mean some issues in corner cases.

The question is if we do the shortcuts, how do we don't commit to them long term, as it seems (2.) is the most Kueue-way approach.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T18:29:03Z

IIUC https://github.com/kubernetes-sigs/kueue/issues/7605#issuecomment-3522263590 would require tweaking the logic for finding the RayCluster instead of RayJob, which is quite generic for now, and it would be great to keep it this way.

Maybe user could somehow not be setting a "queue-name" label on RayJob, but create the RayCluster object with that "queue-name" label.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-12T18:48:13Z

I did a test of RayJob InTreeAutoscaling without using Kueue, seeing KubeRay update `replicas` in RayCluster but not in RayJob, when it triggered auto scale.

Thus regarding Kueue + RayJob InTreeAutoscaling, for option 1, it might be ok that we do not update RayJob object, meaning ` it should be reflected into the RayJob object` not needed?

```1. when the RayJob has spec.RayClusterSpec.EnableInTreeAutoscaling set, then it creates the RayCluster, and the RayCluster has the Kueue Workload which conforms to autoscaling. Then, the size of the RayCluster is changed by autoscaler and it should be reflected into the RayJob object. This reflection should be done by a controller inside Ray KubeRay, but I would also be ok to put it under Kueue if it is problematic in KubeRay.```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T18:59:12Z

Yeah, but leaving the inconsistency seems not ideal. If we accept it as a short term approach the challenge is how to have in Kueue "queue-name" label set on the RayCluster, but on the original RayJob. If the "queue-name" is set on both RayCluster and RayJob, then our generic code will create the workload for RayJob (top level): [FindAncestorJobManagedByKueue](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L740).

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-12T22:19:15Z

Yeah, we can engage with Ray community to address it, at the same time, work in Kueue in parallel.

Now the queue name label `kueue.x-k8s.io/queue-name` is already copied from RayCluster to RayJob. In [KubRay code](https://github.com/ray-project/kuberay/blob/4a623fd5b4e7c8f7563319aab3f8a043eed7cf76/ray-operator/controllers/ray/rayjob_controller.go#L924), it copies all labels from RayCluster to RayJob:
```
func (r *RayJobReconciler) constructRayClusterForRayJob(rayJobInstance *rayv1.RayJob, rayClusterName string) (*rayv1.RayCluster, error) {
	labels := make(map[string]string, len(rayJobInstance.Labels))
	for key, value := range rayJobInstance.Labels {
		labels[key] = value
	}
	labels[utils.RayOriginatedFromCRNameLabelKey] = rayJobInstance.Name
	labels[utils.RayOriginatedFromCRDLabelKey] = utils.RayOriginatedFromCRDLabelValue(utils.RayJobCRD)
	rayCluster := &rayv1.RayCluster{
		ObjectMeta: metav1.ObjectMeta{
			Labels:      labels,
			Annotations: rayJobInstance.Annotations,
			Name:        rayClusterName,
			Namespace:   rayJobInstance.Namespace,
		},
		Spec: *rayJobInstance.Spec.RayClusterSpec.DeepCopy(),
	}
```

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-11-12T22:44:04Z

> Yeah, but leaving the inconsistency seems not ideal.

If I'm understanding correctly, the inconsistency would lead to quota being misrepresented in cluster queues, so it would be required to fix the job ancestror logic to only extract resource quotas from the underlying RayCluster

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-12T22:53:41Z

In my testing, the inconsistency seems not causing issue, e.g. I started a RayJob with `replicas: 1`, then Ray AutoScaler updated RayCluster to `replicas: 5`, but left RayJob with `replicas: 1`. The RayJob still ran successfully. Agree we should fix this inconsistency, but this looks not a blocking issue for Kueue to support RayJob InTreeAutoscaling.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-11-12T23:00:16Z

> but this looks not a blocking issue for Kueue to support RayJob InTreeAutoscaling.

If you inspect the ClusterQueue object, does the resources/quotas consumed by the job reflect the RayJob with `replicas: 1` or RayCluster with `replicas: 5`?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-13T00:40:32Z

Hmm... I am still in the middle of playing with Kueue code base to see whether I can get Kueue with RayJob AutoScale work, will let you know if I make progress and can inspect ClusterQueue there.

> > but this looks not a blocking issue for Kueue to support RayJob InTreeAutoscaling.
> 
> If you inspect the ClusterQueue object, does the resources/quotas consumed by the job reflect the RayJob with `replicas: 1` or RayCluster with `replicas: 5`?

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-13T04:11:31Z

> Hmm... I am still in the middle of playing with Kueue code base to see whether I can get Kueue with RayJob AutoScale work, will let you know if I make progress and can inspect ClusterQueue there.
> 
> > > but this looks not a blocking issue for Kueue to support RayJob InTreeAutoscaling.
> > 
> > 
> > If you inspect the ClusterQueue object, does the resources/quotas consumed by the job reflect the RayJob with `replicas: 1` or RayCluster with `replicas: 5`?

I think make Kueue handle logic related to RayCluster is the best long term solution.
Since every CRD in kuberay has RayCluster.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T07:46:22Z

My point is that it is more inlined with how currently Kueue handles workload to put the Workload at the RayJob level, referencing the generic logic in FindAncestorJobManagedByKueue.

In this approach when RayCluster is rescaled then new Pods are created, but they are kept gated until the Workload is resized, this is the generic mechanism how ElasticWorkloads work.

The resize of the RayCluster I imagine would result in resizing the RayJob, which if quota allows is resized, and new Workload object is admitted. At this point we remove the scheduling gates from the Pods. 

This way the states of the RayJob, RayCluster and quota in Workload are in-sync.

The alternative to create the Workload at the RayCluster will require either:
1. changing the FindAncestorJobManagedByKueue with Ray-specific code, which is tricky because we keep this code generic
2. users-disabling in the configMap the rayjob integration
3. some mechanism which would allow users to set "queue-name" at the RayCluster, but not on the RayJob. This would be easy if RayJob kept spec.rayClusterMetadata along with spec.rayClusterSpec, but requires extending the RayJob API.

Even if we go with (1.) I'm thinking if we could design some extension points for the logic, rather than doing ad-hoc checks per CRD. Also, it would be good to somehow make this opt-in, maybe alpha feature gate.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T15:38:55Z

I think there might be a way to implement (1.) without changing FindAncestorJobManagedByKueue, as we can implement the interface IsTopLevel, then we would skip calling FindAncestorJobManagedByKueue and we would create the Workload for the RayCluster (but I haven't tested): https://github.com/kubernetes-sigs/kueue/blob/20904892825b5fee62b240994c7cdadfc4edb641/pkg/controller/jobframework/reconciler.go#L336-L350
We would implement the interface by checking if the RayCluster has the InTreeAutoscaling enabled.

Additionally we may need to disable the reconciliation of RayJob on the same condition (InTreeAutoscaling enabled) in the JobWithSkip interface, similar as done here: https://github.com/kubernetes-sigs/kueue/pull/7218/files#diff-24b8d3ba7104004ba575becf8db0a4ee47c9062f716a744f1afbbdb7bfded0d9R104-R108.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-14T20:03:32Z

Cool, let me implement `IsTopLevel` on `RayCluster` (returning true when EnableInTreeAutoscaling enabled), and see how it goes.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-15T04:29:40Z

Add cross-reference for some discussion in KubeRay: https://github.com/ray-project/kuberay/issues/4190

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-17T12:01:25Z

> Cool, let me implement `IsTopLevel` on `RayCluster` (returning true when EnableInTreeAutoscaling enabled), and see how it goes.

this is fixed, will release in kuberay 1.5.1, thank you

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T12:06:01Z

> Add cross-reference for some discussion in KubeRay: https://github.com/ray-project/kuberay/issues/4190

with this being done in KubeRay I think we could as well implement Workload at the RayJob level without. However, we can still start at the RayCluster level, just let's introduce an alpha feature gate so that we can move the Workload management later.

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-17T12:25:53Z

> > Add cross-reference for some discussion in KubeRay: [ray-project/kuberay#4190](https://github.com/ray-project/kuberay/issues/4190)
> 
> with this being done in KubeRay I think we could as well implement Workload at the RayJob level without. However, we can still start at the RayCluster level, just let's introduce an alpha feature gate so that we can move the Workload management later.

I think start at the RayCluster level is correct.
In kuberay 1.6.0, we are going to introduce RayCronJob CRD, maybe implement at the RayCluster level will not require any additional change?

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-11-17T15:24:11Z

> this is fixed, will release in kuberay 1.5.1, thank you

@Future-Outlier if you're referring to https://github.com/ray-project/kuberay/issues/4190, this won't help with this Kueue issue as we need replicas in `spec` to be updated, not `status`.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-17T19:42:25Z

Turn out `replicas` in RayCluster will not be updated even underlying RayJob `replicas` changed due to auto scaling. It is by design in Ray, per discussion https://github.com/ray-project/kuberay/issues/4190.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-17T22:51:58Z

I tried to skip RayJob and make RayCluster as top level with changes like following, and tested autoscaling:

- RayCluster.IsTopLevel(): return true when `RayCluster.Spec.EnableInTreeAutoscaling` is enabled
- RayJob.Skip(): return true when `RayJob.Spec.RayClusterSpec.EnableInTreeAutoscaling` is enabled

The result is that `RayJob.spec.suspend` was stuck in `true` and the job was never started, no workload/pod created for the job.

I also tried making `RayJob.Skip()` only return `true` when `RayJob.IsSuspended()` is `false`. Then I got two workload created, one for RayJob and one for RayCluster, which is kind of expected: the first workload created when RayJob started (suspended being changed to false), the second workload created by RayCluster when it was treated as top level.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-17T23:01:48Z

I tried another approach to change code: in `reconciler.go`, if current job is `RayCluster` and parent (ancestor) is `RayJob`, explicitly copy number of replicas from RayCluster to RayJob to make them in-sync, and use `JobWithPodLabelSelector. PodLabelSelector` to select pods inside `workloadslicing.StartWorkloadSlicePods()`. Then it seems working. I see a second workload slice created during auto scaling.

This approach seems working, but not sure whether it will introduce other issues... how do you think @mimowo @Future-Outlier ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T07:54:02Z

> The result is that RayJob.spec.suspend was stuck in true and the job was never started, no workload/pod created for the job.

Interesting, did you get the Workload created at the RayCluster as expected?

I think it would be good it you can push a PR ideally with an integration test, then we could see what is going on with debugger.

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-18T14:39:29Z

> I tried another approach to change code: in `reconciler.go`, if current job is `RayCluster` and parent (ancestor) is `RayJob`, explicitly copy number of replicas from RayCluster to RayJob to make them in-sync, and use `JobWithPodLabelSelector. PodLabelSelector` to select pods inside `workloadslicing.StartWorkloadSlicePods()`. Then it seems working. I see a second workload slice created during auto scaling.
> 
> This approach seems working, but not sure whether it will introduce other issues... how do you think [@mimowo](https://github.com/mimowo) [@Future-Outlier](https://github.com/Future-Outlier) ?

if `JobWithPodLabelSelector. PodLabelSelector` doesn't have any special behavior, I guess it will work.
I haven't had time to deep dive how kueue works, so I am just guessing here.

need @andrewsykim to take a deep look at this.


and here's a documentation for you to setup.
https://anyscale-ray--58568.com.readthedocs.build/en/58568/cluster/kubernetes/k8s-ecosystem/kueue.html#ray-autoscaler-with-kueue

@hiboyang

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-18T18:25:11Z

> > The result is that RayJob.spec.suspend was stuck in true and the job was never started, no workload/pod created for the job.
> 
> Interesting, did you get the Workload created at the RayCluster as expected?
> 
> I think it would be good it you can push a PR ideally with an integration test, then we could see what is going on with debugger.

I did not get Workload created at the RayCluster either in this case.

There is some process in our side to push a PR, I am working on it, will send it out once ready.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-19T22:48:16Z

@mimowo @Future-Outlier Here is PR to update RayCluster.IsTopLevel() and RayJob.Skip(): https://github.com/kubernetes-sigs/kueue/pull/7769 . With this change, RayJob/RayCluster will get stuck in suspended state, and do not run.

### Comment by [@Future-Outlier](https://github.com/Future-Outlier) — 2025-11-20T01:29:47Z

> [@mimowo](https://github.com/mimowo) [@Future-Outlier](https://github.com/Future-Outlier) Here is PR to update RayCluster.IsTopLevel() and RayJob.Skip(): [#7769](https://github.com/kubernetes-sigs/kueue/pull/7769) . With this change, RayJob/RayCluster will get stuck in suspended state, and do not run.

Hi, @hiboyang 
do you mind run 3 examples to make sure this works with kuberay
1. RayJob + autoscaler
2. RayService + autoscaler
3. RayCluster + autoscaler

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-11-20T16:35:22Z

My understanding is following: since the RayJob.Skip() is true, than it will be skipped in Reconcile loop and thus no workload will be created. Since the job is always suspend the RayCluster won't be created as well. 

> I tried to skip RayJob and make RayCluster as top level with changes like following, and tested autoscaling:
> 
> * RayCluster.IsTopLevel(): return true when `RayCluster.Spec.EnableInTreeAutoscaling` is enabled
> * RayJob.Skip(): return true when `RayJob.Spec.RayClusterSpec.EnableInTreeAutoscaling` is enabled
> 
> The result is that `RayJob.spec.suspend` was stuck in `true` and the job was never started, no workload/pod created for the job.
> 
> I also tried making `RayJob.Skip()` only return `true` when `RayJob.IsSuspended()` is `false`. Then I got two workload created, one for RayJob and one for RayCluster, which is kind of expected: the first workload created when RayJob started (suspended being changed to false), the second workload created by RayCluster when it was treated as top level.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-11-20T16:53:46Z

It seems this will work only if Skip() is called when the RayJob is unsuspended and the RayCluster subsequently adopts and stays in sync with the RayJob's workload.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-11-20T18:33:55Z

@Future-Outlier, for kueue without my change, `RayJob + autoscaler` is not working by design. `RayService + autoscaler` is working. For `RayCluster + autoscaler`, I haven't tested it yet, we mostly focus on RayJob/RayService now.

I got suggestion to update webhook to not suspend RayJob when auto scaling is enabled, so RayJob will create RayCluster. Will try this and see how it goes.

### Comment by [@xing-anyscale](https://github.com/xing-anyscale) — 2025-11-20T22:51:50Z

> [@Future-Outlier](https://github.com/Future-Outlier), for kueue without my change, `RayJob + autoscaler` is not working by design. `RayService + autoscaler` is working. For `RayCluster + autoscaler`, I haven't tested it yet, we mostly focus on RayJob/RayService now.
> 
I did the test that `RayCluster + autoscaler` autoscaling works.

### Comment by [@400Ping](https://github.com/400Ping) — 2025-11-23T10:43:00Z

> [@Future-Outlier](https://github.com/Future-Outlier), for kueue without my change, `RayJob + autoscaler` is not working by design. `RayService + autoscaler` is working. For `RayCluster + autoscaler`, I haven't tested it yet, we mostly focus on RayJob/RayService now.
> 
> I got suggestion to update webhook to not suspend RayJob when auto scaling is enabled, so RayJob will create RayCluster. Will try this and see how it goes.

I did the test for Autoscaling with RayCluster & RayService when writing doc for it, see [this](https://github.com/ray-project/ray/pull/58568)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T07:34:43Z

/close
The functionality is covered with https://github.com/kubernetes-sigs/kueue/pull/8082. We are now working on follow up cleanups. I will open dedicated issue(s).

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-11T07:34:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7605#issuecomment-3640627101):

>/close
>The functionality is covered with https://github.com/kubernetes-sigs/kueue/pull/8082. We are now working on follow up cleanups. I will open dedicated issue(s).


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
