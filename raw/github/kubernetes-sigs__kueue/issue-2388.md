# Issue #2388: A new Workload condition which signalize it should be deactivated

**Summary**: A new Workload condition which signalize it should be deactivated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2388

**Last updated**: 2024-06-26T16:30:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-10T11:21:02Z
- **Updated**: 2024-06-26T16:30:22Z
- **Closed**: 2024-06-26T16:30:22Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 19

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A new Workload condition called e.g. `DeactivationTarget` that would signalize that a Workload which has that condition should be deactivated. This condition would also contain Message which then can be passed to the `Deactivated` condition.

**Why is this needed**:
 This condition would be used with the `WaitForPodsReady` feature and the Provisioning controller. It would discard need to reverse engineer reason of Workload being deactivated as it's currently in [the workload controller](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L187-L197). It would also provide more descriptive information about AdmissionCheck that has been Rejected


**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-06-10T11:26:44Z

More discussion about it #2291

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-06-10T11:26:53Z

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-10T11:53:45Z

+1

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-06-12T10:36:31Z

For visibility and discussion @tenzen-y @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-12T15:20:07Z

Just because we have so many conditions, I would like this condition to just be temporary. In other words, we should remove this condition, as opposed to mark it as `False`, when no longer needed.
That way, we can hopefully avoid developers depending on it.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-13T08:20:40Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T19:45:22Z

This concept looks similar to the batch/job interim condition, SuccessCriteriaMet, and FailureTarget.
But, this new condition is used only to trigger other reconciling. In other words, this is an alternative approach of the `.spec.active` to trigger to stop Jobs.

> Just because we have so many conditions, I would like this condition to just be temporary. In other words, we should remove this condition, as opposed to mark it as False, when no longer needed.
That way, we can hopefully avoid developers depending on it.

Basically, I agree with you. But, instead of adding the temporary state to the Workload conditions only for the triggerring the evictions, shouldn't create the dedicated API?
Additionally, I'm suspecting that the temporary condition potentially causes some race conditions and bugs.
So, I would like to propose a new subresource, "Eviction" against the Workload resource similar to the Pod Eviction subresource. 

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T14:19:06Z

I suspect when you say "subresource" you just mean a new struct in the Workload status API?

That could be a good option. Which other fields do you have in mind, other than the message?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-19T10:06:43Z

> Additionally, I'm suspecting that the temporary condition potentially causes some race conditions and bugs.

Do you have some specific scenarios on your mind? I don't see any that would be intrinsic to the approach, but I might be missing something.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-19T15:14:06Z

I guess it could look something like:

```yaml
status:
  deactivationTarget:
    reason: Foo
    message: "a human readable reason"
```

I'm fine either way.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-19T16:25:11Z

Removing a condition is a bit unusual in kube, typically we just set them to false. 

So, if we were to remove the condition, then I'm leaning slightly towards the `deactivationTarget` structure.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-19T18:54:30Z

Also.... would it make sense to make it part of the `spec`?

Then, Kueue could use 1 API call to set both `deactivationTarget` (or `deactivationDetails` if it's in spec) and `active=false`.
A second API call would do the Eviction using `deactivationDetails`.

And then we can have the webhook clear the `deactivationDetail` when a user sets `active=true`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-20T06:16:03Z

> I suspect when you say "subresource" you just mean a new struct in the Workload status API?
> 
> That could be a good option. Which other fields do you have in mind, other than the message?

I was thinking whether we can add a subresource similar to this one: https://github.com/kubernetes/kubernetes/blob/78377c4d105533f76d12886f82128469b6f3c0e9/pkg/apis/policy/types.go#L159-L174

Can we implement the similarly API?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-20T06:35:51Z

> Also.... would it make sense to make it part of the spec?

I see what you mean, but I have two concerns:

1. we move even more stuff to spec which is managed by controllers, and this seems to me violate the [API convention](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status), quote:  

"Types with both spec and status stanzas can (and usually should) have distinct authorization scopes for them. This allows users to be granted full write access to spec and read-only access to status, **while relevant controllers are granted read-only access to spec but full write access to status.**"

2. indeed, we save the API call, but I think the update to the status just before deactivation is actually desired to bump `status.requeingState.count` to exceed the `backoffLimitCount`. I think the current behavior is misleading, because the counter equals `status.requeingState.count` before and after the last attempt.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-20T06:41:10Z

> I was thinking whether we can add a subresource similar to this one: https://github.com/kubernetes/kubernetes/blob/78377c4d105533f76d12886f82128469b6f3c0e9/pkg/apis/policy/types.go#L159-L174
> Can we implement the similarly API?

I guess we could but it seems extra complexity, and extra API call to update it separately from the status (see 2. in the previous comment). What are the benefits?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T19:49:33Z

> I was thinking whether we can add a subresource similar to this one: https://github.com/kubernetes/kubernetes/blob/78377c4d105533f76d12886f82128469b6f3c0e9/pkg/apis/policy/types.go#L159-L174
> 
> Can we implement the similarly API?

I see. I don't think these kind of subresources can be implemented via CRDs. But additionally, they heavily rely on doing things on the apiserver side, as opposed to controllers.

If we were to do it via controllers, it would eventually have to translate to changes to the spec and status of the Workload object. So we would be back to square one.

Then, we are left with 3 options:
1. use a condition
2. use a dedicated field in status
3. use a dedicated field in spec.

> "Types with both spec and status stanzas can (and usually should) have distinct authorization scopes for them. This allows users to be granted full write access to spec and read-only access to status, while relevant controllers are granted read-only access to spec but full write access to status."

But Kueue is already the full owner of the spec and status. OTOH, users can only write to spec.
Uhm.... maybe option 1 ends up being the best after all.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T14:41:50Z

Since there are no strong opinions against, let's move forward with #2409, which matches option 1 above.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-25T14:46:38Z

> Since there are no strong opinions against, let's move forward with #2409, which matches option 1 above.

I have no objections against option 1 above. Only concern is the condition is temporary.
I'm suspecting that making the condition temporary will bring us new race conditions.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-25T14:56:08Z

It shouldn't, because we are removing this condition in the same request when we set Evicted=true.

https://github.com/kubernetes-sigs/kueue/blob/3a8edc9d380bba6ae723bda6d5ab029a7aa40494/pkg/controller/core/workload_controller.go#L198-L214
