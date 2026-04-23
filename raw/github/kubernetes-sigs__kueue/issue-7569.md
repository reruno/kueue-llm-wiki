# Issue #7569: Ray autoscaler cannot safely work with Kueue admission model (head node termination during suspend/requeue)

**Summary**: Ray autoscaler cannot safely work with Kueue admission model (head node termination during suspend/requeue)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7569

**Last updated**: 2026-04-08T14:17:25Z

---

## Metadata

- **State**: open
- **Author**: [@zhenyu](https://github.com/zhenyu)
- **Created**: 2025-11-06T18:34:59Z
- **Updated**: 2026-04-08T14:17:25Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Support for partial re-admission / subgroup-level elasticity in Kueue workloads so that control-plane–centric systems like Ray can autoscale safely.
Specifically, allow a workload (or JobSet) to contain sub-groups with different elasticity constraints—for example:

a non-preemptible / non-scalable-down group for the Ray head node (control plane, min = 1, max = 1)

one or more elastic groups for Ray workers (min..max range) that Kueue can resize independently, without suspending the whole workload.

This would let the Ray autoscaler request or release workers without killing the head node when Kueue reschedules or changes quotas.
**Why is this needed**:
In the current model, when a workload’s resource shape changes, Kueue typically performs suspend → requeue → re-admit for the entire workload.
That works for atomic batch jobs but not for elastic, stateful clusters where the control plane must persist.

In KubeRay, the head pod holds all cluster metadata (GCS, scheduling, control).
If the workload is suspended, the head node is terminated and the whole Ray cluster context is lost—making autoscaling impossible.

[#77](https://github.com/kubernetes-sigs/kueue/issues/77?utm_source=chatgpt.com)
 already discusses support for elastic or dynamically sized jobs and mentions Ray, but it does not explicitly address the “sticky control-plane / subgroup-level admission” case.
This request focuses on that gap.

I’ve confirmed this behavior with Red Hat contributors working on Kueue and KubeRay; currently Kueue cannot keep the head node alive during autoscale or flavor change operations.
If my understanding is inaccurate, please feel free to correct me. 🙏
**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@zhenyu](https://github.com/zhenyu) — 2025-11-06T18:38:04Z

@astefanutti , I talked this f2f in Ray submit  with  @accorvin and Adam Miller. Please take a look and thanks a lot

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-06T19:24:10Z

cc @andrewsykim

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-11-07T09:25:03Z

/cc

### Comment by [@astefanutti](https://github.com/astefanutti) — 2025-11-07T10:12:08Z

@zhenyu linking some related work that covers in-tree auto-scaling of RayClusters:

The update to the dynamically sized jobs KEP, specifically Phase 2 – RayCluster WorkloadSlice Support: https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs#phase-2--raycluster-workloadslice-support-in-single-cluster-configuration

The corresponding implementation #6662 that adapts Kueue workload to maintain a dedicated PodSet for the head node and allow the dynamic scaling of the PodSet for the workers.

And the related documentation:
* https://kueue.sigs.k8s.io/docs/concepts/elastic_workload/
* https://kueue.sigs.k8s.io/docs/tasks/run/rayclusters/#c-limitations

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T17:37:34Z

cc @yaroslava-serdiuk who is looking into Ray integration with Kueue

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:36:31Z

/priority important-longterm

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-01-21T10:40:41Z

Hi @zhenyu , could you please clarify are you having issues with (1) Ray Autoscaler behaviour or the issue related to (2) the lack for partial preemption? 
Those are two separate scenarios:
1. The Ray Autoscaler should work fine with Kueue, since the existing pods (nodes in Ray) are not removed in case of scale up. The Kueue underneath replace the Workload object, but the Job itself is not going to be suspended. 
2. The partial preemption is not supported for elastic workloads as of now.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-03-13T11:01:59Z

@mimowo there was no update on the issue for some time. Should we consider closing it?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T11:05:53Z

I wouldn't close it if this remains an issue. Sure there was no activity, but maybe because the problem is hard, not because there is no problem. Maybe it is enough to update the documentation with the recommended workaround. I'm not totally sure, but since we don't know fully I would keep it open.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2026-03-13T13:23:53Z

> I’ve confirmed this behavior with Red Hat contributors working on Kueue and KubeRay; currently Kueue cannot keep the head node alive during autoscale or flavor change operations.

@zhenyu  can you confirm whether you tested this with Kueue's elastic job feature enabled or disabeld?

### Comment by [@jjmalarkey](https://github.com/jjmalarkey) — 2026-04-08T03:53:05Z

@mimowo @andrewsykim I have reproduced part of this issue. In my local sandbox example with ElasticJobs FG enabled, I submitted a priority WL that triggered preemption of the elastic workload and suspended the entire RayCluster. 

If there is a known workaround I would be interested in trying it out. Or if there is a conversation about what this solution looks like. At the moment it weirdly makes the ElasticJobs more desirable for high priorityclass workloads only, because otherwise an admitted elastic workload for a RayCluster exposes the RayCluster to greater risk of suspension with resource contention.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-04-08T14:06:53Z

It's expected behavior. If the workload is preempted it will be fully suspended (i.e the whole RayCluster). 
In case of equal priority, the kueue will pick the most recent admitted workload. I suppose for ElasticWorkloads the admission time might be more recent since the admission time will represent the last resize.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-04-08T14:17:25Z

The kueue does not support partial preemption at the moment (i.e preempt only working groups and keep head node), we have an open issue for that:  https://github.com/kubernetes-sigs/kueue/issues/975
