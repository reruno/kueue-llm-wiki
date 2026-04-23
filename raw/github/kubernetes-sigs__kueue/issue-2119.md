# Issue #2119: namespace-scope configuration of manageJobsWithoutQueueName

**Summary**: namespace-scope configuration of manageJobsWithoutQueueName

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2119

**Last updated**: 2024-07-18T17:21:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-05-03T16:32:57Z
- **Updated**: 2024-07-18T17:21:26Z
- **Closed**: 2024-07-18T17:21:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 22

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kueue supports a global configuration `manageJobsWithoutQueueName`.  We would like to be able
to set this configuration flag to be true only for specific namespaces.

**Why is this needed**:

We would like to be able to use Kueue to manage batch-oriented production clusters where we can
enforce that all workloads submitted in certain namespaces (ie, user namespaces) must be submitted
through a Kueue-managed queue.  Setting `manageJobsWithoutQueueName` to true globally is not viable
without also disabling the `batch/job` integration because when it is enabled it interferes with system 
operations that create Jobs to perform administrative tasks.

Our workaround in Kueue 0.6 is to not use manageJobsWithoutQueueName and instead use RBACs
to deny users in those namespaces the ability to directly create batchv1.Jobs (forcing them to submit 
them via AppWrappers, which can be configured separately from Kueue to act as-if manageJobsWithoutQueueName
were true just for AppWrappers).  This is not optimal, because the extra level of wrapping for a resource type
that Kueue could support natively adds friction to the user experience. 

**Completion requirements**:

It should be possible to provide a list of namespaces where `manageJobsWithoutQueueName` is true as part
of the Kueue configuration.   Ideally it would be possible to update this list dynamically without needing to 
restart the Kueue controller. 

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-24T07:28:53Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T13:33:20Z

I'm on the fence on this one.

One of the original principles of Kueue was to be lean, which in this topic means not to be a policy enforcer. We provided some basic namespace selectors in the ClusterQueues, but it's preferable not to expand into more policies.

Have you tried implementing this using a native validating admission policy? https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-24T13:51:51Z

I think the high-level feedback is that in our usage of Kueue, we've come to realize that a global `manageJobsWithoutQueueNames` is not useful for us as currently implemented.  Globally enabling suspend-by-default behavior for batch/Jobs breaks too many things (especially on OpenShift).  

We can see two possible approaches to making queuing-by-default useful to us:
1. Using a namespace selector to have finer grained-control on whether manageJobsWithoutQueueNames is true/false as proposed in this issue.  
2. Adding a jobOptions to the Kueue configuration with the same functionality as the existing podOptions to enable finer-grained control over queuing of batch/Jobs.  If we had this capability, then I believe the existing global scope for manageJobsWithoutQueueName could do what we need.

If you think option 2 is a better option for Kueue's design point, I'm happy to pursue that instead.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-24T14:18:21Z

 > Have you tried implementing this using a native validating admission policy? https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/

Thanks for the pointer.  This could be useful to us eventually, but we currently need to support Kubernetes versions back to 1.27.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T14:28:23Z

`ValidatingAdmissionPolicy` is alpha since v1.27 (disabled by default), and beta since v1.28 (enabled by default).
v1.27 end-of-life is a month from now https://kubernetes.io/releases/

So it doesn't feel like it's the right time to implement this functionality in Kueue.

Any chance you can enable the alpha feature in v1.27?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-24T14:37:55Z

Turing on an alpha feature isn't viable for us.  But, the long term solution should be viable, so we don't have to do something in Kueue. 

I guess the key question is do you ever intend to have `manageJobsWithoutQueueNames` be true _and_ have the `batch/jobs` integration enabled in Kueue?   Because that combination is broken in subtle and hard to debug ways on clusters where system operations are performed using batch Jobs. 

Is it useful for us to open an issue about that combination in particular?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-24T15:13:47Z

I would be leaning towards option (1.), and say that being able to exclude, by namespace selector, some administrative namespaces from `manageJobsWithoutQueueName: true` via Kueue API can be handy. It is similar to what we do for pod integrations, where we exclude some of the namespaces.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T15:43:47Z

I agree that the functionality is useful. But (1) there is an alternative in 1.28+ and (2) it's hard to say when to stop implementing policies. What might be enough for your use case might not be enough for everyone.

I'm kind of ok with implementing this now, but I just do not want to set a precedent for future feature requests in this area.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T15:48:02Z

> I guess the key question is do you ever intend to have manageJobsWithoutQueueNames be true and have the batch/jobs integration enabled in Kueue? Because that combination is broken in subtle and hard to debug ways on clusters where system operations are performed using batch Jobs.

