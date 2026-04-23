# Issue #4038: Make it easy to describe the preempting workload

**Summary**: Make it easy to describe the preempting workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4038

**Last updated**: 2025-03-10T12:43:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@avrittrohwer](https://github.com/avrittrohwer)
- **Created**: 2025-01-22T20:12:23Z
- **Updated**: 2025-03-10T12:43:48Z
- **Closed**: 2025-03-10T12:43:48Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 38

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make it easy to `kubectl describe` the workload that evicted another workload.

**Why is this needed**:

Kueue Workloads have events like `kueue-admission  Preempted to accommodate a workload (UID: <UID>) due to fair sharing within the cohort`

As far as I can tell kubectl --selector field only supports filtering on values in the object .metadata.labels.  The Workload UID is in the .metadata.UID field which can not be filtered on by kubectl --selector.   For clusters with few workloads grepping on kubectl get workloads -A would work but does not scale for clusters with thousands of workloads.

**Completion requirements**:

Make it easy to `kubectl describe` the Workload that preempted another workload.  Simple solution: add the Workload UID to the Workload labels.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ x] Docs update -> add docs on how to get details of preempting workload.

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-23T14:38:03Z

Have you looked at kueuectrl? maybe the UX would be better using the CLI?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T14:47:13Z

I don't remember if kueuectl would allow it, probably not. However, in any case as an external binary the only way to find the preempting workload by UID would be to list all workloads first, which is not scalable indeed.

I like the idea of adding the UID as a label. cc @tenzen-y WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-27T08:02:42Z

