# Issue #2973: Promote VisibilityOnDemand to Beta

**Summary**: Promote VisibilityOnDemand to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2973

**Last updated**: 2024-09-23T10:04:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T09:23:20Z
- **Updated**: 2024-09-23T10:04:01Z
- **Closed**: 2024-09-23T10:04:01Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 25

## Description

**What would you like to be added**:

Promote the VisibilityOnDemand to Beta.

**Why is this needed**:

1. the feature is assumed to be enabled by kueuectl "POSITION IN QUEUE" column in the `kueuectl list workload` command
2. The feature is in alpha quite long already
3. The enablement involves 2 steps which is sometimes confusing to users

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T09:23:46Z

/cc @mwielgus @mwysokin @PBundyra @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T10:06:00Z

From the graduation criteria:
> Release the API in beta and guarantee backwards compatibility,

This is the objective of the change.

> Reconsider introducing a throttling mechanism based on user and review feedback,

I'm not aware of users' feedback to justify the effort. We can move it to GA criteria.

> Consider introducing FlowScheme and PriorityLevelConfiguration to allow admins to easily tune API priorities.

Similar, I'm not aware of the feedback to justify the effort, I would suggest moving it to criteria for GA.

There were also ideas for new endpoints like https://github.com/kubernetes-sigs/kueue/pull/2145, but it is not clear they are needed for now. I think we should be ok to graduate the API we have. We should be good to still add the new endpoints while in Beta if needed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-04T12:23:48Z

An important question when graduating is whether we want to include `visibility-api.yaml` as part of the main YAML.
I suppose there are no downsides.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-06T12:10:00Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T12:22:09Z

> An important question when graduating is whether we want to include `visibility-api.yaml` as part of the main YAML.
> I suppose there are no downsides.

I see no downsides, so I would embed it for simplicity of deployment.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-06T12:38:52Z

@mimowo @alculquicondor What about QueueVisibility? Should we graduate it too?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T12:43:08Z

No, we aim to deprecate it, and remove in the long run.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-06T14:33:13Z

Shouldn't we add some guard that we planned in the design phase? 
https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-2-pending-workloads-visibility#graduation-criteria

IIUC, the current visibility endpoint, is not guarded by any mechanism. So, at least, I think it would be better to provide APF configurations, and it would be nice to have a throttling mechanism.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-06T14:36:45Z

If we do not provide any guards for the kube-apiserver, I guess that the internet-exposed kube-apiserver faces some dangers.

Indeed, if we want to use the MultiKueue, we need to create a public k8s cluster, not a supported private cluster, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T15:01:48Z

> IIUC, the current visibility endpoint, is not guarded by any mechanism. So, at least, I think it would be better to provide APF configurations, and it would be nice to have a throttling mechanism.

I think there is a basic protection mechanism by APF, assigning one unit (seat) to every request. This may not be very accurate as listing workload may take proportionally more time.

> Indeed, if we want to use the MultiKueue, we need to create a public k8s cluster, not a supported private cluster, right?

I'm not sure how MultiKueue changes that. The single regular clusters might be public, but there is authentication which would prevent external actors.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-06T15:18:35Z

But I agree it requires some extra research. In particular, I it would be good to refresh the knowledge on the default protection mechanism, and see how much effort there is to provide a dedicated FlowSchema.

So, I would suggest to record the findings in the KEP first before the code PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T15:37:44Z

> I think there is a basic protection mechanism by APF, assigning one unit (seat) to every request. This may not be very accurate as listing workload may take proportionally more time.

I guess that it would be better to provide the kueue-sysytem namespace dedicated FlowSchema so that we can prevent the kueue-manager occupies the kube-apiserver seats when the visibility endpoints are attacked by malicious people.
But, before we introduce the FlowSchema, we need to investigate a little bit if the mechanism improves the problems.

> The single regular clusters might be public, but there is authentication which would prevent external actors.

Yes, that's right. But, even if the malicious people do not have the credentials to access the kube-apiserver, they can give high load to kube-apiserver via visibility endpoints.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T15:43:53Z

> I guess that it would be better to provide the kueue-sysytem namespace dedicated FlowSchema so that we can prevent the kueue-manager occupies the kube-apiserver seats when the visibility endpoints are attacked by malicious people.
But, before we introduce the FlowSchema, we need to investigate a little bit if the mechanism improves the problems.

@mbobrovskyi is investigating this, and will summarize the findings, but from what we see the default `global-default` schema of the P&F mechanism protects the endpoint. Yes, we can introduce a custom FlowSchema or Kueue, but it is a complication and I'm not sure it is needed. We don't have any feedback from users that the built-in mechanism is not enough.

