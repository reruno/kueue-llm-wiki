# Issue #4106: Add Support for Plain Pods with Known OwnerReferences

**Summary**: Add Support for Plain Pods with Known OwnerReferences

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4106

**Last updated**: 2026-02-14T08:24:11Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@BenHinthorne](https://github.com/BenHinthorne)
- **Created**: 2025-01-30T13:58:20Z
- **Updated**: 2026-02-14T08:24:11Z
- **Closed**: 2026-02-14T08:24:11Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 30

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to add the ability for pods annotated with `kueue.x-k8s.io/standalone` to be suspended even if their owner is a known Kueue integration (open to suggestions one exact annotation wording). 

Currently, in the [pod_webhook](https://github.com/kubernetes-sigs/kueue/blob/198d276002b12066b19601da9a0a7ca8ae4879b3/pkg/controller/jobs/pod/pod_webhook.go#L172), if the pod has an ownerReference of a `Kind` known to Kueue, Kueue will not suspend this pod and a workload will never be created for it. I would like to add the ability to bypass this check, and allow the pod to be suspended and have a workload be created for it, if the user opts in via an annotation. 

**Why is this needed**:

At a high level, this would give users more flexibility to process plain pods with Kueue. For example, let's consider Spark Applications, which don't yet have native support within Kueue. In short, Spark Apps operate with a Driver pod, which then creates Executor pods. The Executor  owner is the Driver pod, and thus of Kind Pod. Currently, the ownerReference check mentioned above prevents the user from being able to have Kueue process the Executors at all. If users could add the `standalone` annotation to the Executor pods, then they would be able to use Kueue to manage Spark Apps via plain pods. The same concept could extend to any CRD not yet natively integrated for Kueue, that may follow a similar pattern of Pods owning Pods. 

Similarly, this option would also give users the flexibility to process _known workload types_ as plain pods, should they choose to do so. This flexibility would be helpful for users to be able to process dynamically sized jobs (at least until https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs#implementation-history is fully supported), as well as give them the choice if they would like gang scheduling behavior or not. For example, let's consider RayJobs. Currently, RayJobs will be processed by Kueue as a single workload, and any pods resulting from the job autoscaling aren't yet supported. If users could allow for pods owned by a RayJob to be processed as plain pods, then they could choose to process RayJobs as single pods (forgoing gang scheduling), and process any dynamically scaled pods in the same way. 

**Completion requirements**:

This enhancement requires the following artifacts:

Will link an example PR in the comments, and wait for feedback before proceeding with any doc updates. 

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@BenHinthorne](https://github.com/BenHinthorne) — 2025-01-30T14:12:36Z

I created a draft PR for how this would work here: https://github.com/kubernetes-sigs/kueue/pull/4109

I have tested this in my local env!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-30T15:04:14Z

I would think a KEP is worth going through on this one.

There is parallel work going on to support SparkApplications from @everpeace. Is there is support for Spark do you need this feature?

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-01-30T18:20:58Z

When an owner is a pod, can it ever be the case that we don't want Kueue to manage the child object? I might be missing something here, but if a pod is creating workloads then is it ever truly a owner in the sense as the other integrations? Could we remove pods from the list of integrations that we care about when checking whether the owner is Kueue managed?

### Comment by [@everpeace](https://github.com/everpeace) — 2025-01-31T00:49:22Z

> There is parallel work going on to support SparkApplications from @everpeace. Is there is support for Spark do you need this feature?

Thanks for pinging. Although it can be a bit abuse (I'm not sure, sorry), as far as I know, Kueue already have `kueue.x-k8s.io/pod-suspending-parent` annotation. I think the below pod will be suspended as expected by this line:
https://github.com/kubernetes-sigs/kueue/blob/198d276002b12066b19601da9a0a7ca8ae4879b3/pkg/controller/jobs/pod/pod_webhook.go#L137-L142


```yaml
kind: Pod
metadata:
  name: a-pod-owned-by-another-pod
  annotations:
    kueue.x-k8s.io/pod-suspending-parent: pod
  labels:
    kueue.x-k8s.io/queue-name: queue-1
  ownerReferences:
  - apiVersion: v1
    controller: true
    kind: Pod
    name: a-owner-pod
    uid: xxxxxx
spec:
  ...
``` 

For spark case, in my `kueue.x-k8s.io/pod-group-sets` PR(#4102), I've tested locally pod-group-sets feature by putting `kueue.x-k8s.io/pod-suspending-parent` annotation to executor pods like below, and it works as expected. I will work on `SparkApplication` integration as a next step.

```console
./bin/spark-submit \
    --master k8s://https://127.0.0.1:58900 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
...
    --conf spark.kubernetes.driver.annotation.kueue.x-k8s.io/pod-group-total-count=3 \
    --conf spark.kubernetes.driver.annotation.kueue.x-k8s.io/pod-group-sets='[{"count":1,"name":"driver"},{"count":2,"name":"worker","template":..omit..}]' \
    --conf spark.kubernetes.driver.label.kueue.x-k8s.io/queue-name=queue-1 \
    --conf spark.kubernetes.driver.label.kueue.x-k8s.io/pod-group-name=spark-pi \
    --conf spark.kubernetes.driver.label.kueue.x-k8s.io/pod-group-role=driver \
...
    # THIS ONE!
    --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-suspending-parent=pod \
    --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-group-total-count=3 \
    --conf spark.kubernetes.executor.label.kueue.x-k8s.io/queue-name=queue-1 \
    --conf spark.kubernetes.executor.label.kueue.x-k8s.io/pod-group-name=spark-pi \
    --conf spark.kubernetes.executor.label.kueue.x-k8s.io/pod-group-role=executor \
    local:///opt/spark/examples/jars/spark-examples.jar 5000
```

### Comment by [@BenHinthorne](https://github.com/BenHinthorne) — 2025-02-11T19:52:00Z

> > There is parallel work going on to support SparkApplications from [@everpeace](https://github.com/everpeace). Is there is support for Spark do you need this feature?
> 
> Thanks for pinging. Although it can be a bit abuse (I'm not sure, sorry), as far as I know, Kueue already have `kueue.x-k8s.io/pod-suspending-parent` annotation. I think the below pod will be suspended as expected by this line:
> 
> [kueue/pkg/controller/jobs/pod/pod_webhook.go](https://github.com/kubernetes-sigs/kueue/blob/198d276002b12066b19601da9a0a7ca8ae4879b3/pkg/controller/jobs/pod/pod_webhook.go#L137-L142)
> 
> Lines 137 to 142 in [198d276](/kubernetes-sigs/kueue/commit/198d276002b12066b19601da9a0a7ca8ae4879b3)
> 
>  func (w *PodWebhook) Default(ctx context.Context, obj runtime.Object) error { 
>  	pod := FromObject(obj) 
>  	log := ctrl.LoggerFrom(ctx).WithName("pod-webhook") 
>  	log.V(5).Info("Applying defaults") 
>   
>  	_, suspend := pod.pod.GetAnnotations()[SuspendedByParentAnnotation] 
> kind: Pod
> metadata:
>   name: a-pod-owned-by-another-pod
>   annotations:
>     kueue.x-k8s.io/pod-suspending-parent: pod
>   labels:
>     kueue.x-k8s.io/queue-name: queue-1
>   ownerReferences:
>   - apiVersion: v1
>     controller: true
>     kind: Pod
>     name: a-owner-pod
>     uid: xxxxxx
> spec:
>   ...
> For spark case, in my `kueue.x-k8s.io/pod-group-sets` PR([#4102](https://github.com/kubernetes-sigs/kueue/pull/4102)), I've tested locally pod-group-sets feature by putting `kueue.x-k8s.io/pod-suspending-parent` annotation to executor pods like below, and it works as expected. I will work on `SparkApplication` integration as a next step.
> 
> ./bin/spark-submit \
>     --master k8s://https://127.0.0.1:58900 \
>     --deploy-mode cluster \
>     --name spark-pi \
>     --class org.apache.spark.examples.SparkPi \
> ...
>     --conf spark.kubernetes.driver.annotation.kueue.x-k8s.io/pod-group-total-count=3 \
>     --conf spark.kubernetes.driver.annotation.kueue.x-k8s.io/pod-group-sets='[{"count":1,"name":"driver"},{"count":2,"name":"worker","template":..omit..}]' \
>     --conf spark.kubernetes.driver.label.kueue.x-k8s.io/queue-name=queue-1 \
>     --conf spark.kubernetes.driver.label.kueue.x-k8s.io/pod-group-name=spark-pi \
>     --conf spark.kubernetes.driver.label.kueue.x-k8s.io/pod-group-role=driver \
> ...
>     # THIS ONE!
>     --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-suspending-parent=pod \
>     --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-group-total-count=3 \
>     --conf spark.kubernetes.executor.label.kueue.x-k8s.io/queue-name=queue-1 \
>     --conf spark.kubernetes.executor.label.kueue.x-k8s.io/pod-group-name=spark-pi \
>     --conf spark.kubernetes.executor.label.kueue.x-k8s.io/pod-group-role=executor \
>     local:///opt/spark/examples/jars/spark-examples.jar 5000

Ah interesting, thanks for pointing out the `kueue.x-k8s.io/pod-suspending-parent` parent annotation! I also tested this out on my set up and it worked as expected, with the behavior I was hoping to have with the proposed `standalone-pod` annotation. 

My concern with using this annotation is that I would fear (as you alluded to) that it's not entirely what it's meant for, and so if it's implementation changes down the road, but we are depending on this behavior, we could run into trouble. I tracked down the [original PR](https://github.com/kubernetes-sigs/kueue/pull/3803) where `pod-suspending-parent` was introduced, but tbh I am not 100% sure on the reason this annotation was introduced. The PR description says:

"Adjusts default suspension logic in Deployment/StatefulSet webhooks to correctly handle the case where they
are children of another Kueue-managed Kind."

So maybe the annotation was actually built for this purpose? Allowing for pods that are children of another kueue managed kind to opt into management with the annotation. I'm not 100% sure though, maybe @dgrove-oss (author of original PR) could weigh in? Is the usage of the `kueue.x-k8s.io/pod-suspending-parent` annotation valid for the use case described in this issue?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-12T13:52:29Z

> So maybe the annotation was actually built for this purpose? Allowing for pods that are children of another kueue managed kind to opt into management with the annotation.

This is the purpose of the annotation.  Currently, I would classify the annotation as an implementation mechanism not as part of the stable API for Kueue.  We do need the functionality, so assuming something like it would be available in future releases is probably relatively low risk, but the details could change.  Is that fair @mimowo ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T14:31:23Z

Yes, I think we will need the functionality the annotation provides going forward. Since the original introduction to use in the pod_webhook, we also already depend on it for LWS and StatefulSet integrations. I think it is safe to assume it is going to stay. 

As a related side note, I was never truly convinced about its name, so we may consider changing it :), some alternative names would be `kueue.x-k8s.io/pod-managing-framework`. If we want to rename it is probably better now then later, wdyt @dgrove-oss ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T14:50:46Z

Still, IIUC the `kueue.x-k8s.io/pod-suspending-parent` annotation does not solve the problem initially raised in the issue to allow supporting Spark Without full blown integration. I think there is actually great value in supporting integrations via Pods so that users of Kueue can "help themselves" rather than implement full blown built-in integrations in Kueue, due to maintenance cost of the integrations. 

So, my preference is to support something like `kueue.x-k8s.io/pod-standalone` and unblock the issue. Given the relative ease of implementation I'm happy to consider it for 0.11.  Also, this is way easier and risky than https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs (which is out of question for 0.11).

There are some questions:
1. should it be generalized to other CRDs - then we may prefer to call it `kueue.x-k8s.io/standalone`. I believe the implementation will be simple, but not sure about use cases. I think some users of JobSet in Kueue will want to mark the individual Jobs as standalone too. So my preference is to make it generic day one (or at least explore it as an option).

2. related to the use case:

>  RayJobs will be processed by Kueue as a single workload, and any pods resulting from the job autoscaling aren't yet supported. 

IIUC this is a problem only if you need to enable "Ray" integration in your cluster. Otherwise you could just leave it disabled and add the "queue-name" label at the PodTemplate level. If you need to enable the "Ray" integration in your cluster, then the way to go would be to add "queue-name" and "standalone" annotations at the PodTemplate level. Is this correct?

Any opinions @tenzen-y @dgrove-oss? Would you like to drive @BenHinthorne?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T14:55:46Z

In the past we introduced some annotations without KEP, and this one would be very simple. OTOH adding a KEP never hurts so, it would be great place to discuss the remaining open questions .

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-12T20:39:54Z

> As a related side note, I was never truly convinced about its name, so we may consider changing it :), some alternative names would be `kueue.x-k8s.io/pod-managing-framework`. If we want to rename it is probably better now then later

Agree `pod-managing-framework` is a better name and that we should either rename it pre 0.11 or we have to live with it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T09:01:54Z

Yeah, but `pod-suspending-parent` is already released in 0.10 so I think we would need transition period of a couple of releases where we support both - `pod-suspending-parent` being deprecated and supported in "reads" while "pod-managing-framework" would be set in "writes". 

I'm ok if you are up to the challenge, but I'm also ok to live with it, maybe just improve the documentation.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-13T12:07:22Z

Forgot that we had released it already.  I'm fine with improving the docs and living with it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-14T10:55:40Z

> should it be generalized to other CRDs - then we may prefer to call it kueue.x-k8s.io/standalone. I believe the implementation will be simple, but not sure about use cases. I think some users of JobSet in Kueue will want to mark the individual Jobs as standalone too. So my preference is to make it generic day one (or at least explore it as an option).

I'm leaning toward `kueue.x-k8s.io/standalone` since RayCluster obviously has a similar usecase for autoscaling.
But, we can reconsider if we really want to support the autoscaling by RayCluster level instead of Pod integration level, later.

The changing already release annotations are challenging for backward compatibility. So, from now, I'd like to select annotation name condiered for other usecases.

### Comment by [@BenHinthorne](https://github.com/BenHinthorne) — 2025-02-25T14:30:01Z

👋 Hey folks, sorry for the delay in response here. Thanks for all the discussion. I just wanted to clarify my current understanding and how to move forward!

My current understanding is that the `kueue.x-k8s.io/pod-suspending-parent` annotation solves the use case originally mentioned in the issue, at least for plain pods (from this [comment](https://github.com/kubernetes-sigs/kueue/issues/4106#issuecomment-2653775184)). However, I _don't think_ it's currently generalized for all CRDs, plus it sounds like we would prefer another name than `pod-suspending-parent`. 

> I think there is actually great value in supporting integrations via Pods so that users of Kueue can "help themselves" rather than implement full blown built-in integrations in Kueue, due to maintenance cost of the integrations.

I agree with @mimowo here, I think there would be value in this! And same with the Ray Autoscaling use case mentioned by @tenzen-y, this annotation would allow for flexibility for users handling autoscaling too. 

So, to move forward, it sounds like a plan would be to:

Introduce a `kueue.x-k8s.io/standalone-pod` annotation, which concretely would allow a pod to be suspended even if it's parent is a known integration for Kueue. This would give users flexibility in handling CRDs without full blown integrations (for example like SparkApps, which currently have pods owning pods, so users can't process them as plain pods without this annotation). 

Similarly, it would allow users to process dynamically scaled jobs as plain pods too. 

> If you need to enable the "Ray" integration in your cluster, then the way to go would be to add "queue-name" and "standalone" annotations at the PodTemplate level. Is this correct?

I think this is a valid use case, where the initial RayJob would be processed as a full RayJob via the integration, but then any dynamic scaling of the job could then be processed as plain pods. This flexibility would be great! FWIW, I have also seen dynamically size SparkApps, that even when SparkApps have an integration with Kueue this behavior would be helpful.

So for next steps, would folks prefer a KEP? If so, I'm happy to drive it! Let me know if my understanding above aligns with everyones, otherwise happy to clarify everything :)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-25T14:48:14Z

> Introduce a kueue.x-k8s.io/standalone-pod annotation, 

I would just call it `kueue.x-k8s.io/standalone`. I see it also useful to annotate Jobs within JobSet. This way you can achieve lazy quota allocation for JobSet Jobs. So, you place the queue-name at the level of Jobs and also mark them as standalone. Allocating all quota eagerly for some JobSets might not be optimal.

> I think this is a valid use case, where the initial RayJob would be processed as a full RayJob via the integration, but then any dynamic scaling of the job could then be processed as plain pods. 

So, you would get the "main" RayJob to have the workload and be admitted, and only the extra pods to be "standalone". How would the annotation be added only to the "extra" pods?

> So for next steps, would folks prefer a KEP? If so, I'm happy to drive it! Let me know if my understanding above aligns with everyones, otherwise happy to clarify everything :)

This sounds great. Let me also cc @mwielgus in case he has some thoughts / ideas / concerns.

### Comment by [@BenHinthorne](https://github.com/BenHinthorne) — 2025-02-25T22:01:36Z

> I would just call it kueue.x-k8s.io/standalone
👍 Makes sense to me. 

>  How would the annotation be added only to the "extra" pods?
Ah this is a good point... I'm not entirely sure, and I don't think it would be standard across job types (Ray, Spark, etc.). I'd have to think more about how this use case would be addressed, perhaps something to discuss in the KEP...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T20:25:19Z

> > So for next steps, would folks prefer a KEP? If so, I'm happy to drive it! Let me know if my understanding above aligns with everyones, otherwise happy to clarify everything :)
> 
> This sounds great. Let me also cc @mwielgus in case he has some thoughts / ideas / concerns.

I would vote KEP, first. Because we already have similar annotations, `kueue.x-k8s.io/pod-suspending-parent`. 
So, I especially want to clarify what new `kueue.sigs.k8s.io/standalone` resolve, and what is differences (or responsibility differences) between those annotations.

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-04-23T12:29:01Z

This seems related to what I ran into recently.  While working on #4815 (enable RayCluster and RayJob objects to switch on the ray in-tree autoscaler) I noticed that the pods that RayCluster creates would not cause Kueue to create a Workload because their owner (A RayCluster object) is managed by Kueue.

Looking at the flow of code for Deployment objects I noticed that the difference is that the pod objects have a `ReplicaSet` owner. The ReplicaSet objects are not managed by Kueue so in the pod webhook logic the Deployment objects follow a different path.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-22T12:53:48Z

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

### Comment by [@dhenkel92](https://github.com/dhenkel92) — 2025-07-28T15:23:56Z

/remove-lifecycle stale

### Comment by [@ankursaini2006](https://github.com/ankursaini2006) — 2025-09-01T15:13:47Z

Hello,

I am trying to test Spark Application with the version 0.13.3 and it seems that the executors are not managed by the Kueue. It was working perfectly with the version 0.9.0 since there was no ownerReference check. I have also tested by putting the annotation `kueue.x-k8s.io/pod-suspending-parent` on the executors, but the executors remains in SchedulingGated. Does anyone know why it is behaving like this ? It seems there is implementation for Spark applications.

Thanks

### Comment by [@munali](https://github.com/munali) — 2025-09-04T14:15:39Z

@ankursaini2006 We ran into this as well.

The issue was introduced with this [PR](https://github.com/kubernetes-sigs/kueue/pull/4808) where the managed by kueue annotation does not get added by the webhook (ie. this line `pod.pod.Labels[constants.ManagedByKueueLabelKey] = constants.ManagedByKueueLabelValue` [here](https://github.com/epam/kubernetes-kueue/blob/c8469bf01695f203288c3530429164785dd1b4a8/pkg/controller/jobs/pod/pod_webhook.go#L186)) for the executor pods since they have the annotation  `kueue.x-k8s.io/pod-suspending-parent`. To get around this you can add that label to the executor pods.

Without the label is required to remove the schedule gate

if the ManagedLabelKey is not set to true, and an executor pod of the Spark Job happens to be the 0th pod in the list then the [jobframework](https://github.com/kubernetes-sigs/kueue/blob/7a3498f047900c8a66ac3f86fb4248cbca1edc5c/pkg/controller/jobframework/reconciler.go#L252) will [skip](https://github.com/kubernetes-sigs/kueue/blob/7a3498f047900c8a66ac3f86fb4248cbca1edc5c/pkg/controller/jobs/pod/pod_controller.go#L547) the reconciliation and never [ungate](https://github.com/kubernetes-sigs/kueue/blob/7a3498f047900c8a66ac3f86fb4248cbca1edc5c/pkg/controller/jobframework/reconciler.go#L514) the pods

I realize this is hacky, but seemed to work for now. Ideally a better sol'n might be to update the code and move the adding of the label into the pod_webhook's `if suspended` [section](https://github.com/epam/kubernetes-kueue/blob/c8469bf01695f203288c3530429164785dd1b4a8/pkg/controller/jobs/pod/pod_webhook.go#L190). @mbobrovskyi wdyt?

### Comment by [@ankursaini2006](https://github.com/ankursaini2006) — 2025-09-04T15:11:15Z

@munali Thank you.
Indeed I found the same thing while looking into the code so after adding the ManagedLabelKey, it worked. As you said this is hacky and a better solution should be implemented.

### Comment by [@ankursaini2006](https://github.com/ankursaini2006) — 2025-09-09T08:30:16Z

Hello  

While testing Spark applications, I found that LocalQueueDefaulting also does not work for Spark jobs since default queue  is updated only in the [section of if suspend](https://github.com/kubernetes-sigs/kueue/blob/8e7ead7d8c00699232e4bb100b07cff93d2b9a5d/pkg/controller/jobs/pod/pod_webhook.go#L172). I believe this label should always be updated. @munali @mbobrovskyi wdyt ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T06:36:56Z

Regarding Spark Jobs I see this enhancement in progress: https://github.com/kubeflow/spark-operator/pull/2387

cc @everpeace 

Also, in Kueue we are moving forward with the ElasticJobs which probably could be adopted to Spark, cc @ichekrygin .

When both enhancement happen, would it eliminate the need for Spark to be run on Pods, or there are still some use cases requiring that?

Even if the use-cases are unblocked, but it would take time to sink and adopt, then I would be happy to unblock the use-cases using Pod-based integration in the short/term mid-term. However,  I'm not sure if the Pod-based integration is blocked at the moment seems like people found ways to make it work now, see https://github.com/kubernetes-sigs/kueue/issues/4106#issuecomment-3253952637. I'm thinking if we should document / add tests for this approach.

### Comment by [@everpeace](https://github.com/everpeace) — 2025-09-11T14:58:50Z

> When both enhancement happen, would it eliminate the need for Spark to be run on Pods, or there are still some use cases requiring that?

I think that's an important point, and I'm also curious about this. I'd like to hear user's voice. As far as I know, `SparkApplication` (of kubeflow's spark-operator) would be the first choice to run spark jobs on the Kubernetes clusters. This can fits large batch jobs. But, I also know that there are interactive use-case or users that spawns spark jobs via pyspark library, spark-submit CLI in JupyterLab/VS Code whcih are sometimes inside of Kubernetes, sometimes not inside of Kuberntes.

> However, I'm not sure if the Pod-based integration is blocked at the moment seems like people found ways to make it work now, see https://github.com/kubernetes-sigs/kueue/issues/4106#issuecomment-3253952637. I'm thinking if we should document / add tests for this approach.

That's great idea. I can have working example below (pod integration).

<details>
<summary>setup(kind, spark-opertor, kueue)</summary>

```shell
❯ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.33.1) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
```

```shell
#
# Install spark-operator
#
❯ helm repo add --force-update spark-operator https://kubeflow.github.io/spark-operator
"spark-operator" has been added to your repositories

❯ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "spark-operator" chart repository
Update Complete. ⎈Happy Helming!⎈

❯ helm install spark-operator spark-operator/spark-operator --namespace spark-operator --version 2.3.0 --create-namespace --wait
NAME: spark-operator
LAST DEPLOYED: Thu Sep 11 23:16:30 2025
NAMESPACE: spark-operator
STATUS: deployed
REVISION: 1
TEST SUITE: None

#
# Create spark ServiceAccount in default namespace first
# (This is required for driver pod to create executor pods)
#
❯ kubectl create serviceaccount spark \
  && kubectl create clusterrolebinding spark-role \
    --clusterrole=edit --serviceaccount=default:spark --namespace=default
serviceaccount/spark created
clusterrolebinding.rbac.authorization.k8s.io/spark-role created
```

```shell
#
# Install Kueue (with pod integration)
#
❯ kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.13.3/manifests.yaml
namespace/kueue-system serverside-applied
customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io serverside-applied
...
validatingwebhookconfiguration.admissionregistration.k8s.io/kueue-validating-webhook-configuration serverside-applied

# Enable pod integration
❯ kubectl edit cm -n kueue-system kueue-manager-config
...
-  # - "pod"
+  - "pod"
configmap/kueue-manager-config edited

❯ kubectl rollout restart deployment -n kueue-system kueue-controller-manager
deployment.apps/kueue-controller-manager restarted

```

```shell
#
# create queue-1 ClusterQueue/LocalQueue
#
kubectl apply -f - <<EOT
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: queue-1
spec:
  namespaceSelector: {}
  resourceGroups:
    - coveredResources:
        - cpu
        - memory
      flavors:
        - name: default
          resources:
            - name: cpu
              nominalQuota: 10
            - name: memory
              nominalQuota: 10Gi
  fairSharing:
    weight: 1
  preemption:
    reclaimWithinCohort: LowerPriority
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100000
    withinClusterQueue: LowerOrNewerEqualPriority  
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: queue-1
  namespace: default
spec:
  clusterQueue: queue-1
EOT

resourceflavor.kueue.x-k8s.io/default created
clusterqueue.kueue.x-k8s.io/queue-1 created
localqueue.kueue.x-k8s.io/queue-1 created
```
</details>

### `SparkApplication` with pod integration & workaround

<details>
<summary> detailed example </summary>

```shell
#
# SparkApplication with pod integration
# by putting labels/annotations to driver/executor pod template explicitly.
# But, ideally, putting single label to SparkApplication would be better.
#
❯ kubectl apply -f - <<EOT
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-pi
  namespace: default
spec:
  type: Scala
  mode: cluster
  image: spark:3.5.4
  imagePullPolicy: IfNotPresent
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: local:///opt/spark/examples/jars/spark-examples.jar
  arguments:
  - "50000"
  dynamicAllocation:
    enabled: true
    maxExecutors: 3
  sparkVersion: 3.5.4
  driver:
    labels:
      kueue.x-k8s.io/queue-name: queue-1
    coreRequest: "1"
    coreLimit: "1"
    memory: "1024m"
    memoryOverhead: "0"
    serviceAccount: "spark"
  executor:
    labels:
      kueue.x-k8s.io/queue-name: queue-1
      kueue.x-k8s.io/managed: "true" # This should be required in v0.13.3 or later
    annotations:
      kueue.x-k8s.io/pod-suspending-parent: pod.  # This is an workaround for driver generated pods to activate pod integration
    coreRequest: "1"
    coreLimit: "1"
    memory: "1024m"
    memoryOverhead: "0"
    serviceAccount: "spark"
    deleteOnTermination: false
EOT
sparkapplication.sparkoperator.k8s.io/spark-pi created

❯ kubectl get workloads.kueue.x-k8s.io,clusterqueue,localqueue,sparkapplications,pod
NAME                                                                 QUEUE     RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/pod-spark-pi-0a7d2a9939314cfa-exec-1-0a064   queue-1   queue-1       True       True       44s
workload.kueue.x-k8s.io/pod-spark-pi-0a7d2a9939314cfa-exec-2-aca1f   queue-1   queue-1       True       True       43s
workload.kueue.x-k8s.io/pod-spark-pi-0a7d2a9939314cfa-exec-3-c40ea   queue-1   queue-1       True       True       43s
workload.kueue.x-k8s.io/pod-spark-pi-driver-cb8c6                    queue-1   queue-1       True       True       50s

NAME                                  COHORT   PENDING WORKLOADS
clusterqueue.kueue.x-k8s.io/queue-1            0

NAME                                CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/queue-1   queue-1        0                   0

NAME                                             STATUS      ATTEMPTS   START                  FINISH                 AGE
sparkapplication.sparkoperator.k8s.io/spark-pi   COMPLETED   1          2025-09-11T14:32:32Z   2025-09-11T14:33:21Z   51s

NAME                                   READY   STATUS      RESTARTS   AGE
pod/spark-pi-0a7d2a9939314cfa-exec-1   0/1     Completed   0          44s
pod/spark-pi-0a7d2a9939314cfa-exec-2   0/1     Completed   0          43s
pod/spark-pi-0a7d2a9939314cfa-exec-3   0/1     Completed   0          43s
pod/spark-pi-driver                    0/1     Completed   0          50s
```
</details>

```yaml
#
# SparkApplication with pod integration
# by putting labels/annotations to driver/executor pod template explicitly.
# But, ideally, putting single label to SparkApplication would be better.
#
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
spec:
  driver:
    labels:
      kueue.x-k8s.io/queue-name: queue-1
  ...
  executor:
    labels:
      kueue.x-k8s.io/queue-name: queue-1
      kueue.x-k8s.io/managed: "true" # This should be required in v0.13.x, v0.12.x and v0.11.4+
    annotations:
      kueue.x-k8s.io/pod-suspending-parent: pod.  # This is an workaround for driver generated pods to activate pod integration
```  

### `spark-submit` CLI with pod integration & workaround

<details>
<summary> detailed example </summary>

```shell
#
# spark-submit CLI from batch/v1 Job
#
kubectl apply -f - <<'EOT'
apiVersion: batch/v1
kind: Job
metadata:
  # Note: this job is NOT under Kueue management.
  name: spark-pi
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      serviceAccountName: spark
      containers:
      - name: spark-submit
        image: spark:3.5.4
        imagePullPolicy: Always
        command:
        - sh
        - -c
        # Note 1:
        #   Spark can not disable kerberos even the job does not use it.
        #   As a workaround, we can pass an empty krb5.conf.
        #   ref: https://issues.apache.org/jira/browse/SPARK-31800
        # Note 2:
        #   This example passes many Spark configurations via --conf option for demonstration purpose.
        #   Configuration can be passed via various ways.
        #   ref: https://spark.apache.org/docs/latest/configuration.html
        - >
          touch krb5.conf; /opt/spark/bin/spark-submit
          --master k8s://https://kubernetes.default.svc
          --deploy-mode cluster
          --conf spark.app.name=$(JOB_NAME)
          --conf spark.kubernetes.kerberos.krb5.path=krb5.conf
          --conf spark.kubernetes.namespace=$(K8S_NAMESPACE)
          --conf spark.kubernetes.container.image=spark:3.5.4
          --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark
          --conf spark.driver.cores="1"
          --conf spark.driver.memory="1024m"
          --conf spark.kubernetes.driver.limit.cores="1"
          --conf spark.kubernetes.driver.label.kueue.x-k8s.io/queue-name=queue-1
          --conf spark.executor.cores="1"
          --conf spark.executor.memory="1024m"
          --conf spark.kubernetes.executor.limit.cores="1"
          --conf spark.kubernetes.executor.deleteOnTermination=false
          --conf spark.kubernetes.executor.label.kueue.x-k8s.io/queue-name=queue-1
          --conf spark.kubernetes.executor.label.kueue.x-k8s.io/managed=true
          --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-suspending-parent=pod
          --conf spark.dynamicAllocation.enabled=true
          --conf spark.dynamicAllocation.minExecutor=1
          --conf spark.dynamicAllocation.initialExecutor=1
          --conf spark.dynamicAllocation.maxExecutors=3
          --class org.apache.spark.examples.SparkPi
          local:///opt/spark/examples/jars/spark-examples.jar 50000
        env:
        - name: K8S_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: SERVICE_ACCOUNT
          valueFrom:
            fieldRef:
              fieldPath: spec.serviceAccountName
        - name: JOB_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          limits:
            cpu: 300m
            memory: 512Mi
EOT
job.batch/spark-pi created

❯ kubectl get workloads.kueue.x-k8s.io,clusterqueue,localqueue,sparkapplications,pod
NAME                                                                       QUEUE     RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/pod-spark-pi-698339993945a1fd-exec-1-c4d0f         queue-1   queue-1       True       True       74s
workload.kueue.x-k8s.io/pod-spark-pi-698339993945a1fd-exec-2-f7138         queue-1   queue-1       True       True       73s
workload.kueue.x-k8s.io/pod-spark-pi-698339993945a1fd-exec-3-5ab8b         queue-1   queue-1       True       True       73s
workload.kueue.x-k8s.io/pod-spark-pi-pn946-d4a1e79939457823-driver-2031d   queue-1   queue-1       True       True       81s

NAME                                  COHORT   PENDING WORKLOADS
clusterqueue.kueue.x-k8s.io/queue-1            0

NAME                                CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/queue-1   queue-1        0                   0

NAME                                         READY   STATUS      RESTARTS   AGE
pod/spark-pi-698339993945a1fd-exec-1         0/1     Completed   0          74s
pod/spark-pi-698339993945a1fd-exec-2         0/1     Completed   0          73s
pod/spark-pi-698339993945a1fd-exec-3         0/1     Completed   0          73s
pod/spark-pi-pn946                           0/1     Completed   0          101s
pod/spark-pi-pn946-d4a1e79939457823-driver   0/1     Completed   0          81s
```
</details>

```yaml
#
# spark-submit CLI from batch/v1 Job
#
kubectl apply -f - <<'EOT'
apiVersion: batch/v1
kind: Job
spec:
  template:
    spec:
      containers:
        # This example passes many Spark configurations via --conf option for demonstration purpose.
        # Configuration can be passed via various ways.
        # ref: https://spark.apache.org/docs/latest/configuration.html
      - name: spark-submit
        command:
        - sh
        - -c
        - >
          /opt/spark/bin/spark-submit
          --conf spark.kubernetes.driver.label.kueue.x-k8s.io/queue-name=queue-1
          --conf spark.kubernetes.executor.label.kueue.x-k8s.io/queue-name=queue-1
          --conf spark.kubernetes.executor.label.kueue.x-k8s.io/managed=true
          --conf spark.kubernetes.executor.annotation.kueue.x-k8s.io/pod-suspending-parent=pod
          ...
```

As shown above, without `SparkApplication` CR integration, there is a workaround to put spark pods under Kueue management.  I think it's good idea to document it. I also agree direct `SparkApplication` integration would be better for long term.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-16T07:29:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T08:22:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-14T08:24:06Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-14T08:24:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4106#issuecomment-3901392453):

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
