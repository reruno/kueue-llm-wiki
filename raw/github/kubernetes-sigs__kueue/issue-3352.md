# Issue #3352: Add Kueue support for Kubeflow Notebook

**Summary**: Add Kueue support for Kubeflow Notebook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3352

**Last updated**: 2025-01-29T20:51:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varshaprasad96](https://github.com/varshaprasad96)
- **Created**: 2024-10-28T22:59:07Z
- **Updated**: 2025-01-29T20:51:35Z
- **Closed**: 2024-12-18T06:18:54Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 59

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Enable Kueue to manage Kubeflow Notebook CRs (https://www.kubeflow.org/docs/components/notebooks/api-reference/notebook-v1/). 

**Why is this needed**:
Notebook themselves can be resource heavy (in terms of being GPU enabled), and having Kueue manage it like any other workload on the cluster would be helpful.  

**Open Questions**
I've been working on a PoC to enable this - however, looks like the underlying implementation of a Notebook resource is a Pod. The spec of the Notebook CR only defines a [PodspecTemplate](https://github.com/kubeflow/kubeflow/blob/ec82fbf58b79cff529d948b96e44ffd06bdfe679/components/notebook-controller/api/v1/notebook_types.go#L33), without a suspend field. 
Does implementing a similar mechanism as with pod integration sound reasonable -  wherein we add a scheduling [gate](https://github.com/kubernetes-sigs/kueue/blob/90ef60760b849e475f7cf32d07669bb91bbb479f/pkg/controller/jobs/pod/pod_webhook.go#L182) with a default webhook, and when it is ready to be accepted we ungate the pod. Or can the Notebook introduce a `suspend` field, to say expose the functionality of pausing/stopping the underlying Jupyter server which can be controlled by Kueue (not sure if this would be an ask by the NB users)?

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-28T23:00:28Z

cc: @alculquicondor @tenzen-y

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-28T23:07:29Z

Looking into the [issues](https://github.com/kubeflow/kubeflow/issues/4857) - seems like a `stop` feature does exist in v1beta1 API (hub version) of Notebooks where an annotation could be set to scale down the replica count to 0 (https://github.com/kubeflow/kubeflow/blob/ec82fbf58b79cff529d948b96e44ffd06bdfe679/components/notebook-controller/controllers/notebook_controller.go#L363).

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-29T13:34:34Z

Can you get this working with the pod integration?

I think suspend and first class support for the workload would be the best long term option but for POC and first integration I wonder if seeing if this can work with pod integration would be helpful.

My main reasoning for going with first class support would be in case the underlying objects change (pod to Job etc).

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-29T13:50:09Z

> I think suspend and first class support for the workload would be the best long term option but for POC and first integration I wonder if seeing if this can work with pod integration would be helpful.

Hey @kannon92, the idea is to avoid enabling pod integration directly as that previously caused drastic effects on platform, with managing non-notebook pods in the same namespace, and could not retry brining up the failed ones. Which is why the idea is to enable first-class support to the NB API directly and not expose pod integration on Kueue (at least intentionally for customers).

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-29T14:07:13Z

So if you don’t want pod integration then I think adding suspend field to notebook controller would be the option.

Have you brought this up with KubeFlow community about Kueue integration?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T16:38:38Z

@varshaprasad96 Thank you for raising this issue. Since v0.9.0, we will start the StatefulSet support. Could you verify if the Kueue StatefulSet integration could resolve your issue?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T16:40:28Z

We have already include the StatefulSet integration in the RC version: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.9.0-rc.1

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-29T22:40:53Z

@tenzen-y I am confused on your statfulset request. From what I can tell and what @varshaprasad96 mentions, it seems that the notebook controller is submitting pods. Is there a statefulset integration with KubeFlow notebooks?

Edit: Nvm I see https://github.com/kubeflow/kubeflow/blob/ec82fbf58b79cff529d948b96e44ffd06bdfe679/components/notebook-controller/controllers/notebook_controller.go#L138 that it seems that statefulsets are created from the pod spec template.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T08:43:23Z

> @tenzen-y I am confused on your statfulset request. From what I can tell and what @varshaprasad96 mentions, it seems that the notebook controller is submitting pods. Is there a statefulset integration with KubeFlow notebooks?
> 
> Edit: Nvm I see https://github.com/kubeflow/kubeflow/blob/ec82fbf58b79cff529d948b96e44ffd06bdfe679/components/notebook-controller/controllers/notebook_controller.go#L138 that it seems that statefulsets are created from the pod spec template.

Yeah, AFAIK, the notebook instance seems to be created via StatefulSet. So, I'm wondering if we can use the Kueue StatefulSet integration.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T08:51:02Z

This might be a good idea to make it work of free. The only caveat I see is that StatefulSet integration does not support resizes yet (not sure if this is needed for notebook though).

So actually it might all just work if you ensure the StatefulSet instance has the queue-name label.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-31T08:54:22Z

> This might be a good idea to make it work of free. The only caveat I see is that StatefulSet integration does not support resizes yet (not sure if this is needed for notebook though).
> 
> So actually it might all just work if you ensure the StatefulSet instance has the queue-name label.

In general, the Notebook Server is a Stateful application, and it is hard to make it HA. So, I guess that resizing is not needed.

### Comment by [@thesuperzapper](https://github.com/thesuperzapper) — 2024-10-31T16:47:16Z

Hey all, I am one of the maintainers of Kubeflow Notebooks.

But I am not quite sure if I understand how Kueue could be used to improve Notebooks.

Can one of the maintainers of Kueue explain how it relates to non-job workloads that are managed by other controllers?

---

Also, we are actually working on a Kubeflow Notebooks 2.0 right now, and it's quite a different design. While we still use StatefulSets internally, the outer `Notebook` CRD has been replaced with a cluster `WorkspaceKind` and namespaced `Workspace` resource. 

The key difference is that the `Workspace` CRD is now templated based on the selected `WorkspaceKind` and is not a wrapper around PodSpec, this will probably solve the problems faced by @varshaprasad96, see here for more info:

- https://github.com/kubeflow/notebooks/issues/85

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T16:51:33Z

@thesuperzapper this is great news. PTAL [here](https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/tasks/run/statefulset.md) - the doc documents how to schedule StatefulSets with Kueue (requires main version of Kueue, which can be isntalled like here: https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version)

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-10-31T21:47:23Z

Thanks @thesuperzapper @mimowo @tenzen-y for your reply. Replying to the questions below:

> But I am not quite sure if I understand how Kueue could be used to improve Notebooks.

Kueue is a workload queuing system primarily aimed at managing batch jobs, with resource quotas as a central feature. While its initial design is for batch workloads, we've seen interest from users who want to extend Kueue’s capabilities to non-batch workloads, to leverage its quota management, admission policies, and fair sharing model.

Notebooks, especially GPU-enabled ones, can demand substantial resources, similar to other ML batch workloads. Managing them through Kueue allows users to schedule Notebooks more efficiently within cluster resources. For reference, there has been work on integrating plain pods, StatefulSets, and Deployments into Kueue’s ecosystem makes it possible to use Kueue's resource management without duplicating functionalities of the native Kubernetes scheduler (https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/). 

The way we could expect NB integration to work would be (similar to [ray clusters](https://kueue.sigs.k8s.io/docs/tasks/run/rayclusters/)) - the individual NB pods are managed by nb-controller, but the responsibility of admitting the NB pod for scheduling it on a node would be done by Kueue based on available designated quota set by the admin. 

> Notebook Server is a Stateful application, and it is hard to make it HA. So, I guess that resizing is not needed.

I tried this by enabling SS integration and using it to manage NB (with v1beta APIs for now) and it works well. But the issue in here is that the replica count is immutable, so if a user likes to use the [stop/pause feature in NB by adding annotations](https://github.com/kubeflow/kubeflow/issues/4857#issuecomment-673060856) that doesn't work. Once paused, the Validating Webhook does not allow the spec to be changed, which means a stopped NB cannot be restarted.

> Also, we are actually working on a Kubeflow Notebooks 2.0 right now, and it's quite a different design. 

Thanks for pointing this out, I'll look into the v2 API. The major concern here seems to be a `suspend` equivalent field in NB API, that the Kueue can manage to admit/pre-empt resources. But there is a caveat in here - Notebooks are long running workloads, containing user-facing data, so in the scenario where Kueue preempt's and deletes notebooks at any time, especially in the absence of backup or persistent storage, this could lead to data loss and unexpected disruptions for a user which is not ideal. 

The question comes to be on how we intend the lifecycle of a Notebook resource to be considering the fact that it's going to be a non-batch workload (regardless of the underlying implementation). I'm not sure what a reasonable solution for being able to "suspend" Notebooks by Kueue would be without having to completely kill the underlying Pod.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T08:07:52Z

@varshaprasad96 thanks for the summary!

> I tried this by enabling SS integration and using it to manage NB (with v1beta APIs for now) and it works well. But the issue in here is that the replica count is immutable, so if a user likes to use the https://github.com/kubeflow/kubeflow/issues/4857#issuecomment-673060856 that doesn't work. Once paused, the Validating Webhook does not allow the spec to be changed, which means a stopped NB cannot be restarted.

Interesting, maybe a small fix somewhere is possible? Validating Webhook of which project is blocking that?

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-11-05T13:39:26Z

> Interesting, maybe a small fix somewhere is possible? Validating Webhook of which project is blocking that?

Yes, its in Kueue - within the statefulset webhook
https://github.com/kubernetes-sigs/kueue/blob/b3c53d530490f9c108bdc396da841a01a6027056/pkg/controller/jobs/statefulset/statefulset_webhook.go#L127-L131

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T13:49:18Z

hm, but then I'm not sure I understand " which means a stopped NB cannot be restarted". We base the StatefulSet integration on the PodGroup support, which means that when Kueue evicts a StatefulSet, then the PodGroup gets evicted and the newly created pods are gated (until the workload is unsuspended). So we use gating pods rather than "suspend" field for StatefulSet, Deployment and soon LWS integration.

So, I imagine the workflow does not require modifying the StatefulSet spec, unless I'm missing something (and I didn't test any of that).

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-11-05T23:55:36Z

> So, I imagine the workflow does not require modifying the StatefulSet spec, unless I'm missing something (and I didn't test any of that).

This is actually done by the `notebook-controller`. In the sense, when the user wants to pause a NB, they do so by adding an annotation to the respective pod:
eg:
```
kubectl annotate notebook/<pod> kubeflow-resource-stopped="true" -n notebook
```

The notebook-controller kicks in, and scales down the replica count in the stateful set. The validating webhook by Kueue denies the request:

```
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.11.0/pkg/internal/controller/controller.go:227
1.730850184723808e+09	ERROR	controller.notebook	Reconciler error	{"reconciler group": "kubeflow.org", "reconciler kind": "Notebook", "name": "notebook-sample-v1", "namespace": "notebook", "error": "admission webhook \"vstatefulset.kb.io\" denied the request: spec.replicas: Invalid value: 0: field is immutable"}
```

This means that stop/pause feature by adding annotations would not be available to users.

The above was tested using v1 APIs of NB. I'm not sure yet, if it's the same with v2 APIs.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T06:02:01Z

I see, thanks for sharing the info. So, in this scenario we always scale down to 0, then scale up from 0 to full size? 


If this is the case I think we could support this special case relatively easy in the integration by removing the entire pod group, and recreating.

### Comment by [@akram](https://github.com/akram) — 2024-11-06T07:52:32Z

Hi @mimowo ,
I will start working with @varshaprasad96 on this topic and we were discussing the scale down to 0 impacts yesterday indeed and we wanted to test it. If I am not wrong that was to see if it could work around the issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:01:04Z

sounds great, feel free to investigate and if possible send a PR.

We already planned some scaling support here: https://github.com/kubernetes-sigs/kueue/issues/3279, but this issue has a bit bigger scope - scaling down and up by recreating the PodGroup. Your case might be simpler (as a special case), but maybe not that much. In both cases PodGroup size is considered immutable.

cc @mwielgus 

Edit: If we can support it without API changes then I would be leaning to include it in 0.9.1, but let's see.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T08:36:07Z

> Edit: If we can support it without API changes then I would be leaning to include it in 0.9.1, but let's see.

In that case, I would like to add it to v0.10 since the v0.10 will be released in easily Dec, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:50:39Z

Yes, early release of 0.10 is another possibility, we can keep both options open for now and see how things go.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T08:53:31Z

> Yes, early release of 0.10 is another possibility, we can keep both options open for now and see how things go.

As far as I know, the patch version includes only bug fixes. But this request looks like an enhancement (scale support).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:56:25Z

We did cherry-pick small features in the past if they didn't impact API (which is potentially the case here), examples in release-notes [0.7.1](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.7.1) or [0.8.1](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.1), but I agree the early release of 0.10 is the cleanest path.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:02:23Z

> We did cherry-pick small features in the past if they didn't impact API (which is potentially the case here), examples in release-notes [0.7.1](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.7.1) or [0.8.1](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.1), but I agree the early release of 0.10 is the cleanest path.

It would be better not to include the new enhancement in the patch release to avoid introducing additional bugs as much as possible to the minor version. If we want to release any enhancement, I would recommend releasing a new minor early.

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-release/cherry-picks.md#what-kind-of-prs-are-good-for-cherry-picks

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T09:09:42Z

@akram @varshaprasad96 I know that also @mbobrovskyi is going to work on the solution to scaling under: https://github.com/kubernetes-sigs/kueue/issues/3279.

The idea we discussed with @mbobrovskyi is that for StatefulSet we will have an extra controller, when the controller detects that the size changed (sees the `replicas` count different than in the Workload object), then it will remove the old Pod Group and create the new Pod Group. In the special case of scaling down to 0 it will just delete the old PodGroup, and we will create the PodGroup when scaled back to >0.

It would be great if you could help reviewing and testing the approach.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-11-07T18:33:54Z

Thanks @mimowo and @mbobrovskyi. We will keep an eye and verify if it matches our needs. 

One question on the NB side:
We insist that the underlying NB pods use persistent volumes to store data. In case that a Notebook is preempted, should the notebook-controller be modified to add a finalizer to perform backups? 

Alternatively, is it reasonable to assume that, when Kueue is managing NBs based on cluster quotas (with the potential risk of preempting NB workloads), the responsibility falls to the admin and user to:

1. Ensure sufficient quota is allocated for Notebooks to reduce preemption risk.
2. Configure NB workloads with the highest priority to further minimize the likelihood of preemption.

@thesuperzapper could you please provide your thoughts on this. Is the v2 design considering backups along with the culling feature?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T11:15:48Z

> We insist that the underlying NB pods use persistent volumes to store data. In case that a Notebook is preempted, should the notebook-controller be modified to add a finalizer to perform backups?

TBH this is out-of-scope for Kueue integrations (at least for now, we don't support check-pointing natively in Kueue for any integrations, Jobs etc). I guess a finalizer is an option, or you may consider long enough `spec.terminationGracePeriodSeconds` on the pod template. 

In the approach I discussed with @mbobrovskyi Kueue does not delete the Pods, they are fully managed by StatefulSets, we just remove the Kueue finalizer, to let the pod go, but this should allow you to use another finalizer or control the graceful deletion.

You may want to test this PR: https://github.com/kubernetes-sigs/kueue/pull/3487. 

FYI @tenzen-y since the support requires changes to RBAC I think 0.9.1 is out of question anyway. We will aim to release the feature in 0.10.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-11-09T19:11:21Z

@mimowo Fair, this is an issue with the `notebook-controller` as back up and restore can not only be caused by Kueue but it can be through Kube-scheduler's preemption too. Will open an issue in the Kubeflow repo to get more insights from the community.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2024-11-14T17:22:41Z

cc @shravan-achar @akshaychitneni @bigsur0

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-14T19:57:22Z

I actually have a working solution for it for some time... The solution is to add an integration controller/webhook just like other job CRDs supported by Kueue, and change Notebook's annotation `kubeflow-resource-stopped` for suspend/resume. Kubeflow's Notebook controller will scale the backed StatefulSet accordingly. Does it make sense that I submit a PR?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T20:40:10Z

@xiongzubiao thanks for letting us know, maybe before you invest time in preparing the PR check the one we already have in-flight PR https://github.com/kubernetes-sigs/kueue/pull/3487. 

This PR supports Notebook at the StatefulSet level, and was initially tested: https://github.com/kubernetes-sigs/kueue/pull/3487#pullrequestreview-2425535895. We would prefer the support at the StatefulSet level as more generic that could be reused in other contexts.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-14T20:56:59Z

@mimowo Thanks for the explanation. Yes, #3487 sounds a more general solution. I will give it a try!

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2024-11-15T11:58:13Z

Hi Folks, just drop a few ideas here on how Kueue can be integrated with Jupyter Notebooks.

Jupyter is capable to run remote Kernels via gateway. One of the examples could be to use the Enterprise Gateway to provision remote Kernels: https://github.com/jupyter-server/enterprise_gateway (cc @lresende @zsailer)
In that case, the remote Kernel represents the runtime which is attached to the Notebook/Text Editor to execute the user's commands.
The Kernel can be as simple as the iPython process, or Spark cluster with iPython process running on the driver or Almond Kernel for Scala Spark: https://github.com/almond-sh/almond. Additionally, users can trigger the "derivative" jobs (e.g. TrainJob, JobSet, TFJob) using the Python Kernel.

All of those workloads (Python Kernel, Spark Kernel, or "derivative" workload) can be considered as **interactive** and needs to have higher priority over non-interactive workloads. @shravan-achar can share more on how those **interactive** workloads should work with queues.

In this scenario, Kueue should work directly with the Jupyter Kernels and "derivative" workloads, not with the stateful Jupyter Servers since Jupyter Servers don't require expensive compute resources (e.g. GPUs, TPUs).

I understand that today Kubeflow Notebooks don't support remote Kernel, but it is something which we can discuss in the future (cc @vikas-saxena02)

We talked a little bit about our remote Kernel orchestration in this Scheduling Talk: https://youtu.be/DdW5WUAvNuY?list=PLj6h78yzYM2OOkGhEJgb3Lx6YWoA3xQl4

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-16T01:37:33Z

> @mimowo Thanks for the explanation. Yes, #3487 sounds a more general solution. I will give it a try!

I confirm that it works when adding a queue label to the Notebook object. The Notebook can be suspended/resumed by changing the special annotation that the notebook-controller watches.

The only problem is, the Workload object corresponds to the pod. Its `active` field can't be used to suspend/resume the admission anymore, like other job-type workloads supports.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T07:27:04Z

> I confirm that it works when adding a queue label to the Notebook object. The Notebook can be suspended/resumed by > changing the special annotation that the notebook-controller watches.

Awesome!

> The only problem is, the Workload object corresponds to the pod. Its active field can't be used to suspend/resume the 
> admission anymore, like other job-type workloads supports.

Actually, for statefulSet, the workload object corresponds to PodGroup, and so the action field should suspend/resume the entire group. If this does not work I believe this is a "fixable" bug rather than a limitation of the mechanism. @mbobrovskyi can you check that?

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-18T18:19:14Z

> Actually, for statefulSet, the workload object corresponds to PodGroup, and so the action field should suspend/resume the entire group.

It doesn't work exactly same as a plain StatefulSet. I (as a user) adds the queue label in Notebook object's `metadata.labels`. But when the `notebook-controller` creates the backed StatefulSet, it adds the queue label in StatefulSet's `spec.template.metadata.labels`, not in `metadata.labels`. I think that is why no PodGroup is added.

I am not sure if it should be fixed in `notebook-controller` side or `kueue` side though.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-18T18:39:04Z

> It doesn't work exactly same as a plain StatefulSet. I (as a user) adds the queue label in Notebook object's metadata.labels. But when the notebook-controller creates the backed StatefulSet, it adds the queue label in StatefulSet's spec.template.metadata.labels, not in metadata.labels. I think that is why no PodGroup is added.

This is correct behaviour. It should add `kueue.x-k8s.io/queue-name` and `kueue.x-k8s.io/pod-group-name` labels and `kueue.x-k8s.io/pod-group-total-count` annotation on each pod.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T18:42:13Z

> But when the notebook-controller creates the backed StatefulSet, it adds the queue label in StatefulSet's spec.template.metadata.labels, not in metadata.labels. I think that is why no PodGroup is added.

Yeah, the STS webhook we have in Kueue will set up the PodGroup workload based on the `metadata.labels` (see [here](https://github.com/kubernetes-sigs/kueue/blob/e49265bff65dc6f2e0e3b6467a6eee51c8c5e083/pkg/controller/jobs/statefulset/statefulset_webhook.go#L65-L82))

If the label is set at the PodTemplate level, then you have a workload per pod. This is not good for STS, for example, in case of preemption, you may lose pod0, which might be problematic for STS.

> I am not sure if it should be fixed in notebook-controller side or kueue side though.

IIUC inside the `notebook-controller` to set it on the `metadata.labels` of STS, but feel free to share with us the relevant code pointers to help us better understand it.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-18T18:47:07Z

> IIUC inside the notebook-controller to set it on the metadata.labels of STS, but feel free to share with us the relevant code pointers to help us better understand it.

I think here is how the notebook-controller adds queue label to `spec.template.metadata.labels` of STS (by copying from `metadata.labels` of Notebook):
https://github.com/kubeflow/kubeflow/blob/master/components/notebook-controller/controllers/notebook_controller.go#L392

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T19:03:16Z

So the approaches I see:
1. hard-code the special rule to copy the Kueue queue-name label onto `matadata.labels` instead
2. copy all the labels into both places
3. have some form of configurable filter (to avoid hard-coding Kueue label)

It would be great if one could prototype one of them to double-check but it seems to be the decision for the Notebook project at this point. 

EDIT: maybe there are more alternatives - like a dedicated webhook for StatefulSet managed by Notebook.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-19T19:11:25Z

I am testing with adding queue-name label to `metadata.labels` of STS. Here are my current observations:
1. The `queue-name` and `pod-group-name` labels, and `pod-group-total-count` annotation are added to the pod. The Workload object has a `is-group-workload` annotation being true. I believe these are expected.
2. However, when I scale down the STS from 1 to 0, the Workload object is deleted along with the pod. Is this expected?
3. On the other hand, if I change the `active` field of the Workload object from true to false (when STS's replica is 1), the Workload object's admittance status changes from true to false accordingly. But the pod is stuck at terminating state, likely due to the finalizer `kueue.x-k8s.io/managed`. Is this a bug?
4. After manually deleting the finalizer on the pod from step 3, the pod disappears correctly. But the Workload object is automatically admitted again, which creates a new pod automatically. That means I can't really stop the STS by setting the Workload's `active` field.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-20T05:55:45Z

> 1. The `queue-name` and `pod-group-name` labels, and `pod-group-total-count` annotation are added to the pod. The Workload object has a `is-group-workload` annotation being true. I believe these are expected.

Yeah, that’s correct because the StatefulSet creates the pod group.

> 2. However, when I scale down the STS from 1 to 0, the Workload object is deleted along with the pod. Is this expected?

Yes, that’s correct. Kueue removes the Workload if there are no Pods in the group.

> 3. On the other hand, if I change the `active` field of the Workload object from true to false (when STS's replica is 1), the Workload object's admittance status changes from true to false accordingly. But the pod is stuck at terminating state, likely due to the finalizer `kueue.x-k8s.io/managed`. Is this a bug?

We can't suspend Pods; we can only remove the pod group and recreate it with a gate. If you set active=false on the Workload, Kueue evicts the Pods, but the process gets stuck because of the finalizers. So this is correct behaviour.

> 4. After manually deleting the finalizer on the pod from step 3, the pod disappears correctly. But the Workload object is automatically admitted again, which creates a new pod automatically. That means I can't really stop the STS by setting the Workload's `active` field.

This is how the pod group works. After you remove the finalizers, all Pods should disappear, and the Workload should be finalized as well. However, the StatefulSet recreates the Pods, and the Workload is recreated as well. 

Yes, we need to handle this case to remove the finalizers when active=true is set.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-20T17:33:51Z

Thank you @mbobrovskyi .

> Yes, we need to handle this case to remove the finalizers when active=true is set.

This makes a lot of sense to me now. I think the finalizer should be removed also when the workload is re-admitted back from the preempted state.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-20T17:42:05Z

However, it does feel confusing (at least a bit strange...) to make the pod stuck at terminating state when the workload is inactive or preempted, rather than actually scaling down the STS.

I understand that it is a technical limitation of the pod group method, but why not implementing a direct integration for STS (meaning a workload object corresponding to the STS directly)? STS is K8s native, it doesn't sound too much to have a direct integration for it. It will be more straightforward and much easier to understand IMHO.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-21T08:18:23Z

Yes, scaling down the STS to 0 is another option, but it would require modifying the `spec.replicas` field by Kueue, and the `spec` field might be managed by another third-party autoscaler or a human. 

Maybe we should have 2 modes for the STS suspend support (via scaling down to 0, or pod group gating), the method could be selected by annotation. Still, it remains unclear to me if this is a needed complication, so would like to make sure first there are some use-cases blocked by the pod group approach.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-11-21T18:41:52Z

Fair enough. Should I create a new issue for the finalizer bug of the pod group method?

The finalizer causes the pod stuck at terminating state in the following cases:
- When the workload is re-activated.
- When the workload is re-admitted after preemption.
- When the STS is deleted.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T11:20:16Z

Sorry, for returning here late, it was quite a busy period before releasing 0.10.

> Should I create a new issue for the finalizer bug of the pod group method?

Can you please re-test with Kueue 0.10.0 as we make some bug fixes to StatefulSet which may solve the issue already?

Thank you for opening https://github.com/kubernetes-sigs/kueue/issues/3851, to my knowledge this is the last remaining known issue.

@varshaprasad96, @xiongzubiao do you think we can close this issue, or more is needed here? The support for the workload "spec.active" field is already ticketed and actively worked on.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-12-17T12:51:53Z

@mimowo No worries! Yes, I agree that #3851 is the last issue and I am okay with closing this one.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T12:59:32Z

/close
Thank you all for the engagement and fruitful discussions!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-17T12:59:37Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3352#issuecomment-2548398688):

>/close
>Thank you all for the engagements and fruitful discussions!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T14:08:04Z

Actually, It would be great to add a docs page "under https://kueue.sigs.k8s.io/docs/tasks/run/ (or even https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/), to demonstrate how to use Kueue to running Notebook.
@xiongzubiao @varshaprasad96 are you up to?

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2024-12-17T16:51:48Z

+1, agree with @xiongzubiao, the integration PoC internally works well for our internal use case. I can help contribute to the docs!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T17:21:03Z

/reopen
Awesome, looking forward to a contributor to update the docs

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-17T17:21:08Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3352#issuecomment-2549096100):

>/reopen
>Awesome, looking forward to a contributor to update the docs


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2024-12-17T19:10:24Z

Yes, I am happy to contribute too :-)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T06:18:49Z

Cool, actually, let me track the remaining work in the follow up issues, so that the scope is clear: https://github.com/kubernetes-sigs/kueue/issues/3878
Feel free to assign.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-18T06:18:54Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3352#issuecomment-2550450314):

>Cool, actually, let me track the remaining work in the follow up issues, so that the scope is clear: https://github.com/kubernetes-sigs/kueue/issues/3878
>Feel free to assign.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
