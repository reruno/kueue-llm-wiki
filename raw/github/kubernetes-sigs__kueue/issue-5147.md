# Issue #5147: Expose TAS detected topology domains

**Summary**: Expose TAS detected topology domains

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5147

**Last updated**: 2026-04-16T06:33:33Z

---

## Metadata

- **State**: open
- **Author**: [@avrittrohwer](https://github.com/avrittrohwer)
- **Created**: 2025-05-01T16:39:37Z
- **Updated**: 2026-04-16T06:33:33Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Have the ability for Kueue to expose TAS detected topology domains.  For example, with TAS config:

```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "cloud.provider.com/topology-rack"
  - nodeLabel: "kubernetes.io/hostname"
---
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta1
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    cloud.provider.com/node-group: "tas-node-group"
  topologyName: "default"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 64
```

Deployed in a cluster with 2 racks of 4 nodes, each node having 8 GPUs, Kueue could expose:

```
detectedTopologies:
- clusterQueueName: "tas-cluster-queue"
  resourceFlavors:
  - name: "tas-flavor"
    levels:
    - nodeLabel: "cloud.provider.com/topology-rack"
      domains:
      - labelValue: "rack-0"
        nodes: 4
        availableQuota: 32
      - labelValue: "rack-1"
        nodes: 4
        availableQuota: 32
    - nodeLabel: "kubernetes.io/hostname"
      domains:
      - labelValue: "rack-0-node-0"
        nodes: 1
        availableQuota: 8
      - labelValue: "rack-0-node-1"
        nodes: 1
        availableQuota: 8
        ...
      - labelValue: "rack-1-node-3"
        nodes: 1
        availableQuota: 8
```

If rack-0-node-0 became unhealthy:

```
detectedTopologies:
- clusterQueueName: "tas-cluster-queue"
  resourceFlavors:
  - name: "tas-flavor"
    levels:
    - nodeLabel: "cloud.provider.com/topology-rack"
      domains:
      - labelValue: "rack-0"
        nodes: 4
        availableQuota: 24
      - labelValue: "rack-1"
        nodes: 4
        availableQuota: 32
    - nodeLabel: "kubernetes.io/hostname"
      domains:
      - labelValue: "rack-0-node-0"
        nodes: 1
        availableQuota: 0
      - labelValue: "rack-0-node-1"
        nodes: 1
        availableQuota: 8
        ...
      - labelValue: "rack-1-node-3"
        nodes: 1
        availableQuota: 8
```

If rack-0-node-0 unregistered from the cluster:

```
detectedTopologies:
- clusterQueueName: "tas-cluster-queue"
  resourceFlavors:
  - name: "tas-flavor"
    levels:
    - nodeLabel: "cloud.provider.com/topology-rack"
      domains:
      - labelValue: "rack-0"
        nodes: 3
        availableQuota: 24
      - labelValue: "rack-1"
        nodes: 4
        availableQuota: 32
    - nodeLabel: "kubernetes.io/hostname"
      domains:
      - labelValue: "rack-0-node-1"
        nodes: 1
        availableQuota: 8
        ...
      - labelValue: "rack-1-node-3"
        nodes: 1
        availableQuota: 8
```

**Why is this needed**:

This feature would help Kueue Admins ensure TAS is detecting the intended topology domains and would help aid in debugging workloads not getting admitted due to fewer nodes detected than expected  (unhealthy node, misconfigured topology labels, etc).  It would also enable better visualization of detected topologies and their utilization by tools like kueue-viz.

**Completion requirements**:

1. **Decide where the information should be exposed**:  This API has the potential to return very large responses in clusters with lots of nodes that use  kubernetes.io/hostname as a topology level.  It is likely infeasible to put this information in ClusterQueue status due to etcd object size limitations.  This seems a good candidate for an on-demand API like the Pending Workloads on-demand API: https://kueue.sigs.k8s.io/docs/tasks/manage/monitor_pending_workloads/pending_workloads_on_demand/
2. **Decide on supported query parameters**: Give the potential for large API responses, we should support filtering returned TAS information to specific cluster queues, topology levels, any other?
3. **Decide the response format**: in my above examples I had a flat hierarchy based on topology level.  An alternative could be a tree hierarchy like:
   ```
   detectedTopologies:
   - clusterQueueName: "tas-cluster-queue"
     resourceFlavors:
     - name: "tas-flavor"
       levels:
       - nodeLabel: "cloud.provider.com/topology-rack"
         domains:
         - labelValue: "rack-0"
           nodes: 4
           availableQuota: 32
           subLevels:
           - nodeLabel: "kubernetes.io/hostname"
             domains:
             - labelValue: "rack-0-node-0"
               nodes: 1
               availableQuota: 8
               ...
             - labelValue: "rack-0-node-3"
               nodes: 1
               availableQuota: 8
         - labelValue: "rack-1"
           nodes: 4
           availableQuota: 32
           subLevels:
           - nodeLabel: "kubernetes.io/hostname"
             domains:
             - labelValue: "rack-1-node-0"
               nodes: 1
               availableQuota: 8
               ...
             - labelValue: "rack-1-node-3"
               nodes: 1
               availableQuota: 8
   ```
4. **Decide on response information**: the API could also return what workloads are reserving quota.  Would this be useful?

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-05-01T16:45:08Z

This is meant be a starting point for conversation on how to add some visibility into Kueue's TAS internal state, I haven't deeply thought about the response format

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-05-01T16:45:52Z

Related PR: https://github.com/kubernetes-sigs/kueue/pull/4295

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-05-01T16:46:20Z

Related logging ask: https://github.com/kubernetes-sigs/kueue/issues/4091

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T19:55:20Z

Instead of cq status, couldn't we store the information in Topology?
This cq status is much bigger and could bring conflicts during cq status updates, then retrigger the reconciliations much more.

Additionally, the detected actual topology information is deeply tied to Topology resources.
Instead of aggregating cq and topology usages in kueue side, we should just store the actual topology information in Topology, and then consumers like kueue-viz should aggregate cq and topology by themselves.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-05T06:38:16Z

I like this proposal. cc @mwielgus @mwysokin 

> Decide where the information should be exposed

This information belongs to the RF-level. This is because the set of nodes is constrained both by the presence of the Topology labels, and the ResourceFlavor fields, such as spec.nodeLabels, spec.nodeTaints.

This information could be exposed either via ResourceFlavor status, or the visibility API. Given the potential size of the responses and frequent updates, I think the visibility API might be a better fit.

> Decide on supported query parameters:

If we are going to have query parameters, then it needs to be the visibility API.

> Decide the response format:

The examples for format look ok-ish, I'm still not sure about:
- the format assumes only one resource is returned, however, the underlying structure may depend on multiple resources
- the word "quota" may be misleading since we also support regular quota in TAS, maybe we call it "capacity"
- subLevels is a recursive field, I'm not sure if there are examples of that in k8s. We could also consider a format more similar to the TopologyAssignment in workload.status API.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:24:49Z

> > Decide on supported query parameters:
> 
> If we are going to have query parameters, then it needs to be the visibility API.

+1 on visibility API since scraping and aggregating this information and updating object status has higher costs, and I could easily imagine the operation rapidly increasing resource versions, which means it causes conflicts on update operations.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T07:02:35Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-04T07:41:02Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T09:02:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-02T09:52:26Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T10:05:15Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-02T11:03:40Z

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

### Comment by [@samzong](https://github.com/samzong) — 2026-03-08T15:36:14Z

@mimowo @tenzen-y 

I also ran into the lack of Topology visibility in kueueviz, and I think this is worth addressing. 

I need a bit more time to work through what the right Topology-facing shape is so kueueviz can consume it cleanly, but I’m interested in pushing this forward. 

If anyone wants to help, I’d be happy to continue driving this issue until we can easily inspect the full topology, along with its health and load, from kueueviz.

<img width="3770" height="1306" alt="Image" src="https://github.com/user-attachments/assets/e19f4b94-4b28-4dc3-9575-10a81215a052" />

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-07T16:47:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-16T06:33:26Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-16T06:33:33Z

cc @amy