It works for some basic clusters that don't have system operations using jobs. But I'm tempted to remove this functionality altogether once we offer a v1 API.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-24T15:57:02Z

/unassign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T19:03:14Z

I have similar use cases. The option (1) allows us to forcefully suspend all Jobs in the arbitrary namespaces (in general, only user namespaces), right?
But, the ValidatingAdmissionPolicy doesn't bring functionality to forcefully suspend Jobs; that just rejects creation.

I guess that the ValidatingAdmissionPolicy could not replace with option (1), maybe the native Kubernetes need to provide MutatingAdmissionPolicy something.

So, I think that providing option (1) is still valid.
@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T19:51:42Z

> But, the ValidatingAdmissionPolicy doesn't bring functionality to forcefully suspend Jobs; that just rejects creation.

You could reject the creation of Jobs that should have a queue name but don't.

And then you would use `manageJobsWithoutQueueName: false`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T20:00:36Z

> > But, the ValidatingAdmissionPolicy doesn't bring functionality to forcefully suspend Jobs; that just rejects creation.
> 
> You could reject the creation of Jobs that should have a queue name but don't.
> 
> And then you would use `manageJobsWithoutQueueName: false`.

Uhm, it sounds reasonable. Even if we forcefully suspend Jobs without queueName, Job has never been inserted into queue since the Job doesn't have queueName. It means that the result is the same as the approach of rejecting of creation by ValidatingAdmissionPolicy.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T20:08:58Z

And it's even better for the user, as it provides immediate feedback.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T20:17:10Z

> And it's even better for the user, as it provides immediate feedback.

I agree with you. Here, I'm curious about whether we can provide APIs to create ValidatingAdmissionPolicy something like `blockJobsWithoutQueuName`. Once the feature is enabled, the kueue-manager creates the  ValidatingAdmissionPolicy to reject Jobs without queueName.

This has the advantage of easily introducing policies from the batch admins perspective, but it would bring us (kueue upstream) to increase maintenance costs.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-24T20:22:50Z

> > And it's even better for the user, as it provides immediate feedback.
> 
> I agree with you. Here, I'm curious about whether we can provide APIs to create ValidatingAdmissionPolicy something like `blockJobsWithoutQueuName`. Once the feature is enabled, the kueue-manager creates the ValidatingAdmissionPolicy to reject Jobs without queueName.
> 
> This has the advantage of easily introducing policies from the batch admins perspective, but it would bring us (kueue upstream) to increase maintenance costs.

My gut would be that Kueue should just document this (possibly with an example) as a way to achieve a particular kind of cluster configuration.  I think it will be easier for the batch admin if the actual creation of the ValidatingAdmissionPolicy is done using "vanilla" Kubernetes concepts and operations (as opposed to needing to know how to configure Kueue to create it).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T21:06:51Z

> > > And it's even better for the user, as it provides immediate feedback.
> > 
> > 
> > I agree with you. Here, I'm curious about whether we can provide APIs to create ValidatingAdmissionPolicy something like `blockJobsWithoutQueuName`. Once the feature is enabled, the kueue-manager creates the ValidatingAdmissionPolicy to reject Jobs without queueName.
> > This has the advantage of easily introducing policies from the batch admins perspective, but it would bring us (kueue upstream) to increase maintenance costs.
> 
> My gut would be that Kueue should just document this (possibly with an example) as a way to achieve a particular kind of cluster configuration. I think it will be easier for the batch admin if the actual creation of the ValidatingAdmissionPolicy is done using "vanilla" Kubernetes concepts and operations (as opposed to needing to know how to configure Kueue to create it).

That makes sense, but even if we don't provide the dedicated API like `blockJobsWithoutQueueName`, I think that providing the ValidatingAdmissionPolicy and ValidatingAdmissionPolicyRoleBinding would be worth it.

Because batch admins can define Validations using upstream ValidatingAdmissionPolicyRoleBinding for the custom jobs.
Additionally, we (upstream Kueue) provide the validations for native supporting Jobs (batch/job, rayjob...) using ValidatingAdmissionPolicyRoleBinding.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:41:20Z

/assign @IrvingMg 

Could you create a new task page under https://kueue.sigs.k8s.io/docs/tasks/manage/ explaining how to restrict the creation of jobs without queue name using a ValidatingAdmissionPolicy?

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-07-18T16:17:48Z

As we updated the documentation in https://github.com/kubernetes-sigs/kueue/pull/2507 for this case, is it okay if we close this issue?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-07-18T17:12:30Z

Sure.  Fine to close as won't fix -- there's an alternate solution.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-18T17:21:19Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-18T17:21:24Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2119#issuecomment-2237118817):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
