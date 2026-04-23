# Issue #4927: Add spec.replicas and subresource.scale to Workload API to support KEDA-based scale-to-zero

**Summary**: Add spec.replicas and subresource.scale to Workload API to support KEDA-based scale-to-zero

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4927

**Last updated**: 2025-09-21T15:41:56Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ChristianZaccaria](https://github.com/ChristianZaccaria)
- **Created**: 2025-04-11T09:35:03Z
- **Updated**: 2025-09-21T15:41:56Z
- **Closed**: 2025-09-21T15:41:55Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 18

## Description

**What would you like to be added:**
Add to the Workload API the `spec.replicas` and `subresource.scale` fields to allow integration and scaling with [KEDA](https://keda.sh/).

The Kubernetes Event-driven Autoscaling (KEDA) is a component that strives to make application autoscaling simple. It can scale any deployment, statefulset, and custom resource to meet demand, and also perform scale-to-zero to enhance cost-efficiency. Moreover, KEDA can scale based on [almost any metric source](https://keda.sh/docs/2.17/scalers/). KEDA makes use of two custom resources, `ScaledObject` and `TriggerAuthentication`. ScaledObject is used to define how to scale our Custom Resource based on the metrics provided, while TriggerAuthentication is used for providing authentication details to access external metrics.

For `spec.replicas:`
- Type: integer
- Range: 0 to 1 (or to unbounded)
- Default: 1
- Description: KEDA uses this field to scale down the idleing long-running Workload to zero, indicating Kueue to terminate the idleing pods.

For `subresource.scale`:
- subresources:
  - scale:
          # specReplicasPath defines the JSONPath inside of a custom resource that corresponds to Scale.Spec.Replicas.
          - specReplicasPath: .spec.replicas
          # statusReplicasPath defines the JSONPath inside of a custom resource that corresponds to Scale.Status.Replicas.
          - statusReplicasPath: .status.replicas
          # labelSelectorPath defines the JSONPath inside of a custom resource that corresponds to Scale.Status.Selector.
          - labelSelectorPath: .status.labelSelector

**Why is this needed:**
RayClusters, Deployments, and Statefulsets are long-running resources. It can often happen that these resources are idle and not utilizing GPU for a long period of time. This causes resource starvation for other workloads in the queue. With KEDA we can scale down the Workload, and have the Workload deactivated, scaling down the idle resources. This in turn, helping maximise GPU resource consumption.

**Completion requirements:**
The pre-requisite for this, is to add the `spec.replicas` and [subresource.scale](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#scale-subresource) fields to the Workload API to indicate to KEDA where to write the desired replica count when scaling.

We would need to add logic in the `workload_controller.go` to set the Workload’s `spec.active` property to false if `spec.replicas` has been scaled down to zero by KEDA. To re-activate the unused Workload, the user can manually set the replicas to 1, and the `spec.active` field to `true`.

**This enhancement requires the following artifacts:**

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-11T09:39:02Z

cc: @akram @varshaprasad96

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-11T17:03:33Z

Related: https://github.com/kubernetes-sigs/kueue/issues/77

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T21:51:14Z

I'm not sure of the reason for the Workload API. If we change Workload replicas, there is not affections.
Instead of Workload API, each resource like Deployment, must have a scale resource.

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-16T16:08:48Z

@tenzen-y with the Workload API we can take a holistic approach over all long-running workloads, whether it's a `RayCluster`, `Deployment`, `Statefulset` or any other long-running workload. For context, KEDA can only scale a resource if it exposes a `replicas` field and defines the [/scale subresource properties](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#scale-subresource). By introducing these into the Workload API, we can leverage KEDA alongside Kueue, and add logic in the Workload Controller to automatically deactivate the workload when KEDA decides to scale down the Workload to zero based on metrics. This way freeing up quota for other Workloads in the queue, ultimately maximising utilization.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T16:15:55Z

The Workload object is a child of Jobs like Deployment. So, if we implement scale subresource to Workload, we need to propagate `replicas` change to Jobs. This does not align with kubernetes Owners and Dependents pattern.

https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/

So, I do not think we should implement scale subresource to Worklaod.

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-17T15:13:27Z

I understand what you mean, I see the Workload resource has as OwnerReference i.e., a Job. My understanding of this relationship between them is that a Workload does not directly manipulate a Job object.

Even though the Workload is a child of a Job, currently Kueue allows the Workload's `.spec.active` field the ability to deactivate the Workload, which will ultimately terminate the pods owned by the Job. We could follow a similar pattern with a `replicas` field defined solely in the Workload without the requiring this field in the Job. The workload_controller would reconcile and observe the `replicas` and set the `.spec.active` field to `false`, and hence terminating the idleing pods owned by the Job.

The benefit of this approach is that it will work across all types of jobs, and the logic would be centralised in the workload controller. The alternative to this would be to implement this on each type of job, which would require to add logic and API changes to each of them separately which increases complexity.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-17T21:30:46Z

> even though the Workload is a child of a Job, currently Kueue allows the Workload's .spec.active field the ability to deactivate the Workload, which will ultimately terminate the pods owned by the Job. We could follow a similar pattern with a replicas field defined solely in the Workload without the requiring this field in the Job.

The termination of these pods is not the responsibility of Kueue (workload api) but the workload controller (job, deployment, etc). So Kueue mainly says you can change the active and then kueue controller would "pause" the workload and the controller reacts to that change.

I don't disagree with the idea of using scale for Kueue but it may have to be done by adding support for a scale resource in your workload of choice. 

https://github.com/kubernetes-sigs/kueue/issues/2964 for another example.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-17T21:32:28Z

> The benefit of this approach is that it will work across all types of jobs, and the logic would be centralised in the workload controller. The alternative to this would be to implement this on each type of job, which would require to add logic and API changes to each of them separately which increases complexity.

IMO this is not really a benefit as each workload has to decide what "scale" actually means. Having this logic in Kueue is not very easy to support.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-17T21:38:54Z

That being said, for workloads that have scale (deployment, statefulset), I think supporting scale and Kueue should be considered in scope.

But it does overlap with https://github.com/kubernetes-sigs/kueue/issues/77

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-23T10:16:49Z

>I don't disagree with the idea of using scale for Kueue but it may have to be done by adding support for a scale resource in your workload of choice.

I understand, that could be another option, where the [KEDA's `ScaledObject`](https://keda.sh/docs/2.16/reference/scaledobject-spec/) targets the workload of choice directly and scales the replicas down or up. If this is the case, perhaps no additional logic is required in Kueue.

>The benefit of this approach is that it will work across all types of jobs, and the logic would be centralised in the workload controller. The alternative to this would be to implement this on each type of job, which would require to add logic and API changes to each of them separately which increases complexity.
>>IMO this is not really a benefit as each workload has to decide what "scale" actually means. Having this logic in Kueue is not very easy to support.

Maybe I'm not understanding, what I mean is that scaling could happen in the Workload CR and not in any other CR.  Hence why the logic could be maintained only in the Workload Controller, and work for all types of jobs. I.e., `ScaledObject`:
```
spec:
  scaleTargetRef:
    apiVersion: kueue.x-k8s.io/v1beta1
    name: workload-raycluster-8d6e3
    kind: Workload
```

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-23T10:24:54Z

>That being said, for workloads that have scale (deployment, statefulset), I think supporting scale and Kueue should be considered in scope.

These types of workloads (deployments, statefulsets), they already have the `subresource.scale` properties and `replicas` field. Meaning, I believe KEDA can work with them OOTB. However, scaling would happen on the deployment or statefulset CRs directly. The reason for aiming to scale the Workload CR instead, is to have a single centralised way of deactivating the workload, regardless of their type (Jobs, Deployments, RayClusters, etc).

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-24T14:07:51Z

@kannon92 let me know what you think, thank you!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-24T14:13:06Z

> The reason for aiming to scale the Workload CR instead, is to have a single centralised way of deactivating the workload, regardless of their type (Jobs, Deployments, RayClusters, etc).

Looking at our controller job for each framework, we already implement different approaches for each controller for Stop. I think that each controller should decide how they can stop their workloads.

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-24T14:41:40Z

I see. Perhaps in the case of long-running workloads that don't yet expose the `/scale` endpoint, such as RayClusters, we could make the additions to the RayCluster API to integrate with KEDA. Scaling the `replicas` would be done on the RayCluster CR itself. It could follow a similar pattern where the "global" replicas field of the RayCluster determines whether the pods should be scaled-to-zero or not based on metrics retrieved by KEDA.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-23T15:06:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-22T15:31:58Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-21T15:41:50Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-21T15:41:56Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4927#issuecomment-3316074974):

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