> Yes, that's right. But, even if the malicious people do not have the credentials to access the kube-apiserver, they can give high load to kube-apiserver via visibility endpoints.

I don't think you can query the visibility endpoints without credentials, I would assume this would be bad and is not allowed. However, we may do an experiment on a life cluster to confirm.

EDIT: note that the custom endpoints are exposed by the kube-apiserver via the [aggregation layer](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/), not directly, so the authentication & authorization mechanism is in place, similarly as the P&F.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T15:48:49Z

Anyway, we can discuss this after the summary is made public.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T17:40:17Z

I have confirmed that on GKE (and @mbobrovskyi checked on Kind) that the requests to the custom endpoint are authorized. In particular, I run:

```
curl -kH "Authorization: Bearer $ACCESS_TOKEN" -H "Accept: application/json" "https://$CLUSTER_ENDPOINT/apis/visibility.kueue.x-k8s.io/v1alpha1/clusterqueues/cluster-queue/pendingworkloads"
```
returns me results, while if I remove the `Authorization` header I get:
```
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "nodes is forbidden: User \"system:anonymous\" cannot list resource \"nodes\" in API group \"\" at the cluster scope",
  "reason": "Forbidden",
  "details": {
    "kind": "nodes"
  },
  "code": 403
}        
```
I get the analogous error for other built-in endpoints, such as `https://$CLUSTER_ENDPOINT/api/v1/nodes`

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-11T17:46:39Z

Yes, the Visibility API endpoints are protected by default with `global-default` `FlowSchema` and `PriorityLevelConfiguration`. Below is the configuration for both:

```
apiVersion: flowcontrol.apiserver.k8s.io/v1
kind: FlowSchema
metadata:
  annotations:
    apf.kubernetes.io/autoupdate-spec: "true"
  name: global-default
spec:
  distinguisherMethod:
    type: ByUser
  matchingPrecedence: 9900
  priorityLevelConfiguration:
    name: global-default
  rules:
  - nonResourceRules:
    - nonResourceURLs:
      - '*'
      verbs:
      - '*'
    resourceRules:
    - apiGroups:
      - '*'
      clusterScope: true
      namespaces:
      - '*'
      resources:
      - '*'
      verbs:
      - '*'
    subjects:
    - group:
        name: system:unauthenticated
      kind: Group
    - group:
        name: system:authenticated
      kind: Group
---
apiVersion: flowcontrol.apiserver.k8s.io/v1
kind: PriorityLevelConfiguration
metadata:
  annotations:
    apf.kubernetes.io/autoupdate-spec: "true"
  name: global-default
spec:
  limited:
    lendablePercent: 50
    limitResponse:
      queuing:
        handSize: 6
        queueLengthLimit: 50
        queues: 128
      type: Queue
    nominalConcurrencyShares: 20
  type: Limited
```

I found it when I tried executing a large number of parallel requests to `kubectl get --raw /apis/visibility.kueue.x-k8s.io/v1alpha1/clusterqueues/cluster-queue/pendingworkloads`. 

The `kubectl get --raw /debug/api_priority_and_fairness/dump_priority_levels` return a table with column `DispatchedRequests` that show us how much requests we have for this configuration.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-11T19:09:08Z

The `LimitResponse` type in `PriorityLevelConfiguration` can be set to one of two options:
  - `Reject`: Excess traffic is immediately rejected with an HTTP 429 (Too Many Requests) error.
  - `Queue`: Requests exceeding the threshold are placed in a queue."

The `global-default` configuration uses the `Queue` type. This means that if there is a high volume of requests, they will be added to a queue and wait for their turn to be processed. 

This is an example that what I have:

```
kubectl get --raw /debug/api_priority_and_fairness/dump_priority_levels 
PriorityLevelName, ActiveQueues, IsIdle, IsQuiescing, WaitingRequests, ExecutingRequests, DispatchedRequests, RejectedRequests, TimedoutRequests, CancelledRequests
catch-all,         0,            true,   false,       0,               0,                 39,                 0,                0,                0
exempt,            0,            true,   false,       0,               0,                 2290,               0,                0,                0
global-default,    4,            false,  false,       57,              368,               23614,              1533,             0,                609
leader-election,   0,            true,   false,       0,               0,                 1170,               0,                0,                0
node-high,         0,            true,   false,       0,               0,                 743,                0,                0,                0
system,            0,            true,   false,       0,               0,                 557,                0,                0,                0
workload-high,     0,            true,   false,       0,               0,                 1706,               0,                0,                0
workload-low,      0,            true,   false,       0,               0,                 4595,               0,                0,                0
```