> I don't remember if kueuectl would allow it, probably not. However, in any case as an external binary the only way to find the preempting workload by UID would be to list all workloads first, which is not scalable indeed.
> 
> I like the idea of adding the UID as a label. cc [@tenzen-y](https://github.com/tenzen-y) WDYT?

Thank you for creating this issue. IMO, instead of label with UID, I would propose the CRD field-selector: https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/4358-custom-resource-field-selectors

Have you checked if we can implement a custom field selector for Workload by the feature?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T08:55:24Z

> Have you checked if we can implement a custom field selector for Workload by the feature?

I have not checked this myself. It might be worth trying as an alternative, but not sure this works with `metadata.ownerReferences.uid`. Actually, I see we are indexing the field already in Kueue, but this is in-memory only: https://github.com/kubernetes-sigs/kueue/blob/b9aa1c39d0097ae24a526d41f95bf662dfe5607c/pkg/controller/core/indexer/indexer.go#L40

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-28T10:01:30Z

> > Have you checked if we can implement a custom field selector for Workload by the feature?
> 
> I have not checked this myself. It might be worth trying as an alternative, but not sure this works with `metadata.ownerReferences.uid`. Actually, I see we are indexing the field already in Kueue, but this is in-memory only:
> 
> [kueue/pkg/controller/core/indexer/indexer.go](https://github.com/kubernetes-sigs/kueue/blob/b9aa1c39d0097ae24a526d41f95bf662dfe5607c/pkg/controller/core/indexer/indexer.go#L40)
> 
> Line 40 in [b9aa1c3](/kubernetes-sigs/kueue/commit/b9aa1c39d0097ae24a526d41f95bf662dfe5607c)
> 
>  OwnerReferenceUID          = "metadata.ownerReferences.uid"

I see. In that case, can we try confirming if the custom CRD field is selected? This can be confirmed easily, IMO.
After we confirm the CRD field selector is not runnable, we can add an owner to the label.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T10:43:12Z

sgtm, we can start by checking if the https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/4358-custom-resource-field-selectors#proposal can be used to filter the workloads first

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-01-28T23:45:36Z

Looks like controllergen has support for a `+kubebuilder:selectablefield` marker: https://github.com/kubernetes-sigs/controller-tools/issues/1039

However the Workload UID comes from k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta (https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1beta1/workload_types.go#L616) so I'm not sure how we could add that marker

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T06:22:49Z

Actually, I think in this use-case we need to index `metadata.uid` which is a scalar, so it's worth checking if `+kubebuilder:selectablefield` can be used.

Also, I synced with @deads2k and the KEP only supports scalar fields, so it would not work for `metadata.ownerReferences` which is a list (but IIUC it is not necessary in our case).

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-02-05T21:37:41Z

Looked into the selectableFileds some more.  JSON paths into metadata are explicitly now allowed, from https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#selectablefield-v1-apiextensions-k8s-io:

> Must not point to metdata fields.

Which aligns with the proposal KEP validation rules section: https://github.com/kubernetes/enhancements/blob/master/keps/sig-api-machinery/4358-custom-resource-field-selectors/README.md#validation-rules

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-07T11:49:02Z

> https://github.com/kubernetes/enhancements/blob/master/keps/sig-api-machinery/4358-custom-resource-field-selectors/README.md#validation-rules

I'm currently a slightly confusing since the KEP uses metadata fields as examples: https://github.com/kubernetes/enhancements/blob/master/keps/sig-api-machinery/4358-custom-resource-field-selectors/README.md#openapi-discovery

And they mention `may not` in `selectableFields may not refer to metadata fields.`
Have you seen any validation errors if you add uid fieldSelector to any objects?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-02-07T18:05:19Z

@tenzen-y yes I tested out in https://github.com/kubernetes-sigs/kueue/compare/main...avrittrohwer:kueue:log.

Validation error when applying the CRD to a 1.31 kind cluster:

```
The CustomResourceDefinition "workloads.kueue.x-k8s.io" is invalid: spec.selectableFields[0].jsonPath: Invalid value: ".metadata.UID": is an invalid path: does not refer to a valid field
make: *** [Makefile:235: install] Error 1
```

I tested with // +kubebuilder:selectablefield:JSONPath=\`.spec.queueName\` which worked so I think the issue is with the metadata json path

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-10T16:08:56Z

> [@tenzen-y](https://github.com/tenzen-y) yes I tested out in [main...avrittrohwer:kueue:log](https://github.com/kubernetes-sigs/kueue/compare/main...avrittrohwer:kueue:log).
> 
> Validation error when applying the CRD to a 1.31 kind cluster:
> 
> ```
> The CustomResourceDefinition "workloads.kueue.x-k8s.io" is invalid: spec.selectableFields[0].jsonPath: Invalid value: ".metadata.UID": is an invalid path: does not refer to a valid field
> make: *** [Makefile:235: install] Error 1
> ```
> 
> I tested with // +kubebuilder:selectablefield:JSONPath=`.spec.queueName` which worked so I think the issue is with the metadata json path

Thank you for confirming that! As I can check impl, it seems to be correct...
https://github.com/kubernetes/kubernetes/blob/15a186a888dc2e908681c876e321468b8d32a37b/staging/src/k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/validation/validation.go#L830-L832

Lets's add annotation if @mimowo does not have any objections.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T16:13:21Z

> Lets's add annotation if @mimowo does not have any objections.

You mean the "UID" label? Sure we can do it, and mark it as immutable since UIDs are immutable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-10T16:22:39Z

> > Lets's add annotation if [@mimowo](https://github.com/mimowo) does not have any objections.
> 
> You mean the "UID" label? Sure we can do it, and mark it as immutable since UIDs are immutable.

Yeah, I meant UID label.

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-02-21T00:58:28Z

@mimowo  @tenzen-y  I took an initial pass at this in https://github.com/kubernetes-sigs/kueue/pull/4339.  I haven't contributed to kubebuilder controllers before so let me know if this is the right general approach

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-06T00:11:08Z

Any thoughts on how we want to handle MultiKueue remote workloads?  Should the UID label just get dropped when we make a remote copy?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T07:44:32Z

I see, why the question: because the UID from the worker cluster (present in the condition message of the preempted workload) would not be found anyway on the management cluster.

I think ideally:
1. we set the new UID label on the management workload unconditionally
2. when creating workloads on the worker clusters we inprint the information about the UID from the management cluster (for example in the `MainUID` label)
3. when preemption on the worker cluster happens we put into the message the value of the MainWorkloadUID label which can be used for searching the workload in (1.). Maybe the message could be `kueue-admission  Preempted to accommodate a workload (UID: <Main UID>, Worker UID: <Worker UID>) due to fair sharing within the cohort`. Here Worker UID would be logged only for workloads with "MainUID".

WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T17:29:15Z

Thinking about it more. To be fair I would just do now 1. unconditionally, and defer the MK 2. and 3. as a future improvement.

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-06T18:02:25Z

It is not that much more effort to add a `kueue.x-k8s.io/multikueue-main-workload-uid` label when copying over the workload to the remote cluster.  How about we take that step in this change and leave the preemption logging change as a future improvement?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-06T18:16:37Z

Actually, in the name of keeping integration test changes more scoped in each PR, lets defer all the 'main-workload-uid' labeling on the remote objects to a follow-up change

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T17:01:07Z

The naive approach of adding an update call in Workload Reconcile loop is negatively impacting the scheduability perf tests: https://github.com/kubernetes-sigs/kueue/pull/4339#issuecomment-2705037192.  It seems like increasing the Kueue qps and burst parameters could mitigate this.

Taking a step back however, is there a good reason in the `kueue-admission  Preempted to accommodate a workload (UID: <UID>) due to fair sharing within the cohort` condition we only include the UID?  We have access to the full Workload when we construct the condition: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/preemption/preemption.go#L220.  Why don't we just additionally log the preempting workload's namespace and name?  Then users could very easily kubectl get the preempting workload without using label selector

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:13:51Z

> Why don't we just additionally log the preempting workload's namespace and name?

Logging full name and namespace is ok. We actually have a PR which does it in 0.11: https://github.com/kubernetes-sigs/kueue/commit/7dcff89248f550b18a04b8cc09fbc8cc98dfe65c. I think we could justify cherry-picking it to 0.10.

However, when creating the message for the condition we only include UID to avoid leaking of potentially namespace-sensitive information which could be present just in the workload name. The analogous approach is taken for preemption in the core k8s (for events and condition): https://github.com/kubernetes/kubernetes/blob/0e2a2afc4c7687e71f2dddbb7edfd03f082c6876/pkg/scheduler/framework/preemption/preemption.go#L198

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T17:24:59Z

Ah okay.  Any ideas on an existing controller Workload update or patch call that we could use to also update the labels?  I've run the scheduling perf tests a bunch and adding another update call is adding too much overhead to the workload controller loop

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T17:30:09Z

Maybe I could update the defaulting workload webhook to also run on updates and do the label defaulting there?  It is not possible on creates because the workload object does not have UID yet

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:46:59Z

> adding another update call is adding too much overhead to the workload controller loop

How much of a hit it is? Maybe we could consider just swallowing the pill and bump the thresholds.

> Maybe I could update the defaulting workload webhook to also run on updates and do the label defaulting there?

This actually sounds like it could add even more overhead (but maybe it would not be visible in the perf tests, cannot recall if they install webhooks).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T17:54:39Z

@mimowo @avrittrohwer We should not record preemptor name and namespace in events and logging since those are PII.
So, I think we should revert https://github.com/kubernetes-sigs/kueue/commit/7dcff89248f550b18a04b8cc09fbc8cc98dfe65c and keep UID in logging in this enhancement.

You can find a similar discussion: https://github.com/kubernetes-sigs/kueue/pull/1942#discussion_r1552968087

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:55:31Z

> It is not possible on creates because the workload object does not have UID yet

I know, I was hoping this will change with [MAP](https://kubernetes.io/docs/reference/access-authn-authz/mutating-admission-policy/), as then it all happens within API server, but it seems it will not be visible in the CEL rules (though I haven't seen explicit mention in the KEP).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T17:58:07Z

> So, I think we should revert https://github.com/kubernetes-sigs/kueue/commit/7dcff89248f550b18a04b8cc09fbc8cc98dfe65c and keep UID in logging in this enhancement.

I think no reason to revert, this PR does exactly that - only adds to logging, but does not modify the message used on the condition. Also, we have integration tests showing the message format: https://github.com/kubernetes-sigs/kueue/blob/099a239469e5bb46b8ad3a2d5eef060a3059a1de/test/integration/singlecluster/scheduler/preemption_test.go#L300

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T18:00:09Z

> > So, I think we should revert [7dcff89](https://github.com/kubernetes-sigs/kueue/commit/7dcff89248f550b18a04b8cc09fbc8cc98dfe65c) and keep UID in logging in this enhancement.
> 
> I think no reason to revert, this PR does exactly that - only adds to logging, but does not modify the message used on the condition. Also, we have integration tests showing the message format:
> 
> [kueue/test/integration/singlecluster/scheduler/preemption_test.go](https://github.com/kubernetes-sigs/kueue/blob/099a239469e5bb46b8ad3a2d5eef060a3059a1de/test/integration/singlecluster/scheduler/preemption_test.go#L300)
> 
> Line 300 in [099a239](/kubernetes-sigs/kueue/commit/099a239469e5bb46b8ad3a2d5eef060a3059a1de)
> 
>  Message: fmt.Sprintf("Previously: Preempted to accommodate a workload (UID: %s) due to %s", alphaMidWl.UID, preemption.HumanReadablePreemptionReasons[kueue.InClusterQueueReason]),

Ah, I see. It seems to focus only on logging. In that case, it should be fine. There are no leaks between tenants.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T18:07:13Z

Instead of `kueue.x-k8s.io/multikueue-main-workload-uid` label, why we can not add management or workload cluster UID as a field?
I meant wondering if we can add dedicated fields something like `managemendUID` to recorded management cluster workload UID.
IIUC, adding UID labeling has the motivation to easy list workloads, right? In that case, we can add it to dedicated fields.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T18:28:15Z

Taking a step back - another option is that workloads already contain owner Job UID: kueue.x-k8s.io/job-uid. So, maybe in the messages for preemption we also record Job UID. Then, a user could use it for fast fetch. This would be no new requests, and no performance hit. 

The only problem is that with Pod Groups. However, maybe this is a corner case. Also, we could for a pod group record UID of the "first" pod. This would already allow users to identify the preempting group/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T18:28:43Z

wdyt @tenzen-y @avrittrohwer about the Job UID approach for the fast search?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T18:40:33Z

> wdyt [@tenzen-y](https://github.com/tenzen-y) [@avrittrohwer](https://github.com/avrittrohwer) about the Job UID approach for the fast search?

I don't think that would help, because we have the same problem of 'how do I get a job by its UID' which is not supported by kubernetes: https://github.com/kubernetes/kubernetes/issues/20572

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-07T18:50:17Z

We will search workloads by JobUID, as it is already recorded on the workload object: https://github.com/kubernetes-sigs/kueue/blob/099a239469e5bb46b8ad3a2d5eef060a3059a1de/pkg/controller/jobframework/reconciler.go#L1022. 

Lavereging the fact at the moment of wokload creation we already have JobUID, but not workloadUID.
So we only need to let user know the JobUID (along with the Workload UID in preemption.go).

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T18:54:28Z

Right, but once the user has JobUID, how do they kubectl get it by UID?

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T18:55:05Z

Oh they could do `kubectl get workloads --selector=kueue.x-k8s.io/job-uid=<UID>`.  I was thinking how would they do `kubectl get <jobAPI>`

### Comment by [@avrittrohwer](https://github.com/avrittrohwer) — 2025-03-07T18:58:02Z

Adding jobUID to the condition and event message is a much easier change.  Lets do that

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T20:38:09Z

> Taking a step back - another option is that workloads already contain owner Job UID: kueue.x-k8s.io/job-uid. So, maybe in the messages for preemption we also record Job UID. Then, a user could use it for fast fetch. This would be no new requests, and no performance hit.
> 
> The only problem is that with Pod Groups. However, maybe this is a corner case. Also, we could for a pod group record UID of the "first" pod. This would already allow users to identify the preempting group/

That sounds reasonable.
