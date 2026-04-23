# Issue #3094: [MultiKueue] AdmissionCheck conditions are confusing

**Summary**: [MultiKueue] AdmissionCheck conditions are confusing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3094

**Last updated**: 2024-10-22T15:54:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-19T12:45:37Z
- **Updated**: 2024-10-22T15:54:53Z
- **Closed**: 2024-10-22T15:54:53Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 36

## Description

**What happened**:

I got feedback from a user running into an issue with MultiKueue, and getting distracted by confusing AdmissionCheck conditions, and wasting time during investigations.

```yaml
  - lastTransitionTime: "2024-09-07T10:27:28Z"
      message: only one multikueue managed admission check can be used in one ClusterQueue
      observedGeneration: 1
      reason: MultiKueue
      status: "True"
      type: SingleInstanceInClusterQueue
    - lastTransitionTime: "2024-09-07T10:27:28Z"
      message: admission check cannot be applied at ResourceFlavor level
      observedGeneration: 1
      reason: MultiKueue
      status: "True"
      type: FlavorIndependent
```

**What you expected to happen**:

No user-facing conditions used by MultiKueue for its inner-workings.

**How to reproduce it (as minimally and precisely as possible)**:

Setup MultiKueue according to https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/. 

**Anything else we need to know?**:

The mechanism was introduced as part of [Single instance admission check.](https://github.com/kubernetes-sigs/kueue/pull/1635#top)(https://github.com/kubernetes-sigs/kueue/pull/1635), but the solution based on status conditions was contested and deferred to be revisted on future releases https://github.com/kubernetes-sigs/kueue/pull/1635#discussion_r1466659290. 

I propose to:
- drop the conditions, and hard-code dependencies between built-in Admission checks, as suggested in the [comment](https://github.com/kubernetes-sigs/kueue/pull/1635#discussion_r1466659290). This approach will also let us easily implement https://github.com/kubernetes-sigs/kueue/issues/2021
- move the user-facing configuration as part of the support for external Admission Checks (I can open a follow up issue for this)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T12:46:04Z

/cc @alculquicondor @tenzen-y @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T13:21:18Z

Unfortunately, at this point, the conditions are not just about MK, there could be any (external) admission check that uses them.

Granted, the current messages read as if there is a problem, when there is none. We could start by providing better messages.

Another question comes to mind: what if there is one admission check that is ok with flavor independence and one that is not? Wouldn't both try to change the condition, rendering it unusable?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T13:27:46Z

> Unfortunately, at this point, the conditions are not just about MK, there could be any (external) admission check that uses them.

Could we deprecate them, and drop as we move the API to Beta? I think it is ok as Alpha API doesn't guarantee backwards compatibility.

> Granted, the current messages read as if there is a problem, when there is none. We could start by providing better messages.

Exactly, this is what the user was concerned about -was searching if the CQ configuration is wrong being confused by the status, while the issue was with Kueue not restarted after JobSet install (another issue).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T13:29:01Z

> Another question comes to mind: what if there is one admission check that is ok with flavor independence and one that is not? Wouldn't both try to change the condition, rendering it unusable?

Probably yes, but I haven't checked yet, can check, but kinda hoping we can drop them all together.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T13:29:40Z

> Could we deprecate them, and drop as we move the API to Beta? I think it is ok as Alpha API doesn't guarantee backwards compatibility.

The constants are in the beta API package though.

Forgetting about backwards compatibility for a second: @trasc, could we move the conditions to the AdmissionCheckStatus instead?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T13:34:18Z

> The constants are in the beta API package though.

Right, but even Beta does not need to be backwards-compatible if we have a justification, looking at this: https://kubernetes.io/docs/reference/using-api/#api-versioning:

"The schema and/or semantics of objects may change in incompatible ways in a subsequent beta or stable API version. When this happens, migration instructions are provided. Adapting to a subsequent beta or stable API version may require editing or re-creating API objects, and may not be straightforward. The migration may require downtime for applications that rely on the feature."

On top of that, I highly doubt any users would want to use them outside of MultiKueue, and MK is still alpha as a feature.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T13:50:26Z

> > Could we deprecate them, and drop as we move the API to Beta? I think it is ok as Alpha API doesn't guarantee backwards compatibility.
> 
> The constants are in the beta API package though.
> 
> Forgetting about backwards compatibility for a second: @trasc, could we move the conditions to the AdmissionCheckStatus instead?

The intention with them (at least for SingleInstance) was to allow the cluster queue to detect the miss configuration and mark it'self as Inactive. We could in theory do it but I belive it's harder for the user to understand what is actually happening. The queue will look healthy but none of it's workload get admitted and need to check at least one workload to get the reason.

 (depending on when we do the AdmissionCheckStatus update we can also end up putting extra pressure on the scheduler to reserve quota just to be given back ).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T14:05:47Z

/cc @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T14:20:56Z

> Forgetting about backwards compatibility for a second: @trasc, could we move the conditions to the AdmissionCheckStatus instead?

It would relieve the confusion a bit, so +1 if we need to keep them in some form, but I would suggest dropping entirely.

> The intention with them (at least for SingleInstance) was to allow the cluster queue to detect the miss configuration and mark it'self as Inactive. 

When the CQ is mis-configured already convey this information via the ClusterQueue "Active=False" condition reason (which is determined [here](https://github.com/kubernetes-sigs/kueue/blob/82b62260d6e12d4cd1dddbdc79af711da1b1dc73/pkg/cache/clusterqueue.go#L234), and currently redundant in case of mis-configuration. It would be nice to expand the human-readable message though [here](https://github.com/kubernetes-sigs/kueue/blob/82b62260d6e12d4cd1dddbdc79af711da1b1dc73/pkg/cache/clusterqueue.go#L259).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T14:25:54Z

Opened https://github.com/kubernetes-sigs/kueue/issues/3099 to follow up on the discussion and improve debuggability.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T14:49:51Z

> The intention with them (at least for SingleInstance) was to allow the cluster queue to detect the miss configuration and mark it'self as Inactive. We could in theory do it but I belive it's harder for the user to understand what is actually happening. The queue will look healthy but none of it's workload get admitted and need to check at least one workload to get the reason.

Just to make sure we are in the same page, I'm talking about https://kueue.sigs.k8s.io/docs/reference/kueue.v1beta1/#kueue-x-k8s-io-v1beta1-AdmissionCheckStatus

The way I'm thinking about is that the AdmissionCheckStatus would have the `SingleInstanceInClusterQueue` and/or `FlavorIndependent`. Then, the ClusterQueues that use these admission checks could flip their "Active" condition based on them. So, there will still be a failure in the ClusterQueue status, but in the form of the Active condition being false.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T15:18:48Z

> > The intention with them (at least for SingleInstance) was to allow the cluster queue to detect the miss configuration and mark it'self as Inactive. We could in theory do it but I belive it's harder for the user to understand what is actually happening. The queue will look healthy but none of it's workload get admitted and need to check at least one workload to get the reason.
> 
> Just to make sure we are in the same page, I'm talking about https://kueue.sigs.k8s.io/docs/reference/kueue.v1beta1/#kueue-x-k8s-io-v1beta1-AdmissionCheckStatus
> 
> The way I'm thinking about is that the AdmissionCheckStatus would have the `SingleInstanceInClusterQueue` and/or `FlavorIndependent`. Then, the ClusterQueues that use these admission checks could flip their "Active" condition based on them. So, there will still be a failure in the ClusterQueue status, but in the form of the Active condition being false.

Status not State :), they should be there, I think the description of the issue is wrong.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T15:35:39Z

That is possible, I got the snippet from a confused user asking if this is indication of a problem and I assumed it is in CQ. I will double check and update the description

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T15:37:36Z

I see, in that case, maybe the solution is simpler: instead of making it a "condition", they can be dedicated fields, maybe called "properties" or something along those lines.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T15:58:04Z

Custom field was one of the proposals back then, but we chose the condition to avoid API changes.

However if we have concensus, it sure can be done.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T16:08:36Z

True, I remember some details.
In any case, given customer feedback, I think it's valuable to transition to dedicated fields so that we can remove the confusing messages and have dedicated messages in the Active condition as https://github.com/kubernetes-sigs/kueue/issues/3099 suggests

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T16:25:14Z

Updated, these are AdmissionCheck status conditions. 

I'm not sure the user wants to see the properties too. I think this was just redherring as it looks suspicious in the current form. IIRC they were introduced to provide a mechanism to express "don't set two instances of MultiKueue AC in a single CQ".  

I would suggest we  drop them entirely and validate the conditions based on hard-coded rules (for the built-in ACs).

if we want to have the dependencies configurable I think we need some form of API for it, and thus probably KEP update, so I'm hoping we can defer this for later, when working on "Allow validation of custom rules for AdmissionChecks".

EDIT: conceptually, I think, the declarative API, would rather be on AdmissionCheck type (like MultiKueue) rather than on a concrete instance of AdmissionCheck. One place we could express this is a global configuration. Maybe there we could have some "properties" like `singleInstaceAdmissionCheckTypes []string`, or `flavorIndependentAdmissionCheckTypes []string` (names TBD).

### Comment by [@trasc](https://github.com/trasc) — 2024-09-19T16:34:10Z

> I'm not sure the user wants to see the properties too. I think this was just redherring as it looks suspicious in the current form. IIRC they were introduced to provide a mechanism to express "don't set two instances of MultiKueue AC in a single CQ".

It was added to say "don't set two instances of  ACs managed by the same controller in a single CQ" and lately we have "don't set this AC at flavor level".

> EDIT: conceptually, I think, the declarative API, would rather be on AdmissionCheck type (like MultiKueue) rather than on a concrete instance of AdmissionCheck. One place we could express this is a global configuration.

It should be about the AC controller and we should add an API object containing this, it was also proposed and rejected one of the reason being the need of user configuration.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T16:39:46Z

> It was added to say "don't set two instances of ACs managed by the same controller in a single CQ" and lately we have "don't set this AC at flavor level".

Right, assuming we need to support the validation rule for custom admission checks. My suggestion is that we could start with support for built-in ACs, and support custom ones in the future KEP, where we plan it properly.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T16:57:29Z

+1 on @mimowo as a lower effort solution (from a process' perspective)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T18:58:28Z

> Right, assuming we need to support the validation rule for custom admission checks. My suggestion is that we could start with support for built-in ACs, and support custom ones in the future KEP, where we plan it properly.

This evolving features step-by-step sound good to me. Anyway, explaining the step and planning in the KEP would be worth it.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T05:15:41Z

> Right, assuming we need to support the validation rule for custom admission checks. My suggestion is that we could start with support for built-in ACs, and support custom ones in the future KEP, where we plan it properly.

In my opinion restricting the usage for a hard-coded list of built-in ACCs is a step back, I'd prefer to start a discussion around a list of  "proprieties" as mentioned here: https://github.com/kubernetes-sigs/kueue/issues/3094#issuecomment-2361365503 .

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-20T13:01:58Z

I believe we should proceed with deleting them for now, especially since, we remove them anyway in the ideal solution (replacing with the declarative API).

I'm happy to open a dedicated issue to support some declarative API to drive validation rules for external controllers. However, given our current workstreams, it's unlikely we'll be able to properly review this before the end of November. Additionally, we haven't received any user or customer feedback requesting support for validation rules for external jobs, so I think its priority remains low until we hear otherwise.

Therefore, I don't think we should block the graduation of MultiKueue on this. We can incrementally add the API later. It would be great if we could promote MultiKueue in version 0.9.

Opened: https://github.com/kubernetes-sigs/kueue/issues/3106

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T13:51:56Z

> I'm happy to open a dedicated issue to support some declarative API to drive validation rules for external controllers.

Why should we have distinctive approaches for internal and external ACCs?

### Comment by [@trasc](https://github.com/trasc) — 2024-09-20T13:54:35Z

> Therefore, I don't think we should block the graduation of MultiKueue on this.

This is not a MultiKueue problem is an AdmissionCheck one. (we should probably retitle the issue).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-20T14:09:05Z

> Why should we have distinctive approaches for internal and external ACCs?

Due to amount of work needed to support external vs internal ones. Note that, for the regular Jobs (no multiKueue), Kueue was only supporting built-in Jobs (just batch/Job) for a couple of first releases.

Another differentiating factor is priority based on user feedback / requirements.

>This is not a MultiKueue problem is an AdmissionCheck one. (we should probably retitle the issue).

Is is only MultiKueue which uses them. The users reported the issue when experimenting with MultiKueue, I think it is fair to stay this way.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2024-09-23T12:01:21Z

Today @mimowo spent 20 minutes explaining this thing too me. I finally got what was the point of the conditions, but i'm afraid the end user will have even bigger problems to understand them. Given that, I would suggest deprecation and removal of these conditions.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T06:38:31Z

Another motivation to drop the condition noticed while working on the messages in https://github.com/kubernetes-sigs/kueue/pull/3127#discussion_r1775164411. I find it **very hard** to construct good, informative messages, with the current mechanism.

To move forward for dropping them I see two possibilities:
1. Drop them and say in release notes:"ACTION REQUIRED: the Admission check status conditions “FlavorIndependent” and “SingleInstanceInClusterQueue”, If you were using any of these conditions for your external AdmissionCheck you will need to provide the validation by an external controller"
2. Don’t add them in Kueue (essentially drop [this](https://github.com/kubernetes-sigs/kueue/blob/45bc472d8f777177a840a00dca68d1d7c983aa88/pkg/controller/admissionchecks/multikueue/admissioncheck.go#L130-L150), but continue supporting them for until v1beta2.

While (2.) is backwards compatible, I’m leaning towards option (1.) because I believe it is highly unlikely anyone would use them by now. Second, they only support validation, so the happy path isn’t affected.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-09-27T09:02:09Z

@trasc I don't have a huge expertise in these area but both @mwielgus and @mimowo explained it to me and @alculquicondor seems to also be on-board so if my voice has any weight at all I'm +1 for what @mimowo's proposing.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T09:41:17Z

@mimowo I would recommend introducing the feature gate for those conditions. As the K8s deprecation guide, we need to provide the proper migration ways, and the AdmissionCheck API is assumed to be used by third-party AdmissionCheck controllers.

So, my recommendation to mitigate the painful points for the existing users is to introduce the dedicated feature gate and disable the feature by default. Then, we take the proper deprecation steps.

For example, we keep the feature gate for a while like a year, or bump AdmissionCheck API version to v1beta2.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T09:51:34Z

@tenzen-y IIUC the approach (3.) you are suggesting is to introduce a feature gate which controls the logic for the conditions: adding them and supporting, disabled by default and deprecated.  I think we could drop the feature gate regardless of moving to v1beta2, because the conditions don't impact the schema, so we could say "drop the feature gate in 0.10 or 0.11, or so).

EDIT: the release note could say: "ACTION REQUIRED: the Admission check status conditions “FlavorIndependent” and “SingleInstanceInClusterQueue” are no longer supported by default, If you were using any of these conditions for your external AdmissionCheck you need to enable the `AdmissionChecksValidationHack` feature gate. For the future releases you will need to provide validation by an external controller."

This sounds very reasonable to me, for me this is equally preferred as (1.). Let's hear what others think.

### Comment by [@trasc](https://github.com/trasc) — 2024-09-27T09:57:03Z

If the rephrase of the conditions messages it not sufficient we could:

1. (temporary) Hard-code multikueue as being  `SingleInstanceInClusterQueue` and `FlavorIndependent` in the cache.
2. No longer set the the conditions in MultiKueue AdmissionChecks
(these should cover the reported issue)

In a follow-up:
1. Find an alternative to the condition based approach (something like https://github.com/kubernetes-sigs/kueue/issues/3094#issuecomment-2361436478 or by adding a new API type that describes the properties of an AC controller)
2. Deprecate the conditions based approach.
3. Migrate MultiKueue to the new approach and drop the hard-coded MultiKueue part from cache.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T10:55:08Z

> @tenzen-y IIUC the approach (3.) you are suggesting is to introduce a feature gate which controls the logic for the conditions: adding them and supporting, disabled by default and deprecated. I think we could drop the feature gate regardless of moving to v1beta2, because the conditions don't impact the schema, so we could say "drop the feature gate in 0.10 or 0.11, or so).

Yes, that is what I wanted to say. Thank you for expanding. It might be better to deprecate and disable it by default in v0.9 and then completely remove it in v0.10.0. Considering planning to release v0.9 in October, we can give them a reprieve for 5 or 6 months (about half a year). WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T10:57:11Z

If we decide to release v0.10 more early, we want to postpone the removal of the feature to v0.11.0 so that we can give them a reprieve for half a year.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T11:00:52Z

sgtm

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-11T10:34:30Z


/assign
