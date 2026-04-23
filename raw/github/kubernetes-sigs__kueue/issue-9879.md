# Issue #9879: Restarted pods remain schedule-gated

**Summary**: Restarted pods remain schedule-gated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9879

**Last updated**: 2026-04-10T11:32:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ns-sundar](https://github.com/ns-sundar)
- **Created**: 2026-03-15T23:53:19Z
- **Updated**: 2026-04-10T11:32:37Z
- **Closed**: 2026-04-10T11:32:36Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When Kueue with elastic jobs gate is deployed with KubeRay, and a Ray Serve workload with elastic job annotation is created, after killing a Ray worker pod, the restarted pod remains permanently gated with Kueue's elastic job gate. 

  - This is readily reproducible with Kueue 0.15. Seen to happen when the worker pod is scheduled on GPU instance types, but not CPU instance types. Happens when the pod is non-force-deleted, but not when it is force-deleted. 

**What you expected to happen**:
The restarted pod should get its scheduling gate removed and run normally.

**How to reproduce it (as minimally and precisely as possible)**:
 - Deploy Kueue 0.15 with ElasticJobsViaWorkloadSlices=true feature gate
 - Deploy KubeRay
 - Submit a Ray Serve workload whose Ray Cluster has the annotation and kueue.x-k8s.io/elastic-job: "true" and spec.enableInTreeAutoscaling=true
 - [In our environment, this happens on GPU instances, but not CPU instances. As explained below, this may be incidental.]
 - Kill a worker pod without force deletion. 

**Anything else we need to know?**:
The pod remains gated due to the race described below. I have a partial fix for this race. I request community input for this partial fix, and discussions for a full fix. 

### Problem
During a restart scenario, here are the main events.

1. The current pod A gets a deletion timestamp and eventually terminates.
2. KubeRay sees the pod count change and creates a new pod. The new pod has the Kueue schedule gate by default.
3. KubeRay updates Ray Cluster CR status. The following steps happen concurrently.
    1. The Ray cluster reconciliation is triggered in Kueue.
        1. [A] Kueue’s Ray Cluster reconcile loop looks up the pods for this Ray cluster and ungates them.
    2. The informer cache in Kueue gets updated that pod A is deleted.
        1. [B] The old pod A is removed from Kueue’s workload slice index.
    3. The informer cache in Kueue gets updated that pod B is added.
        1. [C] The new pod B gets added to Kueue’s workload slice index.

There is no further update of the Ray Cluster CR, and so no further triggers of Kueue’s reconcile loop.

There are 6 possible sequences in which the 3 events may occur: ABC, ACB, BAC, BCA, CAB, CBA. This creates a race condition, as shown by the following sequence of events.

 * Problem path: If A happens before C, the new pod does not get ungated. That’s because the reconcile loop does not see the new pod, and the reconciler is not triggered by any later event.  The event sequences ABC, ACB and BAC fall under this sequence.
 * Happy path: If C happens before A, the new pod gets ungated. All good. The possible event sequences are CAB, CBA and BCA. 

If a pod for a workload is being deleted, there are 2 sets of scenarios, and any proposed fix should address both:
 * Restart scenarios: The pod crashed, was evicted or was manually deleted. A new equivalent pod will eventually replace it.
 * Downscale due to autoscaling: no new pod will replace it.

### Partial fix
Among the problematic event sequences — ABC, ACB and BAC — the first two can be addressed with a simple fix: when a pod associated with a workload has a deletion timestamp, defer reconciliation for a short time, such as D=1000 milliseconds.

* If this were a pod restart scenario, this gives time for a new pod to be added to the indexer. If this were a downscale scenario, the creation of the new workload to reflect the downscaling may be a little delayed but will happen eventually.
* Caveats with Fix: 
    * Pods may occasionally get stuck during termination and may remain indefinitely in deleting state. For example, finalizers not getting removed, volume unmount failed, etc. In that corner case, Ray Cluster reconciliation may get postponed indefinitely.
    * The fix does not address the sequence BAC. So, after the deferral by D milliseconds, the next reconcile loop may see that B has already happened and C has not. That would correspond to the BAC sequence. So, this issue would recur.

This fix is seen to work in our environment for Ray Serve workloads with D=1000 milliseconds.

### Full fix is difficult
To handle the event sequence BAC, we note that during Ray Cluster reconciliation in Kueue, the old pod A has already been removed from the index, while the new pod has not been added yet. 

This situation can be detected by comparing the total number of pods when the workload was admitted to the currently available set of pods. In that situation, we could defer reconciliation by D seconds, like the partial fix above.

However, this will fail the downscaling scenario — because the pod count is intentionally lower, this change will never create a new workload.

### Workaround for Recovery
The pod remains gated because no further reconcile loop is triggered for that Ray Cluster. We can trigger it manually by applying a dummy annotation to the Ray Cluster. That is seen to ungate the pod. 

**Environment**:
- Kubernetes version (use `kubectl version`): 1.35 (and 1.29)
- Kueue version (use `git describe --tags --dirty --always`): 0.15 
- Cloud provider or hardware configuration: AWS

## Discussion

### Comment by [@ns-sundar](https://github.com/ns-sundar) — 2026-03-15T23:54:09Z

/mimowo May I request your input on this issue?

### Comment by [@rueian](https://github.com/rueian) — 2026-03-17T21:26:29Z

I am a bit curious whether kueue can observe ABC events in any order. If so, I feel like that is a bug in the informer cache.

But anyway, could this be caused by the fact that there may be no subsequent update to the RayCluster CR after the replacement pod is created, so Kueue never gets another reconcile and therefore never sees the new pod to ungate it?

If so, I think one possible fix would be for Kueue to reconcile RayClusters periodically, rather than relying only on watched-object updates, similar to how KubeRay does an unconditional requeue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-18T06:41:59Z

My understanding is that the genericJob reconciler (used for RayCluster) in Kueue does not watch Pod events directly. Instead, it reacts to changes on the RayCluster object itself.

So if a Pod remains suspended for long enough, I would expect `status.ReadyWorkerReplicas` to drop, and that status change should trigger another reconcile in Kueue. 

**Potential quick fix**: as a quick fix maybe we can find that for some reason the status.ReadyWorkerReplicas is not changing on your cluster. I wonder whether in your case ReadyWorkerReplicas remains at 0 throughout, so no additional status update is emitted.

Could you share the output of:

`kubectl get raycluster -w --output-watch-events -o yaml`

**Long term fix** I think that the proper fix will be to refactor how the Pods are unsuspended for scheduling gated jobs. Instead of triggering the process from within the Reconciler we should have a dedicated Pod controller for updating Pods corresponding to elastic Jobs. I imagine the design should be analogous to TopologyUngater for TAS. We would react to Pod updates, and when Pod update happens then we trigger unsuspend if the corresponding Workload is admitted. We know from the workload status admission the expected number of Pods, and we know how many are running.

cc @sohankunkerkar @ichekrygin who are also pretty familar with the elastic Jobs.

**Mitigation:** when encountering rare Pod failures, and if you are ok with Restarting the entire RayJob, then try WaitForPodsReady.recoveryTimeout. When the timeout is reached, the entire RayCluster will be rescheduled, which may be a reasonable temporary workaround.

### Comment by [@ns-sundar](https://github.com/ns-sundar) — 2026-03-19T03:04:41Z

Thank you all.

Hi Rueian,
>  could this be caused by the fact that there may be no subsequent update to the RayCluster CR after the > replacement pod is created, so Kueue never gets another reconcile and therefore never sees the new > pod to ungate it?
Yes, that's exactly what I am seeing.

Meanwhile, there's another change being proposed which always does a RequeueAfter after StartWorkSlicePods(). That seems to address all these concerns. If all validations pass, we can close this issue.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-03-19T16:05:09Z

> Thank you all.
> 
> Hi Rueian,
> 
> > could this be caused by the fact that there may be no subsequent update to the RayCluster CR after the > replacement pod is created, so Kueue never gets another reconcile and therefore never sees the new > pod to ungate it?
> > Yes, that's exactly what I am seeing.
> 
> Meanwhile, there's another change being proposed which always does a RequeueAfter after StartWorkSlicePods(). That seems to address all these concerns. If all validations pass, we can close this issue.

Cool, we experimented exactly same thing `does RequeueAfter after StartWorkSlicePods()` and it worked. Will send out a PR soon.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-03-19T22:35:09Z

Created PR https://github.com/kubernetes-sigs/kueue/pull/10035 with `JobWithCustomRequeue` to trigger requeue. Would love to hear feedbacks.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-10T11:32:30Z

I think this should be already addressed by https://github.com/kubernetes-sigs/kueue/issues/10258
/close
let's re-open if not

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-10T11:32:37Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9879#issuecomment-4223455284):

>I think this should be already addressed by https://github.com/kubernetes-sigs/kueue/issues/10258
>/close
>let's re-open if not


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