And also the `apiserver_flowcontrol_rejected_requests_total` metrics that what I have:

```
# This one rejected because queue full
apiserver_flowcontrol_rejected_requests_total{endpoint="https", flow_schema="global-default", instance="172.18.0.4:6443", job="apiserver", namespace="default", priority_level="global-default", reason="queue-full", service="kubernetes"} | 924
-- | --
# This one rejected due to time-out
apiserver_flowcontrol_rejected_requests_total{endpoint="https", flow_schema="global-default", instance="172.18.0.4:6443", job="apiserver", namespace="default", priority_level="global-default", reason="time-out", service="kubernetes"} | 719
```

Possible rejection: 
- `queue-full`, indicating that too many requests were already queued.
- `concurrency-limit`, indicating that the PriorityLevelConfiguration is configured to reject rather than queue excess requests.
- `time-out`, indicating that the request was still in the queue when its queuing time limit expired.
- `cancelled`, indicating that the request is not purge locked and has been ejected from the queue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-11T20:16:19Z

> I guess that it would be better to provide the kueue-sysytem namespace dedicated FlowSchema so that we can prevent the kueue-manager occupies the kube-apiserver seats when the visibility endpoints are attacked by malicious people.
But, before we introduce the FlowSchema, we need to investigate a little bit if the mechanism improves the problems.

I think you right, it should help. We will have different queues that allow us to do not block `kube-system` or another namespaces when `kueue-system` namespace is overloaded. I also tested this scenario, and it worked well.

Just a question. Should we have dedicated `FlowSchema` for `kube-system` namespace or just for Visibility API?  WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T11:11:30Z

> I think you right, it should help. We will have different queues that allow us to do not block `kube-system` or another namespaces when `kueue-system` namespace is overloaded. I also tested this scenario, and it worked well.
> 
> Just a question. Should we have dedicated `FlowSchema` for `kube-system` namespace or just for Visibility API? WDYT?

If we can configure the FlowScheme only for the visibility endpoint, it would be great since we want to continue the Kueue operation when the visibility endpoints are attacked by malicious people.

Is it possible to configure the FliowScheme only for visibility endpoints?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T11:14:20Z

The main problem is that the visibility endpoints use the global-defaults FlowScheme since most of the controllers and workloads belong to the global defaults. So, when the global-defaults are occupied by the visibility endpoints, the cluster admin and batch users will lose way to operate cluster and themselves Jobs.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-13T12:11:10Z

> Is it possible to configure the FliowScheme only for visibility endpoints?

Yes, we can configure for `visibility.kueue.x-k8s.io` API group. I can prepare PR for it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T12:15:34Z

> > Is it possible to configure the FliowScheme only for visibility endpoints?
> 
> 
> 
> Yes, we can configure for `visibility.kueue.x-k8s.io` API group. I can prepare PR for it.

Thank you for letting me know. Could you wait for a while?

Actually, we are investigating the cloud provider specifications for FlowScheme. After we resolve some questions, @mimowo will comment here or KEP PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-13T12:59:10Z

> > > Is it possible to configure the FliowScheme only for visibility endpoints?
> > 
> > 
> > Yes, we can configure for `visibility.kueue.x-k8s.io` API group. I can prepare PR for it.
> 
> Thank you for letting me know. Could you wait for a while?
> 
> Actually, we are investigating the cloud provider specifications for FlowScheme. After we resolve some questions, @mimowo will comment here or KEP PR.

Let's continue the discussion at https://github.com/kubernetes-sigs/kueue/pull/3032#discussion_r1758821963.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-18T10:32:51Z

@mimowo @tenzen-y 

It's a lot of task related to this issue. We should merge them in this order:

- [x] https://github.com/kubernetes-sigs/kueue/pull/3032
- [x] https://github.com/kubernetes-sigs/kueue/pull/3083
- [x] https://github.com/kubernetes-sigs/kueue/pull/3086
- [x] https://github.com/kubernetes-sigs/kueue/pull/3043
- [x] https://github.com/kubernetes-sigs/kueue/pull/3084
- [x] https://github.com/kubernetes-sigs/kueue/pull/3097
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3008

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-18T10:40:18Z

We still have a pending discussion about including P&F config: https://github.com/kubernetes-sigs/kueue/pull/3043#discussion_r1760626660. I think we may need to rework the PR to put it in docs, and update the KEP.
