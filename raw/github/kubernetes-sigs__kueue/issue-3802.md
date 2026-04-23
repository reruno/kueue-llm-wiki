# Issue #3802: [MultiKueue] Support Deployment Integration

**Summary**: [MultiKueue] Support Deployment Integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3802

**Last updated**: 2025-07-09T11:57:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Bobbins228](https://github.com/Bobbins228)
- **Created**: 2024-12-10T16:59:46Z
- **Updated**: 2025-07-09T11:57:13Z
- **Closed**: 2025-07-09T11:55:24Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 20

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The ability to create Kubernetes deployments on remote Clusters through MultiKueue
**Why is this needed**:

Support for various integrations already exist i.e. Jobset, KubeFlow Jobs, MPI, Batch. 
Our use case is for long running model serving deployments that can be created remotely from a Manager Cluster.

**Completion requirements**:

Deployments can be created/managed locally on the Manager Cluster and through MultiKueue created/managed on the Worker Cluster(s) without the risk of running on the Manager.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T07:25:39Z

cc @mwielgus @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-11T15:48:25Z

In the ideal solution, I think that we need to implement the managedBy field in all workload objects like Deployment and StatefulSet. 

@mimowo Do you have any concerns about implementing the managedBy feature same as the batch/v1 Job?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T15:58:43Z

We don't know yet the best path forward, from the initial discussion with @mwielgus we would like to support MultiKueue for Pods. Then, Deployement and StatefulSet integrations would work for free. The users using pod integration could also benefit. The problem is how to achieve "managedBy" for pods. The initial ideas we discussed:
1. gate the pod on the management cluster and block status updates 
2. gate the pod on the management cluster and support status updates
3. schedule the pod on the management cluster, but on a virtual MultiKueue node

1, might will work ok, but might not be transparent to the end-users. 2 is relatively simple technically, but the issue is that we update the status, while the pod is gated, which might be violating the Pod API. 3. is harder, but would allow to update the Pod status without tricks.

### Comment by [@Bobbins228](https://github.com/Bobbins228) — 2025-01-06T15:21:50Z

@mimowo Can you elaborate a bit more on option 3? Not entirely sure what you mean by a virtual MultiKueue node. Thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T09:00:56Z

@Bobbins228 sure.

In this idea we would have a dedicated single "virtual" node (without real kubelet, just Node API object, could be called "multikueue-virtual-node"). On the management cluster Kueue would bind the pods managed by MultiKueue to that node (resulting in the "spec.NodeName=multikueue-virtual-node". Then, MultiKueue would take the responsibility of Kubelet and update the Pod status based on the worker cluster.

### Comment by [@Bobbins228](https://github.com/Bobbins228) — 2025-01-13T14:44:14Z

@mimowo With future AppWrapper MultiKueue support would we not run into the same issues with updating individual statuses of the Kubernetes Objects created through AppWrapper?  
For example if I created a Pod using an AppWrapper from the Manager cluster I would not be able to get that Pod's up to date status from the remote?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-13T14:51:49Z

cc @dgrove-oss to keep me honest here, but I believe the AppWrapper integration for MultiKueue should work the same way as other CRDs. 

For other CRDs, like Job or JobSet, we use the `spec.managedBy` field to skip reconciling the API object on the management cluster, and as a consequence, avoid creation of pods on the management cluster. So, in that case the pods will only be created on the worker clusters and they will have the correct status. The status of the API object is copied from the worker cluster to the management cluster by MultiKueue - so the [AppWrapperStatus](https://github.com/project-codeflare/appwrapper/blob/d9c34c21ccf2ba7cf22cb981baf9492367380eaa/api/v1beta2/appwrapper_types.go#L86C6-L86C22) will be "mirrored" only.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-13T15:01:50Z

> cc @dgrove-oss to keep me honest here, but I believe the AppWrapper integration for MultiKueue should work the same way as other CRDs.
> 
> For other CRDs, like Job or JobSet, we use the `spec.managedBy` field to skip reconciling the API object on the management cluster, and as a consequence, avoid creation of pods on the management cluster. So, in that case the pods will only be created on the worker clusters and they will have the correct status. The status of the API object is copied from the worker cluster to the management cluster by MultiKueue - so the [AppWrapperStatus](https://github.com/project-codeflare/appwrapper/blob/d9c34c21ccf2ba7cf22cb981baf9492367380eaa/api/v1beta2/appwrapper_types.go#L86C6-L86C22) will be "mirrored" only.

This matches my understanding of how it should work. We've implemented  a `spec.managedBy` in AppWrapper to support Multi-Kueue.  So the integration should work just like any other CRD that has a managedBy.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-01-13T17:34:05Z

@dgrove-oss @mimowo - Thanks for the inputs! This would be helpful!

Would upstream still be interested in exploring Option 3 of providing direct Pod integration in Kueue? @Bobbins228 and I have been working on getting a PoC ready with a virtual node and wanted to check if it would be beneficial to have direct integration support or the suggestion would be to use AppWrapper and create pods/deployments/SS underneath it?

One plus point of having direct pod integration would be to be able to manage serving workloads directly on MK though we are still to figure out how to schedule pods belonging to a single Deployment/SS on multiple clusters (even with Option 3) to get the true benefit.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-14T08:07:17Z

@varshaprasad96 we are definitely looking forward for native support of Pods in MultiKueue. 

The main reason being the ability to integrate MultiKueue with 3-party frameworks or in-house software which would otherwise need to be modified to use AppWrapper (which is a point of friction for many surely).

Also:
- IIUC the partial preemption of Deployments would not work when wrapped in AppWrapper, whilst it can be easily work via Pods
- some users may want to actually be able to create the "suspended" pods locally, and fetch the logs of the Pods from the MultiKueue worker cluster, allowing to retrieve logs from worker clusters via `kubectl logs`, somewhat similar to: https://github.com/kubernetes-sigs/kueue/issues/3526

As for the implementation, I think it is also reasonable to start with (2.) using a dedicated scheduling gate, and only later implement (3.) when proven to be needed - as this seems more involving.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-01-14T09:33:38Z

@mimowo Thanks for the input! We were exploring the use of [virtual-kubelet](https://github.com/virtual-kubelet/virtual-kubelet) to create virtual nodes and schedule pods + sync status for them. But as you mentioned, Option 2, is way more easier, and if #3526 is implemented that would fit the use case pretty well.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T14:42:45Z

As discussed on the PR https://github.com/kubernetes-sigs/kueue/pull/4034#pullrequestreview-2569714297 the next step would be to use a dedicated scheduling gate so that we can transition the AdmissionCheck to Ready when we make the pod running. 

I believe (3.) from https://github.com/kubernetes-sigs/kueue/issues/3802#issuecomment-2536397425 could be addressed as a separate issue, maybe as part of https://github.com/kubernetes-sigs/kueue/issues/3526 (but not sure).

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-03-31T14:59:13Z

If we create one workload object in the worker cluster per pod, how can we ensure advanced scheduling constructs like colocation of all deployment in a single cluster or is this something outside the scope of multikueue or kueue in general?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-31T15:09:04Z

I think this is very much in the scope. I would like to have two modes of scheduling a Deployment in MultiKueue - one by pod and also by the whole deployment level. we could determine which mode to choose by analogy annotation on the deployment for example.

### Comment by [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla) — 2025-03-31T15:21:13Z

This is exactly, how we intend to solve the colocation problem in our clusters as well, (with an annotation or well defined label). If folks are interested, one of us either (https://github.com/atosatto or I) can get started on the design and implementation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-31T15:25:13Z

it will be awesome, the only downside I see is lack of scaling, but we can block it by webhook. not sure how to enable clocation via single workload + scaling, but it is not a blocker to me. 

cc @mwielgus @mwysokin

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-04T03:34:40Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-09T11:47:02Z

Any reason to keep this open?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T11:54:25Z

There was mentioned in some comments colocation of Deployment Pods in one cluster. 

However, this is a bit of scope creep compared to the original issue, so I'm ok to close this and open a dedicated one.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-09T11:57:13Z

> There was mentioned in some comments colocation of Deployment Pods in one cluster.
> 
> However, this is a bit of scope creep compared to the original issue, so I'm ok to close this and open a dedicated one.

Indeed, we already have a dedicated one: https://github.com/kubernetes-sigs/kueue/issues/5734
